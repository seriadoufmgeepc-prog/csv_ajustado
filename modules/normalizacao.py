from __future__ import annotations
import re
import unicodedata
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Optional

MESES = {
    "jan": "01", "janeiro": "01", "fev": "02", "fevereiro": "02", "mar": "03", "marco": "03", "março": "03",
    "abr": "04", "abril": "04", "mai": "05", "maio": "05", "jun": "06", "junho": "06", "jul": "07", "julho": "07",
    "ago": "08", "agosto": "08", "set": "09", "setembro": "09", "out": "10", "outubro": "10", "nov": "11", "novembro": "11",
    "dez": "12", "dezembro": "12",
}


def sem_acentos(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", str(texto)) if unicodedata.category(c) != "Mn")


def limpar_espacos(texto: object) -> str:
    if texto is None:
        return ""
    if str(texto).lower() in {"nan", "none", "nat"}:
        return ""
    return re.sub(r"\s+", " ", str(texto)).strip()


def somente_digitos(valor: object, tamanho: Optional[int] = None) -> str:
    digitos = re.sub(r"\D", "", limpar_espacos(valor))
    return digitos.zfill(tamanho) if tamanho and digitos else digitos


def codigo_ug(valor: object) -> str:
    return somente_digitos(valor, 6)


def codigo_restricao(valor: object) -> str:
    return somente_digitos(valor, 3)


def normalizar_competencia(valor: object) -> str:
    bruto = limpar_espacos(valor)
    if not bruto:
        return ""
    m = re.search(r"(\d{1,2})\s*/\s*(\d{4})", bruto)
    if m:
        return f"{int(m.group(1)):02d}/{m.group(2)}"
    m = re.search(r"([A-Za-zçÇãÃéÉ]+)\s*/\s*(\d{4})", bruto)
    if m:
        mes = MESES.get(sem_acentos(m.group(1)).lower()[:3], "") or MESES.get(sem_acentos(m.group(1)).lower(), "")
        return f"{mes}/{m.group(2)}" if mes else bruto
    return bruto


def _decimal_para_centavos(texto: str) -> str:
    """Converte valor monetário com separador decimal em inteiro de centavos."""
    txt = texto.strip().replace("R$", "").replace(" ", "")
    txt = re.sub(r"[^0-9,.-]", "", txt)
    if not txt or txt in {"-", ".", ","} or txt.startswith("-"):
        return ""

    try:
        if "," in txt:
            # Formato brasileiro: 1.234.567,89
            normalizado = txt.replace(".", "").replace(",", ".")
        elif "." in txt:
            partes = txt.split(".")
            # Um único ponto com 1 ou 2 casas finais é tratado como separador decimal.
            # Demais pontos são considerados separadores de milhar.
            if len(partes) == 2 and 1 <= len(partes[1]) <= 2:
                normalizado = txt
            else:
                normalizado = txt.replace(".", "")
        else:
            return re.sub(r"\D", "", txt)
        centavos = (Decimal(normalizado).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) * 100).to_integral_value()
        return str(int(centavos))
    except (InvalidOperation, ValueError):
        return ""


def moeda_para_digitos(valor: object) -> str:
    """Normaliza o campo Valor para o layout STN/SIAFI.

    Regra do anexo STN: o Valor é opcional, numérico, com até 17 posições,
    sem pontos ou vírgulas, sendo as duas últimas posições correspondentes
    aos centavos. Assim, "1002356" significa R$ 10.023,56.

    Entradas com vírgula/ponto decimal, como "10.023,56" ou "10023.56",
    são convertidas para centavos. Entradas apenas com dígitos são mantidas
    como já digitadas, pois já representam o formato de upload do SIAFI.
    """
    texto = limpar_espacos(valor)
    if not texto:
        return ""
    if re.search(r"[.,]", texto):
        return _decimal_para_centavos(texto)
    return somente_digitos(texto)


def formatar_valor_siafi_brl(valor: object) -> str:
    """Formata o valor bruto do SIAFI como moeda brasileira para conferência visual."""
    digitos = somente_digitos(valor)
    if not digitos:
        return ""
    try:
        numero = (Decimal(digitos) / Decimal(100)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        return ""
    inteiro, decimal = f"{numero:.2f}".split(".")
    inteiro_fmt = f"{int(inteiro):,}".replace(",", ".")
    return f"{inteiro_fmt},{decimal}"


def valor_siafi_valido(valor: object) -> bool:
    digitos = limpar_espacos(valor)
    return digitos == "" or bool(re.fullmatch(r"\d{1,17}", digitos))


def texto_siafi(valor: object, limite: int = 1024) -> str:
    texto = limpar_espacos(valor)
    texto = texto.replace("¿", "'")
    texto = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", " ", texto)
    texto = limpar_espacos(texto)
    return texto[:limite]


def normalizar_coluna(nome: object) -> str:
    s = sem_acentos(limpar_espacos(nome)).lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s
