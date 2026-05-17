FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY lib.py .
COPY app.py .
COPY demo-faas-call.html .

EXPOSE 8080

CMD ["gunicorn", "--timeout", "180","--bind", "0.0.0.0:8080", "app:app"]