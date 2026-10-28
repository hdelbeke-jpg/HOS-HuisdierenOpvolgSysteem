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
