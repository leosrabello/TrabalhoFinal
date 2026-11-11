
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

import ui  # parte visual: CSS e acabamento dos gráficos
from ml.avaliacao import avaliar, prever                                       # Frente 3
from ml.dados import ALVO, COLUNAS_IGNORADAS, preparar_dados, separar_treino_teste  # Frente 1
from ml.modelos import criar_modelo, treinar                                   # Frente 2

st.set_page_config(page_title="Manutenção de Piscinas", page_icon="🏊", layout="wide")
st.markdown(ui.CSS, unsafe_allow_html=True)

CSV_EXEMPLO = Path(__file__).parent / "data" / "piscinas.csv"

# Nomes amigáveis dos campos da piscina. Colunas fora desta lista usam o próprio nome.
ROTULOS = {
    "volume_m3": "Volume (m³)",
    "tipo_piscina": "Tipo",
    "uso": "Uso",
    "banhistas_semana": "Banhistas por semana",
    "cidade": "Cidade",
    "bairro": "Bairro",
    "area_m2": "Área (m²)",
    "profundidade_media_m": "Profundidade média (m)",
    "tem_cobertura": "Tem cobertura",
    "exposicao_sol": "Exposição ao sol",
    "frequencia_manutencao": "Frequência de manutenção",
    "consumo_cloro_kg_mes": "Consumo de cloro (kg/mês)",
}
# Campos que aparecem logo de cara; os demais ficam em "Mais detalhes".
CAMPOS_PRINCIPAIS = ["volume_m3", "tipo_piscina", "uso", "banhistas_semana"]


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


def assinatura(df):
    """Uma "impressão digital" da base, para saber se ela mudou desde o treino."""
    return int(pd.util.hash_pandas_object(df, index=False).sum())


def fluxo_de_treino(df, nome, parametros):
    """Junta as Frentes 1-3: prepara a base, treina o modelo e mede no teste.

    Devolve tudo o que a tela precisa e que fica guardado no st.session_state.
    """
    X, y = preparar_dados(df)
    X_treino, X_teste, y_treino, y_teste = separar_treino_teste(X, y)
    modelo = treinar(criar_modelo(nome, parametros), X_treino, y_treino)
    return {
        "modelo": modelo,
        "metricas": avaliar(modelo, X_teste, y_teste),
        "config": (nome, parametros),
        "base": assinatura(df),
        "linhas": (len(X_treino), len(X_teste)),
        "real_previsto": pd.DataFrame({"Real": y_teste.to_numpy(), "Previsto": modelo.predict(X_teste)}),
    }


def descrever(config):
    """Texto curto do modelo, ex.: 'KNN (k = 5)'."""
    nome, parametros = config
    if "profundidade" in parametros:
        return f"{nome} (profundidade {parametros['profundidade']})"
    if "k" in parametros:
        return f"{nome} (k = {parametros['k']})"
    return nome


def moeda(valor):
    """Formata em reais: 1234.5 -> 'R$ 1.234,50'."""
    return "R$ " + f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def campo_piscina(coluna):
    """Cria o campo de entrada de uma coluna, começando no valor típico da base."""
    serie = df[coluna].dropna()
    if serie.empty:
        return None
    rotulo = ROTULOS.get(coluna, coluna)
    if pd.api.types.is_numeric_dtype(serie):
        minimo = 0 if serie.min() >= 0 else None
        if pd.api.types.is_integer_dtype(serie):
            return st.number_input(rotulo, min_value=minimo, value=int(serie.median()), step=1,
                                     key=f"campo_{coluna}")
        return st.number_input(rotulo, min_value=None if minimo is None else 0.0,
                                 value=round(float(serie.median()), 2), key=f"campo_{coluna}")
    opcoes = sorted(serie.astype(str).unique())
    return st.selectbox(rotulo, opcoes, index=opcoes.index(serie.astype(str).mode().iloc[0]),
                          key=f"campo_{coluna}")


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
    "4. **Predição**: escolha o modelo, re-treine e preveja o custo."
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

