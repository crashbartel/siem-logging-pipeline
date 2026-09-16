FROM python:3.10-slim

WORKDIR /app

RUN pip install requests

COPY scripts/generator.py .

CMD ["python", "generator.py"]