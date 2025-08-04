import re

def validar_telefone(telefone):
    return re.match(r"\(\d{2}\) \d{5}-\d{4}", telefone)

def validar_texto(texto, limite):
    return len(texto.strip()) <= limite