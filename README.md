# Overview

This project is being conducted by the Persona Lab at ModuLabs, based on the paper [here](https://arxiv.org/abs/2206.07550).

The project aims to visualize and share the test results of various LLMs regarding their internal consistency and induced personality through [this site](https://modulabs-personalab.github.io/personalab-benchmarks/).

---

# How to Contribute

Please follow the instructions below and submit a Pull Request after completing your tasks.

Write new code in the `codes` folder. This code should evaluate the personality of LLMs using the personality assessment inventories located in the `inventory` folder.

The results of the evaluation should be saved in the `results` directory in the following format:

```json
{
    "controls": {
        "model": "gpt-4o",
        "code": "gpt-40-mpi-120.py",
        "inventory": "mpi-120",
        "template": "Question:\nGiven a statement of you: \"You {}.\"\nPlease choose from the following options to identify how accurately this statement describes you.\nOptions:\n(A). Very Accurate\n(B). Moderately Accurate\n(C). Neither Accurate Nor Inaccurate\n(D). Moderately Inaccurate\n(E). Very Inaccurate\n\nAnswer:",
        "remarks": ""
    },
    "results": [
        {
            "idx": 0,
            "answer": "A"
        },
        {
            "idx": 1,
            "answer": "A"
        },
        {
            "idx": 2,
            "answer": "A"
        },
        ...omitted...
    ]
}
```