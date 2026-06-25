# 🌿 Plant Disease Detection
Deep Learning project to classify crop diseases from leaf images using CNNs and Transfer Learning.

## Dataset
PlantVillage — 20,000+ images, 15 classes across multiple crops

## Models
| Model | Architecture | Val Accuracy |
|-------|-------------|-------------|
| V1 | Custom CNN (3 blocks) | 93.0% |
| V2 | MobileNetV2 Transfer Learning | 97.4% |

## Quick Start
```bash
docker build -t plant-disease-api:v1 .
docker run -p 8000:8000 plant-disease-api:v1
```

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/predict` | POST | Upload leaf image for classification |
| `/docs` | GET | Swagger UI |

## Project Structure
```
PlantDiseaseProject/
├── src/                  # FastAPI app
├── models/               # Trained models
├── training/             # Training scripts
├── data/                 # Dataset
├── kubernetes/           # K8s manifests
├── .github/workflows/    # CI/CD pipeline
├── Dockerfile
├── requirements.txt
└── README.md
```
