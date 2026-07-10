import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="🐼 PANDA SQL – Minicurso 2026",
    page_icon="🐼",
    layout="wide"
)

# ─────────────────────────────────────────
# BANCO DE DADOS (em memória)
# ─────────────────────────────────────────
def criar_banco():
    conn = sqlite3.connect(":memory:")

    # Clientes (adaptado para estilo Olist: cidades minúsculas, sem acento)
    conn.execute("""CREATE TABLE clientes (
        id_cliente TEXT,
        id_unico_cliente TEXT,
        cinco_digitos_cep_cliente TEXT,
        cidade_cliente TEXT,
        estado_cliente TEXT
    )""")
    conn.executemany("INSERT INTO clientes VALUES (?,?,?,?,?)", [
        ('c001','u001','01001','sao paulo','SP'),
        ('c002','u002','20001','rio de janeiro','RJ'),
        ('c003','u003','13001','campinas','SP'),
        ('c004','u004','30001','belo horizonte','MG'),
        ('c005','u005','11001','santos','SP'),
        ('c006','u006','80001','curitiba','PR'),
        ('c007','u007','40001','salvador','BA'),
        ('c008','u008','38401','uberlandia','MG'),
        ('c009','u009','60001','fortaleza','CE'),
        ('c010','u010','18001','sorocaba','SP'),
    ])

    # Pedidos (equivalente a olist_orders_dataset)
    conn.execute("""CREATE TABLE pedidos (
        id_pedido TEXT,
        id_cliente TEXT,
        status_pedido TEXT,
        data_hora_compra TEXT,
        data_entrega_cliente TEXT,
        data_estimada_entrega TEXT
    )""")
    conn.executemany("INSERT INTO pedidos VALUES (?,?,?,?,?,?)", [
        ('p001','c001','delivered','2017-01-05 10:30:00','2017-10-10','2018-01-15'),
        ('p002','c002','delivered','2017-03-10 14:20:00','2017-11-20','2018-03-20'),
        ('p003','c003','shipped'  ,'2018-06-15 09:00:00',None,'2018-07-01'),
        ('p004','c004','delivered','2017-09-20 16:45:00','2018-02-28','2018-10-05'),
        ('p005','c005','canceled' ,'2018-01-01 12:00:00',None,'2018-01-15'),
        ('p006','c006','delivered','2017-11-25 08:15:00','2017-12-05','2017-12-10'),
        ('p007','c007','unavailable','2018-08-30 20:00:00',None,'2018-09-15'),
        ('p008','c008','shipped'  ,'2016-12-10 11:11:00',None,'2017-01-05'),
        ('p009','c009','delivered','2018-05-18 17:30:00','2018-05-28','2018-06-01'),
        ('p010','c010','delivered','2018-02-14 09:00:00','2018-02-22','2018-03-01'),
    ])

    # Produtos (equivalente a olist_products_dataset)
    conn.execute("""CREATE TABLE produtos (
        id_produto TEXT,
        categoria_produto TEXT,
        peso_produto_g INTEGER
    )""")
    conn.executemany("INSERT INTO produtos VALUES (?,?,?)", [
        ('pr001','cama_mesa_banho',500),
        ('pr002','eletronicos',300),
        ('pr003','informatica_acessorios',200),
        ('pr004','perfumaria',100),
        ('pr005','brinquedos',250),
        ('pr006','informatica_acessorios',150),
        ('pr007','papelaria',50),
    ])

    # Geolocalização (equivalente a geolocalização do Olist)
    conn.execute("""CREATE TABLE geolocalizacao (
        prefixo_codigo_postal TEXT,
        latitude_geolocalizacao REAL,
        geolocalizacao_longitude REAL,
        cidade_geolocalizacao TEXT,
        estado_geolocalizacao TEXT
    )""")
    conn.executemany("INSERT INTO geolocalizacao VALUES (?,?,?,?,?)", [
        ('01001',-23.5505,-46.6333,'sao paulo','SP'),
        ('20001',-22.9068,-43.1729,'rio de janeiro','RJ'),
        ('13001',-22.9056,-47.0608,'campinas','SP'),
        ('30001',-19.9167,-43.9345,'belo horizonte','MG'),
        ('11001',-23.9608,-46.3336,'santos','SP'),
    ])

    # Itens de pedido (equivale a olist_order_items_dataset)
    conn.execute("""CREATE TABLE itens_pedidos (
        id_pedido TEXT,
        id_produto TEXT,
        preco REAL,
        valor_frete REAL
    )""")
    conn.executemany("INSERT INTO itens_pedidos VALUES (?,?,?,?)", [
        ('p001','pr001',120.0,0.0),
        ('p001','pr002',90.0,10.0),
        ('p002','pr003',200.0,0.0),
        ('p003','pr004',80.0,5.0),
        ('p004','pr005',150.0,0.0),
        ('p005','pr006',110.0,20.0),
    ])

    # Pagamentos (equivalente a olist_order_payments_dataset)
    conn.execute("""CREATE TABLE pagamentos (
        id_pedido TEXT,
        tipo_pagamento TEXT,
        parcelamento_pagamento INTEGER,
        valor_pagamento REAL
    )""")
    conn.executemany("INSERT INTO pagamentos VALUES (?,?,?,?)", [
        ('p001','credit_card',3,120.0),
        ('p002','boleto',1,200.0),
        ('p003','credit_card',12,80.0),
        ('p004','voucher',1,150.0),
        ('p005','debit_card',10,110.0),
    ])

    # Avaliações (equivalente a olist_order_reviews_dataset)
    conn.execute("""CREATE TABLE avaliacoes (
        id_pedido TEXT,
        nota_avaliacao INTEGER,
        comentario TEXT
    )""")
    conn.executemany("INSERT INTO avaliacoes VALUES (?,?,?)", [
        ('p001',5,'ótimo'),
        ('p002',4,'bom'),
        ('p003',2,'atrasou'),
        ('p004',1,'ruim'),
        ('p005',3,'ok'),
    ])

    conn.commit()
    return conn

