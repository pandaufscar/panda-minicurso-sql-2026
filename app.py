import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="🐼 PANDA SQL – Minicurso 2026",
    page_icon="🐼",
    layout="wide"
)

DB_VERSION = "vitoria_rennan_2026_07_10"

# ─────────────────────────────────────────
# BANCO DE DADOS
# ─────────────────────────────────────────
def criar_banco():
    conn = sqlite3.connect(":memory:")

    # Tabelas da Semana 1 (Vitória)
    conn.execute("""
        CREATE TABLE clientes (
            id_cliente TEXT,
            cidade_cliente TEXT,
            estado_cliente TEXT
        )
    """)
    conn.executemany("INSERT INTO clientes VALUES (?,?,?)", [
        ("c001", "sao paulo", "SP"),
        ("c002", "rio de janeiro", "RJ"),
        ("c003", "campinas", "SP"),
        ("c004", "curitiba", "PR"),
        ("c005", "salvador", "BA"),
        ("c006", "fortaleza", "CE"),
        ("c007", "joinville", "SC"),
        ("c008", "sorocaba", "SP"),
    ])

    conn.execute("""
        CREATE TABLE pedidos (
            id_pedido TEXT,
            id_cliente TEXT,
            status_pedido TEXT,
            data_hora_compra TEXT,
            data_entrega_cliente TEXT,
            data_estimada_entrega TEXT
        )
    """)
    conn.executemany("INSERT INTO pedidos VALUES (?,?,?,?,?,?)", [
        ("p001", "c001", "delivered",  "2017-01-05 10:30:00", "2018-01-15", "2018-01-10"),
        ("p002", "c002", "delivered",  "2017-03-10 14:20:00", "2018-03-20", "2018-03-25"),
        ("p003", "c003", "shipped",    "2018-06-15 09:00:00", None,         "2018-07-01"),
        ("p004", "c004", "delivered",  "2018-09-20 16:45:00", "2018-10-05", "2018-09-30"),
        ("p005", "c005", "canceled",   "2018-01-01 12:00:00", None,         "2018-01-15"),
        ("p006", "c006", "delivered",  "2017-11-25 08:15:00", "2017-12-05", "2017-12-10"),
        ("p007", "c007", "unavailable","2018-08-30 20:00:00", None,         "2018-09-15"),
        ("p008", "c008", "shipped",    "2018-02-10 11:11:00", None,         "2018-02-15"),
        ("p009", "c001", "delivered",  "2018-05-18 17:30:00", "2018-06-01", "2018-05-28"),
        ("p010", "c002", "delivered",  "2018-02-14 09:00:00", "2018-02-22", "2018-03-01"),
    ])

    conn.execute("""
        CREATE TABLE produtos (
            id_produto TEXT,
            categoria_produto TEXT,
            peso_produto_g INTEGER,
            quantidade_fotos_produto INTEGER
        )
    """)
    conn.executemany("INSERT INTO produtos VALUES (?,?,?,?)", [
        ("pr001", "informatica_acessorios", 150, 3),
        ("pr002", "informatica_acessorios", 600, 4),
        ("pr003", "eletronicos", 300, 5),
        ("pr004", "cama_mesa_banho", 500, 2),
        ("pr005", "brinquedos", 250, 4),
        ("pr006", "perfumaria", 100, 2),
        ("pr007", "papelaria", 50, 1),
    ])

    conn.execute("""
        CREATE TABLE geolocalizacao (
            cidade_geolocalizacao TEXT,
            estado_geolocalizacao TEXT
        )
    """)
    conn.executemany("INSERT INTO geolocalizacao VALUES (?,?)", [
        ("sao paulo", "SP"),
        ("rio de janeiro", "RJ"),
        ("campinas", "SP"),
        ("curitiba", "PR"),
        ("salvador", "BA"),
        ("fortaleza", "CE"),
        ("joinville", "SC"),
        ("sorocaba", "SP"),
    ])

    # Tabelas da Semana 2 (Rennan) - nomes originais do PDF
    conn.execute("""
        CREATE TABLE olist_order_items_dataset (
            order_id TEXT,
            product_id TEXT,
            seller_id TEXT,
            price REAL,
            freight_value REAL
        )
    """)
    conn.executemany("INSERT INTO olist_order_items_dataset VALUES (?,?,?,?,?)", [
        ("p001", "pr001", "s1", 120.0, 10.0),
        ("p002", "pr002", "s2",  90.0,  0.0),
        ("p003", "pr003", "s3", 200.0,  5.0),
        ("p004", "pr004", "s4",  80.0,  0.0),
        ("p005", "pr005", "s5", 150.0, 20.0),
        ("p006", "pr006", "s6", 110.0,  0.0),
        ("p007", "pr007", "s7",  70.0, 15.0),
    ])

    conn.execute("""
        CREATE TABLE olist_order_payments_dataset (
            order_id TEXT,
            payment_type TEXT,
            payment_installments INTEGER,
            payment_value REAL
        )
    """)
    conn.executemany("INSERT INTO olist_order_payments_dataset VALUES (?,?,?,?)", [
        ("p001", "credit_card", 3, 120.0),
        ("p002", "boleto", 1, 200.0),
        ("p003", "credit_card", 12, 80.0),
        ("p004", "voucher", 1, 150.0),
        ("p005", "debit_card", 10, 110.0),
    ])

    conn.execute("""
        CREATE TABLE olist_order_reviews_dataset (
            order_id TEXT,
            review_score INTEGER,
            review_comment_message TEXT
        )
    """)
    conn.executemany("INSERT INTO olist_order_reviews_dataset VALUES (?,?,?)", [
        ("p001", 5, "otimo"),
        ("p002", 4, "bom"),
        ("p003", 2, "atrasou"),
        ("p004", 1, "ruim"),
        ("p005", 3, "ok"),
    ])

    # Views Olist para bater com o PDF
    conn.execute("""
        CREATE VIEW olist_customers_dataset AS
        SELECT
            id_cliente AS customer_id,
            cidade_cliente AS customer_city,
            estado_cliente AS customer_state
        FROM clientes
    """)

    conn.execute("""
        CREATE VIEW olist_orders_dataset AS
        SELECT
            id_pedido AS order_id,
            id_cliente AS customer_id,
            status_pedido AS order_status,
            data_hora_compra AS order_purchase_timestamp,
            data_entrega_cliente AS order_delivered_customer_date,
            data_estimada_entrega AS order_estimated_delivery_date
        FROM pedidos
    """)

    conn.execute("""
        CREATE VIEW olist_products_dataset AS
        SELECT
            id_produto AS product_id,
            categoria_produto AS product_category_name,
            peso_produto_g AS product_weight_g
        FROM produtos
    """)

    conn.commit()
    return conn


