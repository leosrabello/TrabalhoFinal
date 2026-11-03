
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

import ui  # parte visual: CSS e acabamento dos gráficos

st.set_page_config(page_title="Manutenção de Piscinas", page_icon="🏊", layout="wide")
st.markdown(ui.CSS, unsafe_allow_html=True)

CSV_EXEMPLO = Path(__file__).parent / "data" / "piscinas.csv"


def ler_arquivo(arquivo):
    """Lê o arquivo enviado conforme a extensão e devolve um DataFrame."""
    nome = arquivo.name.lower()
    if nome.endswith(".csv"):
        return pd.read_csv(arquivo)
    if nome.endswith(".json"):
        return pd.read_json(arquivo)
    if nome.endswith(".xml"):
        return pd.read_xml(arquivo)
    raise ValueError("Formato não suportado. Use .csv, .xml ou .json.")


# ---- Barra lateral: upload (ou arquivo de exemplo) ------------------------
st.sidebar.markdown(ui.marca(), unsafe_allow_html=True)
st.sidebar.subheader("Dados")
enviado = st.sidebar.file_uploader("Arquivo (.csv, .xml ou .json)", type=["csv", "xml", "json"])

if enviado is not None:
    try:
        df = ler_arquivo(enviado)
        st.sidebar.success(f"{len(df)} linhas carregadas.")
    except Exception as erro:
        st.sidebar.error(f"Não foi possível ler: {erro}")
        st.stop()
    origem = f"arquivo {enviado.name}"
else:
    df = pd.read_csv(CSV_EXEMPLO)
    st.sidebar.caption("Usando o arquivo de exemplo (piscinas.csv).")
    origem = "base de exemplo"

st.sidebar.divider()
st.sidebar.markdown(
    "**Como usar**\n\n"
    "1. Envie uma base ou use o exemplo.\n"
    "2. **Dados**: prévia e resumo estatístico.\n"
    "3. **Visualizações**: barras, pizza e mapa.\n"
    "4. **Predição**: escolha o modelo e preveja o custo."
)

# ---- Cabeçalho ------------------------------------------------------------
resumo = [(len(df), "piscinas")]
if "cidade" in df.columns:
    resumo.append((df["cidade"].nunique(), "cidades"))
resumo.append(("", origem))

with st.container(key="hero"):
    st.markdown(ui.hero(resumo), unsafe_allow_html=True)

aba_dados, aba_graficos, aba_predicao = st.tabs(["Dados", "Visualizações", "Predição"])

# ---- Aba 1: Dados ---------------------------------------------------------
with aba_dados:
    st.markdown(ui.titulo_secao("Prévia dos dados", "dados", "As primeiras linhas da base e os números principais."),
                unsafe_allow_html=True)

    with st.container(key="numeros"):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Piscinas", len(df))
        c2.metric("Colunas", df.shape[1])
        if "volume_m3" in df.columns:
            c3.metric("Volume médio", f"{df['volume_m3'].mean():.0f} m³")
        if "custo_manutencao_mensal" in df.columns:
            c4.metric("Custo médio por mês", f"R$ {df['custo_manutencao_mensal'].mean():.0f}")

    st.dataframe(df, width="stretch", height=340)
    with st.expander("Resumo estatístico"):
        st.dataframe(df.describe(), width="stretch")

