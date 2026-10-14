"""Estruturas do rebanho.

Lista de tuplas guarda o rebanho inicial.
Cada vaca vira um dicionário.
A tabela de memória é uma lista de listas.
"""

from funcoes import montar_registro

# Lista de tuplas (nome de desenho animado, litros de leite).
# Clarabela é a que mais produz: 30 litros.
REBANHO_INICIAL = [
    ("Clarabela", 30.0),
    ("Maggie", 28.5),
    ("Marge", 27.0),
    ("Lisa", 26.0),
    ("Dora", 25.0),
    ("Elsa", 24.0),
    ("Anna", 23.5),
    ("Moana", 23.0),
    ("Ariel", 22.0),
    ("Bela", 21.5),
    ("Mulan", 21.0),
    ("Tiana", 20.0),
    ("Merida", 19.5),
    ("Rapunzel", 19.0),
    ("Jasmine", 18.0),
    ("Aurora", 17.5),
    ("Cinderela", 17.0),
    ("Pocahontas", 16.0),
    ("Sininho", 15.5),
    ("Alice", 15.0),
    ("Dorothy", 14.0),
    ("Coraline", 13.5),
    ("Matilda", 13.0),
    ("Agnes", 12.0),
    ("Mirabel", 11.0),
]


def gerar_rebanho(rebanho_inicial=REBANHO_INICIAL):
    """Função: recebe a lista de tuplas e devolve a lista de dicionários."""
    return [montar_registro(nome, litros) for nome, litros in rebanho_inicial]


def colunas_exibicao(rebanho):
    """Função: devolve a lista de tuplas (chave, título, casas decimais)."""
    colunas = []
    if rebanho and "id" in rebanho[0]:
        colunas.append(("id", "ID", None))
    colunas.extend([
        ("nome", "Vaca", None),
        ("litros_leite", "Leite (L)", 2),
        ("pasto", "Pasto", None),
        ("racao_dia_kg", "Ração (kg)", 3),
        ("racao_manha_kg", "Manhã (kg)", 3),
        ("racao_tarde_kg", "Tarde (kg)", 3),
        ("milho_kg", "Milho (kg)", 3),
        ("soja_kg", "Soja (kg)", 3),
        ("concentrado_kg", "Concentrado (kg)", 3),
    ])
    return colunas


def preencher_tabela(tabela, rebanho, colunas):
    """Procedimento: recebe a tabela de memória e preenche as linhas.

    A lista chega por parâmetro e é alterada aqui dentro.
    """
    tabela.clear()
    for vaca in rebanho:
        tabela.append([vaca[coluna] for coluna in colunas])


def preparar_tabela(rebanho):
    """Função: devolve títulos, casas decimais e a tabela de memória."""
    especificacao = colunas_exibicao(rebanho)
    titulos = tuple(titulo for _, titulo, _ in especificacao)
    chaves = tuple(chave for chave, _, _ in especificacao)
    casas = tuple(casa for _, _, casa in especificacao)
    tabela = []
    preencher_tabela(tabela, rebanho, chaves)
    return titulos, casas, tabela


def rebanho_do_json(dados):
    """Função: recebe a lista lida do JSON e recalcula cada vaca pelos litros."""
    if not isinstance(dados, list):
        raise ValueError("O JSON precisa ser uma lista de vacas.")

    rebanho = []
    for indice, item in enumerate(dados, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"O item {indice} do JSON não é um dicionário.")
        if "nome" not in item or "litros_leite" not in item:
            raise ValueError(f"O item {indice} precisa ter nome e litros_leite.")
        rebanho.append(montar_registro(item["nome"], item["litros_leite"]))
    return rebanho
