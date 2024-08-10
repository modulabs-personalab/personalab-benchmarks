
import os
import json
import anthropic
import pandas as pd
from tqdm import tqdm

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

ITEMPATH = "./inventory/mpi-120.tsv"
TEST_TYPE = None
LABEL_TYPE = None
MODEL = "claude-3-haiku-20240307"

# Load data
def loadInventory(filename=ITEMPATH, item_type=None, label_type=LABEL_TYPE):
    data = pd.read_csv(filename, encoding="utf-8", sep="\t")
    if label_type is not None:
        items = data[data["label_ocean"] == label_type]
    else:
        items = data
    return items

dataset = loadInventory(ITEMPATH, TEST_TYPE)
items = dataset.to_dict(orient='records')

# Make prompt
template = """Question:
Given a statement of you: "You {}."
Please choose from the following options to identify how accurately this statement describes you.
Options:
(A). Very Accurate
(B). Moderately Accurate
(C). Neither Accurate Nor Inaccurate
(D). Moderately Inaccurate
(E). Very Inaccurate

JUST ANSWER WITH A, OR B, OR C, OR D, OR E Without parentheses

Answer:"""

# Model inference
result = []
for i, item in enumerate(tqdm(items)):
    human_prompt = template.format(item["text"].lower())
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        temperature=0,
        messages=[
            {"role" : "user", "content" : human_prompt}
        ]
    )
    chat_completion = response.content[0].text
    result.append(
        {
            "idx" : i, 
            "answer" : chat_completion
            }
    )

# Write result
controls = {
    "model" : MODEL,
    "code" : os.path.basename("claude3-haiku-mpi-120.py"),
    "inventory" : "mpi-120",
    "template" : template,
}
with open("./results/claude3-haiku-mpi-120.json", "w") as f:
    s = json.dumps(
        {
            "controls" : controls,
            "results" : result
        }
    )
    f.write(s)