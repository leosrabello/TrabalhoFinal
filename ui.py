"""Elementos visuais. São puramente decorativos.

São alguns ícones em SVG desenhados à mão e um bloco de CSS. Nada muda o
funcionamento do app — é só a aparência.

A ideia do visual vem da própria piscina: as cores da água e dos azulejos, a
faixa de pastilhas na linha d'água e os números grandes e condensados das
marcações de profundidade da borda.
"""

# Paleta
AZUL = "#0a7ea4"         # água
AZUL_FUNDO = "#075a76"   # água funda
AZUL_CLARO = "#5fb7d4"   # reflexo
TINTA = "#0f2a37"        # texto
CINZA = "#5b6f7a"        # texto secundário
LINHA = "#e3e9ec"        # rejunte
FUNDO_HERO = "#ecf6f9"   # azulejo claro
CONDENSADA = '"Barlow Condensed", sans-serif'

# CSS do app. Os blocos com estilo próprio são st.container(key="..."): o
# Streamlit dá a cada um a classe st-key-..., e é por ela que o CSS os encontra.
CSS = f"""
<style>
  .block-container {{ padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1120px; }}
  header[data-testid="stHeader"] {{ background: transparent; }}
  .modebar-container {{ display: none; }}  /* esconde a barra de ferramentas dos gráficos */

  /* cabeçalho */
  .st-key-hero {{
    position: relative; background: {FUNDO_HERO}; border-radius: 8px; overflow: hidden;
    padding: 26px 34px 30px; margin-bottom: .8rem;
  }}
  .hero h1 {{
    font-family: {CONDENSADA}; font-weight: 600; font-size: 3.1rem; line-height: 1;
    letter-spacing: -.01em; margin: 0 0 .7rem 0; padding: 0; color: {TINTA};
  }}
  .hero p {{ margin: 0 0 1.3rem 0; color: {CINZA}; font-size: 1.08rem; line-height: 1.5; max-width: 30rem; }}
  .resumo {{ display: flex; flex-wrap: wrap; gap: 0; color: {CINZA}; font-size: .95rem; }}
  .resumo span {{ padding: 0 .9rem; border-left: 1px solid #c9dfe6; }}
  .resumo span:first-child {{ padding-left: 0; border-left: 0; }}
  .resumo b {{ font-family: {CONDENSADA}; font-weight: 600; font-size: 1.2rem; color: {TINTA}; margin-right: .2rem; }}

  /* faixa de pastilhas da linha d'água, no pé do cabeçalho */
  .st-key-hero::after {{
    content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 12px;
    background: repeating-linear-gradient(90deg,
      {AZUL} 0 12px, #ffffff 12px 14px, {AZUL_CLARO} 14px 26px, #ffffff 26px 28px);
  }}

  /* abas: texto simples, sublinhado na cor da água */
  .stTabs [data-baseweb="tab-list"] {{ gap: 1.8rem; }}
  .stTabs [data-baseweb="tab"] {{ padding: 0 0 .5rem 0; }}
  .stTabs [data-baseweb="tab"] p {{ font-size: 1.05rem; font-weight: 500; color: {CINZA}; }}
  .stTabs [aria-selected="true"] p {{ color: {TINTA}; font-weight: 600; }}
  .stTabs [data-baseweb="tab-highlight"] {{ background: {AZUL}; height: 2px; }}
  .stTabs [data-baseweb="tab-panel"] {{ padding-top: 1.4rem; }}

  /* números como marcações de profundidade: grandes, condensados, separados por rejunte */
  .st-key-numeros {{ border-top: 1px solid {LINHA}; border-bottom: 1px solid {LINHA}; padding: 14px 0; margin-bottom: 1.2rem; }}
  .st-key-numeros [data-testid="stColumn"] + [data-testid="stColumn"] {{ border-left: 1px solid {LINHA}; padding-left: 1.2rem; }}
  [data-testid="stMetricValue"] {{ font-family: {CONDENSADA}; font-weight: 600; font-size: 2.6rem; color: {AZUL_FUNDO}; }}
  [data-testid="stMetricLabel"] p {{ color: {CINZA}; font-size: .92rem; }}

  /* blocos de gráfico e de predição */
  [class*="st-key-card"] {{ border: 1px solid {LINHA}; border-radius: 6px; padding: 18px 22px; }}
  .card-titulo {{ font-family: {CONDENSADA}; font-weight: 600; font-size: 1.3rem; color: {TINTA}; margin-bottom: .1rem; }}
  .passo {{
    display: inline-grid; place-items: center; width: 1.5rem; height: 1.5rem; margin-right: .5rem;
    border-radius: 3px; background: {FUNDO_HERO}; color: {AZUL_FUNDO}; font-size: 1rem; vertical-align: 2px;
  }}

  .sec {{ display: flex; align-items: center; gap: .55rem; margin: 0 0 .1rem; }}
  .sec h3 {{ font-family: {CONDENSADA}; font-weight: 600; font-size: 1.7rem; margin: 0; padding: 0; }}
  .sec-sub {{ color: {CINZA}; font-size: 1rem; margin: 0 0 1.1rem 0; }}

  /* resultado da predição: uma placa de profundidade */
  .st-key-card_resultado {{ background: {AZUL_FUNDO}; border-color: {AZUL_FUNDO}; }}
  .st-key-card_resultado .card-titulo {{ color: #ffffff; }}
  .st-key-card_resultado .passo {{ background: rgba(255, 255, 255, .15); color: #ffffff; }}
  .resultado {{ text-align: center; padding: 1.3rem 0 .4rem; }}
  .resultado .valor {{ font-family: {CONDENSADA}; font-weight: 600; font-size: 3.6rem; line-height: 1; color: #ffffff; }}
  .resultado .nota {{ color: #c7e4ee; font-size: .92rem; margin-top: .6rem; }}

  /* celular: menos margem no cabeçalho e o resumo em linhas, sem separadores */
  @media (max-width: 640px) {{
    .st-key-hero {{ padding: 22px 20px 30px; }}
    .resumo {{ gap: .2rem 1rem; }}
    .resumo span {{ padding: 0; border-left: 0; }}
  }}

  /* barra lateral */
  .marca {{ display: flex; align-items: center; gap: .5rem; margin: -.4rem 0 .6rem; }}
  .marca b {{ font-family: {CONDENSADA}; font-weight: 600; font-size: 1.45rem; color: {TINTA}; }}
  .rodape {{ text-align: center; color: {CINZA}; font-size: .85rem; margin-top: .4rem; }}
</style>
"""

