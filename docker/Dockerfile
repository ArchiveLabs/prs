FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set non-sensitive environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY ./prs/ /app/prs/
RUN chmod +x /app/prs/app.py

# Run FastAPI app
CMD ["sh", "-c", "\
  python -m uvicorn prs.app:app \
    --host 0.0.0.0 \
    --port 8083 \
    --workers=${PRS_WORKERS:-1} \
    --log-level=${PRS_LOG_LEVEL:-info} \
    --proxy-headers \
    ${PRS_RELOAD:+--reload} \
"]
