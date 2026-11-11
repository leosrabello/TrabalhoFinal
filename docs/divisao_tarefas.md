# Divisão de tarefas

O trabalho foi dividido em quatro frentes. As Frentes 1 a 3 entregam funções independentes dentro da pasta `ml/`; a Frente 4 junta tudo na tela.

## Frente 1 — Preparar os dados (`ml/dados.py`)

- `preparar_dados(df)` → `X, y`
  - `y` é a coluna `custo_manutencao_mensal`; linhas sem o alvo são descartadas.
  - `X` é o resto, sem `id`, `latitude` e `longitude`, com as colunas de texto convertidas por `pd.get_dummies` e números faltantes preenchidos com a média.
- `separar_treino_teste(X, y)` → `X_treino, X_teste, y_treino, y_teste` (80/20, `random_state=42`).

## Frente 2 — Os modelos (`ml/modelos.py`)

- `criar_modelo(nome, parametros)` devolve o regressor do scikit-learn já configurado:

  | Nome na tela | Modelo | Parâmetro |
  |---|---|---|
  | Árvore de Decisão | `DecisionTreeRegressor` | `profundidade` → `max_depth` |
  | KNN | `KNeighborsRegressor` | `k` → `n_neighbors` |
  | Regressão Linear | `LinearRegression` | — |

- `treinar(modelo, X_treino, y_treino)` ajusta e devolve o modelo.

## Frente 3 — Prever + métricas (`ml/avaliacao.py`)

- `prever(modelo, dados_da_piscina)` recebe um dicionário com os dados digitados, aplica o mesmo `get_dummies`, alinha às colunas do treino e devolve o custo previsto (`float`).
- `avaliar(modelo, X_teste, y_teste)` devolve `{"R²", "MAE", "RMSE"}`.

## Frente 4 — Ligar tudo na tela (`app.py`)

- `fluxo_de_treino(df, nome, parametros)` chama, em ordem, `preparar_dados` → `separar_treino_teste` → `criar_modelo` → `treinar` → `avaliar`, e devolve o modelo, as métricas, a configuração usada e os pontos de real × previsto.
- **Modelo na sessão:** o resultado fica em `st.session_state["treino"]`. O Streamlit roda o script inteiro a cada clique; sem a sessão, o modelo seria treinado de novo toda vez.
- **Quando treina:** na primeira vez que o app abre e sempre que o botão **Re-treinar** é clicado. Se o modelo, os parâmetros ou a base mudarem sem re-treinar, a tela avisa qual modelo está em uso.
- **Prever custo:** monta um dicionário com os campos da piscina (os principais à vista e os demais em "Mais detalhes", começando nos valores mais comuns da base) e chama `prever`.
- **Métricas:** R², MAE e RMSE do modelo em uso, medidos nas piscinas de teste, e um gráfico de real × previsto.
- README e esta documentação.

## Como testar o re-treino com uma base nova

1. `python gerar_dados.py` gera um `data/piscinas.csv` novo (outros valores sorteados).
2. No app, envie o arquivo pela barra lateral.
3. A aba Predição avisa que a base mudou; clique em **Re-treinar** e veja as métricas novas.