# Acabamento comum a todos os gráficos Plotly: fundo transparente, grade clara,
# fonte do app e legenda embaixo. Cada gráfico chama estilo_grafico(fig).
CORES_GRAFICO = [AZUL, AZUL_CLARO, AZUL_FUNDO, "#9fd3e4", "#3f97b6", "#cfe9f1"]
CORES_MAPA = [AZUL, "#e0a43a", "#3aa57d", "#7d6bc2", "#d9604c", CINZA]

def estilo_grafico(fig, altura=330):
    fig.update_layout(
        template="plotly_white", height=altura, margin=dict(t=10, b=10, l=10, r=10),
        font=dict(family="Barlow, sans-serif", size=14, color=CINZA),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="#ffffff", bordercolor=LINHA, font=dict(color=TINTA)),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.05, yanchor="top", title_text=""),
    )
    fig.update_xaxes(showline=False, zeroline=False, gridcolor="#eef2f4")
    fig.update_yaxes(showline=False, zeroline=False, gridcolor="#eef2f4")
    return fig

# Faixa de ondas fina, usada como divisória decorativa (largura total).
def onda(cor=AZUL_CLARO, largura="100%"):
    return f"""
    <svg viewBox="0 0 600 24" width="{largura}" height="20" preserveAspectRatio="none"
         fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M0 12 q 25 -12 50 0 t 50 0 t 50 0 t 50 0 t 50 0 t 50 0 t 50 0
               t 50 0 t 50 0 t 50 0 t 50 0 t 50 0"
            stroke="{cor}" stroke-width="1.4"/>
    </svg>
    """

# Pequenos ícones de traço fino para os títulos de seção.
def icone(nome, cor=AZUL):
    s = f'stroke="{cor}" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    base = 'viewBox="0 0 24 24" width="22" height="22" xmlns="http://www.w3.org/2000/svg"'
    if nome == "dados":   # tabela
        return f'<svg {base}><rect x="3" y="4" width="18" height="16" rx="2" {s}/><path d="M3 9h18M9 4v16" {s}/></svg>'
    if nome == "grafico":  # barras
        return f'<svg {base}><path d="M4 20V10M10 20V4M16 20v-8M20 20H3" {s}/></svg>'
    if nome == "gota":     # predição
        return f'<svg {base}><path d="M12 3s6 7 6 11a6 6 0 0 1-12 0c0-4 6-11 6-11Z" {s}/></svg>'
    return ""

def titulo_secao(texto, nome_icone, sub=None):
    html = f'<div class="sec">{icone(nome_icone)}<h3>{texto}</h3></div>'
    if sub:
        html += f'<p class="sec-sub">{sub}</p>'
    return html

def hero(resumo):
    """Texto do cabeçalho; `resumo` é uma lista de (valor, rótulo)."""
    itens = "".join(f"<span><b>{v}</b> {r}</span>" for v, r in resumo)
    return f"""
    <div class="hero">
      <h1>Manutenção de piscinas</h1>
      <p>Envie uma base de piscinas e explore os dados, os gráficos e a predição do custo mensal.</p>
      <div class="resumo">{itens}</div>
    </div>
    """

def marca():
    return f'<div class="marca">{icone("gota")}<b>Piscinas</b></div>'

def card_titulo(texto, passo=None):
    numero = f'<span class="passo">{passo}</span>' if passo else ""
    return f'<div class="card-titulo">{numero}{texto}</div>'

def resultado(valor="R$ —", nota="O modelo de ML será conectado aqui na Frente 3."):
    return f'<div class="resultado"><div class="valor">{valor}</div><div class="nota">{nota}</div></div>'
