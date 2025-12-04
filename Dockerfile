# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Dependencies installieren
RUN pip install --no-cache-dir fastapi uvicorn[standard] xgboost numpy pydantic

# App-Code kopieren
COPY app.py ./

# Modell-Verzeichnis anlegen und Modell kopieren
RUN mkdir /models
COPY model.json /models/model.json

# Env-Var für Modellpfad
ENV MODEL_PATH=/models/model.json

# Container-Port (muss mit ServingTemplate übereinstimmen)
EXPOSE 8080

# Startbefehl für FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
