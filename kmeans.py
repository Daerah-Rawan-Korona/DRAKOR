# -*- coding: utf-8 -*-
"""kmeans.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iQUbnmCfiVcKZL_XISv-Qoo31CKV_xwh
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
from sklearn.cluster import KMeans

from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import scale

import sklearn.metrics as sm
from sklearn import datasets
from sklearn.metrics import confusion_matrix, classification_report

!pip install luwiji
from luwiji.cluster import demo

"""SAMPLE DATA"""

x1, y1 = demo.blob_data()
x2, y2 = demo.moon_data()
x3, y3 = demo.circle_data()

x1

"""VISUALIZE"""

x = x1
plt.scatter(x[:, 0], x[:, 1], s = 10)
plt.axis("equal");

"""KMEANS CLUSTERING"""

kmeans = KMeans(n_clusters=3)

cluster = kmeans.fit_predict(x)

cluster

kmeans.cluster_centers_



