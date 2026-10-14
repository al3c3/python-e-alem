"""Ordenha das vacas leiteiras.

Subalgoritmos: funções em funcoes.py e procedimentos em procedimentos.py.
Estruturas: lista, tupla, dicionário e tabela de memória em rebanho.py.
Arquivos texto e JSON em arquivos.py.
Banco Oracle: tabela ordenha, conexão igual à do crud.py.
"""

import oracledb

from arquivos import (
    ARQUIVO_JSON,
    ARQUIVO_TXT,
    gravar_json,
    gravar_texto,
    ler_arquivo_texto,
    ler_json,
    montar_relatorio,
)
from banco import (
    atualizar_vaca,
    buscar_por_id,
    contar_vacas,
    excluir_vaca,
    garantir_tabela,
    inserir_vaca,
    listar_ordenha,
    substituir_rebanho,
    tupla_para_registro,
    tuplas_para_registros,
)
from conexao import conectar
from funcoes import FORMULA, descrever_regra, montar_registro, resumir_rebanho, vaca_maior_producao
from procedimentos import (
    exibir_resumo,
    exibir_tabela_memoria,
    exibir_vaca,
    explicar_estruturas,
    limpar_tela,
    pausar,
)
from rebanho import REBANHO_INICIAL, gerar_rebanho, preparar_tabela, rebanho_do_json

MARGEM = "    "


def consultar(cursor):
    """Função: devolve o rebanho e a origem ('oracle' ou 'memoria')."""
    linhas = listar_ordenha(cursor)
    if linhas:
        return tuplas_para_registros(linhas), "oracle"
    return gerar_rebanho(), "memoria"


def mostrar_rebanho(rebanho, origem):
    """Procedimento: mostra a origem, a tabela de memória e o resumo."""
    if origem == "oracle":
        print("Registros lidos da tabela ordenha.\n")
    elif origem == "json":
        print("Registros lidos do arquivo JSON.\n")
    else:
        print("A tabela ordenha está vazia. Estes dados estão só na memória.\n")
    titulos, casas, tabela = preparar_tabela(rebanho)
    exibir_tabela_memoria(titulos, tabela, casas)
    exibir_resumo(resumir_rebanho(rebanho))
    return titulos, casas, tabela


def cadastrar(cursor, conexao):
    """Procedimento: lê nome e litros, calcula a ração e grava na ordenha."""
    print("--- Cadastrar vaca ---")
    nome = input(MARGEM + "Nome da vaca: ")
    litros = float(input(MARGEM + "Litros de leite: ").strip().replace(",", "."))
    vaca = montar_registro(nome, litros)
    inserir_vaca(cursor, vaca)
    conexao.commit()
    print("\nVaca gravada na tabela ordenha.\n")
    exibir_vaca(vaca)


def carregar_rebanho_inicial(cursor, conexao):
    """Procedimento: grava as 25 vacas na tabela ordenha."""
    print("--- Carregar as 25 vacas ---")
    rebanho = gerar_rebanho()
    quantidade = contar_vacas(cursor)
    if quantidade:
        confirma = input(
            MARGEM + f"A tabela já tem {quantidade} vaca(s). Substituir tudo? [S]im ou [N]ão: "
        )
        if confirma.strip().upper() != "S":
            print("Operação cancelada.")
            return
    substituir_rebanho(cursor, conexao, rebanho)
    gravadas = tuplas_para_registros(listar_ordenha(cursor))
    print(f"\n{len(gravadas)} vacas gravadas na tabela ordenha.\n")
    exibir_vaca(vaca_maior_producao(gravadas))


def alterar_leite(cursor, conexao):
    """Procedimento: recebe o id, recalcula a ração e atualiza a ordenha."""
    print("--- Alterar litros de leite ---")
    id_vaca = int(input(MARGEM + "ID da vaca: ").strip())
    linha = buscar_por_id(cursor, id_vaca)
    if linha is None:
        print(f"Não há vaca cadastrada com o id {id_vaca}.")
        return
    atual = tupla_para_registro(linha)
    exibir_vaca(atual)
    print("\nO nome permanece. A ração é recalculada pelos litros novos.")
    litros = float(input(MARGEM + "Novos litros de leite: ").strip().replace(",", "."))
    nova = montar_registro(atual["nome"], litros)
    atualizar_vaca(cursor, id_vaca, nova)
    conexao.commit()
    nova["id"] = id_vaca
    print("\nDados alterados.\n")
    exibir_vaca(nova)


def excluir(cursor, conexao):
    """Procedimento: apaga uma vaca pelo id recebido."""
    print("--- Excluir vaca ---")
    id_vaca = int(input(MARGEM + "ID da vaca: ").strip())
    linha = buscar_por_id(cursor, id_vaca)
    if linha is None:
        print(f"Não há vaca cadastrada com o id {id_vaca}.")
        return
    exibir_vaca(tupla_para_registro(linha))
    confirma = input(MARGEM + "Confirma a exclusão? [S]im ou [N]ão: ")
    if confirma.strip().upper() != "S":
        print("Operação cancelada.")
        return
    excluir_vaca(cursor, id_vaca)
    conexao.commit()
    print("\nVaca apagada da tabela ordenha.")


