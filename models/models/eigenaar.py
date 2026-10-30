class Eigenaar:

  def __init__(self, id_eigenaar, naam):
    self.id_eigenaar = id_eigenaar
    self.naam = naam
    self.huisdieren = []  # Lijst van Huisdier-objecten

  def voeg_huisdier_toe(self, huisdier):
    """Voegt een huisdier toe aan de lijst van deze eigenaar."""
    self.huisdieren.append(huisdier)

  def __str__(self):
    if self.huisdieren:
      namen_huisdieren = ", ".join([h.naam for h in self.huisdieren])
    else:
      namen_huisdieren = "geen geregistreerde huisdieren"

    return f"Eigenaar {self.naam} (ID: {self.id_eigenaar}) heeft de volgende huisdieren: {namen_huisdieren}."
