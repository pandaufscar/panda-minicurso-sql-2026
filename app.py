import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="🐼 PANDA SQL – Minicurso 2026",
    page_icon="🐼",
    layout="wide"
)

# ─────────────────────────────────────────
# BANCO DE DADOS
# ─────────────────────────────────────────
def criar_banco():
    conn = sqlite3.connect(":memory:")

    conn.execute("""CREATE TABLE clientes (
        id_cliente TEXT, id_unico_cliente TEXT,
        cinco_digitos_cep_cliente TEXT, cidade_cliente TEXT, estado_cliente TEXT
    )""")
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

    conn.execute("""CREATE TABLE pedidos (
        id_pedido TEXT, id_cliente TEXT, status_pedido TEXT,
        data_hora_compra TEXT, pedido_aprovado TEXT,
        data_entrega_transportadora TEXT, data_entrega_cliente TEXT,
        data_estimada_entrega TEXT
    )""")
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

    conn.execute("""CREATE TABLE produtos (
        id_produto TEXT, nome_categoria_produto TEXT,
        comprimento_nome_produto INTEGER, comprimento_descricao_produto INTEGER,
        quantidade_foto_produto INTEGER, peso_produto_g INTEGER,
        comprimento_produto_cm INTEGER, altura_produto_cm INTEGER,
        largura_produto_cm INTEGER
    )""")
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

    conn.execute("""CREATE TABLE geolocalizacao (
        prefixo_codigo_postal TEXT, latitude_geolocalizacao REAL,
        geolocalizacao_longitude REAL, cidade_geolocalizacao TEXT,
        estado_geolocalizacao TEXT
    )""")
    conn.executemany("INSERT INTO geolocalizacao VALUES (?,?,?,?,?)", [
        ('01001',-23.5505,-46.6333,'sao paulo','SP'),
        ('20001',-22.9068,-43.1729,'rio de janeiro','RJ'),
        ('13001',-22.9056,-47.0608,'campinas','SP'),

