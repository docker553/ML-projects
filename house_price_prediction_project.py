# -*- coding: utf-8 -*-
"""House_Price_Prediction_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BF5JS1ExHBllke_XtF_fGiAosP90uNN_

# Get the Data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statistics

import warnings
warnings.filterwarnings("ignore")

from google.colab import files
files.upload()

housing = pd.read_csv("housing.csv")

housing.head(5)

housing.info()

housing.describe()

housing.shape

housing.columns

housing.nunique()

housing.isnull().sum()

"""## Visualizing the data to gain insights.

"""

housing.hist(bins=50,figsize=(15,15));

housing1 = housing.copy()

housing1.plot(kind="scatter", x="longitude", y="latitude",alpha=0.25)

housing1.plot(kind="scatter", x="longitude", y="latitude", alpha=0.25,
    s=housing["population"]/100, label="population", figsize=(10,5),
    c="median_house_value",colormap='viridis', colorbar=True,
    sharex=False)

corr_matrix = housing1.corr()

corr_matrix

housing1.plot(kind="scatter", x="median_income", y="median_house_value",
             alpha=0.25)

housing1["rooms_per_household"] = housing1["total_rooms"]/housing1["households"]
housing1["bedrooms_per_room"] = housing1["total_bedrooms"]/housing1["total_rooms"]
housing1["population_per_household"]=housing1["population"]/housing1["households"]

housing1.shape

housing1.columns

corr_matrix=housing1.corr()
corr_matrix

housing1.isnull().sum()

plt.figure(figsize=(10,10))
sns.heatmap(corr_matrix,cmap='viridis',annot=True,robust=True)

"""## 1. Data Cleaning"""

housing_features = housing1.drop('median_house_value', axis = 1)
print(housing_features.columns)

housing_features.head()

housing_target = housing1['median_house_value']
housing_target.shape

housing1 = housing1.drop("median_house_value", axis=1)
housing1.columns

housing1.isnull().sum()

from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy="median")

housing2 = housing1.drop("ocean_proximity", axis=1)
housing2.columns

imputer.fit(housing2)

imputer.statistics_

transformed_values = imputer.transform(housing2)
transformed_values

housing_transformed = pd.DataFrame(transformed_values)
housing_transformed.head()

housing_transformed.columns = ['longitude', 'latitude', 'housing_median_age', 'total_rooms',
       'total_bedrooms', 'population', 'households', 'median_income',
       'rooms_per_household', 'bedrooms_per_room', 'population_per_household']
housing_transformed.head()

housing_transformed.isnull().sum()

"""### 2. Handling Categorical attributes

---


"""

from sklearn.preprocessing import OneHotEncoder

cat_encoder = OneHotEncoder()

housing_cat = housing[['ocean_proximity']]
housing_cat

housing.ocean_proximity.value_counts()

dummy_values=cat_encoder.fit_transform(housing_cat)
dummy_values

dummy_values.toarray()

cat_encoder.categories_

housing_cat = pd.DataFrame(dummy_values.toarray())
housing_cat.head()

housing_cat.columns = ['<1H OCEAN', 'INLAND', 'ISLAND', 'NEAR BAY', 'NEAR OCEAN']

housing_cat.head()

"""## 3. Feature Scaling"""

from sklearn.preprocessing import StandardScaler
std_scaler = StandardScaler()

std_scaler.fit(housing_transformed)

housing_transformed.describe()

scaled_values=std_scaler.transform(housing_transformed)

housing_scaled = pd.DataFrame(scaled_values)

housing_scaled.columns = ['longitude', 'latitude', 'housing_median_age', 'total_rooms',
       'total_bedrooms', 'population', 'households', 'median_income',
       'rooms_per_household', 'bedrooms_per_room', 'population_per_household']

housing_scaled.describe()

housing_prepared = housing_scaled.join(housing_cat)

housing_prepared.shape

housing_prepared.head()

housing_prepared.isnull().sum()

"""##  Checking VIF values to detect multi-collinearity and dropping those variables with high VIF values"""

from statsmodels.stats.outliers_influence import variance_inflation_factor

X=housing_prepared
Y=housing_target

def calc_vif(X):
    vif = pd.DataFrame()
    vif["variables"] = X.columns
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    return(vif)

calc_vif(X)

X1 = X.drop(['total_bedrooms'],axis=1)

def calc_vif(X1):
    vif = pd.DataFrame()
    vif["variables"] = X1.columns
    vif["VIF"] = [variance_inflation_factor(X1.values, i) for i in range(X1.shape[1])]
    return(vif)

calc_vif(X1)

X2 = X1.drop(['latitude'],axis=1)

def calc_vif(X2):
    vif = pd.DataFrame()
    vif["variables"] = X2.columns
    vif["VIF"] = [variance_inflation_factor(X2.values, i) for i in range(X2.shape[1])]
    return(vif)

calc_vif(X2)

X3 = X2.drop(['households'],axis=1)

