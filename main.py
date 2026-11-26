import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
from shapely.geometry import Point, LineString, Polygon
import geopandas as gpd
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

# Estilo visual dos gráficos
sns.set_theme(style='whitegrid', palette='Set2')
plt.rcParams['figure.figsize'] = (12, 5)
plt.rcParams['font.size'] = 12

dados = pd.read_json('data/onibus.json')
data = dados.drop_duplicates(subset='linha', keep='first')

tabelaParadas = []
tabelaHorarios = []
tabelaSentidos = []
tabelaOnibus = []
codigoSentido = 0

for linha in data.itertuples(index=False):
    tabelaOnibus.append((linha.linha, linha.nomeLinha))

    for sentido in linha.sentidos:
        codigoSentido += 1
        tabelaSentidos.append((codigoSentido, linha.linha, sentido["nomeSentido"]))

        # Paradas
        for ordem, parada in enumerate(sentido["paradas"], start=1):
            tabelaParadas.append((linha.linha, codigoSentido, ordem, parada.strip().rstrip(",")))

        # Horários
        for dia in sentido["horarios"]:
            for lista_horarios in dia["horarios"]:
                for horario in lista_horarios:
                    tabelaHorarios.append((linha.linha, codigoSentido, horario))

df_paradas = pd.DataFrame(tabelaParadas, columns=["CodigoLinha", "CodigoSentido", "Ordem", "Parada"])
df_horarios = pd.DataFrame(tabelaHorarios, columns=["CodigoLinha", "CodigoSentido", "Horario"])
df_tabela = pd.DataFrame(tabelaOnibus, columns=["CodigoLinha", "NomeLinha"])
df_tabelaSentido = pd.DataFrame(tabelaSentidos, columns=["CodigoSentido", "CodigoLinha", "NomeSentido"])


# Paradas mais atendidadas pelas linhas
tParadas = (
    df_paradas
    .groupby("Parada")
    .size()
    .reset_index(name="QuantidadeLinha")
)

print(tParadas.nlargest(10, 'QuantidadeLinha'))


# x = tParadas.groupby(['CodigoLinha'])['Parada'].apply(list)
# y = tParadas.groupby(['CodigoLinha'])['Parada'].count()



# fig, ax = plt.subplots()

# ax.bar(x.index, y.values, width=1, edgecolor="white", linewidth=0.7)

# plt.xticks(rotation=45, ha="right")
# plt.tight_layout()
# plt.show()


