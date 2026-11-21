from datetime import datetime
from config import DB_PATH
from database import db_manager
from models.eigenaar import Eigenaar
from models.huisdier import Huisdier
from models.meting import Meting


def toon_menu():
  print("\n--- HUISDIEREN OPVOLG SYSTEEM (HOS) ---")
  print("1. Eigenaar toevoegen")
  print("2. Eigenaren bekijken")
  print("3. Huisdier toevoegen aan eigenaar")
  print("4. Huisdieren bekijken")
  print("5. Meting/logboek toevoegen")
  print("6. Logboek van een huisdier bekijken")
  print("7. Logboek van een huisdier exporteren naar CSV")
  print("0. Stoppen")


def toon_alle_eigenaren():
  """Hulpfunctie om alle geregistreerde eigenaren op te halen en te tonen."""
  rijen = db_manager.haal_alle_eigenaren_op(DB_PATH)
  if len(rijen) == 0:
    print("Er zijn nog geen eigenaren geregistreerd.")
    return []

  eigenaren = []
  for r in rijen:
    e = Eigenaar(id_eigenaar=r[0], naam=r[1])
    eigenaren.append(e)

  print("\n--- Overzicht Eigenaren ---")
  for e in eigenaren:
    print(f" - [{e.id_eigenaar}] {e.naam}")
  return eigenaren


def toon_alle_huisdieren_per_eigenaar():
  """Hulpfunctie om alle dieren per eigenaar te tonen."""
  rijen_eigenaren = db_manager.haal_alle_eigenaren_op(DB_PATH)
  if len(rijen_eigenaren) == 0:
    print("Er zijn nog geen eigenaren of huisdieren geregistreerd.")
    return []

  print("\n--- Overzicht Huisdieren per Eigenaar ---")
  beschikbare_dier_ids = []

  for r in rijen_eigenaren:
    eigenaar = Eigenaar(id_eigenaar=r[0], naam=r[1])
    print(f"\nEigenaar: {eigenaar.naam} (ID: {eigenaar.id_eigenaar})")

    rijen_dieren = db_manager.haal_huisdieren_op_voor_eigenaar(
        DB_PATH, eigenaar.id_eigenaar
    )
    if len(rijen_dieren) == 0:
      print("  (Geen geregistreerde huisdieren)")
    else:
      for d in rijen_dieren:
        dier = Huisdier(
            id_huisdier=d[0],
            naam=d[1],
            soort=d[2],
            geboortejaar=d[3],
            chipnummer=d[4],
            kleur_vacht=d[5],
            kleur_ogen=d[6],
            is_gesteriliseerd=bool(d[7]),  # <-- Hier stond d[8], dit is nu d[7]
        )
        print(f"  - Huisdier [{dier.id_huisdier}]: {dier.naam} ({dier.soort})")
        beschikbare_dier_ids.append(dier.id_huisdier)

  return beschikbare_dier_ids


