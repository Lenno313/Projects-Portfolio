import fastf1
import os
from database import get_db_session
from .models import DimDriver, DimRace, FactResult
from loguru import logger

class F1Ingestor:
    def __init__(self, cache_dir: str = 'projects/f1_history/f1_cache'):
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        fastf1.Cache.enable_cache(cache_dir)

    def get_or_create_driver(self, db, driver_res):
        """Prüft, ob Fahrer existiert. Falls nicht, wird er angelegt."""
        driver = db.query(DimDriver).filter_by(driver_name=driver_res['FullName']).first()
        if not driver:
            driver = DimDriver(
                driver_name=driver_res['FullName'],
                constructor=driver_res['TeamName']
            )
            db.add(driver)
            db.flush() # ID generieren
        return driver

    def ingest_2025_results(self):
        """Lädt Ergebnisse Saison 2025 in das Star-Schema."""
        schedule = fastf1.get_event_schedule(2025)
        
        for _, event in schedule.iterrows():
            if event['EventFormat'] == 'testing':
                continue
                
            try:
                # Session laden (nur Ergebnisse)
                session = fastf1.get_session(2025, event['EventName'], 'R')
                session.load(telemetry=False, weather=False, laps=False)
                
                with get_db_session() as db:
                    # 1. Dimension: Rennen
                    race = db.query(DimRace).filter_by(season=2025, round=event['RoundNumber']).first()
                    if not race:
                        race = DimRace(
                            season=2025,
                            round=event['RoundNumber'],
                            circuit_name=event['Location'],
                            date=str(event['EventDate'])
                        )
                        db.add(race)
                        db.flush()

                    # 2. Dimension & Fakten: Ergebnisse
                    for _, driver_res in session.results.iterrows():
                        # Fahrer in DimDriver sicherstellen
                        driver = self.get_or_create_driver(db, driver_res)

                        # Faktentabelle füllen (FactResult)
                        res = FactResult(
                            race_id=race.id,
                            driver_id=driver.id,
                            position=int(driver_res['Position']),
                            points=float(driver_res['Points']),
                            fastest_lap_time=str(driver_res['Time']) # Oder spezifische Spalte
                        )
                        db.add(res)
                    
                    db.commit() # Alles zusammen speichern
                logger.success(f"Update: {event['EventName']} erfolgreich.")
                
            except Exception as e:
                logger.debug(f"Event {event['EventName']} fehlgeschlagen.")
