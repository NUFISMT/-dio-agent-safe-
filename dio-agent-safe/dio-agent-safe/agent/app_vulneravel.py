"""
Versão ORIGINAL usada como alvo de teste da skill de análise de
vulnerabilidades. NÃO USE EM PRODUÇÃO.

Vulnerabilidade: SQL Injection (CWE-89 / CAPEC-66). A consulta é montada
por f-string, concatenando diretamente o que o usuário digitou. Um valor
como `' OR '1'='1' --` no campo de usuário transforma a condição em
verdadeira e comenta o restante da consulta, podendo liberar acesso sem
senha correta. A classificação de risco (crítico ou não) depende de como
o app é exposto e dos privilégios da conta retornada.

A versão corrigida está em agent/app.py.
"""

import sqlite3


def fazer_login(usuario, senha):
    conexao = sqlite3.connect('banco_de_dados.db')
    cursor = conexao.cursor()

    query = f"SELECT * FROM usuarios WHERE username = '{usuario}' AND password = '{senha}'"

    cursor.execute(query)
    resultado = cursor.fetchone()
    conexao.close()

    if resultado:
        return "Acesso Permitido!"
    else:
        return "Acesso Negado."
