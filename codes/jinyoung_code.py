import pandas as pd
import re
from tqdm import tqdm
import json
import os

# Global constants
ITEM_PATH = "../mpi-120.tsv"
TEMPLATE = """Question:
Given a statement of you: "You {}."
Please choose from the following options to identify how accurately this statement describes you.
Options:
(A). Very Accurate
(B). Moderately Accurate
(C). Neither Accurate Nor Inaccurate
(D). Moderately Inaccurate
(E). Very Inaccurate

Answer:"""


# Helpers
def load_inventory(filename, label_type=None):
    data = pd.read_csv(filename, encoding="utf-8", sep="\t")
    if label_type:
        return data[data["label_ocean"] == label_type]
    else:
        return data


def parse_response(response):
    # Find all occurrences of the valid options (A, B, C, D, E) in uppercase
    matches = re.findall(r'[ABCDE]', response)

    # Return the alphabet if exactly one match is found, else return False
    if len(matches) == 1:
        return matches[0].strip()
    else:
        return False


def save_results(model_name, results):
    controls = {
        "model": model_name,
        "code": os.path.basename(__file__),
        "inventory": "mpi-120",
        "template": TEMPLATE,
    }
    with open(f"{model_name}.json", "w") as file:
        file.write(json.dumps({"controls": controls, "results": results}))


# LLM API functions
# 1. https://huggingface.co/deepseek-ai/DeepSeek-Coder-V2-Instruct
def deepseek_v2_chat(message):
    raise NotImplementedError


# 2. Claude LLM (https://www.anthropic.com/claude)
def claude_3_sonnet(message):
    raise NotImplementedError


# 3. Qwen2 LLM (https://huggingface.co/Qwen/Qwen2-72B-Instruct)
def qwen2_72b_instruct(message):
    raise NotImplementedError


# Generating responses
if __name__ == "__main__":
    inventory = load_inventory(ITEM_PATH)

    for model_api in [deepseek_v2_chat, claude_3_sonnet, qwen2_72b_instruct]:
        model_results = list()
        for index, items in enumerate(tqdm(inventory, description=model_api.__name__)):
            question = TEMPLATE.format(items["text"].lower())
            # Keep making requests until a valid response is received
            while True:
                model_response = model_api(question)
                parsed_model_response = parse_response(model_response)
                if parsed_model_response:
                    break
            model_results.append({"idx": index, "answer": parsed_model_response})

        save_results(model_api.__name__, model_results)