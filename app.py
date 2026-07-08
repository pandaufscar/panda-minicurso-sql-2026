import streamlit as st
import sqlite3
import pandas as pd

# ─────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────
st.set_page_config(
    page_title="🐼 PANDA SQL – Minicurso 2026",
    page_icon="🐼",
    layout="wide"
)

# ─────────────────────────────────────────
# BANCO DE DADOS (criado automaticamente)
# ─────────────────────────────────────────
def criar_banco():
    conn = sqlite3.connect(":memory:")

    # Tabela: clientes
    conn.execute("""
        CREATE TABLE clientes (
            id_cliente TEXT,
            id_unico_cliente TEXT,
            cinco_digitos_cep_cliente TEXT,
            cidade_cliente TEXT,
            estado_cliente TEXT
        )
    """)
    conn.executemany("INSERT INTO clientes VALUES (?,?,?,?,?)", [
        ('c001','u001','01001','São Paulo','SP'),
        ('c002','u002','20001','Rio de Janeiro','RJ'),
        ('c003','u003','13001','Campinas','SP'),
        ('c004','u004','30001','Belo Horizonte','MG'),
        ('c005','u005','11001','Santos','SP'),
        ('c006','u006','80001','Curitiba','PR'),
        ('c007','u007','40001','Salvador','BA'),
        ('c008','u008','38401','Uberlândia','MG'),
        ('c009','u009','60001','Fortaleza','CE'),
        ('c010','u010','18001','Sorocaba','SP'),
        ('c011','u011','89001','Joinville','SC'),
        ('c012','u012','88001','Florianópolis','SC'),
        ('c013','u013','29001','Vitória','ES'),
        ('c014','u014','49001','Aracaju','SE'),
        ('c015','u015','57001','Maceió','AL'),
    ])

    # Tabela: pedidos
    conn.execute("""
        CREATE TABLE pedidos (
            id_pedido TEXT,
            id_cliente TEXT,
            status_pedido TEXT,
            data_hora_compra TEXT,
            pedido_aprovado TEXT,
            data_entrega_transportadora TEXT,
            data_entrega_cliente TEXT,
            data_estimada_entrega TEXT
        )
    """)
    conn.executemany("INSERT INTO pedidos VALUES (?,?,?,?,?,?,?,?)", [
        ('p001','c001','delivered','2017-01-05 10:30:00','2017-01-05 11:00:00','2017-01-07','2017-10-10','2018-01-15'),
        ('p002','c002','delivered','2017-03-10 14:20:00','2017-03-10 15:00:00','2017-03-12','2017-11-20','2018-03-20'),
        ('p003','c003','shipped', '2018-06-15 09:00:00','2018-06-15 09:30:00','2018-06-17',None,'2018-07-01'),
        ('p004','c004','delivered','2017-09-20 16:45:00','2017-09-20 17:00:00','2017-09-22','2018-02-28','2018-10-05'),
        ('p005','c005','canceled', '2018-01-01 12:00:00',None,None,None,'2018-01-15'),
        ('p006','c006','delivered','2017-11-25 08:15:00','2017-11-25 09:00:00','2017-11-27','2017-12-05','2017-12-10'),
        ('p007','c007','delivered','2018-08-30 20:00:00','2018-08-30 20:30:00','2018-09-01','2018-09-10','2018-09-15'),
        ('p008','c008','shipped', '2016-12-10 11:11:00','2016-12-10 12:00:00','2016-12-12',None,'2017-01-05'),
        ('p009','c009','delivered','2018-05-18 17:30:00','2018-05-18 18:00:00','2018-05-20','2018-05-28','2018-06-01'),
        ('p010','c010','delivered','2017-07-22 13:45:00','2017-07-22 14:00:00','2017-07-24','2017-07-30','2017-08-05'),
        ('p011','c011','delivered','2018-02-14 09:00:00','2018-02-14 09:30:00','2018-02-16','2018-02-22','2018-03-01'),
        ('p012','c012','delivered','2017-05-05 15:00:00','2017-05-05 15:30:00','2017-05-07','2017-05-13','2017-05-20'),
        ('p013','c013','canceled', '2018-11-20 10:00:00',None,None,None,'2018-12-01'),
        ('p014','c014','delivered','2017-08-08 12:00:00','2017-08-08 12:30:00','2017-08-10','2017-08-15','2017-08-20'),
        ('p015','c015','shipped', '2018-03-25 16:00:00','2018-03-25 16:30:00','2018-03-27',None,'2018-04-10'),
    ])

    # Tabela: produtos
    conn.execute("""
        CREATE TABLE produtos (
            id_produto TEXT,
            nome_categoria_produto TEXT,
            comprimento_nome_produto INTEGER,
            comprimento_descricao_produto INTEGER,
            quantidade_foto_produto INTEGER,
            peso_produto_g INTEGER,
            comprimento_produto_cm INTEGER,
            altura_produto_cm INTEGER,
            largura_produto_cm INTEGER
        )
    """)
    conn.executemany("INSERT INTO produtos VALUES (?,?,?,?,?,?,?,?,?)", [
        ('p001','cama_mesa_banho',18,120,3,500,30,10,20),
        ('p002','eletronicos',14,200,5,300,20,8,15),
        ('p003','cama_mesa_banho',15,80,2,200,25,5,18),
        ('p004','esporte_lazer',16,150,4,800,40,20,30),
        ('p005','eletronicos',17,300,8,100,15,3,10),
        ('p006','moveis_decoracao',19,500,12,5000,80,50,60),
        ('p007','cama_mesa_banho',20,90,3,600,35,12,25),
        ('p008','informatica',13,180,6,150,18,5,12),
        ('p009','esporte_lazer',21,200,7,1200,50,25,35),
        ('p010','informatica',16,250,9,200,22,6,14),
        ('p011','perfumaria',10,100,2,100,10,8,8),
        ('p012','perfumaria',12,110,3,120,12,9,9),
        ('p013','brinquedos',11,130,4,300,20,15,18),
        ('p014','brinquedos',13,140,5,400,25,18,20),
        ('p015','papelaria',9,60,1,50,15,1,10),
        ('p016','moveis_decoracao',22,600,15,8000,90,60,70),
        ('p017','esporte_lazer',18,170,6,900,45,22,32),
        ('p018','informatica',14,220,8,180,20,5,13),
        ('p019','cama_mesa_banho',16,95,2,550,32,11,22),
        ('p020','eletronicos',15,280,7,250,19,7,14),
    ])

    # Tabela: geolocalizacao
    conn.execute("""
        CREATE TABLE geolocalizacao (
            prefixo_codigo_postal TEXT,
            latitude_geolocalizacao REAL,
            geolocalizacao_longitude REAL,
            cidade_geolocalizacao TEXT,
            estado_geolocalizacao TEXT
        )
    """)
    conn.executemany("INSERT INTO geolocalizacao VALUES (?,?,?,?,?)", [
        ('01001',-23.5505,-46.6333,'sao paulo','SP'),
        ('20001',-22.9068,-43.1729,'rio de janeiro','RJ'),
        ('13001',-22.9056,-47.0608,'campinas','SP'),
        ('30001',-19.9167,-43.9345,'belo horizonte','MG'),
        ('11001',-23.9608,-46.3336,'santos','SP'),
        ('80001',-25.4284,-49.2733,'curitiba','PR'),
        ('40001',-12.9714,-38.5014,'salvador','BA'),
        ('38401',-18.9186,-48.2772,'uberlandia','MG'),
        ('60001',-3.7172,-38.5433,'fortaleza','CE'),
        ('18001',-23.5015,-47.4526,'sorocaba','SP'),
        ('89001',-26.3045,-48.8487,'joinville','SC'),
        ('88001',-27.5954,-48.5480,'florianopolis','SC'),
        ('29001',-20.3222,-40.3381,'vitoria','ES'),
        ('49001',-10.9472,-37.0731,'aracaju','SE'),
        ('57001',-9.6658,-35.7350,'maceio','AL'),
        ('69001',-3.1190,-60.0217,'manaus','AM'),
        ('66001',-1.4558,-48.5044,'belem','PA'),
        ('74001',-16.6864,-49.2643,'goiania','GO'),
        ('70001',-15.7797,-47.9297,'brasilia','DF'),
        ('64001',-5.0920,-42.8038,'teresina','PI'),
    ])

    conn.commit()
    return conn


