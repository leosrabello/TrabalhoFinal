"""Fábrica e treinamento dos modelos de regressão do projeto."""

from numbers import Integral
import unicodedata

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor


def _parametro_inteiro_positivo(parametros, nomes, padrao, nome_exibicao):
    """Obtém um parâmetro inteiro positivo aceitando nomes alternativos."""
    valor = next((parametros[nome] for nome in nomes if nome in parametros), padrao)
    if isinstance(valor, bool) or not isinstance(valor, Integral) or valor < 1:
        raise ValueError(f"O parâmetro '{nome_exibicao}' deve ser um inteiro positivo.")
    return int(valor)


def criar_modelo(nome, parametros=None):
    """Cria um regressor configurado para prever o custo de manutenção.

    ``nome`` aceita ``Árvore``/``Árvore de Decisão``, ``KNN`` e
    ``Regressão``/``Regressão Linear`` (também sem acentos).
    ``parametros`` pode informar ``profundidade`` (ou ``max_depth``) para a
    árvore e ``k`` (ou ``n_neighbors``) para o KNN.
    """
    if not isinstance(nome, str):
        raise ValueError("O nome do modelo deve ser um texto.")
    if parametros is None:
        parametros = {}
    if not isinstance(parametros, dict):
        raise TypeError("'parametros' deve ser um dicionário.")

    nome_normalizado = unicodedata.normalize("NFKD", nome.strip().casefold())
    nome_normalizado = "".join(
        caractere for caractere in nome_normalizado
        if not unicodedata.combining(caractere)
    )

    if nome_normalizado in {
        "arvore",
        "?rvore",
        "arvore de decisao",
        "arvore de decis?o",
        "?rvore de decis?o",
    }:
        profundidade = _parametro_inteiro_positivo(
            parametros, ("profundidade", "max_depth"), 5, "profundidade"
        )
        return DecisionTreeRegressor(max_depth=profundidade, random_state=42)

    if nome_normalizado == "knn":
        k = _parametro_inteiro_positivo(parametros, ("k", "n_neighbors"), 5, "k")
        return KNeighborsRegressor(n_neighbors=k)

    if nome_normalizado in {
        "regressao",
        "regressao linear",
        "regress?o",
        "regress?o linear",
    }:
        return LinearRegression()

    raise ValueError(
        f"Modelo '{nome}' não reconhecido. Use Árvore, KNN ou Regressão."
    )


def treinar(modelo, X_treino, y_treino):
    """Ajusta o modelo aos dados de treino e devolve o mesmo modelo treinado."""
    modelo.fit(X_treino, y_treino)
    return modelo
