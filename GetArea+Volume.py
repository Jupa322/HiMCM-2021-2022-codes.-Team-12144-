import pandas as pd

# n represents the water surface elevation.
n = 374.5992
area = 0
volume = 0
# file name can be changed to collect values from all elevation datasets.
df = pd.read_csv("waterelevfinal1.csv")
datanumber = len(df["elevation"])
for i in range(0,datanumber):
    if df["elevation"][i] <= n:
        area = area + 40000
        volume = volume + 40000 * df["elevation"][i]

print(area,volume)