def mostrar_tabela_memoria(cursor):
    """Procedimento: monta e explica a tabela de memória."""
    print("--- Tabela de memória ---")
    rebanho, origem = consultar(cursor)
    _, _, tabela = mostrar_rebanho(rebanho, origem)
    print()
    exemplo = REBANHO_INICIAL[0]
    if origem == "oracle":
        exemplo = (rebanho[0]["nome"], rebanho[0]["litros_leite"])
    explicar_estruturas(rebanho, tabela, FORMULA, exemplo)


def salvar_texto(cursor):
    """Procedimento: grava o relatório da ordenha em arquivo texto."""
    rebanho, origem = consultar(cursor)
    titulos, casas, tabela = preparar_tabela(rebanho)
    conteudo = montar_relatorio(titulos, tabela, casas, resumir_rebanho(rebanho))
    gravar_texto(ARQUIVO_TXT, conteudo)
    print(f"Arquivo texto gravado em:\n{ARQUIVO_TXT}")
    if origem == "memoria":
        print("A tabela ordenha está vazia. O arquivo saiu do rebanho em memória.")


def salvar_json(cursor):
    """Procedimento: grava a lista de dicionários em JSON."""
    rebanho, origem = consultar(cursor)
    gravar_json(ARQUIVO_JSON, rebanho)
    print(f"Arquivo JSON gravado em:\n{ARQUIVO_JSON}")
    if origem == "memoria":
        print("A tabela ordenha está vazia. O arquivo saiu do rebanho em memória.")


def mostrar_texto():
    """Procedimento: lê o arquivo texto e mostra na tela."""
    if not ARQUIVO_TXT.exists():
        print(f"Ainda não existe o arquivo:\n{ARQUIVO_TXT}")
        print("Use a opção 7 para gravar.")
        return
    print(ler_arquivo_texto(ARQUIVO_TXT))


def importar_json(cursor, conexao):
    """Procedimento: lê o JSON, recalcula a ração e pode gravar na ordenha."""
    if not ARQUIVO_JSON.exists():
        print(f"Ainda não existe o arquivo:\n{ARQUIVO_JSON}")
        print("Use a opção 8 para gravar.")
        return
    rebanho = rebanho_do_json(ler_json(ARQUIVO_JSON))
    print("Ração recalculada a partir dos litros lidos no JSON.\n")
    mostrar_rebanho(rebanho, "json")
    confirma = input(MARGEM + "Gravar estas vacas na tabela ordenha? [S]im ou [N]ão: ")
    if confirma.strip().upper() != "S":
        print("Arquivo lido. Nada foi alterado no Oracle.")
        return
    substituir_rebanho(cursor, conexao, rebanho)
    print(f"\n{len(rebanho)} vacas gravadas na tabela ordenha.")


def imprimir_menu():
    """Procedimento: mostra o menu da ordenha."""
    print("---- ORDENHA - VACAS LEITEIRAS ----")
    print(descrever_regra())
    print(
        """
    1 - Cadastrar vaca
    2 - Carregar as 25 vacas
    3 - Listar ordenha
    4 - Alterar litros de leite
    5 - Excluir vaca
    6 - Mostrar tabela de memória
    7 - Gravar arquivo texto
    8 - Gravar arquivo JSON
    9 - Ler arquivo texto
    10 - Ler arquivo JSON
    0 - Sair
    """
    )


def main():
    print("Conectando ao Oracle...")
    try:
        conn = conectar()
    except oracledb.Error as erro:
        print(f"Não foi possível conectar: {erro}")
        return

    print("Conectado ao Oracle.")
    cursor = conn.cursor()
    try:
        garantir_tabela(cursor)
    except oracledb.Error as erro:
        print(f"Erro ao preparar a tabela ordenha: {erro}")
        cursor.close()
        conn.close()
        return

    while True:
        limpar_tela()
        imprimir_menu()
        try:
            opcao = input(MARGEM + "Escolha -> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAplicação encerrada.")
            break

        if opcao == "0":
            print("Aplicação encerrada.")
            break

        try:
            match opcao:
                case "1":
                    cadastrar(cursor, conn)
                case "2":
                    carregar_rebanho_inicial(cursor, conn)
                case "3":
                    rebanho, origem = consultar(cursor)
                    mostrar_rebanho(rebanho, origem)
                case "4":
                    alterar_leite(cursor, conn)
                case "5":
                    excluir(cursor, conn)
                case "6":
                    mostrar_tabela_memoria(cursor)
                case "7":
                    salvar_texto(cursor)
                case "8":
                    salvar_json(cursor)
                case "9":
                    mostrar_texto()
                case "10":
                    importar_json(cursor, conn)
                case _:
                    print("Opção inválida.")
        except ValueError as erro:
            print(erro)
        except oracledb.Error as erro:
            conn.rollback()
            print(f"Erro na transação do BD: {erro}")
        except FileNotFoundError as erro:
            print(f"Arquivo não encontrado: {erro.filename}")
        except (EOFError, KeyboardInterrupt):
            print("\nAplicação encerrada.")
            break

        try:
            pausar()
        except (EOFError, KeyboardInterrupt):
            print("\nAplicação encerrada.")
            break

    cursor.close()
    conn.close()
    print("Obrigado por utilizar a ordenha.")


if __name__ == "__main__":
    main()
