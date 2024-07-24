
# DeepSeek-v2-chat : https://platform.deepseek.com/api-docs/api/create-chat-completion
# !pip install openai
from openai import OpenAI
import re

client = OpenAI(api_key=os.environ['deepseek_api_key'], base_url="https://api.deepseek.com")

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
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "JUST ANSWER WITH A, OR B, OR C, OR D, OR E Without any parentheses."},
            {"role": "user", "content": question}
        ],
        temperature=1,
        max_tokens=3,
    )
    answer = chatCompletion.choices[0].message.content
    
    # 첫 알파벳만 추출
    match = re.search(r'[A-Za-z]', answer)
    if match: answer = match.group()

    result.append({"idx":i, "answer":answer })
#%%
print(result[:5])

# write
import json
controls = {
    "model": "deepseek-v2-chat",
    "code": os.path.basename('deepseek-v2-chat-mpi-120.py'), # current file name
    "inventory": "mpi-120",
    "template": template,
    "remarks": "temperature: 1.0, max_tokens: 3"
}
with open("deepseek-v2-chat-mpi-120.json", "w") as f:
    s = json.dumps({
        "controls": controls,
        "results": result
    })
    f.write(s)