# ─────────────────────────────────────────
# SESSÃO
# ─────────────────────────────────────────
if "conn" not in st.session_state:
    st.session_state["conn"] = criar_banco()
if "acertos" not in st.session_state:
    st.session_state["acertos"] = set()

conn = st.session_state["conn"]


# ─────────────────────────────────────────
# DESAFIOS
# ─────────────────────────────────────────
DESAFIOS = [
    {
        "id": 1,
        "semana": "📘 Semana 1 — Introdução e SELECT",
        "titulo": "Desafio 1 — Visualizar todos os clientes",
        "enunciado": "Use o `SELECT` para visualizar **todas as colunas** da tabela `clientes`.",
        "gabarito": "SELECT * FROM clientes",
        "dica": "Use `SELECT * FROM nome_da_tabela` — o `*` significa 'todas as colunas'.",
        "ordered": False
    },
    {
        "id": 2,
        "semana": "📘 Semana 1 — Introdução e SELECT",
        "titulo": "Desafio 2 — Colunas específicas",
        "enunciado": "Selecione apenas `id_cliente` e `estado_cliente` da tabela `clientes`.",
        "gabarito": "SELECT id_cliente, estado_cliente FROM clientes",
        "dica": "Liste as colunas separadas por vírgula: `SELECT col1, col2 FROM tabela`.",
        "ordered": False
    },
    {
        "id": 3,
        "semana": "📗 Semana 2 — Consultas Básicas e Filtragem",
        "titulo": "Desafio 3 — Filtrar clientes por estado (WHERE)",
        "enunciado": "Liste o `id_cliente` e `estado_cliente` de todos os clientes do estado **'SC'**.",
        "gabarito": "SELECT id_cliente, estado_cliente FROM clientes WHERE estado_cliente = 'SC'",
        "dica": "Use `WHERE estado_cliente = 'SC'` para filtrar.",
        "ordered": False
    },
    {
        "id": 4,
        "semana": "📗 Semana 2 — Consultas Básicas e Filtragem",
        "titulo": "Desafio 4 — Estados que começam com 'S' (LIKE)",
        "enunciado": "Liste `id_cliente` e `estado_cliente` dos clientes cujo estado começa com a letra **'S'**.",
        "gabarito": "SELECT id_cliente, estado_cliente FROM clientes WHERE estado_cliente LIKE 'S%'",
        "dica": "Use `LIKE 'S%'` — o `%` representa qualquer sequência de caracteres depois do 'S'.",
        "ordered": False
    },
    {
        "id": 5,
        "semana": "📗 Semana 2 — Consultas Básicas e Filtragem",
        "titulo": "Desafio 5 — Categorias específicas (IN)",
        "enunciado": "Selecione `id_produto` e `nome_categoria_produto` de produtos cuja categoria seja **'perfumaria'** ou **'brinquedos'**.",
        "gabarito": "SELECT id_produto, nome_categoria_produto FROM produtos WHERE nome_categoria_produto IN ('perfumaria', 'brinquedos')",
        "dica": "Use `IN ('valor1', 'valor2')` em vez de vários `OR`.",
        "ordered": False
    },
    {
        "id": 6,
        "semana": "📗 Semana 2 — Consultas Básicas e Filtragem",
        "titulo": "Desafio 6 — Pedidos entre duas datas (BETWEEN)",
        "enunciado": "Selecione `id_pedido` e `data_entrega_cliente` da tabela `pedidos`, onde a entrega esteja entre **'2017-10-04'** e **'2018-10-04'**, em ordem **crescente**.",
        "gabarito": "SELECT id_pedido, data_entrega_cliente FROM pedidos WHERE data_entrega_cliente BETWEEN '2017-10-04' AND '2018-10-04' ORDER BY data_entrega_cliente ASC",
        "dica": "Use `BETWEEN '2017-10-04' AND '2018-10-04'` e depois `ORDER BY data_entrega_cliente ASC`.",
        "ordered": True
    },
    {
        "id": 7,
        "semana": "📙 Semana 3 — Ordenação, Limites e Nulos",
        "titulo": "Desafio 7 — Ordenar por data de compra (ORDER BY ASC)",
        "enunciado": "Selecione `data_hora_compra` da tabela `pedidos` em **ordem crescente**.",
        "gabarito": "SELECT data_hora_compra FROM pedidos ORDER BY data_hora_compra ASC",
        "dica": "Use `ORDER BY data_hora_compra ASC` — do mais antigo para o mais recente.",
        "ordered": True
    },
    {
        "id": 8,
        "semana": "📙 Semana 3 — Ordenação, Limites e Nulos",
        "titulo": "Desafio 8 — Top 10 registros (LIMIT)",
        "enunciado": "Selecione `data_estimada_entrega` e `data_entrega_cliente` da tabela `pedidos`, ordenados por `data_estimada_entrega` de forma **crescente**, mostrando apenas **10 registros**.",
        "gabarito": "SELECT data_estimada_entrega, data_entrega_cliente FROM pedidos ORDER BY data_estimada_entrega ASC LIMIT 10",
        "dica": "Combine `ORDER BY data_estimada_entrega ASC` com `LIMIT 10` no final da query.",
        "ordered": True
    },
    {
        "id": 9,
        "semana": "📙 Semana 3 — Ordenação, Limites e Nulos",
        "titulo": "Desafio 9 — Encontrar valores nulos (IS NULL)",
        "enunciado": "Selecione **todos os registros** da tabela `clientes` onde `id_cliente`, `cidade_cliente` **ou** `estado_cliente` seja **nulo**.",
        "gabarito": "SELECT * FROM clientes WHERE id_cliente IS NULL OR cidade_cliente IS NULL OR estado_cliente IS NULL",
        "dica": "Use `IS NULL` para verificar campos sem valor. Combine com `OR` para checar várias colunas.",
        "ordered": False
    },
]


