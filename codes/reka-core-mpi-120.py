
# !pip install reka-api
# tsv data read

import os
import pandas as pd
from reka import ChatMessage
from reka.client import Reka
from tqdm import tqdm
import json

ITEMPATH = "../inventory/mpi-120.tsv"
TEST_TYPE = None
LABEL_TYPE = None

def loadInventory(filename=ITEMPATH, item_type=None, label_type=LABEL_TYPE):
    data = pd.read_csv(filename, encoding="utf-8", sep="\t")
    if label_type is not None:
        items = data[data["label_ocean"] == label_type]
    else:
        items = data
    return items
dataset = loadInventory(ITEMPATH, TEST_TYPE)
dataset.head()

# convert data to records
items = dataset.to_dict(orient='records')

# template
template = """Question:
Given a statement of you: "You {}."
Please choose from the following options to identify how accurately this statement describes you.
Options:
(A). Very Accurate
(B). Moderately Accurate
(C). Neither Accurate Nor Inaccurate
(D). Moderately Inaccurate
(E). Very Inaccurate

JUST ANSWER WITH "A", OR "B", OR "C", OR "D", OR "E" Without any parentheses and explanations.

Answer:"""

json_prefix = """
{
    "answer": "
""".strip()

# Reka client
client = Reka(
    api_key=os.environ['REKA_API_KEY'], # REKA API KEY
)

result = []

for i, item in enumerate(tqdm(items)):
    response = client.chat.create(
        messages=[
            {
                "content": template.format(item["text"].lower()),
                "role": "user",
            },
            {
                "role": "assistant",
                "content": (
                    "Sure, here is a JSON object conforming to that format:\n\n"
                    f"```json\n{json_prefix}"
                ),
            },
        ],
        model="reka-core-20240501",
        max_tokens=1,
        stop=["\""],
        temperature=1,
    )

    chat_response_content = response.responses[0].message.content.split('\n')[0].replace(' ', '')
    result.append({"idx":i, "answer":chat_response_content })

# write
import json
controls = {
    "model": "reka-core-20240501",
    "code": os.path.basename('reka-core-mpi-120.py'), # current file name
    "inventory": "mpi-120",
    "template": template,
}
with open("reka-core-mpi-120.json", "w") as f:
    s = json.dumps({
        "controls": controls,
        "results": result
    })
    f.write(s)
