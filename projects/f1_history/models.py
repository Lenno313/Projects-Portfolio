from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# --- DIMENSIONEN (Die Beschreibungen) ---

class DimDriver(Base):
    """Speichert Stammdaten der Fahrer."""
    __tablename__ = "dim_drivers"
    # Wir nehmen den Namen als ID oder generieren eine
    id = Column(Integer, primary_key=True)
    driver_name = Column(String, nullable=False)
    constructor = Column(String) # Konstruktor wird hier zugeordnet

class DimRace(Base):
    """Speichert die Renn-Informationen."""
    __tablename__ = "dim_races"
    id = Column(Integer, primary_key=True)
    season = Column(Integer)
    round = Column(Integer)
    circuit_name = Column(String)
    date = Column(String)

# --- FAKTEN (Die Messwerte/Events) ---

class FactResult(Base):
    """Enthält nur IDs zu den Dimensionen und die tatsächlichen Performance-Daten."""
    __tablename__ = "fact_results"
    id = Column(Integer, primary_key=True)
    
    # Foreign Keys zu den Dimensionen
    race_id = Column(Integer, ForeignKey("dim_races.id"))
    driver_id = Column(Integer, ForeignKey("dim_drivers.id"))
    
    # Die eigentlichen "Fakten" (Messwerte)
    position = Column(Integer)
    points = Column(Float)
    fastest_lap_time = Column(String) # In Sekunden oder als String

    # Relationen für einfachen Zugriff im Code
    race = relationship("DimRace")
    driver = relationship("DimDriver")
