import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="🐼 Plataforma SQL – Grupo de Estudos",
    page_icon="🐼",
    layout="wide"
)

# =========================================================
# BANCO DE DADOS EM MEMÓRIA
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
        ("c005", "salvador", "BA"),
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
        ("p001", "c001", "delivered",   "2017-01-05 10:30:00", "2018-01-15", "2018-01-10"),
        ("p002", "c002", "delivered",   "2017-03-10 14:20:00", "2018-03-20", "2018-03-25"),
        ("p003", "c003", "shipped",     "2018-06-15 09:00:00", None,         "2018-07-01"),
        ("p004", "c004", "delivered",   "2018-09-20 16:45:00", "2018-10-05", "2018-09-30"),
        ("p005", "c005", "canceled",    "2018-01-01 12:00:00", None,         "2018-01-15"),
        ("p006", "c001", "unavailable", "2018-03-01 08:00:00", None,         "2018-03-10"),
        ("p007", "c002", "shipped",     "2018-02-10 11:11:00", None,         "2018-02-15"),
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
        ("pr002", "informatica_acessorios", 4, 600),
        ("pr003", "eletronicos",            5, 300),
        ("pr004", "cama_mesa_banho",        2, 500),
        ("pr005", "brinquedos",             4, 250),
        ("pr006", "perfumaria",             2, 100),
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
    ])

    # ---------- Tabelas Olist (Semana WHERE) ----------
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
        ("p003", "credit_card", 12, 80.0),
        ("p004", "voucher",     1, 150.0),
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

    # Views para olist_customers_dataset / olist_orders_dataset / olist_products_dataset
    conn.execute("""
        CREATE VIEW olist_customers_dataset AS
        SELECT
            id_cliente      AS customer_id,
            cidade_cliente  AS customer_city,
            estado_cliente  AS customer_state
        FROM clientes
    """)
    conn.execute("""
        CREATE VIEW olist_orders_dataset AS
        SELECT
            id_pedido              AS order_id,
            id_cliente             AS customer_id,
            status_pedido          AS order_status,
            data_hora_compra       AS order_purchase_timestamp,
            data_entrega_cliente   AS order_delivered_customer_date,
            data_estimada_entrega  AS order_estimated_delivery_date
        FROM pedidos
    """)
    conn.execute("""
        CREATE VIEW olist_products_dataset AS
        SELECT
            id_produto             AS product_id,
            categoria_produto      AS product_category_name,
            peso_produto_g         AS product_weight_g
        FROM produtos
    """)

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
# DESAFIOS (PDFs)
# =========================================================
DESAFIOS = [
    # ----------------- SEMANA 1 – SELECT -----------------
    {
        "secao": "Semana 1 – SELECT",
        "titulo": "Exercício 1 – SELECT * FROM clientes",
        "enunciado": "Exiba todas as informações da tabela `clientes`.",
        "gabarito": "SELECT * FROM clientes",
        "explicacao": (
            "O comando `SELECT *` retorna todas as colunas da tabela.\n"
            "Aqui, todas as colunas e todas as linhas da tabela `clientes` serão exibidas."
        ),
        "dica": "Copie exatamente: `SELECT * FROM clientes;`",
        "ordered": False,
    },
    {
        "secao": "Semana 1 – SELECT",
        "titulo": "Exercício 2 – id_cliente e cidade_cliente",
        "enunciado": "Exiba o identificador do cliente e a cidade onde ele mora.",
        "gabarito": "SELECT id_cliente, cidade_cliente FROM clientes",
        "explicacao": (
            "Em vez de usar `*`, você lista apenas as colunas desejadas após o `SELECT`.\n"
            "A consulta retorna só `id_cliente` e `cidade_cliente`."
        ),
        "dica": "Use: `SELECT id_cliente, cidade_cliente FROM clientes;`",
        "ordered": False,
    },
    {
        "secao": "Semana 1 – SELECT",
        "titulo": "Exercício 3 – dados de pedidos",
        "enunciado": "Exiba `id_pedido`, `status_pedido` e `data_hora_compra`.",
        "gabarito": "SELECT id_pedido, status_pedido, data_hora_compra FROM pedidos",
        "explicacao": "Mesma ideia: escolha as colunas específicas da tabela `pedidos`.",
        "dica": "Observe a ordem das colunas no PDF.",
        "ordered": False,
    },
    {
        "secao": "Semana 1 – SELECT",
        "titulo": "Exercício 4 – dados de produtos",
        "enunciado": "Liste `id_produto`, `categoria_produto` e `peso_produto_g`.",
        "gabarito": "SELECT id_produto, categoria_produto, peso_produto_g FROM produtos",
        "explicacao": "Você está selecionando três colunas da tabela `produtos`.",
        "dica": "As colunas devem estar na mesma ordem do enunciado.",
        "ordered": False,
    },

    # ----------------- SEMANA 1 – FROM -------------------
    {
        "secao": "Semana 1 – FROM",
        "titulo": "Exercício 1 – SELECT * FROM geolocalizacao",
        "enunciado": "Exiba todas as informações da tabela `geolocalizacao`.",
        "gabarito": "SELECT * FROM geolocalizacao",
        "explicacao": (
            "`FROM` indica de qual tabela os dados vêm.\n"
            "Aqui você está pegando todas as colunas da tabela `geolocalizacao`."
        ),
        "dica": "Use exatamente `FROM geolocalizacao`.",
        "ordered": False,
    },
    {
        "secao": "Semana 1 – FROM",
        "titulo": "Exercício 2 – cidade e estado",
        "enunciado": "Liste `cidade_geolocalizacao` e `estado_geolocalizacao`.",
        "gabarito": "SELECT cidade_geolocalizacao, estado_geolocalizacao FROM geolocalizacao",
        "explicacao": "Você seleciona colunas específicas, mas a origem continua sendo `geolocalizacao`.",
        "dica": "SELECT colunas … FROM geolocalizacao.",
        "ordered": False,
    },
    {
        "secao": "Semana 1 – FROM",
        "titulo": "Exercício 3 – clientes (FROM)",
        "enunciado": "Exiba `id_cliente` e `cidade_cliente` usando a tabela `clientes`.",
        "gabarito": "SELECT id_cliente, cidade_cliente FROM clientes",
        "explicacao": "Reforço da ideia de FROM aplicando em outra tabela.",
        "dica": "É muito parecido com o exercício 2 do SELECT.",
        "ordered": False,
    },
    {
        "secao": "Semana 1 – FROM",
        "titulo": "Exercício 4 – pedidos (FROM)",
        "enunciado": "Liste `id_pedido` e `status_pedido` da tabela `pedidos`.",
        "gabarito": "SELECT id_pedido, status_pedido FROM pedidos",
        "explicacao": "Novamente: selecione colunas e use `FROM pedidos`.",
        "dica": "Não esqueça o `FROM pedidos`.",
        "ordered": False,
    },

    # ----------------- SEMANA 1 – AS ---------------------
    {
        "secao": "Semana 1 – AS",
        "titulo": "Exercício 1 – alias em clientes",
        "enunciado": (
            "Exiba `id_cliente` e `cidade_cliente`, renomeando para "
            "`\"Código do Cliente\"` e `\"Cidade\"`."
        ),
        "gabarito": 'SELECT id_cliente AS "Código do Cliente", cidade_cliente AS "Cidade" FROM clientes',
        "explicacao": (
            "`AS` cria um apelido (alias) para a coluna apenas no resultado.\n"
            "A coluna continua se chamando `id_cliente` na tabela, mas aparece como `Código do Cliente`."
        ),
        "dica": "Use exatamente as aspas duplas ao redor dos nomes.",
        "ordered": False,
    },
    {
        "secao": "Semana 1 – AS",
        "titulo": "Exercício 2 – alias em pedidos",
        "enunciado": "Renomeie `id_pedido` para `\"Pedido\"` e `status_pedido` para `\"Status\"`.",
        "gabarito": 'SELECT id_pedido AS "Pedido", status_pedido AS "Status" FROM pedidos',
        "explicacao": "Mesma ideia de alias, agora na tabela `pedidos`.",
        "dica": "Não esqueça o `AS` entre o nome original e o alias.",
        "ordered": False,
    },
    {
        "secao": "Semana 1 – AS",
        "titulo": "Exercício 3 – alias em produtos",
        "enunciado": (
            "Exiba `categoria_produto` e `quantidade_fotos_produto`, renomeando para "
            "`\"Categoria\"` e `\"Quantidade de Fotos\"`."
        ),
        "gabarito": 'SELECT categoria_produto AS "Categoria", quantidade_fotos_produto AS "Quantidade de Fotos" FROM produtos',
        "explicacao": "Você está deixando o resultado mais legível sem mudar a tabela de verdade.",
        "dica": "Os nomes entre aspas devem bater com o PDF.",
        "ordered": False,
    },
    {
        "secao": "Semana 1 – AS",
        "titulo": "Exercício 4 – alias em geolocalizacao",
        "enunciado": (
            "Liste `cidade_geolocalizacao` e `estado_geolocalizacao`, renomeando para "
            "`\"Cidade\"` e `\"UF\"`."
        ),
        "gabarito": 'SELECT cidade_geolocalizacao AS "Cidade", estado_geolocalizacao AS "UF" FROM geolocalizacao',
        "explicacao": "Alias também pode ser aplicado a campos de outras tabelas, como `geolocalizacao`.",
        "dica": "Aplica o mesmo padrão dos exercícios anteriores.",
        "ordered": False,
    },

    # ------------- WHERE / OPERADORES / AND/OR/NOT -------------
    # Bloco 1 — WHERE
    {
        "secao": "WHERE",
        "titulo": "WHERE 1 – pedidos delivered",
        "enunciado": "Liste todos os pedidos com status `'delivered'`.",
        "gabarito": "SELECT * FROM olist_orders_dataset WHERE order_status = 'delivered'",
        "explicacao": (
            "`WHERE` filtra linhas.\n"
            "Aqui, só ficam as linhas onde `order_status = 'delivered'` é verdadeiro."
        ),
        "dica": "Use exatamente `order_status = 'delivered'`.",
        "ordered": False,
    },
    {
        "secao": "WHERE",
        "titulo": "WHERE 2 – pedidos canceled",
        "enunciado": "Liste todos os pedidos com status `'canceled'`.",
        "gabarito": "SELECT * FROM olist_orders_dataset WHERE order_status = 'canceled'",
        "explicacao": "Mesmo filtro do anterior, mudando o valor do status.",
        "dica": "Cuidado com aspas simples ao redor de `canceled`.",
        "ordered": False,
    },
    {
        "secao": "WHERE",
        "titulo": "WHERE 3 – clientes de sao paulo",
        "enunciado": "Liste `customer_id`, `customer_city`, `customer_state` de quem mora em `'sao paulo'`.",
        "gabarito": "SELECT customer_id, customer_city, customer_state FROM olist_customers_dataset WHERE customer_city = 'sao paulo'",
        "explicacao": (
            "Os dados de cidade no Olist estão em minúsculas e sem acento.\n"
            "Por isso usamos `'sao paulo'`."
        ),
        "dica": "Não use `São Paulo` com acento.",
        "ordered": False,
    },
    {
        "secao": "WHERE",
        "titulo": "WHERE 4 – produtos informatica_acessorios",
        "enunciado": "Liste `product_id` e `product_category_name` de produtos `informatica_acessorios`.",
        "gabarito": "SELECT product_id, product_category_name FROM olist_products_dataset WHERE product_category_name = 'informatica_acessorios'",
        "explicacao": "Segue exatamente o exemplo do PDF.",
        "dica": "A categoria é `informatica_acessorios` (sem acento).",
        "ordered": False,
    },

    # Bloco 2 — Operadores de comparação
    {
        "secao": "Operadores",
        "titulo": "Operador 1 – price > 100",
        "enunciado": "Liste itens de pedido com `price` maior que 100.",
        "gabarito": "SELECT * FROM olist_order_items_dataset WHERE price > 100",
        "explicacao": (
            "O operador `>` compara valores numéricos.\n"
            "Só aparecem linhas com `price` maior que 100."
        ),
        "dica": "Não use `>=`, é só `>`.",
        "ordered": False,
    },
    {
        "secao": "Operadores",
        "titulo": "Operador 2 – parcelas >= 10",
        "enunciado": "Liste pagamentos com `payment_installments >= 10`.",
        "gabarito": "SELECT * FROM olist_order_payments_dataset WHERE payment_installments >= 10",
        "explicacao": "`>=` significa maior ou igual.",
        "dica": "Compare exatamente com 10.",
        "ordered": False,
    },
    {
        "secao": "Operadores",
        "titulo": "Operador 3 – review_score < 3",
        "enunciado": "Liste avaliações com `review_score` menor que 3.",
        "gabarito": "SELECT * FROM olist_order_reviews_dataset WHERE review_score < 3",
        "explicacao": "`<` retorna apenas notas menores que 3 (1 e 2).",
        "dica": "Esse filtro ignora notas 3, 4 e 5.",
        "ordered": False,
    },
    {
        "secao": "Operadores",
        "titulo": "Operador 4 – freight_value <> 0",
        "enunciado": "Liste itens em que `freight_value` é diferente de 0 (houve frete).",
        "gabarito": "SELECT * FROM olist_order_items_dataset WHERE freight_value <> 0",
        "explicacao": "`<>` é o operador 'diferente de'.",
        "dica": "Equivalente a `!=` em algumas linguagens.",
        "ordered": False,
    },

    # Bloco 3 — AND / OR / NOT
    {
        "secao": "AND / OR / NOT",
        "titulo": "Lógico 1 – delivered atrasados (AND)",
        "enunciado": (
            "Liste pedidos com status `'delivered'` e que foram entregues **depois** "
            "da data estimada de entrega."
        ),
        "gabarito": "SELECT * FROM olist_orders_dataset WHERE order_status = 'delivered' AND order_delivered_customer_date > order_estimated_delivery_date",
        "explicacao": (
            "`AND` exige que as duas condições sejam verdadeiras ao mesmo tempo:\n"
            "- status delivered\n"
            "- data de entrega maior que a data estimada."
        ),
        "dica": "Use exatamente a comparação `>` entre as datas.",
        "ordered": False,
    },
    {
        "secao": "AND / OR / NOT",
        "titulo": "Lógico 2 – canceled OU unavailable (OR)",
        "enunciado": "Liste pedidos com status `'canceled'` ou `'unavailable'`.",
        "gabarito": "SELECT * FROM olist_orders_dataset WHERE order_status = 'canceled' OR order_status = 'unavailable'",
        "explicacao": "`OR` retorna linhas que atendem a pelo menos uma das condições.",
        "dica": "Não esqueça de repetir `order_status` nas duas comparações.",
        "ordered": False,
    },
    {
        "secao": "AND / OR / NOT",
        "titulo": "Lógico 3 – pagamentos NÃO credit_card (NOT)",
        "enunciado": "Liste pagamentos cujo `payment_type` não seja `'credit_card'`.",
        "gabarito": "SELECT * FROM olist_order_payments_dataset WHERE NOT payment_type = 'credit_card'",
        "explicacao": "`NOT` inverte a condição: traz tudo que NÃO é cartão de crédito.",
        "dica": "Também poderia usar `payment_type <> 'credit_card'`.",
        "ordered": False,
    },
    {
        "secao": "AND / OR / NOT",
        "titulo": "Lógico 4 – delivered/shipped desde 2018",
        "enunciado": (
            "Liste pedidos com status `'delivered'` ou `'shipped'`, "
            "e que tenham sido comprados a partir de `2018-01-01`."
        ),
        "gabarito": "SELECT * FROM olist_orders_dataset WHERE (order_status = 'delivered' OR order_status = 'shipped') AND order_purchase_timestamp >= '2018-01-01'",
        "explicacao": (
            "Os parênteses garantem que o `OR` seja avaliado antes do `AND`.\n"
            "Primeiro escolhemos delivered/shipped, depois filtramos pela data."
        ),
        "dica": "Não esqueça dos parênteses ao redor do `OR`.",
        "ordered": False,
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
    st.markdown("## 🐼 Grupo de Estudos SQL")
    st.caption("Plataforma baseada nos exercícios dos PDFs")

    total = len(DESAFIOS)
    acertos = len(st.session_state["acertos"])
    st.metric("Acertos", acertos)
    st.metric("Total", total)
    st.progress(acertos / total if total > 0 else 0)

    st.divider()
    secao_filtro = st.selectbox(
        "Filtrar por bloco",
        ["Todos"] + sorted({d["secao"] for d in DESAFIOS})
    )

    st.divider()
    st.markdown("### Tabelas principais")
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
Todos os exercícios e respostas foram retirados dos PDFs do grupo:

- **Semana 1** – SELECT, FROM, AS  
- **WHERE / Operadores / AND / OR / NOT**  

Para cada exercício:
1. Leia o enunciado  
2. Escreva sua query  
3. Clique em **Verificar**  
4. Use **Dica** ou veja a **Resposta correta** se precisar
""")
st.divider()

if secao_filtro == "Todos":
    desafios_visiveis = DESAFIOS
else:
    desafios_visiveis = [d for d in DESAFIOS if d["secao"] == secao_filtro]

for desafio in desafios_visiveis:
    concluido = desafio["titulo"] in st.session_state["acertos"]
    icon = "✅" if concluido else "📌"

    with st.expander(f"{icon} {desafio['titulo']} — {desafio['secao']}", expanded=False):
        st.markdown(f"**Enunciado:**\n\n{desafio['enunciado']}")

        st.markdown("**Explicação (do PDF):**")
        st.info(desafio["explicacao"])

        query = st.text_area(
            "Sua query SQL:",
            key=f"q_{desafio['titulo']}",
            height=110,
            placeholder="SELECT ..."
        )

        col1, col2, col3 = st.columns([1, 1, 2])

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
                            st.error("Ainda não está igual à resposta esperada.")
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

st.divider()

# =========================================================
# VISUALIZAR TABELAS
# =========================================================
st.subheader("Ver dados das tabelas")

tabs = st.tabs([
    "clientes",
    "pedidos",
    "produtos",
    "geolocalizacao",
    "olist_orders",
    "olist_customers",
    "itens / pagamentos / reviews",
    "olist_products"
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
