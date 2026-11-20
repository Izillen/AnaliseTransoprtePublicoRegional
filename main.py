import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
from shapely.geometry import Point, LineString, Polygon
import geopandas as gpd
import seaborn as sns
import warnings
import json

warnings.filterwarnings('ignore')

# Estilo visual dos gráficos
sns.set_theme(style='whitegrid', palette='Set2')
plt.rcParams['figure.figsize'] = (12, 5)
plt.rcParams['font.size'] = 12

with open("data/onibus.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

tabelaParadas = []
tabelaHorarios = []
tabelaSentidos = []
tabelaOnibus = []
codigoSentido = 0

for linha in dados:
    tabelaOnibus.append((linha["linha"], linha["nomeLinha"]))

    for sentido in linha["sentidos"]:
        codigoSentido += 1
        tabelaSentidos.append((codigoSentido, linha["linha"], sentido["nomeSentido"]))

        # Paradas
        for ordem, parada in enumerate(sentido["paradas"], start=1):
            tabelaParadas.append((codigoSentido, ordem, parada.strip().rstrip(",")))

        # Horários
        for dia in sentido["horarios"]:
            for lista_horarios in dia["horarios"]:
                for horario in lista_horarios:
                    tabelaHorarios.append((codigoSentido, horario))

df_paradas = pd.DataFrame(tabelaParadas, columns=["CodigoSentido", "Ordem", "Parada"])
df_horarios = pd.DataFrame(tabelaHorarios, columns=["CodigoSentido", "Horario"])
df_tabela = pd.DataFrame(tabelaOnibus, columns=["CodigoLinha", "NomeLinha"])
df_tabelaSentido = pd.DataFrame(tabelaSentidos, columns=["CodigoSentido", "CodigoLinha", "NomeSentido"])

