class Meting:

  def __init__(self,id_log,id_huisdier,datum_tijd,type,waarde,eenheid,notitie=""):
    self.id_log = id_log
    self.id_huisdier = id_huisdier
    self.datum_tijd = datum_tijd
    self.type = type
    self.waarde = waarde
    self.eenheid = eenheid
    self.notitie = notitie

  def __str__(self):
    notitie_tekst = f" ({self.notitie})" if self.notitie else ""
    return f"[{self.datum_tijd}] {self.type.title()}: {self.waarde} {self.eenheid}{notitie_tekst}"