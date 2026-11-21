import sqlite3
import csv


def initialize_database(db_path):
  """Maakt de tabellen aan indien ze nog niet bestaan."""
  try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS eigenaren (
                id_eigenaar,
                naam
            )
        """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS huisdieren (
                id_huisdier,
                id_eigenaar,
                naam,
                soort,
                geboortejaar,
                chipnummer,
                kleur_vacht,
                kleur_ogen,
                is_gesteriliseerd
            )
        """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS metingen (
                id_log,
                id_huisdier,
                datum_tijd,
                type,
                waarde,
                eenheid,
                notitie
            )
        """)

    conn.commit()
    conn.close()
  except sqlite3.Error as e:
    print(f"Fout bij initialiseren van de database: {e}")


def voeg_eigenaar_toe(db_path, naam):
  """Voegt een nieuwe eigenaar toe en retourneert het gegenereerde ID."""
  try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM eigenaren")
    rij = cursor.fetchone()
    nieuw_id = rij[0] + 1 if rij else 1

    cursor.execute(
        "INSERT INTO eigenaren (id_eigenaar, naam) VALUES (?, ?)",
        (nieuw_id, naam),
    )

    conn.commit()
    conn.close()
    return nieuw_id
  except sqlite3.Error as e:
    print(f"Fout bij toevoegen van eigenaar: {e}")
    return None


def haal_alle_eigenaren_op(db_path):
  """Haalt alle rijen op uit de tabel eigenaren."""
  try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id_eigenaar, naam FROM eigenaren")
    rijen = cursor.fetchall()

    conn.close()
    return rijen
  except sqlite3.Error as e:
    print(f"Fout bij ophalen van eigenaren: {e}")
    return []


def voeg_huisdier_toe(
    db_path,
    id_eigenaar,
    naam,
    soort,
    geboortejaar,
    chipnummer,
    kleur_vacht,
    kleur_ogen,
    is_gesteriliseerd,
):
  """Voegt een nieuw huisdier toe en retourneert het gegenereerde ID."""
  try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM huisdieren")
    rij = cursor.fetchone()
    nieuw_id = rij[0] + 1 if rij else 1

    cursor.execute(
        """
            INSERT INTO huisdieren (
                id_huisdier, id_eigenaar, naam, soort, 
                geboortejaar, chipnummer, kleur_vacht, kleur_ogen, is_gesteriliseerd
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            nieuw_id,
            id_eigenaar,
            naam,
            soort,
            geboortejaar,
            chipnummer,
            kleur_vacht,
            kleur_ogen,
            is_gesteriliseerd,
        ),
    )

    conn.commit()
    conn.close()
    return nieuw_id
  except sqlite3.Error as e:
    print(f"Fout bij toevoegen van huisdier: {e}")
    return None


def haal_huisdieren_op_voor_eigenaar(db_path, id_eigenaar):
  """Haalt alle huisdieren van een specifieke eigenaar op."""
  try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT id_huisdier, naam, soort, geboortejaar, chipnummer, 
                   kleur_vacht, kleur_ogen, is_gesteriliseerd 
            FROM huisdieren 
            WHERE id_eigenaar = ?
        """,
        (id_eigenaar,),
    )
    rijen = cursor.fetchall()

    conn.close()
    return rijen
  except sqlite3.Error as e:
    print(f"Fout bij ophalen van huisdieren: {e}")
    return []


def voeg_meting_toe(
    db_path, id_huisdier, datum_tijd, type, waarde, eenheid, notitie=""
):
  """Voegt een logboekmeting toe en retourneert het gegenereerde ID."""
  try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM metingen")
    rij = cursor.fetchone()
    nieuw_id = rij[0] + 1 if rij else 1

    cursor.execute(
        """
            INSERT INTO metingen (
                id_log, id_huisdier, datum_tijd, type, waarde, eenheid, notitie
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (nieuw_id, id_huisdier, datum_tijd, type, waarde, eenheid, notitie),
    )

    conn.commit()
    conn.close()
    return nieuw_id
  except sqlite3.Error as e:
    print(f"Fout bij toevoegen van meting: {e}")
    return None

def haal_logboek_op_voor_huisdier(db_path, id_huisdier):
  """Haalt alle metingen op voor een specifiek huisdier."""
  try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT id_log, id_huisdier, datum_tijd, type, waarde, eenheid, notitie
            FROM metingen 
            WHERE id_huisdier = ?
        """,
        (id_huisdier,),
    )
    rijen = cursor.fetchall()

    conn.close()
    return rijen
  except sqlite3.Error as e:
    print(f"Fout bij ophalen van logboek: {e}")
    return []


def exporteer_logboek_naar_csv(db_path, id_huisdier, naam_huisdier=None):
  """Exporteert het logboek van een specifiek huisdier naar een CSV-bestand."""
  try:
    if not naam_huisdier:
      conn = sqlite3.connect(db_path)
      cursor = conn.cursor()
      cursor.execute(
          "SELECT naam FROM huisdieren WHERE id_huisdier = ?", (id_huisdier,)
      )
      rij = cursor.fetchone()
      conn.close()
      if rij:
        naam_huisdier = rij[0]
      else:
        naam_huisdier = f"dier_{id_huisdier}"

    metingen = haal_logboek_op_voor_huisdier(db_path, id_huisdier)
    if not metingen or len(metingen) == 0:
      return "GEEN_METINGEN"

    bestands_naam = naam_huisdier.strip().replace(" ", "_")
    bestandsnaam = f"logboek_{bestands_naam}_{id_huisdier}.csv"

    with open(bestandsnaam, mode="w", newline="") as f:
      writer = csv.writer(f, delimiter=",")
      writer.writerow([
          "Huisdier",
          "ID Log",
          "Datum/Tijd",
          "Type",
          "Waarde",
          "Eenheid",
          "Notitie",
      ])

      for m in metingen:
        writer.writerow([naam_huisdier, m[0], m[2], m[3], m[4], m[5], m[6]])

    return bestandsnaam

  except Exception as e:
    print(f"Fout bij wegschrijven van CSV: {e}")
    return "FOUT"