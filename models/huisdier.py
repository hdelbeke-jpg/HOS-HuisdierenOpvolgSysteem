from datetime import datetime

class Huisdier:

  def __init__(self, id_huisdier, naam, soort, geboortejaar, chipnummer, kleur_vacht, kleur_ogen, is_gesteriliseerd):
    self.id_huisdier = id_huisdier
    self.naam = naam
    self.soort = soort
    self.geboortejaar = geboortejaar
    self.chipnummer = chipnummer
    self.kleur_vacht = kleur_vacht
    self.kleur_ogen = kleur_ogen
    self.is_gesteriliseerd = is_gesteriliseerd

  def bereken_leeftijd(self, huidig_jaar=None):
    """Berekent de leeftijd op basis van het geboortejaar."""
    if huidig_jaar is None:
      huidig_jaar = datetime.now().year
    return huidig_jaar - self.geboortejaar

  def __str__(self):
    leeftijd = self.bereken_leeftijd()
    status_sterilisatie = (
        "gesteriliseerd/gecastreerd"
        if self.is_gesteriliseerd
        else "niet gesteriliseerd/gecastreerd"
    )

    return (
        f"{self.naam} (ID: {self.id_huisdier}) is een {self.soort} van {leeftijd} jaar oud.\n"
        f" - Vacht: {self.kleur_vacht}, Ogen: {self.kleur_ogen}\n"
        f" - Chipnummer: {self.chipnummer} ({status_sterilisatie})"
    )