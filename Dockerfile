FROM python:3.10-slim-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Periodically check if the FastAPI server responds with 200 OK
HEALTHCHECK --interval=600s --timeout=5s --start-period=10s --retries=3 \
    CMD curl --fail http://localhost:8000/ || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]