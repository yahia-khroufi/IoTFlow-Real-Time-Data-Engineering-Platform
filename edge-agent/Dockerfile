FROM python:3.12-slim

WORKDIR /app

COPY ./edge-agent/requirements.txt .
RUN pip install --no-cache-dir --default-timeout=600 -r requirements.txt
COPY common ./common
COPY edge-agent ./edge-agent
COPY models ./models

ENV PYTHONPATH=/app
 
CMD ["python", "edge-agent/main.py"]

