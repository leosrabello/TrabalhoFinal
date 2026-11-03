"""Gera uma base de exemplo de piscinas em data/piscinas.csv.
Rode com: python gerar_dados.py  (útil para testar o 're-treinar com base nova')."""
import numpy as np
import pandas as pd
from pathlib import Path

rng = np.random.default_rng()
N = 220
cidades = {"Curitiba": (-25.4284, -49.2733), "São José dos Pinhais": (-25.53, -49.206),
           "Pinhais": (-25.445, -49.192), "Colombo": (-25.292, -49.224), "Araucária": (-25.593, -49.41)}
bairros = ["Centro", "Batel", "Água Verde", "Portão", "Santa Felicidade",
           "Boqueirão", "Cabral", "Bigorrilho", "Cristo Rei", "Jardim Social"]
tipos, usos = ["Fibra", "Alvenaria", "Vinil"], ["Residencial", "Condomínio", "Academia", "Hotel"]
sol, freq = ["Baixa", "Média", "Alta"], ["Semanal", "Quinzenal", "Mensal"]

cid = rng.choice(list(cidades), N, p=[.45, .15, .15, .15, .10])
lat = np.array([cidades[c][0] for c in cid]) + rng.normal(0, 0.02, N)
lon = np.array([cidades[c][1] for c in cid]) + rng.normal(0, 0.02, N)
tipo = rng.choice(tipos, N, p=[.5, .35, .15])
uso = rng.choice(usos, N, p=[.55, .25, .12, .08])
expo = rng.choice(sol, N, p=[.25, .45, .30])
cob = rng.choice(["Sim", "Não"], N, p=[.35, .65])
frq = rng.choice(freq, N, p=[.35, .40, .25])
volume = np.round(rng.uniform(8, 120, N), 1)
area = np.round(volume / rng.uniform(1.3, 2.2, N), 1)
prof = np.round(volume / area / rng.uniform(0.8, 1.2, N), 2).clip(1.0, 2.8)
banhistas = (rng.poisson(12, N) * np.where(uso == "Residencial", 1,
             np.where(uso == "Condomínio", 4, np.where(uso == "Academia", 6, 8)))).astype(int)

mtipo = {"Fibra": 0, "Alvenaria": 40, "Vinil": 20}
muso = {"Residencial": 0, "Condomínio": 120, "Academia": 180, "Hotel": 220}
msol = {"Baixa": 0, "Média": 25, "Alta": 60}
mfreq = {"Semanal": 80, "Quinzenal": 30, "Mensal": 0}
mcob = {"Sim": -30, "Não": 0}

custo = (150 + volume * 3.5 + np.array([mtipo[t] for t in tipo]) + np.array([muso[u] for u in uso])
         + banhistas * 1.2 + np.array([msol[s] for s in expo]) + np.array([mcob[c] for c in cob])
         + np.array([mfreq[f] for f in frq]) + rng.normal(0, 40, N))
custo = np.round(custo.clip(120, None), 2)
cloro = np.round((volume * 0.06 + banhistas * 0.12 + np.array([msol[s] for s in expo]) * 0.02
                  + np.array([mcob[c] for c in cob]) * (-0.01) + rng.normal(0, 0.6, N)).clip(0.5, None), 2)

df = pd.DataFrame({
    "id": range(1, N + 1), "cidade": cid, "bairro": rng.choice(bairros, N),
    "latitude": np.round(lat, 5), "longitude": np.round(lon, 5),
    "tipo_piscina": tipo, "uso": uso, "volume_m3": volume, "area_m2": area,
    "profundidade_media_m": prof, "tem_cobertura": cob, "exposicao_sol": expo,
    "banhistas_semana": banhistas, "frequencia_manutencao": frq,
    "consumo_cloro_kg_mes": cloro, "custo_manutencao_mensal": custo,
})
Path("data").mkdir(exist_ok=True)
df.to_csv("data/piscinas.csv", index=False)
print(f"Gerado data/piscinas.csv com {len(df)} linhas.")
