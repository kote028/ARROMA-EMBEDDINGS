
import time
import re
import ast
import pandas as pd
from typing import Set
from langchain.tools import BaseTool
from langchain.tools import BaseTool
from pydantic import PrivateAttr
from agent.paths import DATA_DIR


class MolRecommendation(BaseTool):
    name: str = "MolRecommendation"
    description: str = (
        "Choose the odor descriptors using describe sentences. "
        "Input: list of descriptors. Output: molecule information"
    )
    return_direct: bool = True
    
    _df: pd.DataFrame = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._df = pd.read_csv(DATA_DIR / "mixture.csv")[["smiles", "descriptors"]]

        def _to_set(x: str) -> Set[str]:
            if not isinstance(x, str):
                return set()
            return {t.strip().lower() for t in x.split(";") if t.strip()}
        self._df["_label_set"] = self._df["descriptors"].apply(_to_set)


    def _run(self, labels: list) -> str:
        print(f"[TOOL] MolRecommendation called with input: {labels}")

        if isinstance(labels, str):
            match = re.search(r"\[.*\]", labels, re.DOTALL)
            if match:
                labels = ast.literal_eval(match.group(0))

        targets = set(labels)
        if not targets:
            print("error")
            return "[]"

        def _match_info(s: Set[str]):
            matched = sorted(s & targets)
            return len(matched), matched

        match_counts, matched_lists = zip(*self._df["_label_set"].map(_match_info))
        tmp = self._df.copy()
        tmp["_match_count"] = match_counts
        tmp["_matched"] = matched_lists
        tmp["_desc_count"] = tmp["descriptors"].str.count(";") + 1
        tmp["_mol_count"] = tmp["smiles"].str.count(";") + 1

        ranked = (
            tmp[tmp["_match_count"] > 0]
            .sort_values(by=["_match_count", "_desc_count", "_mol_count"], ascending=[False, True, True])
            .head(3)
        )

        answer = f"The scent may resemble {labels}.\n"
        
        if ranked.empty:
            answer += "No ingredients with that scent were found."
        else:
            answer += "Here are some ingredients you can use to create this fragrance:\n"

            for _, row in ranked.iterrows():
                answer += f"- SMILES: {row.get('smiles')}, descriptors: {row.get('descriptors', '')}, matched({int(row['_match_count'])}): {row['_matched']}\n"

        return answer

if __name__ == "__main__":
    time_start = time.time()

    tool = MolRecommendation()
    results = tool._run(["tonka"])

    time_end = time.time()
    print(f"Time taken: {time_end - time_start:.4f} sec")
    print(results)
