"""Funções da ordenha.

Cada função recebe parâmetros e devolve um resultado.
A vaca que produz 30 litros come 9 kg de ração no dia.
"""

LITROS_REFERENCIA = 30
RACAO_REFERENCIA_KG = 9
PASTO = "pasto"

# Tupla da fórmula: (ingrediente, partes).
# 75 partes de milho, 25 de soja e 5 de concentrado proteico.
FORMULA = (
    ("milho_kg", 75),
    ("soja_kg", 25),
    ("concentrado_kg", 5),
)


def arredondar_kg(valor):
    """Função: recebe um número e devolve o peso com 3 casas."""
    return round(float(valor), 3)


def calcular_racao_dia(litros_leite, litros_referencia=LITROS_REFERENCIA, racao_referencia=RACAO_REFERENCIA_KG):
    """Função: recebe os litros e devolve a ração do dia, em kg.

    A conta usa a referência recebida por parâmetro:
    30 litros correspondem a 9 kg.
    """
    litros = float(litros_leite)
    if litros < 0:
        raise ValueError("A produção de leite não pode ser negativa.")
    return arredondar_kg(litros * (racao_referencia / litros_referencia))


def dividir_tratos(racao_dia_kg):
    """Função: recebe a ração do dia e devolve a tupla (manhã, tarde)."""
    manha = arredondar_kg(float(racao_dia_kg) / 2)
    tarde = arredondar_kg(float(racao_dia_kg) - manha)
    return (manha, tarde)


def compor_mistura(racao_kg, formula=FORMULA):
    """Função: recebe os kg do dia e a tupla da fórmula.

    Devolve um dicionário com milho, soja e concentrado proteico.
    As 75, 25 e 5 partes repartem exatamente o peso que a vaca come.
    """
    total_partes = sum(partes for _, partes in formula)
    mistura = {}
    acumulado = 0.0
    for nome, partes in formula[:-1]:
        kg = arredondar_kg(float(racao_kg) * partes / total_partes)
        mistura[nome] = kg
        acumulado += kg
    ultimo_nome = formula[-1][0]
    mistura[ultimo_nome] = arredondar_kg(float(racao_kg) - acumulado)
    return mistura


def trato_do_ingrediente(kg_dia):
    """Função: recebe o kg do dia de um ingrediente e devolve (manhã, tarde)."""
    return dividir_tratos(kg_dia)


def montar_registro(nome, litros_leite):
    """Função: recebe nome e litros e devolve o dicionário completo da vaca."""
    nome_limpo = str(nome).strip()
    if not nome_limpo:
        raise ValueError("Informe o nome da vaca.")
    if len(nome_limpo) > 80:
        raise ValueError("O nome pode ter no máximo 80 caracteres.")

    litros = round(float(litros_leite), 2)
    if litros <= 0:
        raise ValueError("A produção de leite precisa ser maior que zero.")

    racao_dia = calcular_racao_dia(litros)
    manha, tarde = dividir_tratos(racao_dia)
    registro = {
        "nome": nome_limpo,
        "litros_leite": litros,
        "pasto": PASTO,
        "racao_dia_kg": racao_dia,
        "racao_manha_kg": manha,
        "racao_tarde_kg": tarde,
    }
    registro.update(compor_mistura(racao_dia))
    return registro


def resumir_rebanho(rebanho):
    """Função: recebe a lista de vacas e devolve um dicionário com os totais."""
    total = {
        "vacas": len(rebanho),
        "litros_leite": 0.0,
        "racao_dia_kg": 0.0,
        "milho_kg": 0.0,
        "soja_kg": 0.0,
        "concentrado_kg": 0.0,
    }
    for vaca in rebanho:
        for chave in ("litros_leite", "racao_dia_kg", "milho_kg", "soja_kg", "concentrado_kg"):
            total[chave] += float(vaca[chave])
    total["litros_leite"] = round(total["litros_leite"], 2)
    for chave in ("racao_dia_kg", "milho_kg", "soja_kg", "concentrado_kg"):
        total[chave] = arredondar_kg(total[chave])
    return total


def vaca_maior_producao(rebanho):
    """Função: recebe a lista e devolve o dicionário da vaca que mais produz."""
    if not rebanho:
        raise ValueError("O rebanho está vazio.")
    return max(rebanho, key=lambda vaca: float(vaca["litros_leite"]))


def descrever_regra():
    """Função: devolve o texto da regra de alimentação."""
    metade = f"{RACAO_REFERENCIA_KG / 2:.1f}".replace(".", ",")
    return (
        f"Referência: {LITROS_REFERENCIA} litros de leite correspondem a "
        f"{RACAO_REFERENCIA_KG} kg de ração por dia "
        f"({metade} kg de manhã e {metade} kg à tarde). "
        "O pasto é a alimentação de base. "
        "A mistura reparte a ração em 75 partes de milho, "
        "25 partes de soja e 5 partes de concentrado proteico."
    )


def formatar_tabela(titulos, tabela, casas):
    """Função: recebe a tabela de memória e devolve o texto formatado."""

    def celula(valor, casas_coluna):
        if casas_coluna is None:
            return str(valor)
        return f"{float(valor):.{casas_coluna}f}"

    textos = []
    for linha in tabela:
        textos.append([celula(valor, casas[indice]) for indice, valor in enumerate(linha)])

    larguras = [len(str(titulo)) for titulo in titulos]
    for linha in textos:
        for indice, texto in enumerate(linha):
            larguras[indice] = max(larguras[indice], len(texto))

    def juntar(linha):
        return "  ".join(texto.ljust(larguras[indice]) for indice, texto in enumerate(linha))

    separador = "  ".join("-" * largura for largura in larguras)
    linhas = [juntar([str(titulo) for titulo in titulos]), separador]
    linhas.extend(juntar(linha) for linha in textos)
    return "\n".join(linhas)
