"""Procedimentos da ordenha.

Um procedimento recebe parâmetros e executa uma ação.
Ele não devolve um valor para ser usado em outra conta.
"""

import json

from funcoes import formatar_tabela, trato_do_ingrediente


def limpar_tela():
    """Procedimento: limpa o terminal."""
    print("\033[2J\033[H", end="")


def pausar():
    """Procedimento: espera o ENTER para continuar."""
    input("Pressione ENTER")


def exibir_vaca(vaca):
    """Procedimento: mostra uma vaca. O dicionário chega por parâmetro."""
    print(f"Vaca: {vaca['nome']}")
    if "id" in vaca:
        print(f"ID: {vaca['id']}")
    print(f"Leite: {float(vaca['litros_leite']):.2f} L")
    print(f"Pasto: {vaca['pasto']} (alimentação de base, o dia todo)")
    print(f"Ração do dia: {float(vaca['racao_dia_kg']):.3f} kg")
    print(f"  Manhã: {float(vaca['racao_manha_kg']):.3f} kg")
    print(f"  Tarde: {float(vaca['racao_tarde_kg']):.3f} kg")
    print("Mistura — 75 partes de milho, 25 de soja e 5 de concentrado proteico:")
    ingredientes = (
        ("milho_kg", "Milho"),
        ("soja_kg", "Soja"),
        ("concentrado_kg", "Concentrado proteico"),
    )
    for chave, titulo in ingredientes:
        manha, tarde = trato_do_ingrediente(vaca[chave])
        print(
            f"  {titulo}: {float(vaca[chave]):.3f} kg"
            f"  (manhã {manha:.3f} kg, tarde {tarde:.3f} kg)"
        )


def exibir_tabela_memoria(titulos, tabela, casas):
    """Procedimento: imprime a tabela de memória recebida por parâmetro."""
    print(formatar_tabela(titulos, tabela, casas))
    print(f"\n{len(tabela)} linha(s) na tabela de memória.")


def exibir_resumo(resumo):
    """Procedimento: mostra os totais do dicionário recebido por parâmetro."""
    print()
    print(f"Vacas: {resumo['vacas']}")
    print(f"Leite no dia: {float(resumo['litros_leite']):.2f} L")
    print(f"Ração no dia: {float(resumo['racao_dia_kg']):.3f} kg")
    print(f"Milho: {float(resumo['milho_kg']):.3f} kg")
    print(f"Soja: {float(resumo['soja_kg']):.3f} kg")
    print(f"Concentrado proteico: {float(resumo['concentrado_kg']):.3f} kg")


def explicar_estruturas(rebanho, tabela, formula, exemplo_tupla):
    """Procedimento: mostra lista, tupla, dicionário e tabela de memória."""
    print("Estruturas de dados deste rebanho:")
    print(f"- lista: {len(rebanho)} vacas")
    print(f"- tupla da fórmula (ingrediente, partes): {formula}")
    print(f"- tupla de uma vaca inicial (nome, litros): {exemplo_tupla}")
    print(f"- tabela de memória: {len(tabela)} linhas, cada linha é uma lista")
    if tabela:
        print(f"- primeira linha da tabela de memória: {tabela[0]}")
    if rebanho:
        print("- exemplo de dicionário:")
        print(json.dumps(rebanho[0], ensure_ascii=False, indent=2))