# ---- Aba 2: Visualizações -------------------------------------------------
with aba_graficos:
    st.markdown(ui.titulo_secao("Gráficos", "grafico", "Escolha as colunas e compare as categorias."),
                unsafe_allow_html=True)

    txt = [c for c in df.columns if pd.api.types.is_string_dtype(df[c])]
    num = df.select_dtypes(include="number").columns.tolist()
    ca, cb = st.columns(2)

    with ca, st.container(key="card_barras"):
        st.markdown(ui.card_titulo("Média por categoria"), unsafe_allow_html=True)
        if txt and num:
            f1, f2 = st.columns(2)
            cat = f1.selectbox("Categoria", txt, key="bar_cat")
            padrao = num.index("custo_manutencao_mensal") if "custo_manutencao_mensal" in num else 0
            val = f2.selectbox("Valor (média)", num, index=padrao, key="bar_val")
            media = df.groupby(cat)[val].mean().sort_values().reset_index()
            fig = px.bar(media, x=val, y=cat, orientation="h", text_auto=".3s",
                         color_discrete_sequence=[ui.AZUL])
            fig.update_traces(marker_cornerradius=6, textposition="outside", cliponaxis=False)
            ui.estilo_grafico(fig)
            fig.update_layout(bargap=0.35)
            fig.update_xaxes(showticklabels=False, showgrid=False, title=None,
                             range=[0, media[val].max() * 1.15])  # espaço para o número no fim da barra
            fig.update_yaxes(title=None)
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("Precisa de colunas de texto e numéricas.")

    with cb, st.container(key="card_pizza"):
        st.markdown(ui.card_titulo("Proporção por categoria"), unsafe_allow_html=True)
        if txt:
            cat_p = st.selectbox("Categoria", txt, key="pie_cat")
            cont = df[cat_p].value_counts().reset_index()
            cont.columns = [cat_p, "quantidade"]
            fig2 = px.pie(cont, names=cat_p, values="quantidade", hole=0.6,
                          color_discrete_sequence=ui.CORES_GRAFICO)
            fig2.update_traces(textinfo="percent", textfont_color="#ffffff",
                               marker_line_color="#ffffff", marker_line_width=2)
            ui.estilo_grafico(fig2)
            st.plotly_chart(fig2, width="stretch")
        else:
            st.info("Precisa de colunas de texto.")

    st.write("")
    with st.container(key="card_mapa"):
        st.markdown(ui.card_titulo("Localização das piscinas"), unsafe_allow_html=True)
        if {"latitude", "longitude"}.issubset(df.columns):
            cor = "cidade" if "cidade" in df.columns else None
            try:
                fig3 = px.scatter_map(
                    df, lat="latitude", lon="longitude", color=cor,
                    zoom=9.6, color_discrete_sequence=ui.CORES_MAPA,
                )
                fig3.update_traces(marker=dict(size=9, opacity=0.85))
                ui.estilo_grafico(fig3, altura=440)
                fig3.update_layout(map_style="carto-positron", margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig3, width="stretch")
            except Exception:
                st.map(df[["latitude", "longitude"]])
        else:
            st.info("Para o mapa, o arquivo precisa de 'latitude' e 'longitude'.")

# ---- Aba 3: Predição (interface; o modelo entra na Frente 3) --------------
with aba_predicao:
    st.markdown(ui.titulo_secao("Prever o custo mensal", "gota",
                                "Escolha o modelo e os parâmetros, informe os dados da piscina e preveja."),
                unsafe_allow_html=True)

    cfg, inp, res = st.columns([1, 1, 0.9])
    with cfg, st.container(key="card_modelo"):
        st.markdown(ui.card_titulo("Modelo", 1), unsafe_allow_html=True)
        modelo = st.selectbox("Classificador / preditor",
                              ["Árvore de Decisão", "KNN", "Regressão Linear"])
        if modelo == "Árvore de Decisão":
            st.slider("Profundidade máxima", 1, 20, 5)
        elif modelo == "KNN":
            st.slider("Número de vizinhos (k)", 1, 30, 5)
        else:
            st.caption("A Regressão Linear não tem parâmetros para ajustar aqui.")
        st.button("Re-treinar modelo com a base atual", width="stretch")

    with inp, st.container(key="card_entrada"):
        st.markdown(ui.card_titulo("Dados da piscina", 2), unsafe_allow_html=True)
        if "volume_m3" in df.columns:
            st.number_input("Volume (m³)", 1.0, 500.0, 40.0)
        if "tipo_piscina" in df.columns:
            st.selectbox("Tipo", sorted(df["tipo_piscina"].dropna().unique()))
        if "uso" in df.columns:
            st.selectbox("Uso", sorted(df["uso"].dropna().unique()))
        if "banhistas_semana" in df.columns:
            st.number_input("Banhistas por semana", 0, 500, 20)

    with res, st.container(key="card_resultado"):
        st.markdown(ui.card_titulo("Resultado", 3), unsafe_allow_html=True)
        prever = st.button("Prever custo", type="primary", width="stretch")
        if prever:
            st.markdown(ui.resultado(), unsafe_allow_html=True)
        else:
            st.markdown(ui.resultado(nota="Preencha os dados e clique em Prever custo."), unsafe_allow_html=True)

st.write("")
st.markdown(ui.onda(cor=ui.LINHA), unsafe_allow_html=True)
st.markdown('<div class="rodape">Dados de exemplo gerados por gerar_dados.py</div>',
            unsafe_allow_html=True)
