from __future__ import annotations
import csv
import io
from .models import RegistroRestricao
from .normalizacao import moeda_para_digitos, texto_siafi


def _mes_siafi(mes: str | int) -> str:
    mes_str = str(mes).strip()
    if not mes_str.isdigit():
        raise ValueError("O mês da conformidade deve ser numérico, entre 1 e 12.")
    mes_int = int(mes_str)
    if mes_int < 1 or mes_int > 12:
        raise ValueError("O mês da conformidade deve estar entre 1 e 12.")
    return str(mes_int)


def _validar_header(nivel: str, codigo_responsavel: str, mes: str | int) -> tuple[str, str, str]:
    nivel_str = str(nivel).strip()
    if nivel_str not in {"1", "2", "3", "4"}:
        raise ValueError("O nível da conformidade deve ser 1, 2, 3 ou 4.")
    codigo = str(codigo_responsavel).strip()
    if not codigo.isdigit():
        raise ValueError("O código responsável deve conter apenas dígitos.")
    return nivel_str, codigo, _mes_siafi(mes)


def gerar_csv_siafi(nivel: str, codigo_responsavel: str, mes: str | int, registros: list[RegistroRestricao]) -> str:
    """Gera CSV no layout STN/SIAFI: 7 colunas A:G, separadas por ';'."""
    nivel_str, codigo, mes_str = _validar_header(nivel, codigo_responsavel, mes)
    saida = io.StringIO()
    writer = csv.writer(saida, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\r\n")

    # Header: A=H, B=Nível, C=Órgão/UG responsável, D=Mês, E/F vazias, G=pipe.
    writer.writerow(["H", nivel_str, codigo, mes_str, "", "", "|"])

    for r in registros:
        writer.writerow([
            "D",
            str(r.ug).strip(),
            str(r.restricao).strip(),
            texto_siafi(r.motivo),
            texto_siafi(r.providencia),
            moeda_para_digitos(r.valor),
            "|",
        ])

    # Trailer: A=T, B=quantidade de detalhes, C/F vazias, G=pipe.
    writer.writerow(["T", len(registros), "", "", "", "", "|"])
    return saida.getvalue()


def nome_csv_padrao(mes: str | int, ano: str, codigo_responsavel: str = "153062") -> str:
    mes2 = str(mes).zfill(2) if str(mes).isdigit() else "MM"
    ano = ano or "AAAA"
    return f"restricoes_siafi_{codigo_responsavel}_{ano}_{mes2}.csv"
