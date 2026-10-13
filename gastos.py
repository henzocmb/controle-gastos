"""Controle de gastos pessoais com Python + SQLite.

Uso: python gastos.py --help
"""
import argparse
import sqlite3
from datetime import date

DB = "gastos.db"
CATEGORIAS_PADRAO = ["Alimentação", "Transporte", "Moradia", "Lazer", "Estudos", "Outros"]


def conectar():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute(
        """CREATE TABLE IF NOT EXISTS categorias (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               nome TEXT UNIQUE NOT NULL)"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS gastos (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               descricao TEXT NOT NULL,
               valor REAL NOT NULL CHECK (valor > 0),
               data TEXT NOT NULL,
               categoria_id INTEGER NOT NULL,
               FOREIGN KEY (categoria_id) REFERENCES categorias(id))"""
    )
    conn.executemany(
        "INSERT OR IGNORE INTO categorias (nome) VALUES (?)",
        [(c,) for c in CATEGORIAS_PADRAO],
    )
    conn.commit()
    return conn


def adicionar(conn, descricao, valor, categoria, data):
    linha = conn.execute(
        "SELECT id FROM categorias WHERE nome = ? COLLATE NOCASE", (categoria,)
    ).fetchone()
    if linha is None:
        print(f"Categoria inválida. Opções: {', '.join(CATEGORIAS_PADRAO)}")
        return
    conn.execute(
        "INSERT INTO gastos (descricao, valor, data, categoria_id) VALUES (?, ?, ?, ?)",
        (descricao, valor, data, linha[0]),
    )
    conn.commit()
    print("Gasto registrado.")


def listar(conn):
    consulta = """
        SELECT g.id, g.data, g.descricao, c.nome, g.valor
        FROM gastos g
        JOIN categorias c ON c.id = g.categoria_id
        ORDER BY g.data DESC, g.id DESC"""
    linhas = conn.execute(consulta).fetchall()
    if not linhas:
        print("Nenhum gasto registrado.")
        return
    for id_, data, desc, cat, valor in linhas:
        print(f"{id_:>3} | {data} | {desc:<20} | {cat:<12} | R$ {valor:>8.2f}")


def resumo(conn):
    consulta = """
        SELECT c.nome, COUNT(g.id), SUM(g.valor)
        FROM gastos g
        JOIN categorias c ON c.id = g.categoria_id
        GROUP BY c.nome
        ORDER BY SUM(g.valor) DESC"""
    linhas = conn.execute(consulta).fetchall()
    if not linhas:
        print("Nenhum gasto registrado.")
        return
    total = sum(l[2] for l in linhas)
    for nome, qtd, soma in linhas:
        print(f"{nome:<12} | {qtd:>3} gastos | R$ {soma:>8.2f} ({soma / total:.0%})")
    print(f"{'TOTAL':<12} |           | R$ {total:>8.2f}")


def main():
    parser = argparse.ArgumentParser(description="Controle de gastos")
    sub = parser.add_subparsers(dest="comando", required=True)

    p_add = sub.add_parser("add", help="registra um gasto")
    p_add.add_argument("descricao")
    p_add.add_argument("valor", type=float)
    p_add.add_argument("categoria")
    p_add.add_argument("--data", default=date.today().isoformat())

    sub.add_parser("list", help="lista todos os gastos")
    sub.add_parser("resumo", help="total por categoria")

    args = parser.parse_args()
    conn = conectar()
    if args.comando == "add":
        adicionar(conn, args.descricao, args.valor, args.categoria, args.data)
    elif args.comando == "list":
        listar(conn)
    elif args.comando == "resumo":
        resumo(conn)
    conn.close()


if __name__ == "__main__":
    main()
