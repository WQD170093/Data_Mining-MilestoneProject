#Download packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Set the limit of display
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', -1)

Dataset=pd.read_csv(r"C:\Users\User\Desktop\UM\WQD7005\Milestone\psi_data5.csv", header=0,skipinitialspace=True)
#print(PSI).head()
print(Dataset.columns.tolist())


##Plot PSI vs G13 share price
Date_plot=np.array(Dataset['Date'])
PSI_plot=np.array(Dataset['PSI Avg'])
G13_plot=np.array(Dataset['Average of G13'])

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('PSI Avg', color=color)
ax1.plot(Date_plot, PSI_plot, color=color)
ax1.tick_params(axis='y', labelcolor=color)
plt.xticks(rotation=90)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Average of G13', color=color)  # we already handled the x-label with ax1
ax2.plot(Date_plot, G13_plot, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout() # otherwise the right y-label is slightly clipped
plt.show()

##Plot Visitor#, GDP vs G13 share price
Date_plot=np.array(Dataset['Date'])
Tourist_plot=np.array(Dataset['Total International Visitor Arrivals'])
GDP_plot=np.array(Dataset['YOY GDP Growth Rate'])

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('PSI Avg', color=color)
ax1.plot(Date_plot, PSI_plot, color=color)
ax1.tick_params(axis='y', labelcolor=color)
plt.xticks(rotation=90)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Total International Visitor Arrivals', color=color)  # we already handled the x-label with ax1
ax2.plot(Date_plot, Tourist_plot, color=color)
ax2.tick_params(axis='y', labelcolor=color)

color = 'tab:green'
ax2.set_ylabel('YOY GDP Growth Rate', color=color)  # we already handled the x-label with ax1
ax2.plot(Date_plot, GDP_plot, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout() # otherwise the right y-label is slightly clipped
plt.show()


#Correlation matrix
Dataset.columns=['Date','PSI Avg','Visitor Arrivals','GDP Growth','A68U','C6L','H15','M04','G13','Trend']
print(Dataset.corr())

plt.matshow(Dataset.corr())
plt.xticks(range(9),['PSI Avg','Visitor Arrivals','GDP Growth','A68U','C6L','H15','M04','G13','Trend'],rotation=90)
plt.yticks(range(9),['PSI Avg','Visitor Arrivals','GDP Growth','A68U','C6L','H15','M04','G13','Trend'])
plt.colorbar()
plt.figure(figsize=(10,10))
plt.show()
