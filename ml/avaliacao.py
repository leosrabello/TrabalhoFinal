"""Previsao de custos e avaliacao dos modelos de regressao."""

from math import sqrt
from typing import Mapping

import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from ml.dados import ALVO, COLUNAS_IGNORADAS


def _dados_como_dataframe(dados_da_piscina):
    """Converte os dados de uma piscina em um DataFrame de uma linha."""
    if isinstance(dados_da_piscina, pd.DataFrame):
        dados = dados_da_piscina.copy()
    elif isinstance(dados_da_piscina, pd.Series):
        # Uma Series extraida de uma linha com tipos mistos costuma ter dtype
        # ``object``. Voltar primeiro para dict permite que o DataFrame infira
        # novamente os tipos de cada coluna e nao transforme numeros em dummies.
        dados = pd.DataFrame([dados_da_piscina.to_dict()])
    elif isinstance(dados_da_piscina, Mapping):
        dados = pd.DataFrame([dados_da_piscina])
    else:
        raise TypeError(
            "'dados_da_piscina' deve ser um dicionario, Series ou DataFrame."
        )

    if len(dados) != 1:
        raise ValueError("Informe os dados de exatamente uma piscina.")

    return dados


def prever(modelo, dados_da_piscina):
    """Preve o custo mensal de manutencao de uma piscina.

    Os dados podem ser informados como dicionario, ``pandas.Series`` ou
    ``pandas.DataFrame`` de uma linha. As colunas de texto sao transformadas
    no mesmo formato numerico usado em :func:`ml.dados.preparar_dados` e, para
    modelos treinados com um DataFrame, alinhadas automaticamente as features
    vistas durante o treino.

    Retorna:
        O custo previsto como ``float``.
    """
    if not hasattr(modelo, "predict"):
        raise TypeError("'modelo' deve possuir o metodo predict().")

    dados = _dados_como_dataframe(dados_da_piscina)

    # Identificador, localizacao exata e alvo nao fazem parte das features.
    colunas_descartadas = [ALVO, *COLUNAS_IGNORADAS]
    dados = dados.drop(columns=colunas_descartadas, errors="ignore")
    dados = pd.get_dummies(dados)

    # Os estimadores do projeto guardam feature_names_in_ quando sao treinados
    # com o DataFrame produzido por preparar_dados. O reindex garante a mesma
    # ordem, cria categorias ausentes com zero e ignora categorias desconhecidas.
    colunas_do_treino = getattr(modelo, "feature_names_in_", None)
    if colunas_do_treino is not None:
        dados = dados.reindex(columns=colunas_do_treino, fill_value=0)

    dados = dados.fillna(0)
    previsao = modelo.predict(dados)

    if len(previsao) != 1:
        raise ValueError("O modelo nao retornou uma unica previsao.")

    return float(previsao[0])


def avaliar(modelo, X_teste, y_teste):
    """Calcula R2, MAE e RMSE do modelo sobre o conjunto de teste.

    Retorna:
        Um dicionario com as metricas ``R²``, ``MAE`` e ``RMSE``.
    """
    if not hasattr(modelo, "predict"):
        raise TypeError("'modelo' deve possuir o metodo predict().")

    previsoes = modelo.predict(X_teste)

    return {
        "R²": float(r2_score(y_teste, previsoes)),
        "MAE": float(mean_absolute_error(y_teste, previsoes)),
        "RMSE": float(sqrt(mean_squared_error(y_teste, previsoes))),
    }
