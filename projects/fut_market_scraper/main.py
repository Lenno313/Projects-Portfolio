from database import get_db_session, init_db, Base
import models
from ingestor import FifaPriceIngestor
from loguru import logger
import os
import csv
from collections import namedtuple
from datetime import datetime

PlayerRecord = namedtuple('PlayerRecord', ['f_name', 'l_name', 'f_id'])

def load_player_watchlist():
    watchlist = []
    csv_path = os.path.join(os.path.dirname(__file__), "player_watchlist.csv")
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                p = PlayerRecord(row['f_name'], row['l_name'], row['f_id'])
                watchlist.append(p)
        return watchlist
    except FileNotFoundError:
        return []

def load_rating_watchlist():
    """Lies die CSV-Datei für die Ratings aus."""
    ratings = []
    csv_path = os.path.join(os.path.dirname(__file__), "rating_watchlist.csv")
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ratings.append(int(row["rating"].strip()))
    except Exception as e:
        logger.error(f"Fehler bei ratings.csv: {e}")
        return []
    return ratings

def main():
    init_db(models.Base)

    logger.info("Starte FUT Scraper...")
    start_time = datetime.now().replace(second=0, microsecond=0)

    with get_db_session() as session:
        ingestor = FifaPriceIngestor(session)

        watchlist = load_player_watchlist()

        for player in watchlist:
            ingestor.fetch_by_player(f_name=player.f_name, l_name=player.l_name, f_id=player.f_id, start_time=start_time)

        rating_list = load_rating_watchlist()
        for rating in rating_list:
            ingestor.fetch_by_rating(rating, start_time=start_time)
        
        session.commit()
        
    logger.success("FUT-Preise erfolgreich abgerufen!")

if __name__ == "__main__":
    main()