# ---- Aba 3: Predição (Frente 4: liga as Frentes 1-3 na tela) ---------------
# O modelo treinado fica em st.session_state["treino"]: o Streamlit roda o script
# inteiro a cada clique, e sem isso o modelo seria treinado de novo toda vez.
with aba_predicao:
    st.markdown(ui.titulo_secao("Prever o custo mensal", "gota",
                                "Escolha o modelo e os parâmetros, informe os dados da piscina e preveja."),
                unsafe_allow_html=True)

    cfg, inp, res = st.columns([1, 1, 0.9])
    with cfg, st.container(key="card_modelo"):
        st.markdown(ui.card_titulo("Modelo", 1), unsafe_allow_html=True)
        nome_modelo = st.selectbox("Classificador / preditor",
                                   ["Árvore de Decisão", "KNN", "Regressão Linear"])
        if nome_modelo == "Árvore de Decisão":
            parametros = {"profundidade": st.slider("Profundidade máxima", 1, 20, 5)}
        elif nome_modelo == "KNN":
            parametros = {"k": st.slider("Número de vizinhos (k)", 1, 30, 5)}
        else:
            parametros = {}
            st.caption("A Regressão Linear não tem parâmetros para ajustar aqui.")
        retreinar = st.button("Re-treinar modelo com a base atual", width="stretch")

        # Treina na primeira visita e sempre que o botão é clicado.
        if retreinar or "treino" not in st.session_state:
            try:
                st.session_state["treino"] = fluxo_de_treino(df, nome_modelo, parametros)
                if retreinar:
                    st.toast(f"Modelo re-treinado: {descrever((nome_modelo, parametros))}.")
            except Exception as erro:
                st.error(f"Não foi possível treinar: {erro}")

        treino = st.session_state.get("treino")
        if treino:
            if treino["config"] != (nome_modelo, parametros) or treino["base"] != assinatura(df):
                st.warning(f"Em uso: {descrever(treino['config'])}. A base ou a configuração mudou, "
                           "clique em Re-treinar para aplicar.")
            else:
                n_treino, n_teste = treino["linhas"]
                st.caption(f"Treinado com {n_treino} piscinas e testado com {n_teste}.")

    with inp, st.container(key="card_entrada"):
        st.markdown(ui.card_titulo("Dados da piscina", 2), unsafe_allow_html=True)
        features = [c for c in df.columns if c not in [ALVO, *COLUNAS_IGNORADAS]]
        principais = [c for c in CAMPOS_PRINCIPAIS if c in features]
        detalhes = [c for c in features if c not in principais]

        entrada = {c: campo_piscina(c) for c in principais}
        if detalhes:
            with st.expander("Mais detalhes"):
                st.caption("Já preenchidos com os valores mais comuns da base.")
                entrada.update({c: campo_piscina(c) for c in detalhes})
        entrada = {c: v for c, v in entrada.items() if v is not None}

    with res, st.container(key="card_resultado"):
        st.markdown(ui.card_titulo("Resultado", 3), unsafe_allow_html=True)
        clicou_prever = st.button("Prever custo", type="primary", width="stretch")
        if clicou_prever and treino:
            try:
                custo = prever(treino["modelo"], entrada)
                st.markdown(ui.resultado(moeda(custo), f"por mês · {descrever(treino['config'])}"),
                            unsafe_allow_html=True)
            except Exception as erro:
                st.error(f"Não foi possível prever: {erro}")
        elif clicou_prever:
            st.markdown(ui.resultado(nota="Treine um modelo antes de prever."), unsafe_allow_html=True)
        else:
            st.markdown(ui.resultado(nota="Preencha os dados e clique em Prever custo."), unsafe_allow_html=True)

    # Métricas do modelo em uso, medidas nas piscinas separadas para teste.
    if treino:
        st.write("")
        with st.container(key="card_metricas"):
            st.markdown(ui.card_titulo(f"Desempenho · {descrever(treino['config'])}"), unsafe_allow_html=True)
            st.caption("Medido nas piscinas separadas para teste, que o modelo não viu no treino.")
            metricas = treino["metricas"]
            m1, m2, m3 = st.columns(3)
            m1.metric("R²", f"{metricas['R²']:.3f}".replace(".", ","),
                      help="Quanto da variação do custo o modelo explica. 1 é perfeito; perto de 0 é ruim.")
            m2.metric("MAE", moeda(metricas["MAE"]),
                      help="Erro médio absoluto: em média, quanto a previsão erra para mais ou para menos.")
            m3.metric("RMSE", moeda(metricas["RMSE"]),
                      help="Raiz do erro quadrático médio: parecido com o MAE, mas pesa mais os erros grandes.")

            with st.expander("Real × previsto no teste"):
                pontos = treino["real_previsto"]
                fig4 = px.scatter(pontos, x="Real", y="Previsto", color_discrete_sequence=[ui.AZUL])
                lo, hi = pontos.min().min(), pontos.max().max()
                fig4.add_shape(type="line", x0=lo, y0=lo, x1=hi, y1=hi,
                               line=dict(color=ui.AZUL_CLARO, dash="dash", width=1.5))
                fig4.update_traces(marker=dict(size=8, opacity=0.8))
                ui.estilo_grafico(fig4)
                fig4.update_xaxes(title="Custo real (R$)")
                fig4.update_yaxes(title="Custo previsto (R$)")
                st.plotly_chart(fig4, width="stretch")
                st.caption("Quanto mais perto da linha tracejada, melhor a previsão.")

st.write("")
st.markdown(ui.onda(cor=ui.LINHA), unsafe_allow_html=True)
st.markdown('<div class="rodape">Dados de exemplo gerados por gerar_dados.py</div>',
            unsafe_allow_html=True)
