# Controle de Gastos (Python + SQLite)

Aplicação de linha de comando para registrar gastos pessoais e ver o resumo por categoria. O foco é praticar SQL (criação de tabelas, chave estrangeira, JOIN, GROUP BY) integrado ao Python.

## Modelo de dados
- `categorias (id, nome)`
- `gastos (id, descricao, valor, data, categoria_id)` com chave estrangeira para `categorias`

## Como usar
Requer Python 3.8+ (o `sqlite3` já vem na biblioteca padrão).

```bash
python gastos.py add "Almoço" 32.50 Alimentação
python gastos.py add "Ônibus" 4.80 Transporte --data 2026-10-10
python gastos.py list
python gastos.py resumo
```

## Conceitos praticados
SQL (`CREATE TABLE`, `INSERT`, `SELECT`, `JOIN`, `GROUP BY`, `ORDER BY`), consultas parametrizadas (evita SQL injection), `sqlite3`, `argparse`.

## Próximos passos
- Filtro por mês
- Exportar relatório em CSV
- Cadastro de novas categorias
