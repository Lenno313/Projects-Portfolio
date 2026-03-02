# Data-Engineer-Projects

Herzlich willkommen in meinem Data Engineering Repository! Hier dokumentiere ich den Aufbau und die Automatisierung verschiedener Daten-Pipelines, die auf einem **Raspberry Pi Home-Server** in einer **Docker-Umgebung** laufen sollen.

## Motivation
Ziel dieses Repositories ist es, bisherige Projekte von mir zu modularisieren und in strukturierte Daten-Pipelines zu verpacken.

---

## Die Projekte

### Projekt 1: F1 Telemetry & Race Analytics

#### Zusammenfassung
Dieses Projekt ist zweigeteilt: **1a** befasst sich mit der hochfrequenten Echtzeit-Telemetrie via SignalR, während **1b** ein klassisches Data Warehouse für historische Rennergebnisse aufbaut.

<details>
<summary>Details anzeigen</summary>

#### Projekt 1a: Live-Telemetrie (Streaming)
- **Architektur:** Event-driven Ingestor mit asynchronen Callbacks.
- **Features:** In-Memory-Buffering für Bulk-Inserts, Backup-Load-Logik bei Verbindungsabbruch.
- **Tech-Stack:** FastF1 (Livetiming Client), SignalR, NumPy (Resampling).

#### Projekt 1b: Race History (Batch / Warehouse)
- **Architektur:** Klassische ETL-Pipeline zur Historisierung von Saisondaten.
- **Datenmodell:** Implementierung eines Star-Schemas in SQL.
- **Tech-Stack:** Pandas, SQLAlchemy.
</details>

---

### Projekt 2: FIFA Ultimate Team Market Tracker (FUTWIZ)

#### Zusammenfassung
Überwachung von Spielerpreisen auf dem Transfermarkt. Fokus liegt auf der Extraktion von Daten aus HTML-Strukturen, wo keine offizielle API existiert.

<details>
<summary>Details anzeigen</summary>

#### Beschreibung
- **Scraping-Layer:** Headless-Browser-Automatisierung mit Playwright zum Umgehen dynamischer Inhalte.
- **Datenfluss:** Transformation von HTML-Rohdaten in relationale Strukturen via SQLAlchemy.
- **Automatisierung:** Zeitgesteuerte Preisabfragen (Cron-Jobs) zur Erstellung von Zeitreihen-Analysen der Marktwerte.
</details>

---

### Projekt 3: Garmin Health & Activity Ingestor 

#### Zusammenfassung
Abruf von persönlichen Aktivitätsdaten (Leistung, Herzfrequenz, GPS, etc.). Vorbereitung der Daten für ein späteres Dashboard.

<details>
<summary>Details anzeigen</summary>

#### Beschreibung
- **Ingestion:** Anbindung an die Garmin Connect API zum Download verschachtelter JSON-Aktivitätsfiles.
- **Data Cleansing:** Flattening von komplexen JSON-Strukturen in flache Tabellenformate.
- **Ziel:** Bereitstellung von KPIs zur Belastungssteuerung und langfristigen Fitness-Entwicklung.
</details>

---

## Infrastruktur (Raspberry Pi Setup)

Die Steuerung erfolgt über eine zentrale `docker-compose.yml` auf einem Raspberry Pi.

<details>
<summary>Infrastruktur-Details & Docker-Setup</summary>

- **Datenbank:** PostgreSQL Container mit persistenten Volumes auf einer externen Festplatte.
- **Automatisierung:** - Die Skripte werden über Cronjobs auf dem Host-System oder innerhalb eines speziellen Cron-Containers getriggert.
  - Secrets (Passwörter/Keys) werden sicher über `.env`-Dateien verwaltet.
- **Monitoring:** (Geplant) Dashboard zur Überwachung der Pipeline-Status.

</details>

---

## Roadmap
#### Phase 1 - Code-Modularisierung & Aufsetzen der Infrastruktur
- [ ] Überführung der Skripte in eine geordnete Klassenstruktur (Ingestor-Pattern).
    - [ ] Projekt Ia: Live-Ingestor Logik (SignalR & Buffering)
    - [ ] Projekt Ib: History-ETL Pipeline
    - [x] FUT-Scraper
    - [ ] Garmin-Daten
- [ ] Initialer Aufbau der Datenbank-Schemata (SQLAlchemy).
    - [ ] F1 Star-Schema (Fact/Dimension Tables)
    - [x] FUT-Spielerpreise Schema
    - [ ] Garmin-Daten Schema
- [x] Erstellen & Testen von docker-compose & Dockerfiles
- [x] Neuaufsetzen des Raspberry Pi OS (Lite) und Konfiguration der Docker-Engine sowie Docker Compose.
- [ ] Einrichten der persistenten PostgreSQL-Instanz als Docker-Container auf externer Festplatte

#### Phase 2 
- [ ] Database Layer: Deployment des PostgreSQL-Containers
- [ ] Containerisierung: Erstellung von Docker-Images für jeden Ingestor.
- [ ] Automation: Implementierung der Cron-Logik (FIFA täglich, F1 rennwochenendspezifisch).
- [ ] Secret Management: Umstellung aller Hardcoded-Credentials auf Umgebungsvariablen (.env).

#### Phase 3: Weitere Feature-Ideen wie Analytics & Monitoring einbauen
- [ ] Data Quality Checks: Validierungsskripte zur Erkennung von Ingestions-Fehlern.
- [ ] Visualisierung: Aufbau eines Streamlit-Dashboards (Preisverläufe FIFA & Sektorenvergleiche F1).
- [ ] Health Check: Einbindung eines Monitoring-Tools (z.B. Portainer) zur Systemüberwachung.
