# Dockerfile
FROM python:3.13.5-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# default entrypoint just runs your script
CMD ["python3", "main.py"]