def calc_vif(X3):
    vif = pd.DataFrame()
    vif["variables"] = X3.columns
    vif["VIF"] = [variance_inflation_factor(X3.values, i) for i in range(X3.shape[1])]
    return(vif)

calc_vif(X3)

"""## Dropping 3 variables to avoid the problem of multicollinearity . - Households , Total bedrooms , latitude

## Create a Test Set
"""

from sklearn.model_selection import train_test_split

x_train, x_test, y_train,y_test = train_test_split(X3,Y, test_size=0.2, random_state=42)

print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)

"""## Select a model and training it"""

# OLS Model

import statsmodels.api as sm

x_const1 = sm.add_constant(x_train)
model= sm.OLS(y_train, x_const1)
LR1 = model.fit()
print(LR1.params)
print(LR1.summary())

"""## Checking the residual plot for the LR1 model"""

# residuals-plot
res1 = LR1.resid               
std1 = statistics.stdev(res1)

fig = sm.qqplot(res1/std1, line='s')
plt.show()

sns.distplot(res1)

from sklearn.linear_model import LinearRegression

lin_reg = LinearRegression()
lin_reg.fit(x_train, y_train)

y_pred = lin_reg.predict(x_test)
print(y_pred)

from sklearn.metrics import mean_squared_error,r2_score,mean_absolute_error

print(mean_squared_error(y_pred,y_test))
print(mean_absolute_error(y_pred,y_test))
print(r2_score(y_pred,y_test))

print(lin_reg.coef_)
print(lin_reg.intercept_)

"""## Applying CV on Linear Regression Model"""

from sklearn.model_selection import cross_val_score

scores = cross_val_score(lin_reg, x_train, y_train,scoring="neg_mean_squared_error", cv=10)
lin_rmse_scores = np.sqrt(-scores)

lin_rmse_scores

lin_rmse_scores.mean()

"""## Applying Decision Tree"""

from sklearn.tree import DecisionTreeRegressor

dt_reg = DecisionTreeRegressor()
dt_reg.fit(x_train,y_train)

y_pred2 = dt_reg.predict(x_test)
print(y_pred2)

print(mean_squared_error(y_pred2,y_test))
print(mean_absolute_error(y_pred2,y_test))
print(r2_score(y_pred2,y_test))

"""### Better Evaluation using cross validation"""

from sklearn.model_selection import cross_val_score

scores = cross_val_score(dt_reg,x_train,y_train,scoring="neg_mean_squared_error",cv=10)
tree_rmse_scores = np.sqrt(-scores)

tree_rmse_scores

tree_rmse_scores.mean()

feature_imp1 = pd.Series(dt_reg.feature_importances_,index=x_train.columns).sort_values(ascending=False)
print(feature_imp1)

sns.barplot(x=feature_imp1, y=feature_imp1.index)
plt.xlabel('Feature Importance Score')
plt.ylabel('Features')
plt.title("Important Features")
plt.show()

"""### Apply Random Forest"""

from sklearn.ensemble import RandomForestRegressor

forest_reg = RandomForestRegressor()
forest_reg.fit(x_train, y_train)

y_pred3=forest_reg.predict(x_test)
print(y_pred3)

print(mean_squared_error(y_pred3,y_test))
print(mean_absolute_error(y_pred3,y_test))
print(r2_score(y_pred2,y_test))

feature_imp2 = pd.Series(forest_reg.feature_importances_,index=x_train.columns).sort_values(ascending=False)
print(feature_imp2)

sns.barplot(x=feature_imp2, y=feature_imp2.index)
plt.xlabel('Feature Importance Score')
plt.ylabel('Features')
plt.title("Important Features")
plt.show()

"""## Showing here the feature importance of each variable 


1.   Features such as NearOcean ,Near Bay Island have no significant importance for determining the dependent variable  .

### Fine-Tune the Model by calculating the best hyperparameters
"""

from sklearn.model_selection import GridSearchCV

param_grid = [
{'n_estimators': [3, 10, 30], 'max_features': [2, 4, 6, 8]}
]

forest_reg = RandomForestRegressor()
grid_search = GridSearchCV(forest_reg, param_grid, cv=5,
scoring='neg_mean_squared_error',
return_train_score=True)
grid_search.fit(x_train, y_train)

grid_search.best_params_

final_model=grid_search.best_estimator_
final_model

"""## Apply Final model on Test Dataset"""

final_predictions = final_model.predict(x_test)

final_rmse = np.sqrt(mean_squared_error(y_test, final_predictions))

final_rmse

print(mean_squared_error(final_predictions,y_test))
print(mean_absolute_error(final_predictions,y_test))
print(r2_score(final_predictions,y_test))

"""## Final Model Outcomes"""

model = ['lin_reg','dt_reg', 'rf_reg','final_model']
R2 = [0.42,0.598, 0.6,0.72]
model_outcomes = pd.DataFrame({'model':model, 'R2-score' : R2})
model_outcomes

"""## **Both the decision tree and random forest models are giving us the same ## results in terms of accuracy.** """