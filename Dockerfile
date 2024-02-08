FROM python:3.10.6-slim

WORKDIR /code

COPY ./app/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN apt update -y
RUN apt upgrade -y
COPY ./app /code/app
CMD ["gunicorn", "app.main:app", "--workers", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8081"]
