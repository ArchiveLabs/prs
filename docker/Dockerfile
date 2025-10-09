FROM python:3.11

WORKDIR /app

# Install system dependencies including git
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user and group
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Set non-sensitive environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Copy and set permissions for application files
COPY ./prs/ /app/prs/
RUN chmod +x /app/prs/app.py
RUN chown -R appuser:appgroup /app

# Switch to the non-root user before running the app
USER appuser

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
