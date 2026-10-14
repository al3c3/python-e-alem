"""Tabela ordenha no Oracle.

Os procedimentos recebem o cursor e o dicionário da vaca por parâmetro.
"""

COLUNAS_BANCO = (
    "id",
    "nome",
    "litros_leite",
    "pasto",
    "racao_dia_kg",
    "racao_manha_kg",
    "racao_tarde_kg",
    "milho_kg",
    "soja_kg",
    "concentrado_kg",
)

CAMPOS_GRAVACAO = COLUNAS_BANCO[1:]

SQL_CRIAR = """
    CREATE TABLE ordenha (
        id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        nome VARCHAR2(80) NOT NULL,
        litros_leite NUMBER(6,2) NOT NULL,
        pasto VARCHAR2(30) DEFAULT 'pasto' NOT NULL,
        racao_dia_kg NUMBER(8,3) NOT NULL,
        racao_manha_kg NUMBER(8,3) NOT NULL,
        racao_tarde_kg NUMBER(8,3) NOT NULL,
        milho_kg NUMBER(8,3) NOT NULL,
        soja_kg NUMBER(8,3) NOT NULL,
        concentrado_kg NUMBER(8,3) NOT NULL,
        CONSTRAINT uk_ordenha_nome UNIQUE (nome)
    )
"""


def sql_select():
    """Função: devolve o SELECT com as colunas da ordenha."""
    campos = ", ".join(COLUNAS_BANCO)
    return f"SELECT {campos} FROM ordenha"


def dados_ordenha(vaca):
    """Função: separa do dicionário só os campos gravados na tabela."""
    return {campo: vaca[campo] for campo in CAMPOS_GRAVACAO}


def tupla_para_registro(linha):
    """Função: converte uma tupla do Oracle em dicionário."""
    registro = {}
    for chave, valor in zip(COLUNAS_BANCO, linha):
        if chave == "id":
            registro[chave] = int(valor)
        elif chave in ("nome", "pasto"):
            registro[chave] = str(valor)
        else:
            registro[chave] = float(valor)
    return registro


def tuplas_para_registros(linhas):
    """Função: recebe a lista de tuplas e devolve a lista de dicionários."""
    return [tupla_para_registro(linha) for linha in linhas]


def garantir_tabela(cursor):
    """Procedimento: cria a tabela ordenha quando ela ainda não existe."""
    cursor.execute(
        "SELECT COUNT(*) FROM user_tables WHERE table_name = 'ORDENHA'"
    )
    if int(cursor.fetchone()[0]) == 0:
        cursor.execute(SQL_CRIAR)


def inserir_vaca(cursor, vaca):
    """Procedimento: grava o dicionário da vaca recebido por parâmetro."""
    cursor.execute(
        """
        INSERT INTO ordenha (
            nome, litros_leite, pasto, racao_dia_kg, racao_manha_kg,
            racao_tarde_kg, milho_kg, soja_kg, concentrado_kg
        ) VALUES (
            :nome, :litros_leite, :pasto, :racao_dia_kg, :racao_manha_kg,
            :racao_tarde_kg, :milho_kg, :soja_kg, :concentrado_kg
        )
        """,
        dados_ordenha(vaca),
    )


def listar_ordenha(cursor):
    """Função: devolve a lista de tuplas da tabela ordenha."""
    cursor.execute(
        sql_select() + " ORDER BY litros_leite DESC, nome"
    )
    return list(cursor.fetchall())


def buscar_por_id(cursor, id_vaca):
    """Função: recebe o id e devolve uma tupla, ou None."""
    cursor.execute(
        sql_select() + " WHERE id = :id",
        {"id": id_vaca},
    )
    return cursor.fetchone()


def contar_vacas(cursor):
    """Função: devolve quantas vacas estão na tabela ordenha."""
    cursor.execute("SELECT COUNT(*) FROM ordenha")
    return int(cursor.fetchone()[0])


def atualizar_vaca(cursor, id_vaca, vaca):
    """Procedimento: atualiza a vaca do id com o dicionário recebido."""
    dados = dados_ordenha(vaca)
    dados["id"] = id_vaca
    cursor.execute(
        """
        UPDATE ordenha
        SET nome = :nome,
            litros_leite = :litros_leite,
            pasto = :pasto,
            racao_dia_kg = :racao_dia_kg,
            racao_manha_kg = :racao_manha_kg,
            racao_tarde_kg = :racao_tarde_kg,
            milho_kg = :milho_kg,
            soja_kg = :soja_kg,
            concentrado_kg = :concentrado_kg
        WHERE id = :id
        """,
        dados,
    )
    if cursor.rowcount == 0:
        raise ValueError(f"Não há vaca cadastrada com o id {id_vaca}.")


def excluir_vaca(cursor, id_vaca):
    """Procedimento: apaga a vaca do id recebido por parâmetro."""
    cursor.execute(
        "DELETE FROM ordenha WHERE id = :id",
        {"id": id_vaca},
    )
    if cursor.rowcount == 0:
        raise ValueError(f"Não há vaca cadastrada com o id {id_vaca}.")


def substituir_rebanho(cursor, conexao, rebanho):
    """Procedimento: apaga a ordenha e grava a lista recebida por parâmetro."""
    cursor.execute("DELETE FROM ordenha")
    cursor.execute(
        "ALTER TABLE ordenha MODIFY(ID GENERATED AS IDENTITY (START WITH 1))"
    )
    for vaca in rebanho:
        inserir_vaca(cursor, vaca)
    conexao.commit()
