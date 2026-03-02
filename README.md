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

#### Abfragen von Preisen einzelner Spieler
Jede Spielerkarte hat in FUTWIZ eine eigene id, welche zusammen mit dem Spielernamen die URL vervollständigt (z.B. 'BASE_URL + /cristiano-ronaldo/20785'). Da Spieler mehrere Karten besitzen können, ist diese id der Primärschlüssel zu den Karten.

<img width="803" height="348" alt="image" src="https://github.com/user-attachments/assets/7147ccd1-6135-4db8-9539-fc9d90dcb2a2" />

Auf der Spielerseite steht dann jeweils der Preis der Karte auf dem Playstation- und auf dem PC-Markt. Diesen können wir mittels der Playwright-API auslesen lassen.

Welche Spielerkarten man abfragen möchte kann man in einer CSV-Datei eintragen, dazu benötigt man jeweils den Vornamen und Nachnamen des Spielers und ebenso die id der speziellen Karte.

Vor der Preisabfrage werden Datenbankeinträge für die Spieler angelegt. Nach der Abfrage wird dann der Preis mit Zeitpunkt und entsprechender Karten-ID gespeichert.

#### Abfragen von Preisen für bestimmte Bewertungen
FUTWIZ bietet die Möglichkeit, sich die niedrigsten Preise für jede Spielerbewertung anzeigen zu lassen.
Diese haben eine Relevanz für 'Squad-Building-Challenges', bei denen man Teams mit bestimmten Mindestanforderungen (zB. 86 Gesamtwertung) für Belohnungen eintauschen kann.

<img width="787" height="599" alt="image" src="https://github.com/user-attachments/assets/2f791751-1524-4ce1-b214-a8a868d43cea" />

Diese Bewertungen sind immer in der gleichen Reihenfolge und haben für die relevanten Bewertungen, bis 92 reicht, immer zehn Einträge.
Somit kann ich mir auf Basis der gewünschten Bewertung (z.B. 89), die zehn Positionen der jeweiligen Preise berechnen und diese auslesen.

Die Ergebnisse speichere ich als 'RatingSnapshots' in einer Tabelle. Diese enthält jeweils den Zeitpunkt, die Bewertung und den Preis. Zusätzlich schreibe ich in die Tabelle, der 'wie vielt günstigste' Preis es in dieser Bewertung war. So kann ich beispielsweise die günstigsten 5 Preise für die Bewertung in den letzten 3 Wochen auslesen. 

<img width="765" height="313" alt="image" src="https://github.com/user-attachments/assets/5ab01aff-8057-4aed-b19d-3af33fe9be52" />

Welche Bewertungen man abfragen möchte kann man in einer CSV-Datei eintragen.
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
    - [x] Formel1-Historie (Star-Schema)
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
