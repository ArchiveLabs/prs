FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set non-sensitive environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY ./prs/ /app/prs/
RUN chmod +x /app/prs/app.py

RUN apt-get update && apt-get install -y nginx
RUN adduser --disabled-password --gecos "" nginx

COPY ./docker/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/nginx/conf.d/prs.conf /etc/nginx/conf.d/prs.conf

# Run FastAPI app and Nginx
CMD ["sh", "-c", "\
  python -m uvicorn prs.app:app \
    --host 0.0.0.0 \
    --port 1337 \
    --workers=${PRS_WORKERS:-1} \
    --log-level=${PRS_LOG_LEVEL:-info} \
    ${PRS_RELOAD:+--reload} & \
  exec nginx \
"]
