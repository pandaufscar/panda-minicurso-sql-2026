import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="🐼 Minicurso SQL – Plataforma Interativa",
    page_icon="🐼",
    layout="wide"
)

# =========================================================
# BANCO DE DADOS EM MEMÓRIA (MINIMAL)
# =========================================================
def criar_banco():
    conn = sqlite3.connect(":memory:")

    # ---------- Tabelas em português (Semana 1) ----------
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
    ])

    conn.execute("""
        CREATE TABLE pedidos (
            id_pedido TEXT,
            id_cliente TEXT,
            status_pedido TEXT,
            data_hora_compra TEXT
        )
    """)
    conn.executemany("INSERT INTO pedidos VALUES (?,?,?,?)", [
        ("p001", "c001", "delivered",  "2017-01-05 10:30:00"),
        ("p002", "c002", "canceled",   "2017-03-10 14:20:00"),
        ("p003", "c003", "shipped",    "2018-06-15 09:00:00"),
        ("p004", "c004", "delivered",  "2018-09-20 16:45:00"),
    ])

    conn.execute("""
        CREATE TABLE produtos (
            id_produto TEXT,
            categoria_produto TEXT,
            quantidade_fotos_produto INTEGER,
            peso_produto_g INTEGER
        )
    """)
    conn.executemany("INSERT INTO produtos VALUES (?,?,?,?)", [
        ("pr001", "informatica_acessorios", 3, 150),
        ("pr002", "eletronicos",            5, 300),
        ("pr003", "cama_mesa_banho",        2, 500),
        ("pr004", "brinquedos",             4, 250),
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
    ])

    # ---------- Tabelas Olist (para WHERE/LIKE/IN/BETWEEN/ORDER BY) ----------
    conn.execute("""
        CREATE TABLE olist_order_items_dataset (
            order_id TEXT,
            product_id TEXT,
            price REAL,
            freight_value REAL
        )
    """)
    conn.executemany("INSERT INTO olist_order_items_dataset VALUES (?,?,?,?)", [
        ("p001", "pr001", 120.0, 10.0),
        ("p002", "pr002",  90.0,  0.0),
        ("p003", "pr003", 200.0, 20.0),
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
        ("p002", "boleto",      1, 200.0),
        ("p003", "voucher",     1,  80.0),
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
        ("p002", 4, "comentario bom"),
        ("p003", 2, "nao foi bom"),
    ])

    conn.execute("""
        CREATE TABLE olist_customers_dataset (
            customer_id TEXT,
            customer_city TEXT,
            customer_state TEXT
        )
    """)
    conn.executemany("INSERT INTO olist_customers_dataset VALUES (?,?,?)", [
        ("c001", "sao paulo", "SP"),
        ("c002", "rio de janeiro", "RJ"),
        ("c003", "porto alegre", "RS"),
    ])

    conn.execute("""
        CREATE TABLE olist_orders_dataset (
            order_id TEXT,
            customer_id TEXT,
            order_status TEXT,
            order_purchase_timestamp TEXT,
            order_delivered_customer_date TEXT,
            order_estimated_delivery_date TEXT
        )
    """)
    conn.executemany("INSERT INTO olist_orders_dataset VALUES (?,?,?,?,?,?)", [
        ("p001", "c001", "delivered",   "2018-01-10", "2018-01-20", "2018-01-15"),
        ("p002", "c002", "canceled",    "2017-12-05", None,         "2017-12-20"),
        ("p003", "c003", "unavailable", "2018-02-01", None,         "2018-02-15"),
        ("p004", "c001", "shipped",     "2018-03-10", None,         "2018-03-25"),
    ])

    conn.execute("""
        CREATE TABLE olist_products_dataset (
            product_id TEXT,
            product_category_name TEXT,
            product_weight_g INTEGER
        )
    """)
    conn.executemany("INSERT INTO olist_products_dataset VALUES (?,?,?)", [
        ("pr001", "moveis_escritorio", 1500),
        ("pr002", "esporte_lazer",     1200),
        ("pr003", "brinquedos",        800),
    ])

    conn.commit()
    return conn


