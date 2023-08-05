## Random Forest Model

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('../../data/racing_results/preprocessed/seoul/seoul_racing_results.csv')

print(dataset.head())

print(dataset.info())

print(dataset.describe())