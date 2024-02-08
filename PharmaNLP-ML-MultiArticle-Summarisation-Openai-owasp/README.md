# PharmaNLP-ML-MultiArticle-Summarisation-Openai


### For dev
Require Python 3.10.6
```bash

pip install -r app/requirements.txt

# set DEBUG = True in config.py

uvicorn app.main:app --host 0.0.0.0 --port 8081 --reload

```

### Needed Env variables and samples

```bash

ELASTICSEARCH_END_POINT = "http://172.17.0.1:9200"

ELASTICSEARCH_USER_NAME = "elastic"

ELASTICSEARCH_PASSWORD = r"0*****************************k"

MULTI_ARTICLE_SUMMARY_CHAT_OPEN_AI_AZURE_ENGINE = "deployment-1"

MULTI_ARTICLE_SUMMARY_CHAT_OPEN_AI_AZURE_OPENAI_API_TYPE = "azure"

MULTI_ARTICLE_SUMMARY_CHAT_OPEN_AI_AZURE_OPENAI_API_BASE = "https://sub-domain.openai.azure.com/"

MULTI_ARTICLE_SUMMARY_CHAT_OPEN_AI_AZURE_OPENAI_API_VERSION = "2022-12-01"

MULTI_ARTICLE_SUMMARY_CHAT_OPEN_AI_AZURE_OPENAI_API_KEY = "0******************************2"

```

### Create Docker container

```bash

sudo docker pull python:3.10.6-slim

sudo docker build -t image_name .

sudo docker run -d --name container_name -p 8081:8081 image_name

```

### Endpoint

```bash

Health check:
http://127.0.0.1:8081/
Method : GET


Web documentation:
http://127.0.0.1:8081/docs


Generate multi article summary:
http://127.0.0.1:8081/multi_summarizer
Method : POST
Body :
    {
        "project_id": 232881
    }


Generate table summary intro and title:
http://127.0.0.1:8081/get_table_summary_intro_and_title
Method : POST
Body :
    {
        "project_id": 232881
    }

```