# ─────────────────────────────────────────
# COMPARAÇÃO DE RESULTADOS
# ─────────────────────────────────────────
def comparar(df_usuario, df_gabarito, ordered: bool) -> bool:
    try:
        df_u = df_usuario.copy()
        df_g = df_gabarito.copy()
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
# INTERFACE PRINCIPAL
# ─────────────────────────────────────────
st.title("🐼 PANDA SQL — Minicurso 2026")
st.caption("Plataforma interativa de desafios SQL · UFSCar · Grupo PANDA")

st.markdown("""
Bem-vindo ao minicurso de SQL do **PANDA UFSCar**!  
Resolva os desafios usando comandos SQL reais com base no dataset da **Olist**.

**Tabelas disponíveis:** `clientes` · `pedidos` · `produtos` · `geolocalizacao`
""")

st.divider()

total  = len(DESAFIOS)
acertos = len(st.session_state["acertos"])
st.progress(
    acertos / total if total > 0 else 0,
    text=f"Progresso: {acertos} / {total} desafios concluídos"
)

st.divider()

# agrupar por semana
semanas = {}
for d in DESAFIOS:
    semanas.setdefault(d["semana"], []).append(d)

for semana, desafios in semanas.items():
    st.subheader(semana)

    for desafio in desafios:
        icon = "✅" if desafio["id"] in st.session_state["acertos"] else "📌"

        with st.expander(f"{icon} {desafio['titulo']}", expanded=False):
            st.markdown(desafio["enunciado"])

            query = st.text_area(
                "✏️ Escreva sua query SQL aqui:",
                key=f"query_{desafio['id']}",
                height=110,
                placeholder="SELECT ..."
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("✔️ Verificar", key=f"verificar_{desafio['id']}"):
                    q = query.strip()
                    if not q:
                        st.warning("Escreva uma query antes de verificar.")
                    else:
                        try:
                            df_u = pd.read_sql_query(q, conn)
                            df_g = pd.read_sql_query(desafio["gabarito"], conn)

                            if comparar(df_u, df_g, desafio["ordered"]):
                                st.success("✅ Correto! Muito bem!")
                                st.session_state["acertos"].add(desafio["id"])
                                st.balloons()
                            else:
                                st.error("❌ Ainda não está certo. Revise a query.")
                                with st.expander("🔍 Ver resultado da sua query"):
                                    st.dataframe(df_u)
                        except Exception as e:
                            st.error(f"⚠️ Erro na query: {e}")

            with col2:
                if st.button("💡 Ver dica", key=f"dica_{desafio['id']}"):
                    st.info(f"💡 {desafio['dica']}")

    st.divider()

# ─────────────────────────────────────────
# TABELAS DO BANCO
# ─────────────────────────────────────────
st.subheader("📋 Explore as tabelas do banco")
st.caption("Use esses dados como referência para escrever suas queries:")

tab1, tab2, tab3, tab4 = st.tabs(["clientes", "pedidos", "produtos", "geolocalizacao"])

with tab1:
    st.dataframe(pd.read_sql_query("SELECT * FROM clientes", conn), use_container_width=True)
with tab2:
    st.dataframe(pd.read_sql_query("SELECT * FROM pedidos", conn), use_container_width=True)
with tab3:
    st.dataframe(pd.read_sql_query("SELECT * FROM produtos", conn), use_container_width=True)
with tab4:
    st.dataframe(pd.read_sql_query("SELECT * FROM geolocalizacao", conn), use_container_width=True)
