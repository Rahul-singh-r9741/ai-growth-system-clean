FROM python:3.11-slim

WORKDIR /app

# Copy only backend
COPY . /app/backend


# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn python-dotenv requests

EXPOSE 8000

CMD sh -c "uvicorn backend.ai:app --host 0.0.0.0 --port ${PORT:-8000}"
