
from fastapi import FastAPI, File, UploadFile, HTTPException
import tensorflow as tf, numpy as np, json, io, time, os
from PIL import Image

app = FastAPI(title="Plant Disease Detection API", version="1.0.0",
              description="Classifies crop diseases from leaf images")

MODEL_PATH       = os.environ.get("MODEL_PATH", "models/plant_disease_model_v2.h5")
CLASS_NAMES_PATH = os.environ.get("CLASS_NAMES_PATH", "class_names.json")
model = None
class_names = None

@app.on_event("startup")
async def load_model():
    global model, class_names
    model = tf.keras.models.load_model(MODEL_PATH)
    with open(CLASS_NAMES_PATH) as f:
        class_names = json.load(f)
    print(f"Model loaded — {len(class_names)} classes")

def preprocess(image_bytes, size=(224, 224)):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize(size)
    return np.expand_dims(np.array(img) / 255.0, axis=0)

@app.get("/")
async def root():
    return {"message": "Plant Disease Detection API", "version": "1.0.0",
            "endpoints": {"/predict": "POST image",
                          "/health":  "GET status",
                          "/docs":    "Swagger UI"}}

@app.get("/health")
async def health():
    return {"status": "healthy",
            "model_loaded": model is not None,
            "num_classes":  len(class_names) if class_names else 0,
            "timestamp":    time.time()}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    contents = await file.read()
    img  = preprocess(contents)
    t0   = time.time()
    preds = model.predict(img, verbose=0)
    top5 = [{"class": class_names[str(i)],
              "confidence": float(preds[0][i])}
             for i in np.argsort(preds[0])[::-1][:5]]
    return {"status":         "success",
            "filename":       file.filename,
            "top_prediction": top5[0],
            "top5":           top5,
            "is_healthy":     "healthy" in top5[0]["class"].lower(),
            "inference_ms":   round((time.time() - t0) * 1000, 2)}
