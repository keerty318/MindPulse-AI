import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import r2_score
# load the dataset
df = pd.read_csv(
    "Dataset/student_productivity_distraction_dataset_20000.csv"
)

X = df.drop(
    'productivity_score',
    axis=1
)
# input features

y = df['productivity_score']
# output feature

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
# training testing spliting of the dataset


model = RandomForestRegressor(
    n_estimators=100,
    n_jobs=-1,
    # jobs=-1 coz this will help in utilising full cpu power for training the model 
    random_state=42
)

model.fit(X_train, y_train)
# since ds is conti regression model is used

y_pred = model.predict(X_test)
# predicting the output for the test set



score = r2_score(y_test, y_pred)

print(score)
# performance of the model is evaluated using r2 score in regressionwhich is 0.9749... which is very good and model is performing well

# checking feature importance to understand which features are more important for predicting productivity score for viva tis will  help


importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.feature_importances_
})

importance = importance.sort_values(
    by='Importance',
    ascending=False
)

print(importance)


from sklearn.metrics import mean_absolute_error

mae = mean_absolute_error(y_test, y_pred)

print(mae)


from sklearn.metrics import mean_squared_error

rmse = mean_squared_error(
    y_test,
    y_pred
) ** 0.5

print(rmse)