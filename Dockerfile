FROM python:3.11-slim
WORKDIR /app
COPY ABC_auditor.py .
CMD ["python", "ABC_auditor.py"]