# ─────────────────────────────────────────
# ESTADO DA SESSÃO
# ─────────────────────────────────────────
if st.session_state.get("db_version") != DB_VERSION:
    st.session_state["conn"] = criar_banco()
    st.session_state["acertos"] = set()
    st.session_state["db_version"] = DB_VERSION

conn = st.session_state["conn"]


# ─────────────────────────────────────────
# DESAFIOS
# ─────────────────────────────────────────
DESAFIOS = [
    # ===== Vitória =====
    {
        "autor": "Vitória",
        "secao": "SELECT",
        "titulo": "Exercício 1 — SELECT *",
        "enunciado": "Exiba todas as informações da tabela `clientes`.",
        "gabarito": "SELECT * FROM clientes",
        "dica": "Use `SELECT * FROM clientes`.",
        "ordered": False
    },
    {
        "autor": "Vitória",
        "secao": "SELECT",
        "titulo": "Exercício 2 — colunas específicas",
        "enunciado": "Exiba `id_cliente` e `cidade_cliente` da tabela `clientes`.",
        "gabarito": "SELECT id_cliente, cidade_cliente FROM clientes",
        "dica": "Liste as colunas separadas por vírgula.",
        "ordered": False
    },
    {
        "autor": "Vitória",
        "secao": "SELECT",
        "titulo": "Exercício 3 — dados de pedidos",
        "enunciado": "Exiba `id_pedido`, `status_pedido` e `data_hora_compra` da tabela `pedidos`.",
        "gabarito": "SELECT id_pedido, status_pedido, data_hora_compra FROM pedidos",
        "dica": "Siga exatamente a ordem das colunas do PDF.",
        "ordered": False
    },
    {
        "autor": "Vitória",
        "secao": "SELECT",
        "titulo": "Exercício 4 — dados de produtos",
        "enunciado": "Exiba `id_produto`, `categoria_produto` e `peso_produto_g` da tabela `produtos`.",
        "gabarito": "SELECT id_produto, categoria_produto, peso_produto_g FROM produtos",
        "dica": "Use `SELECT id_produto, categoria_produto, peso_produto_g FROM produtos`.",
        "ordered": False
    },
    {
        "autor": "Vitória",
        "secao": "FROM",
        "titulo": "Exercício 1 — geolocalizacao",
        "enunciado": "Exiba todas as informações da tabela `geolocalizacao`.",
        "gabarito": "SELECT * FROM geolocalizacao",
        "dica": "O comando é `SELECT * FROM geolocalizacao`.",
        "ordered": False
    },
    {
        "autor": "Vitória",
        "secao": "FROM",
        "titulo": "Exercício 2 — cidade e estado",
        "enunciado": "Liste `cidade_geolocalizacao` e `estado_geolocalizacao`.",
        "gabarito": "SELECT cidade_geolocalizacao, estado_geolocalizacao FROM geolocalizacao",
        "dica": "Use `FROM geolocalizacao`.",
        "ordered": False
    },
    {
        "autor": "Vitória",
        "secao": "FROM",
        "titulo": "Exercício 3 — clientes",
        "enunciado": "Exiba `id_cliente` e `cidade_cliente` da tabela `clientes`.",
        "gabarito": "SELECT id_cliente, cidade_cliente FROM clientes",
        "dica": "Mesma lógica do exercício anterior.",
        "ordered": False
    },
    {
        "autor": "Vitória",
        "secao": "FROM",
        "titulo": "Exercício 4 — pedidos",
        "enunciado": "Exiba `id_pedido` e `status_pedido` da tabela `pedidos`.",
        "gabarito": "SELECT id_pedido, status_pedido FROM pedidos",
        "dica": "Use `SELECT id_pedido, status_pedido FROM pedidos`.",
        "ordered": False
    },
    {
        "autor": "Vitória",
        "secao": "AS",
        "titulo": "Exercício 1 — alias em clientes",
        "enunciado": 'Renomeie `id_cliente` para "Código do Cliente" e `cidade_cliente` para "Cidade".',
        "gabarito": 'SELECT id_cliente AS "Código do Cliente", cidade_cliente AS "Cidade" FROM clientes',
        "dica": 'Use `AS "Nome"` para renomear a coluna.',
        "ordered": False
    },
    {
        "autor": "Vitória",
        "secao": "AS",
        "titulo": "Exercício 2 — alias em pedidos",
        "enunciado": 'Renomeie `id_pedido` para "Pedido" e `status_pedido` para "Status".',
        "gabarito": 'SELECT id_pedido AS "Pedido", status_pedido AS "Status" FROM pedidos',
        "dica": 'Use `AS` para criar apelidos nas colunas.',
        "ordered": False
    },
    {
        "autor": "Vitória",
        "secao": "AS",
        "titulo": "Exercício 3 — alias em produtos",
        "enunciado": 'Renomeie `categoria_produto` para "Categoria" e `quantidade_fotos_produto` para "Quantidade de Fotos".',
        "gabarito": 'SELECT categoria_produto AS "Categoria", quantidade_fotos_produto AS "Quantidade de Fotos" FROM produtos',
        "dica": 'O alias muda só o nome exibido no resultado.',
        "ordered": False
    },
    {
        "autor": "Vitória",
        "secao": "AS",
        "titulo": "Exercício 4 — alias em geolocalizacao",
        "enunciado": 'Renomeie `cidade_geolocalizacao` para "Cidade" e `estado_geolocalizacao` para "UF".',
        "gabarito": 'SELECT cidade_geolocalizacao AS "Cidade", estado_geolocalizacao AS "UF" FROM geolocalizacao',
        "dica": 'Use `AS "Cidade"` e `AS "UF"`.',
        "ordered": False
    },

    # ===== Rennan =====
    {
        "autor": "Rennan",
        "secao": "WHERE",
        "titulo": "Exercício 1 — delivered",
        "enunciado": "Liste todos os pedidos com status `'delivered'`.",
        "gabarito": "SELECT * FROM olist_orders_dataset WHERE order_status = 'delivered'",
        "dica": "Use `WHERE order_status = 'delivered'`.",
        "ordered": False
    },
    {
        "autor": "Rennan",
        "secao": "WHERE",
        "titulo": "Exercício 2 — canceled",
        "enunciado": "Liste todos os pedidos com status `'canceled'`.",
        "gabarito": "SELECT * FROM olist_orders_dataset WHERE order_status = 'canceled'",
        "dica": "Use `WHERE order_status = 'canceled'`.",
        "ordered": False
    },
    {
        "autor": "Rennan",
        "secao": "WHERE",
        "titulo": "Exercício 3 — clientes de sao paulo",
        "enunciado": "Liste `customer_id`, `customer_city` e `customer_state` de clientes que moram em `'sao paulo'`.",
        "gabarito": "SELECT customer_id, customer_city, customer_state FROM olist_customers_dataset WHERE customer_city = 'sao paulo'",
        "dica": "No dataset, cidade está em minúsculas e sem acento.",
        "ordered": False
    },
    {
        "autor": "Rennan",
        "secao": "WHERE",
        "titulo": "Exercício 4 — categoria informatica_acessorios",
        "enunciado": "Liste `product_id` e `product_category_name` da categoria `'informatica_acessorios'`.",
        "gabarito": "SELECT product_id, product_category_name FROM olist_products_dataset WHERE product_category_name = 'informatica_acessorios'",
        "dica": "Use `WHERE product_category_name = 'informatica_acessorios'`.",
        "ordered": False
    },
    {
        "autor": "Rennan",
        "secao": "Operadores",
        "titulo": "Exercício 1 — preço maior que 100",
        "enunciado": "Liste os itens de pedido com `price > 100`.",
        "gabarito": "SELECT * FROM olist_order_items_dataset WHERE price > 100",
        "dica": "Operador `>`.",
        "ordered": False
    },
    {
        "autor": "Rennan",
        "secao": "Operadores",
        "titulo": "Exercício 2 — parcelas >= 10",
        "enunciado": "Liste os pagamentos com `payment_installments >= 10`.",
        "gabarito": "SELECT * FROM olist_order_payments_dataset WHERE payment_installments >= 10",
        "dica": "Operador `>=`.",
        "ordered": False
    },
    {
        "autor": "Rennan",
        "secao": "Operadores",
        "titulo": "Exercício 3 — review_score < 3",
        "enunciado": "Liste as avaliações com `review_score < 3`.",
        "gabarito": "SELECT * FROM olist_order_reviews_dataset WHERE review_score < 3",
        "dica": "Operador `<`.",
        "ordered": False
    },
    {
        "autor": "Rennan",
        "secao": "Operadores",
        "titulo": "Exercício 4 — frete diferente de 0",
        "enunciado": "Liste os itens com `freight_value <> 0`.",
        "gabarito": "SELECT * FROM olist_order_items_dataset WHERE freight_value <> 0",
        "dica": "Operador `<>` significa diferente de.",
        "ordered": False
    },
    {
        "autor": "Rennan",
        "secao": "AND / OR / NOT",
        "titulo": "Exercício 1 — delivered atrasado",
        "enunciado": "Liste pedidos `delivered` que foram entregues depois da data estimada.",
        "gabarito": "SELECT * FROM olist_orders_dataset WHERE order_status = 'delivered' AND order_delivered_customer_date > order_estimated_delivery_date",
        "dica": "Use `AND` para combinar as duas condições.",
        "ordered": False
    },
    {
        "autor": "Rennan",
        "secao": "AND / OR / NOT",
        "titulo": "Exercício 2 — canceled ou unavailable",
        "enunciado": "Liste pedidos com status `'canceled'` ou `'unavailable'`.",
        "gabarito": "SELECT * FROM olist_orders_dataset WHERE order_status = 'canceled' OR order_status = 'unavailable'",
        "dica": "Use `OR`.",
        "ordered": False
    },
    {
        "autor": "Rennan",
        "secao": "AND / OR / NOT",
        "titulo": "Exercício 3 — pagamento não é credit_card",
        "enunciado": "Liste pagamentos cujo tipo não seja `'credit_card'`.",
        "gabarito": "SELECT * FROM olist_order_payments_dataset WHERE NOT payment_type = 'credit_card'",
        "dica": "Use `NOT`.",
        "ordered": False
    },
    {
        "autor": "Rennan",
        "secao": "AND / OR / NOT",
        "titulo": "Exercício 4 — delivered/shipped desde 2018",
        "enunciado": "Liste pedidos com status `'delivered'` ou `'shipped'` e comprados a partir de `'2018-01-01'`.",
        "gabarito": "SELECT * FROM olist_orders_dataset WHERE (order_status = 'delivered' OR order_status = 'shipped') AND order_purchase_timestamp >= '2018-01-01'",
        "dica": "Os parênteses importam.",
        "ordered": False
    },
]


