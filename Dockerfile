FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

ENV PORT=5000
ENV ENVIRONMENT=production

EXPOSE 5000

CMD ["python", "app/app.py"]
