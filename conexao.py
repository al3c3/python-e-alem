"""Conexão com o Oracle, a mesma usada no crud.py."""

import oracledb


def conectar():
    """Função: abre a conexão e devolve o objeto conn."""
    dsn = oracledb.makedsn(
        "oracle.fiap.com.br",
        1521,
        sid="ORCL",
    )
    return oracledb.connect(
        user="rm575820",
        password="040191",
        dsn=dsn,
        tcp_connect_timeout=20,
    )
