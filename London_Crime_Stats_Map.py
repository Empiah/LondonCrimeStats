import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv('/Users/oliverphipps/Dropbox/6. Python/Python Projects/LondonCrimeStatistics/london-outcomes.csv')

df.info()


data_by_location = df.groupby(['Latitude', 'Longitude'],as_index=False).mean()

data_by_location.head()['Latitude']
scaled_entries = (data_by_location['Longitude'].count() / len(data_by_location['Longitude']))

plt.scatter(data_by_location['Latitude'], data_by_location['Longitude'], s=scaled_entries)

plt.savefig('/Users/phipp/Dropbox/6. Python/Python Projects/LondonCrimeStatistics/LongLatMapCrime.png', dpi=600)
