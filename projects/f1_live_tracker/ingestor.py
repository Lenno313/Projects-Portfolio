from loguru import logger
import pandas as pd
from sqlalchemy import create_engine
from fastf1.livetiming.client import SignalRClient

class LiveIngestor:
    def __init__(self, year, location, session_type, db_url):
        self.year = year
        self.location = location
        self.session_type = session_type
        self.engine = create_engine(db_url)
        self.buffer = []
        self.buffer_limit = 50  
        self.client = SignalRClient()

    def initial_load(self):
        """Sync bisheriger Session-Daten vor Live-Start."""
        logger.info(f"Initial Load gestartet: {self.location}")
        # TODO: FastF1 API call
        pass

    def clean_data(self, raw_data):
        """Flattening der JSON-Struktur."""
        return raw_data

    def backup_load_check(self):
        """Lückenschluss bei Disconnect."""
        pass

    def update_sql(self):
        """Bulk-Insert in DB."""
        if not self.buffer:
            return
        try:
            df = pd.DataFrame(self.buffer)
            df.to_sql('telemetry_live', con=self.engine, if_exists='append', index=False)
            logger.success(f"Buffer Flush: {len(self.buffer)} Records")
            self.buffer = []
        except Exception as e:
            logger.error(f"SQL-Fehler: {e}")

    def on_telemetry_received(self, data):
        """Async Callback für Live-Daten."""
        if data:
            cleaned = self.clean_data(data)
            self.buffer.append(cleaned)
            if len(self.buffer) >= self.buffer_limit:
                self.update_sql()

    def start(self):
        """Einstiegspunkt: Initial Load -> Streaming."""
        self.initial_load()
        logger.info("Verbinde zu SignalR...")
        self.client.on_telemetry = self.on_telemetry_received
        try:
            self.client.start()
        except KeyboardInterrupt:
            logger.warning("Manueller Stop - sichere Buffer...")
            self.update_sql()
