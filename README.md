# Sistema de Manutenção de Piscinas

Aplicação web (Streamlit) para análise de dados e predição do custo mensal de manutenção de piscinas com Machine Learning (scikit-learn).

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Abre sozinho no navegador em `http://localhost:8501`.

## O que o app faz
- Upload de arquivo `.csv`, `.xml` ou `.json` (ou usa o exemplo em `data/piscinas.csv`)
- **Dados**: prévia e resumo estatístico
- **Visualizações**: gráficos de barras e pizza (interativos) e mapa das piscinas
- **Predição**:
  - escolha do modelo — Árvore de Decisão (profundidade), KNN (k) ou Regressão Linear;
  - o modelo é treinado ao abrir a aba e fica guardado na sessão (não é re-treinado a cada clique);
  - **Re-treinar** treina de novo com a base carregada e os parâmetros escolhidos — envie uma base nova e re-treine;
  - **Prever custo** usa os dados da piscina informados na tela (os campos extras começam com os valores mais comuns da base);
  - métricas do modelo no conjunto de teste: **R²**, **MAE** e **RMSE**, mais um gráfico de real × previsto.

## Como o ML funciona

```
base (df) ─► preparar_dados ─► separar_treino_teste ─► criar_modelo ─► treinar ─► avaliar ─► métricas
             (Frente 1)        (Frente 1)              (Frente 2)      (Frente 2)  (Frente 3)
                                                                          │
                     dados digitados na tela ─► prever (Frente 3) ◄───────┘ modelo guardado
                                                                               no st.session_state
```

- O alvo é a coluna `custo_manutencao_mensal`. As colunas `id`, `latitude` e `longitude` não entram como feature.
- As colunas de texto viram colunas 0/1 com `pd.get_dummies`; a função `prever` alinha os dados digitados às mesmas colunas do treino.
- A divisão é 80% treino / 20% teste, com `random_state=42` (sempre a mesma divisão).

## Estrutura

| Arquivo | O que tem |
|---|---|
| `app.py` | Telas do Streamlit e a ligação com o ML (aba Predição) |
| `ui.py` | Parte visual: CSS, ícones e acabamento dos gráficos |
| `ml/dados.py` | `preparar_dados(df)` e `separar_treino_teste(X, y)` |
| `ml/modelos.py` | `criar_modelo(nome, parametros)` e `treinar(modelo, X_treino, y_treino)` |
| `ml/avaliacao.py` | `prever(modelo, dados_da_piscina)` e `avaliar(modelo, X_teste, y_teste)` |
| `gerar_dados.py` | Gera uma base de exemplo nova em `data/piscinas.csv` |

## Divisão de tarefas

| Frente | O que foi feito | Arquivo | Responsável |
|---|---|---|---|
| Front (apresentação 04/11) | Telas, upload, gráficos e mapa | `app.py`, `ui.py` | Leonardo Rabello |
| 1 — Preparar os dados | Separar features/alvo, `get_dummies`, divisão treino/teste | `ml/dados.py` | Leonardo Rabello |
| 2 — Modelos | Fábrica de modelos (Árvore, KNN, Regressão) e treino | `ml/modelos.py` | karasawa |
| 3 — Prever + métricas | Previsão de uma piscina e métricas R², MAE, RMSE | `ml/avaliacao.py` | Gabriel Ribeiro Batista |
| 4 — Integração na tela | Ligar as Frentes 1-3 na aba Predição, re-treino dinâmico, modelo no `st.session_state`, métricas, README | `app.py`, `README.md` | Tatzumikk |

Os detalhes de cada frente e como elas se encaixam estão em [`docs/divisao_tarefas.md`](docs/divisao_tarefas.md).

## Dados
`data/piscinas.csv` é um dataset de exemplo. Para gerar uma base nova, rode `python gerar_dados.py`.
