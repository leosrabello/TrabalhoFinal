# Sistema de Manutenção de Piscinas

Aplicação web (Streamlit) para análise de dados e predição de custo de manutenção de piscinas.

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Abre sozinho no navegador em `http://localhost:8501`.

## O que já funciona (front — apresentação 04/11)
- Upload de arquivo `.csv`, `.xml` ou `.json` (ou usa o exemplo em `data/piscinas.csv`)
- Prévia dos dados e resumo estatístico
- Gráficos de barras e pizza (interativos) e mapa das piscinas
- Tela de predição com escolha de modelo e parâmetros (interface pronta)

## A fazer (até 11/11)
- Conectar o modelo de ML (scikit-learn) na aba Predição
- Re-treinar o modelo com base nova
- Métricas do modelo

## Dados
`data/piscinas.csv` é um dataset de exemplo. Para gerar uma base nova, rode `python gerar_dados.py`.
