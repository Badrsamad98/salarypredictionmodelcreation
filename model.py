import pickle
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression, Lasso
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split

data = pd.read_csv('eda_data_cleaned.csv', index_col=0)
# choosing the relevent columns for the models

data_for_model = data[['average_salary', 'Rating', 'Size', 'Type of ownership', 'Industry', 'Sector', 'Revenue', 'number_of_competitors', 'hourly', 'employer_provided',
                       'job_state', 'same_state', 'Age of the company', 'Python', 'spark', 'aws', 'excel', 'title_simplified', 'seniority', 'description_lenght']]

# getting dummy data
data_dummy = pd.get_dummies(data_for_model)

#train, test and split
X = data_dummy.drop('average_salary', axis=1)
y = data_dummy.average_salary.values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)


# Prediction models: linear regression

# with statsmodes
X_sm = X = sm.add_constant(X)
model = sm.OLS(y, X_sm)
model.fit().summary()
# with sklearn
lr = LinearRegression()
lr.fit(X_train, y_train)

np.mean(cross_val_score(lr, X_train, y_train,
                        scoring='neg_mean_absolute_error', cv=3))

# Prediction models: lasso regression
lm_lasso = Lasso(alpha=.13)
lm_lasso.fit(X_train, y_train)
np.mean(cross_val_score(lm_lasso, X_train, y_train,
                        scoring='neg_mean_absolute_error', cv=3))

# Finding the best 'alpha' coefficient for the lasso regression
alpha = []
error = []

for i in range(1, 100):
    alpha.append(i/100)
    lm_lasso_new = Lasso(alpha=(i/100))
    error.append(np.mean(cross_val_score(lm_lasso_new, X_train,
                                         y_train, scoring='neg_mean_absolute_error', cv=3)))

plt.plot(alpha, error)

err = tuple(zip(alpha, error))
df_err = pd.DataFrame(err, columns=['alpha', 'error'])
df_err[df_err.error == max(df_err.error)]

# Prediction models: random forest

rf = RandomForestRegressor()

np.mean(cross_val_score(rf, X_train, y_train,
                        scoring='neg_mean_absolute_error', cv=3))

# Tunning the model with GridsearchCV

parameters = {'n_estimators': range(10, 300, 10), 'criterion': (
    'mse', 'mae'), 'max_features': ('auto', 'sqrt', 'log2')}

gs = GridSearchCV(rf, parameters, scoring='neg_mean_absolute_error', cv=3)
gs.fit(X_train, y_train)

# training
gs.best_score_
gs.best_estimator_

# test ensembles
tpred_lm = lr.predict(X_test)
tpred_lml = lm_lasso.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)


err_lm = mean_absolute_error(y_test, tpred_lm)
err_lml = mean_absolute_error(y_test, tpred_lml)
err_rf = mean_absolute_error(y_test, tpred_rf)

err_lm_rf = mean_absolute_error(y_test, (tpred_lm+tpred_rf)/2)

# saving the trained model
pickl = {'model': gs.best_estimator_}
pickle.dump(pickl, open('model_file' + ".p", "wb"))

file_name = "model_file.p"
with open(file_name, 'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']

model.predict(np.array(list(X_test.iloc[1, :])).reshape(1, -1))[0]

list(X_test.iloc[1, :])
