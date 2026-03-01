from database import get_db_session, init_db
from projects.f1_data_loader.ingestor import F1Ingestor
from loguru import logger

def main():
    init_db()

    logger.info("Starte das Laden der Formel 1 Daten ...")

    with get_db_session() as session:
        ingestor = F1Ingestor(session)

        # Beispiel - Daten von 2025 laden
        ingestor.ingest_2025_results()

        # TODO Einzelne Telemetrien von Rennen / Qualifyings laden
        
        session.commit()
        
    logger.success("Daten der Formel 1 erfolgreich abgerufen!")

if __name__ == "__main__":
    main()
