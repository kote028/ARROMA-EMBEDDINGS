from langchain.base_language import BaseLanguageModel
from agent.tools import *


def make_tools(llm: BaseLanguageModel, verbose=True):
    all_tools = []

    all_tools += [
        OdorPrediction(),
        MolRecommendation()
    ]
    return all_tools