# ─────────────────────────────────────────
# COMPARAÇÃO
# ─────────────────────────────────────────
def comparar(df_u, df_g, ordered):
    try:
        df_u = df_u.copy()
        df_g = df_g.copy()

        df_u.columns = [c.lower().strip() for c in df_u.columns]
        df_g.columns = [c.lower().strip() for c in df_g.columns]

        if set(df_u.columns) != set(df_g.columns):
            return False

        df_u = df_u[df_g.columns]

        if not ordered:
            cols = list(df_g.columns)
            df_u = df_u.sort_values(by=cols).reset_index(drop=True)
            df_g = df_g.sort_values(by=cols).reset_index(drop=True)
        else:
            df_u = df_u.reset_index(drop=True)
            df_g = df_g.reset_index(drop=True)

        return df_u.astype(str).equals(df_g.astype(str))
    except Exception:
        return False


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🐼 PANDA SQL")
    st.caption("Minicurso 2026 · UFSCar")
    st.divider()

    total = len(DESAFIOS)
    acertos = len(st.session_state["acertos"])
    pct = int((acertos / total) * 100) if total > 0 else 0

    st.metric("Acertos", acertos)
    st.metric("Total", total)
    st.progress(acertos / total if total > 0 else 0, text=f"{pct}% concluído")

    st.divider()
    filtro = st.radio(
        "Filtrar por grupo:",
        ["Todos", "Vitória", "Rennan"],
        index=0
    )

    st.divider()
    st.markdown("### Tabelas")
    st.code(
        "clientes\npedidos\nprodutos\ngeolocalizacao\nolist_customers_dataset\nolist_orders_dataset\nolist_products_dataset\nolist_order_items_dataset\nolist_order_payments_dataset\nolist_order_reviews_dataset",
        language=None
    )


