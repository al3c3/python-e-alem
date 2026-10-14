"""Gravação e leitura de texto e JSON."""

import json
from pathlib import Path

from funcoes import descrever_regra, formatar_tabela

PASTA_DADOS = Path(__file__).resolve().parent / "dados"
ARQUIVO_TXT = PASTA_DADOS / "ordenha.txt"
ARQUIVO_JSON = PASTA_DADOS / "ordenha.json"


def montar_relatorio(titulos, tabela, casas, resumo):
    """Função: recebe a tabela de memória e devolve o relatório em texto."""
    linhas = [
        "ORDENHA DAS VACAS LEITEIRAS",
        "Alimentação de base: pasto.",
        "A mistura é servida duas vezes ao dia, de manhã e à tarde.",
        descrever_regra(),
        "",
        formatar_tabela(titulos, tabela, casas),
        "",
        f"Vacas: {resumo['vacas']}",
        f"Leite no dia: {float(resumo['litros_leite']):.2f} L",
        f"Ração no dia: {float(resumo['racao_dia_kg']):.3f} kg",
        f"Milho: {float(resumo['milho_kg']):.3f} kg",
        f"Soja: {float(resumo['soja_kg']):.3f} kg",
        f"Concentrado proteico: {float(resumo['concentrado_kg']):.3f} kg",
        "",
    ]
    return "\n".join(linhas)


def gravar_texto(caminho, conteudo):
    """Procedimento: grava o texto no caminho recebido por parâmetro."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(conteudo, encoding="utf-8")


def ler_arquivo_texto(caminho):
    """Função: lê o arquivo texto e devolve o conteúdo."""
    return caminho.read_text(encoding="utf-8")


def gravar_json(caminho, rebanho):
    """Procedimento: grava a lista de dicionários no JSON recebido por parâmetro."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(rebanho, arquivo, ensure_ascii=False, indent=2)
        arquivo.write("\n")


def ler_json(caminho):
    """Função: lê o arquivo JSON e devolve a lista de dicionários."""
    with caminho.open(encoding="utf-8") as arquivo:
        return json.load(arquivo)