# =========================================================
# SESSION STATE
# =========================================================
if "conn" not in st.session_state:
    st.session_state["conn"] = criar_banco()
if "acertos" not in st.session_state:
    st.session_state["acertos"] = set()

conn = st.session_state["conn"]

# =========================================================
# DESAFIOS (9 EXERCÍCIOS, 3 POR TÓPICO)
# =========================================================
DESAFIOS = [
    # --------- TÓPICO 1 – SELECT / FROM / AS ---------
    {
        "secao": "Tópico 1 – SELECT / FROM / AS",
        "topico": "SELECT",
        "titulo": "SELECT 1 – SELECT * FROM clientes",
        "enunciado": "Exiba todas as informações da tabela `clientes`.",
        "gabarito": "SELECT * FROM clientes",
        "explicacao": (
            "O comando `SELECT * FROM clientes` retorna todas as colunas e linhas da tabela `clientes`. "
            "É ótimo para explorar os dados pela primeira vez."
        ),
        "dica": "Use `SELECT * FROM clientes`.",
        "ordered": False,
    },
    {
        "secao": "Tópico 1 – SELECT / FROM / AS",
        "topico": "FROM",
        "titulo": "FROM 1 – cidades na geolocalização",
        "enunciado": "Liste `cidade_geolocalizacao` e `estado_geolocalizacao` da tabela `geolocalizacao`.",
        "gabarito": "SELECT cidade_geolocalizacao, estado_geolocalizacao FROM geolocalizacao",
        "explicacao": (
            "`FROM` indica de qual tabela os dados vêm. "
            "Aqui você pega duas colunas específicas da tabela `geolocalizacao`."
        ),
        "dica": "Modelo: `SELECT col1, col2 FROM geolocalizacao`.",
        "ordered": False,
    },
    {
        "secao": "Tópico 1 – SELECT / FROM / AS",
        "topico": "AS",
        "titulo": "AS 1 – alias em clientes",
        "enunciado": (
            "Exiba `id_cliente` e `cidade_cliente`, renomeando as colunas para "
            "`\"Código do Cliente\"` e `\"Cidade\"`."
        ),
        "gabarito": 'SELECT id_cliente AS "Código do Cliente", cidade_cliente AS "Cidade" FROM clientes',
        "explicacao": (
            "`AS` cria um apelido para a coluna apenas no resultado. "
            "Isso deixa o relatório mais legível sem alterar a tabela original."
        ),
        "dica": "Não esqueça das aspas duplas em `\"Código do Cliente\"` e `\"Cidade\"`.",
        "ordered": False,
    },

    # --------- TÓPICO 2 – WHERE / OPERADORES / LÓGICOS ---------
    {
        "secao": "Tópico 2 – WHERE, Operadores e Lógicos",
        "topico": "WHERE",
        "titulo": "WHERE 1 – pedidos delivered",
        "enunciado": "Liste todos os pedidos com `order_status = 'delivered'`.",
        "gabarito": "SELECT * FROM olist_orders_dataset WHERE order_status = 'delivered'",
        "explicacao": (
            "`WHERE` filtra linhas. Aqui só aparecem as linhas onde `order_status` é exatamente `'delivered'`."
        ),
        "dica": "Use `WHERE order_status = 'delivered'` logo após o FROM.",
        "ordered": False,
    },
    {
        "secao": "Tópico 2 – WHERE, Operadores e Lógicos",
        "topico": "Operadores de comparação",
        "titulo": "OP 1 – itens com price > 100",
        "enunciado": "Liste itens de pedido cujo `price` seja maior que 100.",
        "gabarito": "SELECT * FROM olist_order_items_dataset WHERE price > 100",
        "explicacao": (
            "`>` compara o valor de `price` com 100, retornando apenas itens mais caros que esse valor."
        ),
        "dica": "Não use `>=`; o enunciado pede estritamente maior que 100.",
        "ordered": False,
    },
    {
        "secao": "Tópico 2 – WHERE, Operadores e Lógicos",
        "topico": "AND",
        "titulo": "LOG 1 – pedidos delivered atrasados",
        "enunciado": (
            "Liste pedidos com status `'delivered'` e que foram entregues **depois** da data estimada."
        ),
        "gabarito": (
            "SELECT * FROM olist_orders_dataset\n"
            "WHERE order_status = 'delivered'\n"
            "  AND order_delivered_customer_date > order_estimated_delivery_date"
        ),
        "explicacao": (
            "`AND` combina duas condições:\n"
            "- status é `'delivered'`\n"
            "- data de entrega real é maior que a data estimada\n"
            "Assim identificamos pedidos atrasados."
        ),
        "dica": "Use `AND` entre as duas condições, exatamente como no PDF.",
        "ordered": False,
    },

    # --------- TÓPICO 3 – LIKE / IN / ORDER BY ---------
    {
        "secao": "Tópico 3 – LIKE / IN / ORDER BY",
        "topico": "LIKE",
        "titulo": "LIKE 1 – cidade termina com 'paulo'",
        "enunciado": "Liste clientes cuja cidade termina com `'paulo'`.",
        "gabarito": "SELECT * FROM olist_customers_dataset WHERE customer_city LIKE '%paulo'",
        "explicacao": (
            "`LIKE '%paulo'` significa: qualquer coisa antes e terminando em 'paulo'. "
            "Por exemplo, `sao paulo`."
        ),
        "dica": "Coloque o `%` **antes**: `LIKE '%paulo'`.",
        "ordered": False,
    },
    {
        "secao": "Tópico 3 – LIKE / IN / ORDER BY",
        "topico": "IN",
        "titulo": "IN 1 – estados SP, RJ ou MG",
        "enunciado": "Liste clientes que moram em `'SP'`, `'RJ'` ou `'MG'`.",
        "gabarito": (
            "SELECT * FROM olist_customers_dataset\n"
            "WHERE customer_state IN ('SP', 'RJ', 'MG')"
        ),
        "explicacao": (
            "`IN` é atalho para vários OR. Em vez de 3 comparações, usamos uma lista de valores."
        ),
        "dica": "Os valores da lista devem estar entre parênteses e com aspas simples.",
        "ordered": False,
    },
    {
        "secao": "Tópico 3 – LIKE / IN / ORDER BY",
        "topico": "ORDER BY",
        "titulo": "ORDER BY 1 – produtos por peso (DESC)",
        "enunciado": "Liste todos os produtos, do mais pesado para o mais leve.",
        "gabarito": (
            "SELECT * FROM olist_products_dataset\n"
            "ORDER BY product_weight_g DESC"
        ),
        "explicacao": (
            "`ORDER BY product_weight_g DESC` ordena em ordem decrescente de peso. "
            "Sem `DESC`, a ordem seria crescente."
        ),
        "dica": "Lembre de colocar o `ORDER BY` no final da consulta.",
        "ordered": True,
    },
]

