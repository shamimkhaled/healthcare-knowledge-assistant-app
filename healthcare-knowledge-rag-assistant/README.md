# Healthcare Knowledge RAG Assistant
FastAPI Backend  for a RAG-powered knowledge based assistant that answers queries based on retrieval-augmented context after reading medical materials in English and Japanese.

## Features

- FastAPI that uses `/ingest`, `/retrieve`, and `/generate`
- FAISS plus sentence-transformers for retrieval and embedding
- English and Japanese language identification; bilingual output automatically corresponds to the query language
- Authentication of API keys using `X-API-Key`
- GitHub Actions CI/CD and Dockerfile


## Requirements

- Python 3.11+
- Docker

## GitHub Repo Code Files: 
```bash
git clone https://github.com/shamimkhaled/healthcare-knowledge-assistant-app.git    
```

## Setup


```bash
cd healthcare-knowledge-rag-assistant
```

```bash
python -m venv venv
source venv/bin/activate (Linux/Mac)
```

```bash
pip install -r requirements.txt
cp .env.example .env
```

Set `API_KEY` in `.env` ( such as `API_KEY=TEST-API-SW56-3451`).

## Run locally

```bash
uvicorn app.main:app --reload
```

**Build and run locally with Docker:**

```bash
docker build -t healthcare-assistant .
docker run -p 8000:8000 -e API_KEY=TEST-API-SW56-3451 healthcare-assistant
```

Service runs at `http://localhost:8000`.

## API with response

All endpoints require the `X-API-Key` header.

### Health

```bash
curl http://localhost:8000/health
```

### Ingest

```bash
curl -X POST \
  -H "X-API-Key: TEST-API-SW56-3451" \
  -F "files=@data/doc1.txt" \
  http://localhost:8000/ingest
```
Response:
```bash
{
    "message": "Ingestion complete.",
    "files": [
        {
            "filename": "doc1.txt",
            "language": "en",
            "chunks": 1
        }
    ]
}
```

### Retrieve

```bash
curl -H "X-API-Key: TEST-API-SW56-3451" \
  "http://localhost:8000/retrieve?query=diabetes"
```

Response - 
```bash 
{
    "results": [
        {
            "text": "Type 2 diabetes management includes diet changes, regular physical activity,\nand glucose monitoring. First-line therapy often includes metformin, with\nadditional medications based on patient response and comorbidities.",
            "similarity_score": 0.0391
        },
        {
            "text": "Type 2 diabetes management includes lifestyle changes, glucose monitoring,\nand medications such as metformin. Clinical guidelines recommend regular\nHbA1c monitoring and individualized treatment plans based on comorbidities.\n",
            "similarity_score": 0.0382
        },
        {
            "text": "Type 2 diabetes can be controlled through dietary changes, regular exercises, and blood glucose level tests. \nThe treatment may also involve the administration of drugs such as metformin; however, this may vary depending on the response to the drugs.",
            "similarity_score": 0.0373
        }
    ]
}
```

### Generate

Response language defaults to the query language; optional `output_language` overrides it.

```bash
curl -X POST \
  -H "X-API-Key: TEST-API-SW56-3451" \
  -H "Content-Type: application/json" \
  -d '{"query":"What are the latest recommendations for Type 2 diabetes management?"}' \
  http://localhost:8000/generate
  
```

Response - 

```bash 
{
    "response": "Answer (mock LLM):\nBased on the retrieved documents text, It is a response based on your query.\n\nQuery: What are the latest recommendations for Type 2 diabetes management?\n\nContext:\nType 2 diabetes management includes lifestyle changes, glucose monitoring,\nand medications such as metformin. Clinical guidelines recommend regular\nHbA1c monitoring and individualized treatment plans based on comorbidities.\n\n\nType 2 diabetes management includes diet changes, regular physical activity,\nand glucose monitoring. First-line therapy often includes metformin, with\nadditional medications based on patient response and comorbidities.\n\nType 2 diabetes can be controlled through dietary changes, regular exercises, and blood glucose level tests. \nThe treatment may also involve the administration of drugs such as metformin; however, this may vary depending on the response to the drugs.\n\nSources:\n- Type 2 diabetes management includes lifestyle changes, glucose monitoring,\nand medications such as metformin. Clinical guidelines recommend regular\nHbA1c monitoring and individualized treatment plans based on comorbidities.\n\n- Type 2 diabetes management includes diet changes, regular physical activity,\nand glucose monitoring. First-line therapy often includes metformin, with\nadditional medications based on patient response and comorbidities.\n- Type 2 diabetes can be controlled through dietary changes, regular exercises, and blood glucose level tests. \nThe treatment may also involve the administration of drugs such as metformin; however, this may vary depending on the response to the drugs.\n\n(Mock response: In Production, LLM  generate this.)",
    "sources": [
        "Type 2 diabetes management includes lifestyle changes, glucose monitoring,\nand medications such as metformin. Clinical guidelines recommend regular\nHbA1c monitoring and individualized treatment plans based on comorbidities.\n",
        "Type 2 diabetes management includes diet changes, regular physical activity,\nand glucose monitoring. First-line therapy often includes metformin, with\nadditional medications based on patient response and comorbidities.",
        "Type 2 diabetes can be controlled through dietary changes, regular exercises, and blood glucose level tests. \nThe treatment may also involve the administration of drugs such as metformin; however, this may vary depending on the response to the drugs."
    ]
}

```


