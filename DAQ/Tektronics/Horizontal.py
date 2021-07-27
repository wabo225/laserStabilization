from _typeshed import Self
from enum import Enum, auto
from dataclasses import dataclass
from Fields import ReadWriteable


class HorizontalOptions(Enum):
  VIEW = auto()
  RECO = auto()
  POS = auto()
  SCA = auto()
  DEL = auto()

@dataclass
class Horizontal:
  HorizontalOptions = HorizontalOptions
  VIEW: ReadWriteable  = ReadWriteable(str, HorizontalOptions.VIEW)
  RECO: ReadWriteable  = ReadWriteable(int, HorizontalOptions.RECO)
  POS: ReadWriteable = ReadWriteable(float, HorizontalOptions.POS)
  SCA: ReadWriteable = ReadWriteable(float, HorizontalOptions.SCA)
  
  def get(self):
    