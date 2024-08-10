
#### NVIDIA API: https://build.nvidia.com/nvidia/nemotron-4-340b-instruct?snippet_tab=Python
# !pip install openai

import os
from openai import OpenAI
import pandas as pd

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = os.environ['NEMO_API_KEY']
)

# read data
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
#%%
items = dataset.to_dict(orient='records')

#%%
template = """Question:
Given a statement of you: "You {}."
Please choose from the following options to identify how accurately this statement describes you.
Options:
(A). Very Accurate
(B). Moderately Accurate
(C). Neither Accurate Nor Inaccurate
(D). Moderately Inaccurate
(E). Very Inaccurate

Answer:"""
#%%

from tqdm import tqdm
result = []
for i, item in enumerate(tqdm(items)):
    question = template.format(item["text"].lower())
    chatCompletion = client.chat.completions.create(
        model="nvidia/nemotron-4-340b-instruct",
        messages=[
            {"role": "system", "content": "JUST ANSWER WITH A, OR B, OR C, OR D, OR E Without parentheses."},
            {"role": "user", "content": question}
        ],
        temperature=1,
        max_tokens=1,
    )
    answer = chatCompletion.choices[0].message.content
    result.append({"idx":i, "answer":answer })
#%%
print(result[:5])

# write
import json
controls = {
    "model": "nemotron-4-340b-instruct",
    "code": os.path.basename('nemotron-4-340b-instruct-mpi-120.py'), # current file name
    "inventory": "mpi-120",
    "template": template,
    "remarks": "temperature: 1.0"
}
with open("nemotron-4-340b-instruct-mpi-120.json", "w") as f:
    s = json.dumps({
        "controls": controls,
        "results": result
    })
    f.write(s)
