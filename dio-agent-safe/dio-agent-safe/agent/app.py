"""
Versão corrigida do login de exemplo.

Antes: agent/app_vulneravel.py montava a consulta SQL por interpolação de
string, permitindo SQL Injection (CWE-89 / CAPEC-66), técnica mais próxima
no MITRE ATT&CK: T1190 - Exploit Public-Facing Application.

Correções aplicadas:
- consulta parametrizada (o `?` é tratado como dado, nunca como comando);
- senha nunca comparada nem armazenada em texto puro: usa hash com salt
  (scrypt) e comparação em tempo constante (hmac.compare_digest);
- tratamento de erro do banco sem vazar detalhes internos;
- validação básica de tipo das entradas.

A tabela `usuarios` deve ter as colunas: username TEXT, password_salt BLOB,
password_hash BLOB. Contas antigas, criadas com senha em texto puro,
precisam ser migradas ou ter a senha redefinida.
"""

import hashlib
import hmac
import secrets
import sqlite3
from contextlib import closing

DB_PATH = "banco_de_dados.db"
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1
HASH_SIZE = 32


def criar_hash_senha(senha: str) -> tuple[bytes, bytes]:
    """Gera um salt aleatório e o hash scrypt da senha. Use ao cadastrar
    ou redefinir a senha de um usuário."""
    salt = secrets.token_bytes(16)
    senha_hash = hashlib.scrypt(
        senha.encode("utf-8"), salt=salt,
        n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P, dklen=HASH_SIZE,
    )
    return salt, senha_hash


def fazer_login(usuario: str, senha: str) -> str:
    negado = "Acesso negado."
    if not isinstance(usuario, str) or not isinstance(senha, str):
        return negado

    try:
        with closing(sqlite3.connect(DB_PATH)) as conexao:
            resultado = conexao.execute(
                "SELECT password_salt, password_hash "
                "FROM usuarios WHERE username = ?",
                (usuario,),
            ).fetchone()
    except sqlite3.Error:
        return negado

    if resultado is None:
        return negado

    salt, hash_armazenado = resultado
    if not isinstance(salt, bytes) or not isinstance(hash_armazenado, bytes):
        return negado

    hash_informado = hashlib.scrypt(
        senha.encode("utf-8"), salt=salt,
        n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P, dklen=HASH_SIZE,
    )
    if hmac.compare_digest(hash_informado, hash_armazenado):
        return "Acesso permitido!"
    return negado