def main():
  db_manager.initialize_database(DB_PATH)

  while True:
    toon_menu()

    while True:
      try:
        keuze = int(input("Kies een optie (0-7): "))
        if 0 <= keuze <= 7:
          break
        print("Gelieve een getal tussen 0 en 7 te kiezen.")
      except ValueError:
        print("Ongeldige invoer! Gelieve een getal in te vullen.")

    # 1. Eigenaar toevoegen
    if keuze == 1:
      naam = input("Naam van de eigenaar: ").strip()
      while naam == "":
        print("Naam mag niet leeg zijn!")
        naam = input("Naam van de eigenaar: ").strip()

      nieuw_id = db_manager.voeg_eigenaar_toe(DB_PATH, naam)
      if nieuw_id:
        nieuwe_eigenaar = Eigenaar(id_eigenaar=nieuw_id, naam=naam)
        print(f"Eigenaar toegevoegd: {nieuwe_eigenaar}")

    # 2. Eigenaren bekijken
    elif keuze == 2:
      toon_alle_eigenaren()

    # 3. Huisdier toevoegen aan eigenaar
    elif keuze == 3:
      eigenaren = toon_alle_eigenaren()
      if len(eigenaren) == 0:
        continue

      geldige_ids = [e.id_eigenaar for e in eigenaren]

      while True:
        try:
          id_eigenaar = int(
              input("\nGeef het ID van de eigenaar voor dit huisdier: ")
          )
          if id_eigenaar in geldige_ids:
            break
          print(
              f"Eigenaar met ID {id_eigenaar} bestaat niet. Kies uit de lijst."
          )
        except ValueError:
          print("Ongeldige invoer! Gelieve een getal in te vullen.")

      naam = input("Naam van het huisdier: ").strip()
      while naam == "":
        print("Naam mag niet leeg zijn!")
        naam = input("Naam van het huisdier: ").strip()

      soort = input("Soort dier (hond, kat, ...): ").strip()
      while soort == "":
        print("Soort mag niet leeg zijn!")
        soort = input("Soort dier: ").strip()

      huidig_jaar = datetime.now().year
      while True:
        try:
          geboortejaar = int(input("Geboortejaar (bijv. 2021): "))
          if 1980 <= geboortejaar <= huidig_jaar:
            break
          print(f"Geboortejaar moet tussen 1980 en {huidig_jaar} liggen.")
        except ValueError:
          print("Ongeldige invoer! Gelieve een geldig jaartal in te vullen.")

      chipnummer = input("Chipnummer: ").strip()
      kleur_vacht = input("Kleur van de vacht: ").strip()
      kleur_ogen = input("Kleur van de ogen: ").strip()

      while True:
        gesteriliseerd_invoer = (
            input("Is het dier gesteriliseerd? (ja/nee): ").strip().lower()
        )
        if gesteriliseerd_invoer in ["ja", "j"]:
          is_gesteriliseerd = 1
          break
        elif gesteriliseerd_invoer in ["nee", "n"]:
          is_gesteriliseerd = 0
          break
        print("Gelieve enkel met 'ja' of 'nee' te antwoorden.")

      nieuw_dier_id = db_manager.voeg_huisdier_toe(
          DB_PATH,
          id_eigenaar,
          naam,
          soort,
          geboortejaar,
          chipnummer,
          kleur_vacht,
          kleur_ogen,
          is_gesteriliseerd,
      )
      if nieuw_dier_id:
        dier = Huisdier(
            id_huisdier=nieuw_dier_id,
            naam=naam,
            soort=soort,
            geboortejaar=geboortejaar,
            chipnummer=chipnummer,
            kleur_vacht=kleur_vacht,
            kleur_ogen=kleur_ogen,
            is_gesteriliseerd=bool(is_gesteriliseerd),
        )
        print(f"\nHuisdier succesvol toegevoegd:\n{dier}")

    # 4. Huisdieren bekijken
    elif keuze == 4:
      toon_alle_huisdieren_per_eigenaar()

    # 5. Meting toevoegen
    elif keuze == 5:
      dier_ids = toon_alle_huisdieren_per_eigenaar()
      if len(dier_ids) == 0:
        continue

      while True:
        try:
          id_huisdier = int(
              input("\nGeef het ID van het huisdier voor de meting: ")
          )
          if id_huisdier in dier_ids:
            break
          print(
              f"ID {id_huisdier} staat niet in het overzicht. Kies uit de lijst."
          )
        except ValueError:
          print("Ongeldige invoer! Gelieve een geheel getal in te vullen.")

      type_meting = input(
          "Type meting (bijv. Gewicht, Voeding, Medicatie): "
      ).strip()
      while type_meting == "":
        print("Type meting mag niet leeg zijn!")
        type_meting = input("Type meting: ").strip()

      while True:
        try:
          invoer_waarde = input("Waarde (bijv. 4.5): ").replace(",", ".")
          waarde = float(invoer_waarde)
          if waarde > 0:
            break
          print("De waarde moet groter zijn dan 0.")
        except ValueError:
          print("Ongeldige invoer! Gelieve een getal in te vullen.")

      eenheid = input("Eenheid (bijv. kg, gram, stuks): ").strip()
      while eenheid == "":
        print("Eenheid mag niet leeg zijn!")
        eenheid = input("Eenheid: ").strip()

      notitie = input("Optionele notitie: ").strip()
      datum_tijd = datetime.now().strftime("%Y-%m-%d %H:%M")

      nieuw_log_id = db_manager.voeg_meting_toe(
          DB_PATH, id_huisdier, datum_tijd, type_meting, waarde, eenheid, notitie
      )
      if nieuw_log_id:
        m = Meting(
            id_log=nieuw_log_id,
            id_huisdier=id_huisdier,
            datum_tijd=datum_tijd,
            type=type_meting,
            waarde=waarde,
            eenheid=eenheid,
            notitie=notitie,
        )
        print(f"Meting opgeslagen: {m}")

    # 6. Logboek bekijken
    elif keuze == 6:
      dier_ids = toon_alle_huisdieren_per_eigenaar()
      if len(dier_ids) == 0:
        continue

      while True:
        try:
          id_huisdier = int(
              input("\nVoer het ID van het huisdier in om het logboek te bekijken: ")
          )
          if id_huisdier in dier_ids:
            break
          print(
              f"ID {id_huisdier} staat niet in het bovenstaande overzicht."
              " Probeer opnieuw."
          )
        except ValueError:
          print("Ongeldige invoer! Gelieve een geheel getal in te vullen.")

      rijen_metingen = db_manager.haal_logboek_op_voor_huisdier(
          DB_PATH, id_huisdier
      )
      if len(rijen_metingen) == 0:
        print(f"\nGeen metingen gevonden voor huisdier ID {id_huisdier}.")
      else:
        metingen = []
        for m in rijen_metingen:
          meting_obj = Meting(
              id_log=m[0],
              id_huisdier=m[1],
              datum_tijd=m[2],
              type=m[3],
              waarde=m[4],
              eenheid=m[5],
              notitie=m[6],
          )
          metingen.append(meting_obj)

        print(f"\n--- Logboek voor huisdier ID {id_huisdier} ---")
        for item in metingen:
          print(item)
    # 7. Logboek exporteren naar CSV
    elif keuze == 7:
      dier_ids = toon_alle_huisdieren_per_eigenaar()
      if len(dier_ids) == 0:
        continue
      
      while True:
        try:
          id_huisdier = int(
              input("\nVoer het ID van het huisdier in om het logboek te exporteren: ")
          )
          if id_huisdier in dier_ids:
            break
          print(
              f"ID {id_huisdier} staat niet in het bovenstaande overzicht."
              " Probeer opnieuw."
          )
        except ValueError:
          print("Ongeldige invoer! Gelieve een geheel getal in te vullen.")
      
      bestandsnaam = f"logboek_{id_huisdier}.csv"
      succes = db_manager.exporteer_logboek_naar_csv(DB_PATH, id_huisdier, bestandsnaam)

      if succes: 
        print(f"Logboek succesvol geëxporteerd naar {bestandsnaam}.")

      else:
        print("Er is een fout opgetreden bij het exporteren van het logboek.")  

    # 0. Afsluiten
    elif keuze == 0:
      print("Programma afgesloten. Tot ziens!")
      break


if __name__ == "__main__":
  main()