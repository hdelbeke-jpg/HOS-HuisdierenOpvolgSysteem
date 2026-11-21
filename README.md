# HOS-HuisdierenOpvolgSysteem
Dit project in het kader van Programming in Python helpt je een dossier bij te houden per huisdier

DOEL:
bijhouden van
  algemene gegevens
    naam
    geboortejaar
    chipnummer
    uiterlijke kenmerken
  medicatie
    soort
    dosis
    toegekend of niet
      in latere fase: te bevestigen adhv NFC-tag
  voeding
    soort
    dosis
    gekregen of niet
      in latere fase: te bevestigen ahdh NFC-tag
    aantal water gedronken
      in latere fase: te bevestigen adhv NFC-tag
  dierenartsbezoeken
    wanneer
    resultaten
    vragen die je wilt stellen
  testresultaten
    wanneer
    wat
    mogelijkheid vergelijken / grafiek maken?
  beweging
    wandelingen
      in een latere fase: te bevestigen adhv NFC-tag
  status
    energiek
    hongerig
    ...
  andere
    rare zaken gegeten
    loopsheid

Dit per huisdier

Klasse Dier
> id (volgnummer) dier - int
> naam - String
> type dier - String
> geboortejaar - int
> chipnummer - int
> uiterlijke kenmerkien - String (opdelen in kleur vacht, kleur ogen, .... ?)
> isGesteriliseerd - boolean (om dit type ook aan bod te laten komen)

Klasse Metingen
> id log - int
> id dier (verwijzing naar Klasse Dier) - int
> datum_tijd (datetime) - String
> water_ml 
> voeding_gram 
> gewicht_kg

 Klasse Medisch_dossier
 > id log
>id dier
> datum
> type (medicatie of dierenarts)
> omschrijving (vb vaccinatie, ontworming, opvolging medicatie)
> notitie

#30/10/26: 
klasses beginnen uitschrijven - redelijk ruw.
Nog errorhandling erin verwerken, en ook de check als een verkeerde invoer wordt ingegeven dan verwacht
Normaalgezien alle nodige documenten en de virtuele omgeving gemaakt

#17/11/26:
extra opties toegevoegd (lijst van eigenaren oproepen, lijst van huisdieren oproepen, want je onthoudt niet altijd het ID-nummer van deze)
code aangepast met try-except
code leesbaarder proberen maken
er was een foutmelding met de models-map, dus deze verwijderd en opnieuw

#21/11/2026:
readme aanpassen zoals beschreven staat in de opdracht:
# HOS - Huisdieren Opvolg Systeem
Het eerder beschreven project werd aangevuld met de mogelijkheid om het volledige logboek van een geselecteerd huisdier te exporteren naar een CSV-bestand.

## Installatie & Configuratie

Om het project op te starten (volgens de flow van de opdracht):

1. **Virtuele omgeving aanmaken en activeren:**
   - **Windows:**
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

2. **Packages installeren:**
    mijn project gebruikt enkel ingebouwde Python-modules, dus er hoeven geen extra packages geïnstalleerd worden.
    Ik voorzag toch een requirements.txt-documentje

3. **Instellingenbestand configureren (config.py):**
 Maak een lokaal instellingenbestand aan op basis van het voorbeeldbestand:
        Windows: copy config.py.example config.py
        macOS / Linux: cp config.py.example config.py

Controleer of in config.py het pad naar de database als volgt is ingesteld:

DB_PATH = "database/hos_huisdieren.db"

Locatie van de database: hos_huisdieren.db (voor de opdracht beschikbaar via Toledo) in de map database/hos_huisdieren.db

4. **Applicatie starten: Start het programma op via de terminal**

python main.py

5. ** Functionaliteiten van het menu:**
Eigenaar toevoegen: Registreer een nieuwe eigenaar in het systeem.
Eigenaren bekijken: Overzicht tonen van alle geregistreerde eigenaren.
Huisdier toevoegen: Koppel een nieuw dier aan een bestaande eigenaar.
Huisdieren bekijken: Overzicht van alle dieren gegroepeerd per eigenaar.
Meting/log toevoegen: Registreer een meting of logboekregel (gewicht, voeding, etc.) voor een specifiek dier.
Logboek bekijken: Toon de historische metingen en notities van een gekozen dier in de console.
Logboek exporteren naar CSV: Exporteert alle metingen van een gekozen dier naar een overzichtelijk .csv-bestand.
Afsluiten: Het programma netjes beëindigen.