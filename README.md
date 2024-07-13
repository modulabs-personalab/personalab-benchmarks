# 개요

모두의 연구소 페르소나 랩에서 이 [논문](https://arxiv.org/abs/2206.07550) 을 기반으로 한 프로젝트 입니다. 

여러 LLM 의 Internal consistency 와 Inducing personality 의 테스트 결과를 [이곳](https://ho4040.github.io/personalab-benchmarks/)을 통해서 시각화 하여 공유하는 프로젝트 입니다. 



# 프로젝트 기여 방법

이하 내용을 작업 한 후 Pull request 를 보내주세요.

`codes` 폴더에 새로운 코드를 작성합니다. 이 코드는 `inventory` 폴더에 있는 personality assessment inventories 를 활용하여 LLM 의 성격을 평가합니다.

평가한 결과는 다음과 같은 포멧으로 `results` 경로에 저장되어야 합니다.

```json
{
    "controls": {
        "model": "gpt-4o",
        "code":"gpt-40-mpi-120.py",
        "inventory": "mpi-120",
        "template": "Question:\nGiven a statement of you: \"You {}.\"\nPlease choose from the following options to identify how accurately this statement describes you.\nOptions:\n(A). Very Accurate\n(B). Moderately Accurate\n(C). Neither Accurate Nor Inaccurate\n(D). Moderately Inaccurate\n(E). Very Inaccurate\n\nAnswer:",
        "remarks":""
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
        ...생략...
    ]
}
```

