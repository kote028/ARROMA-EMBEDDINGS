from langchain_core.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_ollama import ChatOllama
from rmrkl import ChatZeroShotAgent, RetryAgentExecutor

from agent.prompt import FORMAT_INSTRUCTIONS, QUESTION_PROMPT, REPHRASE_TEMPLATE, SUFFIX
from agent.tool import make_tools


def _make_llm(model: str, temp: float = 0.1, streaming: bool = True):
    return ChatOllama(
        model=model, 
        temperature=temp,
        streaming=streaming,
        callbacks=[StreamingStdOutCallbackHandler()],
    )


class Fragent:
    def __init__(
        self,
        model: str,
        temp: float = 0.1,
        max_iterations: int = 10,
        streaming: bool = True,
        verbose: bool = True,
    ):
        """Initialize Fragent agent using LLaMA3 via Ollama."""
        self.llm = _make_llm(model, temp=temp, streaming=streaming)

        tools = make_tools(self.llm, verbose=verbose)

        self.agent_executor = RetryAgentExecutor.from_agent_and_tools(
            tools=tools,
            agent=ChatZeroShotAgent.from_llm_and_tools(
                self.llm,
                tools,
                suffix=SUFFIX,
                format_instructions=FORMAT_INSTRUCTIONS,
                question_prompt=QUESTION_PROMPT,
            ),
            verbose=verbose,
            max_iterations=max_iterations,
            handle_parsing_errors=True,
        )

        rephrase = PromptTemplate(
            input_variables=["question", "agent_ans"], template=REPHRASE_TEMPLATE
        )
        self.rephrase_chain = rephrase | self.llm

    def run(self, prompt: str) -> str:
        outputs = self.agent_executor({"input": prompt})
        return outputs["output"]

    def rephrase(self, question: str, agent_ans: str) -> str:
        return self.rephrase_chain.run({"question": question, "agent_ans": agent_ans})

if __name__ == "__main__":
    agent = Fragent(model="llama3")

    task1_a = agent.run("How does the molecule CCC1=C(O)C(=O)CC1 smell like?")
    task1_b = agent.run("How does the mixture blend with CC(C)COC(=O)Cc1ccccc1 and CCCCCOC(=O)Cc1ccccc1 smell like?")
    task1_c = agent.run("How does the mixture blend with CC(C)COC(=O)Cc1ccccc1, CCCCCOC(=O)Cc1ccccc1 and CCC1=C(O)C(=O)CC1 smell like?")
    task2_a = agent.run("I want to make a scent that captures the feeling of running through a grassy field.")