# ─────────────────────────────────────────
# CONTEÚDO PRINCIPAL
# ─────────────────────────────────────────
st.title("🐼 Plataforma de Exercícios SQL")
st.markdown("""
Esta versão está pronta com **Vitória + Rennan**.

- **Vitória**: `SELECT`, `FROM`, `AS`
- **Rennan**: `WHERE`, operadores, `AND / OR / NOT`

Os nomes de cidade/categoria seguem o padrão do Olist: **minúsculas e sem acento**.
""")
st.divider()

if filtro == "Todos":
    desafios_visiveis = DESAFIOS
else:
    desafios_visiveis = [d for d in DESAFIOS if d["autor"] == filtro]

secoes = {}
for d in desafios_visiveis:
    chave = f"{d['autor']} — {d['secao']}"
    secoes.setdefault(chave, []).append(d)

for secao, desafios in secoes.items():
    concluidos = sum(1 for d in desafios if d["titulo"] in st.session_state["acertos"])
    st.subheader(secao)

    for desafio in desafios:
        concluido = desafio["titulo"] in st.session_state["acertos"]
        icon = "✅" if concluido else "📌"

        with st.expander(f"{icon} {desafio['titulo']}", expanded=False):
            st.markdown(desafio["enunciado"])

            query = st.text_area(
                "Sua query SQL:",
                key=f"q_{desafio['autor']}_{desafio['secao']}_{desafio['titulo']}",
                height=110,
                placeholder="SELECT ..."
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Verificar", key=f"v_{desafio['autor']}_{desafio['secao']}_{desafio['titulo']}"):
                    q = query.strip()
                    if not q:
                        st.warning("Escreva uma query antes de verificar.")
                    else:
                        try:
                            df_u = pd.read_sql_query(q, conn)
                            df_g = pd.read_sql_query(desafio["gabarito"], conn)

                            if comparar(df_u, df_g, desafio["ordered"]):
                                st.success("Resposta correta!")
                                st.session_state["acertos"].add(desafio["titulo"])
                                st.balloons()
                            else:
                                st.error("Ainda não está certo. Revise sua query.")

                            st.markdown("**Resultado da sua query:**")
                            st.dataframe(df_u, use_container_width=True)

                        except Exception as e:
                            st.error(f"Erro ao executar sua query: {e}")

            with col2:
                if st.button("Dica", key=f"d_{desafio['autor']}_{desafio['secao']}_{desafio['titulo']}"):
                    st.info(desafio["dica"])

    st.divider()


# ─────────────────────────────────────────
# VISUALIZAÇÃO DAS TABELAS
# ─────────────────────────────────────────
st.subheader("Explorar tabelas do banco")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "clientes",
    "pedidos",
    "produtos",
    "geolocalizacao",
    "olist_customers_dataset",
    "olist_orders_dataset",
    "Olist extras"
])

with tab1:
    st.dataframe(pd.read_sql_query("SELECT * FROM clientes", conn), use_container_width=True)

with tab2:
    st.dataframe(pd.read_sql_query("SELECT * FROM pedidos", conn), use_container_width=True)

with tab3:
    st.dataframe(pd.read_sql_query("SELECT * FROM produtos", conn), use_container_width=True)

with tab4:
    st.dataframe(pd.read_sql_query("SELECT * FROM geolocalizacao", conn), use_container_width=True)

with tab5:
    st.dataframe(pd.read_sql_query("SELECT * FROM olist_customers_dataset", conn), use_container_width=True)

with tab6:
    st.dataframe(pd.read_sql_query("SELECT * FROM olist_orders_dataset", conn), use_container_width=True)

with tab7:
    st.dataframe(pd.read_sql_query("SELECT * FROM olist_order_items_dataset", conn), use_container_width=True)
    st.dataframe(pd.read_sql_query("SELECT * FROM olist_order_payments_dataset", conn), use_container_width=True)
    st.dataframe(pd.read_sql_query("SELECT * FROM olist_order_reviews_dataset", conn), use_container_width=True)
    st.dataframe(pd.read_sql_query("SELECT * FROM olist_products_dataset", conn), use_container_width=True)
