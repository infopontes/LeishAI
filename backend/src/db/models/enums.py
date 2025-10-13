import enum

class PresenceAbsence(str, enum.Enum):
    presente = "Presente"
    ausente = "Ausente"

class Severity(str, enum.Enum):
    ausente = "Ausente"
    leve = "Leve"
    grave = "Grave"

class GeneralState(str, enum.Enum):
    bom = "Bom"
    regular = "Regular"
    ruim = "Ruim"

class NutritionalState(str, enum.Enum):
    adequado = "Adequado/Eutrófico"
    leve_moderado = "Leve a Moderado"
    grave = "Grave (Caquético)"

class LesionSeverity(str, enum.Enum):
    normal = "Normal"
    leves_moderadas = "Leves/Moderadas"
    graves = "Graves" # 👈 Adicionado

class DiagnosisResult(str, enum.Enum):
    positivo = "Positivo"
    negativo = "Negativo"

class MucosaColor(str, enum.Enum):
    normal = "Normal (Rosa-claro)"
    levemente_hipercorada = "Levemente Hipercorada"
    cianotica = "Cianótica (azulada)"
    congesta = "Congesta (vermelho-escuro)"
    icterica = "Ictérica (amarelada)"
    palida = "Pálida"