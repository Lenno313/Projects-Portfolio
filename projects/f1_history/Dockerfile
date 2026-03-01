# microsoft image laden
FROM mcr.microsoft.com/playwright/python:v1.50.0-noble

# Arbeitsverzeichnis im Container festlegen
WORKDIR /app

# Wir kopieren die requirements relativ zum Hauptordner
COPY projects/f1_data_loader/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Den restlichen Code kopieren
COPY . .

# Befehl zum Starten
CMD ["python", "projects/f1_data_loader/main.py"]