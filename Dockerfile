FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt


CMD ["python", "app/main.py"]