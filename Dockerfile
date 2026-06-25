FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 curl \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY models/plant_disease_model_v2.h5 ./models/
COPY class_names.json .
ENV MODEL_PATH=models/plant_disease_model_v2.h5
ENV CLASS_NAMES_PATH=class_names.json
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s \
    CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
