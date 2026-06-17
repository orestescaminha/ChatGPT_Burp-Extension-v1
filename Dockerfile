FROM python:3.13-slim

WORKDIR /app
COPY ai_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ai_service/ .

CMD ["python", "main.py"]
