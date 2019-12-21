## Linear Regression

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

dataset=pd.read_csv(r"C:\Users\User\Desktop\UM\WQD7005\Milestone\psi_data5.csv", header=0,skipinitialspace=True)

##Fill up missing values
#dataset.isnull().any()
dataset['Total International Visitor Arrivals'].fillna((dataset['Total International Visitor Arrivals'].mean()), inplace=True)
dataset['YOY GDP Growth Rate'].fillna((dataset['YOY GDP Growth Rate'].mean()), inplace=True)

dataset.columns.tolist()


df = pd.DataFrame(dataset, columns=dataset.columns)
target = pd.DataFrame(dataset, columns=['Average of G13'])

#Dep.Variable:Average of G13
X = df[['PSI Avg', 'Total International Visitor Arrivals', 'YOY GDP Growth Rate','Average of A68U','Average of C6L','Average of H15','Average of M04']]
y = target['Average of G13']

# Note the difference in argument order
model = sm.OLS(y, X).fit()
predictions = model.predict(X) # make the predictions by the model

# Print out the statistics
model.summary()

from sklearn import metrics
print('Mean Absolute Error:', metrics.mean_absolute_error(y, predictions))  
print('Mean Squared Error:', metrics.mean_squared_error(y, predictions))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y, predictions)))

df = pd.DataFrame({'Actual': y, 'Predicted': predictions})
df.plot(kind='bar',figsize=(10,8))
plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
plt.show()


# # Logistic Regression

df = pd.DataFrame(dataset, columns=dataset.columns)
target = pd.DataFrame(dataset, columns=["Trend"])

X = df[['PSI Avg', 'Total International Visitor Arrivals', 'YOY GDP Growth Rate','Average of A68U','Average of C6L','Average of H15','Average of M04']]
y = target["Trend"]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test=train_test_split(X,y,test_size=.5,random_state=1)

from sklearn.linear_model import LogisticRegression
logmodel = LogisticRegression()
print(logmodel.fit(X_train,y_train))
y_pred=logmodel.predict(X_test)

from sklearn.metrics import classification_report
print(classification_report(y_test,y_pred))

from sklearn import metrics
cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
cnf_matrix

