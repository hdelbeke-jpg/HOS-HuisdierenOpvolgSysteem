import sqlite3
from config import DB_PATH
from models.eigenaar import Eigenaar
from models.huisdier import Huisdier
from models.meting import Meting

# 1. VERBINDING & TABELLEN AANMAKEN

def get_connection():
  """Maakt verbinding met SQLite en zet Foreign Keys actief aan."""
  conn = sqlite3.connect(DB_PATH)
  conn.execute("PRAGMA foreign_keys = ON;")
  return conn

def initialize_database():
  """Maakt de tabellen aan op basis van jouw specifieke klassen."""
  conn = get_connection()
  cursor = conn.cursor()

  # 1. Tabel Eigenaren
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS eigenaren (
            id_eigenaar INTEGER PRIMARY KEY AUTOINCREMENT,
            naam TEXT NOT NULL
        );
    """)

  # 2. Tabel Huisdieren (met jouw extra velden!)
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS huisdieren (
            id_huisdier INTEGER PRIMARY KEY AUTOINCREMENT,
            id_eigenaar INTEGER NOT NULL,
            naam TEXT NOT NULL,
            soort TEXT,
            geboortejaar INTEGER,
            chipnummer TEXT,
            kleur_vacht TEXT,
            kleur_ogen TEXT,
            is_gesteriliseerd INTEGER, -- SQLite bewaart booleans als 1 (True) of 0 (False)
            FOREIGN KEY (id_eigenaar) REFERENCES eigenaren(id_eigenaar) ON DELETE CASCADE
        );
    """)

  # 3. Tabel Metingen (het logboek)
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS metingen (
            id_log INTEGER PRIMARY KEY AUTOINCREMENT,
            id_huisdier INTEGER NOT NULL,
            datum_tijd TEXT NOT NULL,
            type TEXT NOT NULL,
            waarde REAL NOT NULL,
            eenheid TEXT NOT NULL,
            notitie TEXT,
            FOREIGN KEY (id_huisdier) REFERENCES huisdieren(id_huisdier) ON DELETE CASCADE
        );
    """)

  conn.commit()
  conn.close()
  print("Database succesvol aangemaakt met de nieuwe structuur!")

# 2. FUNCTIES VOOR EIGENAREN



def voeg_eigenaar_toe(naam):
  """Voegt een nieuwe eigenaar toe aan de database."""
  conn = get_connection()
  cursor = conn.cursor()

  cursor.execute(
      """
        INSERT INTO eigenaren (naam)
        VALUES (?)
    """,
      (naam,),
  )

  conn.commit()
  id_eigenaar = cursor.lastrowid
  conn.close()
  return id_eigenaar


def haal_alle_eigenaren_op():
  """Haalt alle eigenaren op en maakt Eigenaar-objecten aan."""
  conn = get_connection()
  cursor = conn.cursor()

  cursor.execute("SELECT id_eigenaar, naam FROM eigenaren ORDER BY naam")
  rijen = cursor.fetchall()
  conn.close()

  eigenaren = []
  for rij in rijen:
    e = Eigenaar(id_eigenaar=rij[0], naam=rij[1])
    eigenaren.append(e)

  return eigenaren

# 3. FUNCTIES VOOR HUISDIEREN

def voeg_huisdier_toe(
    id_eigenaar,
    naam,
    soort,
    geboortejaar,
    chipnummer,
    kleur_vacht,
    kleur_ogen,
    is_gesteriliseerd,
):
  """Voegt een nieuw huisdier toe met alle specifieke eigenschappen."""
  conn = get_connection()
  cursor = conn.cursor()

  # Zet True/False om naar 1 of 0 voor SQLite
  gesteriliseerd_int = 1 if is_gesteriliseerd else 0

  cursor.execute(
      """
        INSERT INTO huisdieren (id_eigenaar, naam, soort, geboortejaar, chipnummer, kleur_vacht, kleur_ogen, is_gesteriliseerd)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
      (
          id_eigenaar,
          naam,
          soort,
          geboortejaar,
          chipnummer,
          kleur_vacht,
          kleur_ogen,
          gesteriliseerd_int,
      ),
  )

  conn.commit()
  id_huisdier = cursor.lastrowid
  conn.close()
  return id_huisdier


def haal_huisdieren_op_voor_eigenaar(id_eigenaar):
  """Haalt alle huisdieren van een eigenaar op en zet ze om naar Huisdier-objecten."""
  conn = get_connection()
  cursor = conn.cursor()

  cursor.execute(
      """
        SELECT id_huisdier, naam, soort, geboortejaar, chipnummer, kleur_vacht, kleur_ogen, is_gesteriliseerd
        FROM huisdieren
        WHERE id_eigenaar = ?
        ORDER BY naam
    """,
      (id_eigenaar,),
  )

  rijen = cursor.fetchall()
  conn.close()

  huisdieren = []
  for rij in rijen:
    h = Huisdier(
        id_huisdier=rij[0],
        naam=rij[1],
        soort=rij[2],
        geboortejaar=rij[3],
        chipnummer=rij[4],
        kleur_vacht=rij[5],
        kleur_ogen=rij[6],
        is_gesteriliseerd=bool(rij[7]),  # Zet 1/0 weer om naar True/False
    )
    huisdieren.append(h)

  return huisdieren

# 4. FUNCTIES VOOR METINGEN (LOGBOEK)

def voeg_meting_toe(
    id_huisdier, datum_tijd, type, waarde, eenheid, notitie=""
):
  """Voegt een nieuwe meting of logboek-item toe."""
  conn = get_connection()
  cursor = conn.cursor()

  cursor.execute(
      """
        INSERT INTO metingen (id_huisdier, datum_tijd, type, waarde, eenheid, notitie)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
      (id_huisdier, datum_tijd, type, waarde, eenheid, notitie),
  )

  conn.commit()
  conn.close()


def haal_logboek_op_voor_huisdier(id_huisdier):
  """Haalt alle metingen op van een huisdier en zet ze om naar Meting-objecten."""
  conn = get_connection()
  cursor = conn.cursor()

  cursor.execute(
      """
        SELECT id_log, id_huisdier, datum_tijd, type, waarde, eenheid, notitie
        FROM metingen
        WHERE id_huisdier = ?
        ORDER BY datum_tijd DESC
    """,
      (id_huisdier,),
  )

  rijen = cursor.fetchall()
  conn.close()

  logboek = []
  for rij in rijen:
    m = Meting(
        id_log=rij[0],
        id_huisdier=rij[1],
        datum_tijd=rij[2],
        type=rij[3],
        waarde=rij[4],
        eenheid=rij[5],
        notitie=rij[6],
    )
    logboek.append(m)

  return logboek


if __name__ == "__main__":
  initialize_database()