# ─────────────────────────────────────────
# ESTADO
# ─────────────────────────────────────────
if "conn" not in st.session_state:
    st.session_state["conn"] = criar_banco()
if "acertos" not in st.session_state:
    st.session_state["acertos"] = set()

conn = st.session_state["conn"]

# ─────────────────────────────────────────
# DESAFIOS – Vitória (Semana 1) + Rennan (WHERE)
# ─────────────────────────────────────────
DESAFIOS = [
    # ---------- Vitória: SELECT / FROM ----------
    {
        "id": 1,
        "semana": "📘 Semana 1 — SELECT / FROM / AS (Vitória)",
        "titulo": "Exercício 1 — SELECT * FROM clientes",
        "enunciado": "Exiba todas as informações da tabela `clientes`.",
        "gabarito": "SELECT * FROM clientes",
        "dica": "Do PDF: `SELECT * FROM clientes;`",
        "ordered": False,
    },
    {
        "id": 2,
        "semana": "📘 Semana 1 — SELECT / FROM / AS (Vitória)",
        "titulo": "Exercício 2 — id_cliente e cidade_cliente",
        "enunciado": "Exiba o identificador do cliente (`id_cliente`) e a cidade onde ele mora.",
        "gabarito": "SELECT id_cliente, cidade_cliente FROM clientes",
        "dica": "Resposta do PDF: `SELECT id_cliente, cidade_cliente FROM clientes;`",
        "ordered": False,
    },
    {
        "id": 3,
        "semana": "📘 Semana 1 — SELECT / FROM / AS (Vitória)",
        "titulo": "Exercício 3 — id_pedido, status e data da compra",
        "enunciado": "Exiba o `id_pedido`, o `status_pedido` e a `data_hora_compra` da tabela `pedidos`.",
        "gabarito": "SELECT id_pedido, status_pedido, data_hora_compra FROM pedidos",
        "dica": "Resposta do PDF: `SELECT id_pedido, status_pedido, data_hora_compra FROM pedidos;`",
        "ordered": False,
    },
    {
        "id": 4,
        "semana": "📘 Semana 1 — SELECT / FROM / AS (Vitória)",
        "titulo": "Exercício 4 — id_produto, categoria e peso",
        "enunciado": "Liste o `id_produto`, a `categoria_produto` e o `peso_produto_g` da tabela `produtos`.",
        "gabarito": "SELECT id_produto, categoria_produto, peso_produto_g FROM produtos",
        "dica": "Resposta do PDF: `SELECT id_produto, categoria_produto, peso_produto_g FROM produtos;`",
        "ordered": False,
    },
    {
        "id": 5,
        "semana": "📘 Semana 1 — SELECT / FROM / AS (Vitória)",
        "titulo": "Exercício 5 — SELECT * FROM geolocalizacao",
        "enunciado": "Exiba todas as informações da tabela `geolocalizacao`.",
        "gabarito": "SELECT * FROM geolocalizacao",
        "dica": "Resposta do PDF: `SELECT * FROM geolocalizacao;`",
        "ordered": False,
    },
    {
        "id": 6,
        "semana": "📘 Semana 1 — SELECT / FROM / AS (Vitória)",
        "titulo": "Exercício 6 — cidade e estado da geolocalizacao",
        "enunciado": "Liste a `cidade_geolocalizacao` e o `estado_geolocalizacao` da tabela `geolocalizacao`.",
        "gabarito": "SELECT cidade_geolocalizacao, estado_geolocalizacao FROM geolocalizacao",
        "dica": "Resposta do PDF: `SELECT cidade_geolocalizacao, estado_geolocalizacao FROM geolocalizacao;`",
        "ordered": False,
    },
    {
        "id": 7,
        "semana": "📘 Semana 1 — SELECT / FROM / AS (Vitória)",
        "titulo": "Exercício 7 — AS em clientes",
        "enunciado": 'Exiba `id_cliente` e `cidade_cliente`, renomeando para "Código do Cliente" e "Cidade".',
        "gabarito": 'SELECT id_cliente AS "Código do Cliente", cidade_cliente AS "Cidade" FROM clientes',
        "dica": 'Resposta do PDF: `SELECT id_cliente AS "Código do Cliente", cidade_cliente AS "Cidade" FROM clientes;`',
        "ordered": False,
    },
    {
        "id": 8,
        "semana": "📘 Semana 1 — SELECT / FROM / AS (Vitória)",
        "titulo": "Exercício 8 — AS em produtos",
        "enunciado": 'Exiba `categoria_produto` e `quantidade_fotos_produto`, renomeando para "Categoria" e "Quantidade de Fotos".',
        "gabarito": 'SELECT categoria_produto AS "Categoria", peso_produto_g AS "Quantidade de Fotos" FROM produtos',
        "dica": "No seu banco simplificado, usamos `peso_produto_g` como exemplo de coluna numérica.",
        "ordered": False,
    },

    # ---------- Rennan: WHERE / operadores / AND / OR / NOT ----------
    {
        "id": 9,
        "semana": "📗 Semana 2 — WHERE e Operadores (Rennan)",
        "titulo": "Exercício 1 — Pedidos delivered",
        "enunciado": "Liste todos os pedidos que estão com status `'delivered'`.",
        "gabarito": "SELECT * FROM pedidos WHERE status_pedido = 'delivered'",
        "dica": "Adaptado do PDF: `SELECT * FROM olist_orders_dataset WHERE order_status = 'delivered';`",
        "ordered": False,
    },
    {
        "id": 10,
        "semana": "📗 Semana 2 — WHERE e Operadores (Rennan)",
        "titulo": "Exercício 2 — Pedidos canceled",
        "enunciado": "Liste todos os pedidos que estão com status `'canceled'`.",
        "gabarito": "SELECT * FROM pedidos WHERE status_pedido = 'canceled'",
        "dica": "Adaptado do PDF: `WHERE order_status = 'canceled';`",
        "ordered": False,
    },
    {
        "id": 11,
        "semana": "📗 Semana 2 — WHERE e Operadores (Rennan)",
        "titulo": "Exercício 3 — Clientes de sao paulo",
        "enunciado": "Liste `id_cliente`, `cidade_cliente` e `estado_cliente` dos clientes que moram em `'sao paulo'`.",
        "gabarito": "SELECT id_cliente, cidade_cliente, estado_cliente FROM clientes WHERE cidade_cliente = 'sao paulo'",
        "dica": "No Olist, as cidades aparecem em minúsculas e sem acento, como `sao paulo`.",
        "ordered": False,
    },
    {
        "id": 12,
        "semana": "📗 Semana 2 — WHERE e Operadores (Rennan)",
        "titulo": "Exercício 4 — Produtos de informatica_acessorios",
        "enunciado": "Liste `id_produto` e `categoria_produto` dos produtos da categoria `'informatica_acessorios'`.",
        "gabarito": "SELECT id_produto, categoria_produto FROM produtos WHERE categoria_produto = 'informatica_acessorios'",
        "dica": "Adaptado do PDF: `WHERE product_category_name = 'informatica_acessorios';`",
        "ordered": False,
    },
    {
        "id": 13,
        "semana": "📗 Semana 2 — WHERE e Operadores (Rennan)",
        "titulo": "Exercício 5 — Itens com preço > 100",
        "enunciado": "Liste os itens de pedido (`itens_pedidos`) cujo preço (`preco`) seja maior que 100.",
        "gabarito": "SELECT * FROM itens_pedidos WHERE preco > 100",
        "dica": "Adaptado do PDF: `SELECT * FROM olist_order_items_dataset WHERE price > 100;`",
        "ordered": False,
    },
    {
        "id": 14,
        "semana": "📗 Semana 2 — WHERE e Operadores (Rennan)",
        "titulo": "Exercício 6 — Pagamentos com parcela >= 10",
        "enunciado": "Liste os pagamentos em que `parcelamento_pagamento` seja maior ou igual a 10.",
        "gabarito": "SELECT * FROM pagamentos WHERE parcelamento_pagamento >= 10",
        "dica": "Adaptado do PDF: `WHERE payment_installments >= 10;`",
        "ordered": False,
    },
    {
        "id": 15,
        "semana": "📗 Semana 2 — WHERE e Operadores (Rennan)",
        "titulo": "Exercício 7 — Avaliações com nota < 3",
        "enunciado": "Liste as avaliações (`avaliacoes`) em que `nota_avaliacao` seja menor que 3.",
        "gabarito": "SELECT * FROM avaliacoes WHERE nota_avaliacao < 3",
        "dica": "Adaptado do PDF: `WHERE review_score < 3;`",
        "ordered": False,
    },
    {
        "id": 16,
        "semana": "📗 Semana 2 — AND / OR / NOT (Rennan)",
        "titulo": "Exercício 8 — Pedidos delivered e atrasados (AND)",
        "enunciado": """
Liste os pedidos com status `'delivered'` **e** que foram entregues **depois**
da data estimada de entrega (atrasados).
""",
        "gabarito": """
SELECT *
FROM pedidos
WHERE status_pedido = 'delivered'
  AND data_entrega_cliente > data_estimada_entrega
""",
        "dica": "Adaptado exatamente da solução do PDF (order_delivered_customer_date > order_estimated_delivery_date).",
        "ordered": False,
    },
    {
        "id": 17,
        "semana": "📗 Semana 2 — AND / OR / NOT (Rennan)",
        "titulo": "Exercício 9 — Pedidos canceled ou unavailable (OR)",
        "enunciado": "Liste os pedidos com status `'canceled'` **ou** `'unavailable'`.",
        "gabarito": """
SELECT *
FROM pedidos
WHERE status_pedido = 'canceled'
   OR status_pedido = 'unavailable'
""",
        "dica": "Adaptado do PDF: `WHERE order_status = 'canceled' OR order_status = 'unavailable';`",
        "ordered": False,
    },
    {
        "id": 18,
        "semana": "📗 Semana 2 — AND / OR / NOT (Rennan)",
        "titulo": "Exercício 10 — Pagamentos que NÃO são cartão de crédito (NOT)",
        "enunciado": "Liste os pagamentos cujo tipo **não** seja `'credit_card'`.",
        "gabarito": """
SELECT *
FROM pagamentos
WHERE NOT tipo_pagamento = 'credit_card'
""",
        "dica": "Equivalente a `WHERE tipo_pagamento <> 'credit_card';` como no PDF.",
        "ordered": False,
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

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Acertos", acertos)
    with col2:
        st.metric("Total", total)
    st.progress(acertos / total if total > 0 else 0, text=f"{pct}% concluído")

    st.divider()
    semana_filtro = st.radio(
        "Filtrar por semana:",
        ["Todas", "Vitória (Semana 1)", "Rennan (Semana 2)"],
        index=0
    )

    st.divider()
    st.markdown("### Tabelas disponíveis")
    st.code("clientes\npedidos\nprodutos\ngeolocalizacao\nitens_pedidos\npagamentos\navaliacoes")

# ─────────────────────────────────────────
# CONTEÚDO PRINCIPAL
# ─────────────────────────────────────────
st.title("🐼 Plataforma de Exercícios SQL – PANDA")
st.markdown("""
Esta versão da plataforma contém **apenas os exercícios da Vitória (Semana 1) e do Rennan (Semana 2)**,
baseados nos PDFs enviados.

As cidades/categorias seguem o padrão do Olist: **minúsculas e sem acento**, por exemplo:
`sao paulo`, `informatica_acessorios`.
""")
st.divider()

# filtrar desafios
if semana_filtro == "Vitória (Semana 1)":
    desafios_visiveis = [d for d in DESAFIOS if "Vitória" in d["semana"]]
elif semana_filtro == "Rennan (Semana 2)":
    desafios_visiveis = [d for d in DESAFIOS if "Rennan" in d["semana"]]
else:
    desafios_visiveis = DESAFIOS

# agrupar por "semana" (rótulo)
semanas = {}
for d in desafios_visiveis:
    semanas.setdefault(d["semana"], []).append(d)

for semana, desafios in semanas.items():
    concluidos = sum(1 for d in desafios if d["id"] in st.session_state["acertos"])
    st.subheader(f"{semana} · {concluidos}/{len(desafios)} concluídos")

    for desafio in desafios:
        icon = "✅" if desafio["id"] in st.session_state["acertos"] else "📌"
        with st.expander(f"{icon} {desafio['titulo']}", expanded=False):
            st.markdown(desafio["enunciado"])

            query = st.text_area(
                "Escreva sua query SQL aqui:",
                key=f"q_{desafio['id']}",
                height=110,
                placeholder="SELECT ..."
            )

            col1, col2 = st.columns([1, 1])

            with col1:
                if st.button("Verificar", key=f"v_{desafio['id']}"):
                    q = query.strip()
                    if not q:
                        st.warning("Escreva uma query antes de verificar.")
                    else:
                        try:
                            df_u = pd.read_sql_query(q, conn)
                            df_g = pd.read_sql_query(desafio["gabarito"], conn)
                            if comparar(df_u, df_g, desafio["ordered"]):
                                st.success("Resposta correta!")
                                st.session_state["acertos"].add(desafio["id"])
                                st.balloons()
                            else:
                                st.error("Ainda não está certo. Revise sua query.")
                            st.markdown("**Resultado da sua query:**")
                            st.dataframe(df_u, use_container_width=True)
                        except Exception as e:
                            st.error(f"Erro ao executar sua query: {e}")

            with col2:
                if st.button("Ver dica", key=f"d_{desafio['id']}"):
                    st.info(desafio["dica"])

    st.divider()

# ─────────────────────────────────────────
# VISUALIZAÇÃO DAS TABELAS
# ─────────────────────────────────────────
st.subheader("Explorar tabelas do banco")
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    ["clientes", "pedidos", "produtos", "geolocalizacao", "itens_pedidos", "pagamentos", "avaliacoes"]
)

with tab1:
    st.dataframe(pd.read_sql_query("SELECT * FROM clientes", conn), use_container_width=True)
with tab2:
    st.dataframe(pd.read_sql_query("SELECT * FROM pedidos", conn), use_container_width=True)
with tab3:
    st.dataframe(pd.read_sql_query("SELECT * FROM produtos", conn), use_container_width=True)
with tab4:
    st.dataframe(pd.read_sql_query("SELECT * FROM geolocalizacao", conn), use_container_width=True)
with tab5:
    st.dataframe(pd.read_sql_query("SELECT * FROM itens_pedidos", conn), use_container_width=True)
with tab6:
    st.dataframe(pd.read_sql_query("SELECT * FROM pagamentos", conn), use_container_width=True)
with tab7:
    st.dataframe(pd.read_sql_query("SELECT * FROM avaliacoes", conn), use_container_width=True)
