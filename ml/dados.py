"""
Frente 1 — Preparação dos dados para o Machine Learning.

Antes de treinar qualquer modelo, os dados precisam ser arrumados:
  1. separar o que é ENTRADA (features) do que vamos PREVER (alvo);
  2. transformar as colunas de texto em número (o scikit-learn só entende número);
  3. dividir em treino e teste.

Este arquivo entrega duas funções que as outras frentes usam:
  - preparar_dados(df)        -> devolve X (features) e y (alvo)
  - separar_treino_teste(X, y) -> divide em treino e teste
"""

import pandas as pd
from sklearn.model_selection import train_test_split

# Coluna que queremos prever.
ALVO = "custo_manutencao_mensal"

# Colunas que NÃO servem como entrada (identificador e localização exata).
# São descartadas porque não ajudam a prever o custo.
COLUNAS_IGNORADAS = ["id", "latitude", "longitude"]


def preparar_dados(df, alvo=ALVO, colunas_ignoradas=COLUNAS_IGNORADAS):
    """Separa features (X) e alvo (y) e codifica as colunas de texto.

    Parâmetros:
        df: o DataFrame com os dados das piscinas.
        alvo: o nome da coluna que será prevista.
        colunas_ignoradas: colunas que não entram como feature.

    Retorna:
        X: DataFrame só com as features, já em número (pronto pro modelo).
        y: a coluna alvo (o custo).
    """
    # Garante que a coluna alvo existe no arquivo.
    if alvo not in df.columns:
        raise ValueError(f"A coluna alvo '{alvo}' não existe nos dados.")

    # Remove linhas sem o valor do alvo (não dá pra treinar sem a resposta).
    df = df.dropna(subset=[alvo]).copy()

    # y = o que queremos prever.
    y = df[alvo]

    # X = tudo que sobra, menos o alvo e as colunas ignoradas.
    descartar = [alvo] + [c for c in colunas_ignoradas if c in df.columns]
    X = df.drop(columns=descartar)

    # Transforma as colunas de texto (ex.: tipo_piscina, uso) em colunas 0/1.
    # Ex.: a coluna "uso" vira "uso_Residencial", "uso_Hotel", etc.
    X = pd.get_dummies(X)

    # Preenche qualquer número faltante com a média da coluna.
    X = X.fillna(X.mean(numeric_only=True))

    return X, y


def separar_treino_teste(X, y, test_size=0.2, random_state=42):
    """Divide os dados em treino e teste.

    Treino: usado para o modelo aprender.
    Teste: separado, usado depois para medir se o modelo acertou.

    test_size=0.2 -> 20% dos dados vão para teste, 80% para treino.
    random_state=42 -> fixa o sorteio, pra dar sempre a mesma divisão.
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


# Permite testar este arquivo sozinho: python ml/dados.py
if __name__ == "__main__":
    from pathlib import Path

    csv = Path(__file__).resolve().parent.parent / "data" / "piscinas.csv"
    df = pd.read_csv(csv)

    X, y = preparar_dados(df)
    X_treino, X_teste, y_treino, y_teste = separar_treino_teste(X, y)

    print(f"Linhas no total:   {len(df)}")
    print(f"Features (colunas): {X.shape[1]}")
    print(f"Treino: {len(X_treino)} linhas | Teste: {len(X_teste)} linhas")
    print(f"Exemplos de features: {list(X.columns)[:6]} ...")
