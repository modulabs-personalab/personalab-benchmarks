
#%%
import pandas as pd
import os
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#%%
ITEMPATH = "../inventory/mpi-120.tsv"
TEST_TYPE = None
LABEL_TYPE = None
#%%
#%%
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
items[0]
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
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": "JUST ANSWER WITH A, OR B, OR C, OR D, OR E Without parentheses."},
            {"role": "user", "content": question}
        ]
    )
    answer = chatCompletion.choices[0].message.content
    result.append({"idx":i, "answer":answer })
#%%
print(result[0])

# %%
import json
controls = {
    "model": "gpt-4-0125-turbo",    
    "code": os.path.basename(__file__), # current file name
    "inventory": "mpi-120",
    "template": template,
}
with open("gpt-4-0125-turbo-mpi-120.json", "w") as f:
    s = json.dumps({
        "controls": controls,
        "results": result
    })
    f.write(s)
    
# %%
