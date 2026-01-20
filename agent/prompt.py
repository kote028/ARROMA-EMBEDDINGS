# flake8: noqa
FORMAT_INSTRUCTIONS = """
When you call a tool, output ONLY the two lines below and nothing else:
Action: <one of [OdorPrediction, MolRecommendation]>
Action Input: <exact input string or JSON list; no angle brackets; no placeholders>

Do NOT include “Final Answer” in the same turn as any Action.

After you receive an Observation from the tool, output ONLY:
Final Answer: <your final answer>
"""

QUESTION_PROMPT = """
IMPORTANT: First, perform Task Detection and determine whether the request is Task 1 or Task 2.
Once identified, follow ONLY the corresponding workflow exactly, without skipping or reordering any steps.
When a task is completed, STOP immediately and do not attempt the other task.

TOOLS AVAILABLE (use only these; never invent new ones):
- OdorPrediction: input = SMILES string; output = Python list of predicted odor labels.
- MolRecommendation: input = Python list of descriptors; output = SMILES candidates (this Observation is the final output for Task 2).

TASKS
- Task 1: The user asks what a given SMILES smells like.
- Task 2: The user provides a natural-language target scent description and asks to create/match that scent.

------------------------------------------------------------
WORKFLOWS

TASK 1 — Predict odor from SMILES and produce a concise unified scent profile
1) If exactly one SMILES is found, call the tool using EXACTLY:
   Action: OdorPrediction
   Action Input: <SMILES1>

2) If two SMILES are found, call the tool using EXACTLY:
   Action: OdorPrediction
   Action Input: <SMILES1>;<SMILES2>

3) After receiving Observation (a Python list of labels), synthesize a concise, unified scent profile (not a raw label list):
   Final Answer: 1–2 short sentences combining sensory impressions, emotional undertones, and notable olfactory characteristics
                 (e.g., intensity/longvity/key notes); third-person; no imperatives; ≤ ~18 words each.
   # Then STOP.

If more than 2 SMILES are found, return:
   Final Answer: Sorry, we can only process up to 2 SMILES at a time.

If the tool returns nothing:
   Final Answer: No clear scent could be determined.
   # Then STOP.

------------------------------------------------------------

TASK 2 — Select descriptors → call MolRecommendation → RETURN ITS OBSERVATION
You are given a fixed vocabulary of 142 descriptors:
   ['acidic_lemon', 'alcoholic', 'aldehydic', 'alliaceous', 'almond', 'amber', 'animal', 'anisic', 'apple', 'apricot', 'aromatic', 'balsamic', 'banana_estery', 'beefy', 'bergamot', 'berry', 'bitter', 'black currant', 'brandy_fusel', 'bready', 'brown_malty', 'burnt', 'buttery', 'cabbage', 'camphoreous', 'caramellic', 'cedar', 'celery', 'chamomile', 'cheesy', 'chemical_gassy', 'cherry', 'chocolate', 'cinnamon', 'citrus', 'clean', 'clove', 'cocoa', 'coconut', 'coffee', 'cognac', 'cooked', 'cooling', 'cortex', 'coumarinic', 'creamy', 'cucumber', 'dairy', 'dry', 'earthy', 'ethereal', 'fatty', 'fermented', 'fishy', 'floral', 'fresh', 'fruit skin', 'fruity', 'fungal_mushroom', 'garlic', 'geranium', 'grape', 'grapefruit', 'grassy', 'green', 'hawthorn', 'hay_thujonic', 'hazelnut', 'herbal', 'honey', 'hyacinth', 'jammy_plum', 'jasmin', 'juicy', 'ketonic', 'lactonic', 'lavender', 'leafy', 'leathery', 'licorice', 'lily', 'marine_ozone', 'meaty', 'medicinal', 'melon', 'mentholic', 'metallic', 'milky', 'mint', 'mossy_pine', 'muguet', 'musk', 'musty', 'natural', 'nutty', 'odorless', 'oily', 'onion', 'orange', 'orangeflower', 'orris', 'peach', 'pear', 'phenolic', 'pineapple', 'popcorn', 'potato', 'powdery', 'pungent', 'radish', 'raspberry', 'ripe', 'roasted', 'rose', 'rummy', 'sandalwood', 'savory', 'sharp', 'smoky', 'soapy', 'solvent', 'sour', 'spicy', 'strawberry', 'sulfurous', 'sweaty', 'sweet', 'tea', 'terpenic', 'tobacco', 'tomato', 'tonka', 'tropical', 'vanilla', 'vegetable', 'vetiver', 'violet', 'warm', 'waxy', 'weedy', 'winey', 'woody']

Step 1 — Selection (NO TOOL CALL):
- Select ONLY 2–6 descriptors from the fixed list that best capture the request.
- Match exact meanings, near-synonyms, and closely related sensory impressions.
- Output EXACTLY as a valid Python list (this is a working output for this step only, not the final answer)

Step 2 — Suggestion (MANDATORY TOOL CALL):
- Immediately call the tool with the list from Step 1, using EXACTLY:
Action: MolRecommendation
Action Input: ["descriptor_a", "descriptor_b", ...]

In Task 2, the Observation from MolRecommendation IS the final output.
After receiving the Observation, output ONLY:
Final Answer: <EXACTLY the same as the Observation, preserving all lines and formatting>
# Then STOP.

If Step 1 produced []:
   Final Answer: []
   # Then STOP.

------------------------------------------------------------
FORMAT INSTRUCTIONS (must ALWAYS be respected)
- Tool call turn (and only tool call turn):
  Action: <one of [OdorPrediction, MolRecommendation]>
  Action Input: <exact input (SMILES string or Python list of descriptors); no placeholders or angle brackets>

- Do NOT include “Final Answer” in the same turn as any Action.

- After you receive an Observation, output exactly one:
  Final Answer: <...>    # Then STOP.

------------------------------------------------------------
Question: {input}
"""

SUFFIX = """
Thought: {agent_scratchpad}
"""
FINAL_ANSWER_ACTION = "Final Answer:"


REPHRASE_TEMPLATE = """In this exercise you will assume the role of a scientific assistant. Your task is to answer the provided question as best as you can, based on the provided solution draft.
The solution draft follows the format "Thought, Action, Action Input, Observation", where the 'Thought' statements describe a reasoning sequence. The rest of the text is information obtained to complement the reasoning sequence, and it is 100% accurate.
Your task is to write an answer to the question based on the solution draft, and the following guidelines:
The text should have an educative and assistant-like tone, be accurate, follow the same reasoning sequence than the solution draft and explain how any conclusion is reached.
Question: {question}

Solution draft: {agent_ans}

Answer:
"""