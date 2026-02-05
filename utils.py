import unicodedata

def normalizar(texto):
    if not texto:
        return ""

    texto = unicodedata.normalize("NFKD", texto)
    return "".join(
        c for c in texto if not unicodedata.combining(c)
    ).lower().strip()
