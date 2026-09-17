FROM python:3.10-slim

WORKDIR /app

COPY scripts/generator.py .

CMD ["python", "/app/generator.py"]