With explicit language:

```bash
curl -X POST \
  -H "X-API-Key: TEST-API-SW56-3451" \
  -H "Content-Type: application/json" \
  -d '{"query":"diabetes","output_language":"ja"}' \
  http://localhost:8000/generate
```


Response - 

```bash 
{
    "response": "回答 (LLM を模擬):\n取得した文書テキストに基づいて、クエリに基づいた応答です。\n\n質問: 2 型糖尿病管理に関する最新の推奨事項は何ですか?\n\nコンテキスト:\n2 型糖尿病の管理には、ライフスタイルの変更、血糖値のモニタリング、\nメトホルミンなどの薬も。臨床ガイドラインでは定期的な治療を推奨しています\nHbA1c モニタリングと併存疾患に基づく個別の治療計画。\n\n\n2 型糖尿病の管理には、食事の変更、定期的な身体活動、\nそしてグルコースモニタリング。第一選択療法にはメトホルミンが含まれることがよくあります。\n患者の反応や併存疾患に基づいて追加の薬剤を投与します。\n\n2 型糖尿病は、食事の変更、定期的な運動、血糖値検査によって制御できます。 \n治療にはメトホルミンなどの薬物の投与が含まれる場合もあります。ただし、これは薬に対する反応によって異なる場合があります。\n\n出典:\n- 2 型糖尿病の管理には、ライフスタイルの変更、血糖値のモニタリング、\nメトホルミンなどの薬も。臨床ガイドラインでは定期的な治療を推奨しています\nHbA1c モニタリングと併存疾患に基づく個別の治療計画。\n\n- 2 型糖尿病の管理には、食事の変更、定期的な身体活動、\nそしてグルコースモニタリング。第一選択療法にはメトホルミンが含まれることがよくあります。\n患者の反応や併存疾患に基づいて追加の薬剤を投与します。\n- 2 型糖尿病は、食事の変更、定期的な運動、血糖値検査によって制御できます。 \n治療にはメトホルミンなどの薬物の投与が含まれる場合もあります。ただし、これは薬に対する反応によって異なる場合があります。\n\n(模擬応答: 運用環境では、LLM がこれを生成します。)",
    "sources": [
        "Type 2 diabetes management includes lifestyle changes, glucose monitoring,\nand medications such as metformin. Clinical guidelines recommend regular\nHbA1c monitoring and individualized treatment plans based on comorbidities.\n",
        "Type 2 diabetes management includes diet changes, regular physical activity,\nand glucose monitoring. First-line therapy often includes metformin, with\nadditional medications based on patient response and comorbidities.",
        "Type 2 diabetes can be controlled through dietary changes, regular exercises, and blood glucose level tests. \nThe treatment may also involve the administration of drugs such as metformin; however, this may vary depending on the response to the drugs."
    ]
}

```


## Docker

```bash
docker build -t healthcare-assistant .
docker run -p 8000:8000 -e API_KEY=TEST-API-SW56-3451 healthcare-assistant
```

## Design Notes

**Scalability and modularity:** The Healthcare Knowledge RAG Assistant project is designed with discrete modules for embedding, FAISS storage, language detection, and translation, allowing each component to be extended individually. For larger document sets, FAISS db can be substituted by PGVector, Pinecone or a managed vector db; embedding and ingestion can be assigned to background workers to reduce request latency. Configuration is centralized, allowing deployment targets (such as alternative API keys or index locations) to be updated without requiring code changes.

**Future improvements:** For production-quality answers, replace the dummy response in '/generate' with a real LLM (such as OpenAI or Anthropic). More complex chunking and re-ranking, observability for latency and cost, rate limitation, and multi-tenant isolation can be added as needed. Consider audit recording and compliance methods for healthcare purposes.

## CI/CD

GitHub Actions executes on push/PR, installing dependencies, linting with Ruff, and creating the Docker image (see '.github/workflows/ci.yml').
