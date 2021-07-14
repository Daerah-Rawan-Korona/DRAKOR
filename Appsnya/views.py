from django.shortcuts import render
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn.cluster import KMeans
import seaborn as sns
import geopandas as gpd
import json
import io, base64, urllib
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

# Create your views here.


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def peta(request):
    covid = pd.read_csv('D:\Latihan\web\Django\DRAKOR\kmeans\Covid.csv', nrows=34)
    kepatuhan = pd.read_csv("D:\Latihan\web\Django\DRAKOR\kmeans\Kepatuhan.csv")
    covid.columns = covid.columns.str.replace(' ', '')
    case = list(covid.Kasus)
    kasus = [str.replace(",", "") for str in case]
    death = list(covid.Kematian)
    kematian = [str.replace(",", "") for str in death]
    provinsi = list(covid.ProvinsiAsal)
    patuh = list(kepatuhan.Kepatuhan)
    data = np.column_stack((kasus, kematian))

    kmeans = KMeans(n_clusters=3)
    cluster = kmeans.fit_predict(data)
    center = kmeans.cluster_centers_
    
    patuh = [str.replace(",", ".") for str in patuh]
    akhir = np.column_stack((provinsi, cluster, patuh))
    akhir = akhir.tolist()
    gabung = np.column_stack((provinsi, cluster))

    final = []
    kali = 0
    for item in akhir:
        if item[1] == '0':
            kali = 40
        elif item[1] == '1':
            kali = 60
        elif item[1] == '2':
            kali = 80
        final.append((kali*float(item[2]))/100)

    data_akhir = []
    clus = 0
    for item in final:
        if float(item) <= 40:
            clus = 0
        elif float(item) <= 60:
            clus = 1
        elif float(item) <= 80:
            clus = 2
        data_akhir.append(clus)
    data_final = np.column_stack((provinsi, data_akhir, final))

    data_f = data_final
    for x in data_f:
        if x[0] == 'DI Yogyakarta':
            x[0] = "Yogyakarta"
        elif x[0] == 'DKI Jakarta':
            x[0] = 'Jakarta Raya'
    df_final = pd.DataFrame(data_f, columns=['Provinsi', 'Cluster', 'Persentase'])

    df_geo = gpd.read_file("D:\Latihan\web\Django\DRAKOR\kmeans\gadm36_IDN_1.json")

    df_join = df_geo.merge(df_final, how='inner', left_on="NAME_1", right_on="Provinsi")
    df_join = df_join[['Provinsi', 'Cluster', 'Persentase', 'geometry']]

    N = 256

    green = np.ones((N, 4))
    green[:, 0] = np.linspace(142/256, 1, N)
    green[:, 1] = np.linspace(215/256, 1, N)
    green[:, 2] = np.linspace(75/256, 1, N)
    green_cmp = ListedColormap(green)

    red = np.ones((N, 4))

    red[:, 0] = np.linspace(255/256, 1, N)
    red[:, 1] = np.linspace(0/256, 1, N)
    red[:, 2] = np.linspace(65/256, 1, N)
    red_cmp = ListedColormap(red)

    yellow = np.ones((N, 4))

    yellow[:, 0] = np.linspace(255/256, 1, N) # R = 255
    yellow[:, 1] = np.linspace(232/256, 1, N) # G = 232
    yellow[:, 2] = np.linspace(11/256, 1, N)  # B = 11
    yellow_cmp = ListedColormap(yellow)

    dt = np.random.random([100, 100]) * 10

    newcolors2 = np.vstack((green_cmp(np.linspace(0, 0, 128)),
                            yellow_cmp(np.linspace(0, 0, 128)),
                        red_cmp(np.linspace(0, 0, 128))))
    triple = ListedColormap(newcolors2, name='triple')

    values = 'Cluster'
    vmin, vmax = 0,2
    fig, ax = plt.subplots(1, figsize = (30, 10))
    ax.axis('off')
    title = 'Cluster Tingkat Kemungkinan Tertular per Provinsi di Indonesia'
    ax.set_title(title, fontdict={'fontsize': '25', 'fontweight' : '3'})
    ax.annotate('Source: inta Ristekbrin dan Satgas COVID 19',xy=(0.1, .08),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12 ,color='#555555')
    sm = plt.cm.ScalarMappable(cmap=triple, norm=plt.Normalize(vmin=vmin, vmax=vmax))
    cbar = fig.colorbar(sm)
    df_join.plot(column=values, cmap=triple, linewidth=0.8, ax=ax, edgecolor='0.8',norm=plt.Normalize(vmin=vmin, vmax=vmax))

    flike = io.BytesIO()
    fig.savefig(flike, format='png')
    flike.seek(0)
    b64 = base64.b64encode(flike.read())
    uri = urllib.parse.quote(b64)

    return render(request, 'peta.html', {'covid':uri})


def statistik(request):
    return render(request, 'statistik.html')