# =========================================================
# FUNÇÃO DE COMPARAÇÃO
# =========================================================
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

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 🐼 Minicurso SQL")
    st.caption("Plataforma com 3 tópicos · 9 exercícios-chave")

    total = len(DESAFIOS)
    acertos = len(st.session_state["acertos"])
    st.metric("Acertos", acertos)
    st.metric("Total", total)
    st.progress(acertos / total if total > 0 else 0)

    st.divider()
    secao_filtro = st.selectbox(
        "Escolha o tópico",
        ["Todos"] + list(dict.fromkeys(d["secao"] for d in DESAFIOS))
    )

    st.divider()
    st.markdown("### Tabelas usadas")
    st.code(
        "clientes\npedidos\nprodutos\ngeolocalizacao\n"
        "olist_orders_dataset\nolist_customers_dataset\n"
        "olist_order_items_dataset\nolist_order_payments_dataset\n"
        "olist_order_reviews_dataset\nolist_products_dataset",
        language=None
    )

# =========================================================
# CONTEÚDO PRINCIPAL
# =========================================================
st.title("Plataforma Interativa de Exercícios SQL")

st.markdown("""
Esta plataforma foi construída a partir dos exercícios dos PDFs do curso:

- **Tópico 1** – SELECT, FROM, AS  
- **Tópico 2** – WHERE, operadores de comparação e lógicos  
- **Tópico 3** – LIKE, IN, ORDER BY  

Em cada tópico você tem **3 exercícios** com:
- enunciado
- explicação
- dica
- verificação automática
- resposta correta disponível
""")
st.divider()

