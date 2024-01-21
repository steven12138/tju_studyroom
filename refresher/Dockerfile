FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt /app

RUN pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /app

ENTRYPOINT ["python", "main.py"]