if secao_filtro == "Todos":
    desafios_visiveis = DESAFIOS
else:
    desafios_visiveis = [d for d in DESAFIOS if d["secao"] == secao_filtro]

# Agrupar por tópico para criar "sessões"
grupos = {}
for d in desafios_visiveis:
    grupos.setdefault(d["secao"], []).append(d)

for secao, lista in grupos.items():
    st.subheader(secao)
    for desafio in lista:
        concluido = desafio["titulo"] in st.session_state["acertos"]
        icon = "✅" if concluido else "📌"

        with st.container():
            st.markdown(f"### {icon} {desafio['titulo']}  ·  {desafio['topico']}")
            st.markdown(f"**Enunciado:** {desafio['enunciado']}")
            st.markdown("**Explicação:**")
            st.info(desafio["explicacao"])

            query = st.text_area(
                "Sua query SQL:",
                key=f"q_{desafio['titulo']}",
                height=110,
                placeholder="SELECT ..."
            )

            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                if st.button("Verificar", key=f"v_{desafio['titulo']}"):
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
                                st.error("Ainda não está igual ao gabarito.")

                            st.markdown("**Resultado da sua query:**")
                            st.dataframe(df_u, use_container_width=True)
                        except Exception as e:
                            st.error(f"Erro ao executar sua query: {e}")

            with col2:
                if st.button("Dica", key=f"d_{desafio['titulo']}"):
                    st.info(desafio["dica"])

            with col3:
                if st.button("Mostrar resposta correta", key=f"g_{desafio['titulo']}"):
                    st.code(desafio["gabarito"], language="sql")

            st.markdown("---")

st.subheader("Ver dados das tabelas")
tabs = st.tabs([
    "clientes", "pedidos", "produtos", "geolocalizacao",
    "olist_orders", "olist_customers",
    "itens / pagamentos / reviews", "olist_products"
])

with tabs[0]:
    st.dataframe(pd.read_sql_query("SELECT * FROM clientes", conn), use_container_width=True)
with tabs[1]:
    st.dataframe(pd.read_sql_query("SELECT * FROM pedidos", conn), use_container_width=True)
with tabs[2]:
    st.dataframe(pd.read_sql_query("SELECT * FROM produtos", conn), use_container_width=True)
with tabs[3]:
    st.dataframe(pd.read_sql_query("SELECT * FROM geolocalizacao", conn), use_container_width=True)
with tabs[4]:
    st.dataframe(pd.read_sql_query("SELECT * FROM olist_orders_dataset", conn), use_container_width=True)
with tabs[5]:
    st.dataframe(pd.read_sql_query("SELECT * FROM olist_customers_dataset", conn), use_container_width=True)
with tabs[6]:
    st.subheader("olist_order_items_dataset")
    st.dataframe(pd.read_sql_query("SELECT * FROM olist_order_items_dataset", conn), use_container_width=True)
    st.subheader("olist_order_payments_dataset")
    st.dataframe(pd.read_sql_query("SELECT * FROM olist_order_payments_dataset", conn), use_container_width=True)
    st.subheader("olist_order_reviews_dataset")
    st.dataframe(pd.read_sql_query("SELECT * FROM olist_order_reviews_dataset", conn), use_container_width=True)
with tabs[7]:
    st.dataframe(pd.read_sql_query("SELECT * FROM olist_products_dataset", conn), use_container_width=True)
