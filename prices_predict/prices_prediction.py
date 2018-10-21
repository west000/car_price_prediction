#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'West'

import pymysql, datetime, re, time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from scipy.stats import norm
from scipy import stats
from scipy.stats import skew

import matplotlib as mpl
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['SimHei']
mpl.rcParams['font.size'] = 10
sns.set_style("darkgrid",{"font.sans-serif":['simhei', 'Arial']})

NROWS = 200000

def cal_car_state(fix_record):
    state = 0
    if isinstance(fix_record, str) is True:
        a = fix_record.count('喷漆修复')
        b = fix_record.count('覆盖件更换')
        c = fix_record.count('钣金修复')
        d = fix_record.count('有色差')
        state = a * 0.2 + b * 0.3 + c * 0.4 + d * 0.1
        state = state/(a+b+c+d)
    return (1 - state) * 10

current_year = datetime.datetime.now().year
def cal_car_age(first_licence):
    age = current_year - int(first_licence[:4])
    return age

def cal_sale_days(add_date, sale_date):
    if sale_date is None or sale_date == r'\N':
        return None
    format = '%Y-%m-%d'
    add_date = datetime.datetime.strptime(add_date, format)
    sale_date = datetime.datetime.strptime(sale_date, format)
    return (sale_date - add_date).days

def deal_sale_date(sale_date):
    return None if sale_date == r'\N' else sale_date

def parse_version(version, index):
    version = version.split('-')
    if len(version) == 1:
        return '-'
    version = version[1].split(' ')
    return version[index]

def parse_car_serie(version):
    return parse_version(version, 0)

def parse_car_year(version):
    res = re.findall(r'(\d+)款', version)
    return int(res[0]) if len(res) != 0 else np.NaN

def parse_car_displacement(version):
    res = re.findall(r'(\d+\.\d*)', version)
    # print(float(res[0]) if len(res) != 0 else np.NaN, '=====', version)
    return float(res[0]) if len(res) != 0 else np.NaN

def parse_car_version(version):
    version = version.replace('AT', '').replace('MT', '').strip()
    v = parse_version(version, -1)
    # print(v, '====', version)
    return v

def target_var_distribution(train, var):
    sns.distplot(train[var], fit=norm)
    mu, sigma = norm.fit(train[var])
    print('\n mu = {:.2f} and sigma = {:.2f}\n'.format(mu, sigma))
    # 画出分布图
    plt.legend(['Normal dist. ($\mu=$ {:.2f} and $\sigma=$ {:.2f} )'.format(mu, sigma)], loc='best')
    plt.ylabel('Frequency')
    plt.title('%s distribution' % var)
    fig = plt.figure()
    res = stats.probplot(train['current_price'], plot=plt)
    plt.show()

import pickle
def save_model(model, name):
    path = './model/' + name + '.sav'
    pickle.dump(model, open(path, 'wb'))

def load_model(name):
    path = './model/' + name + '.sav'
    return pickle.load(open(path, 'rb'))


beginTime = time.time()
df_train = pd.read_csv(r'./data/test.csv', low_memory=False, nrows=NROWS)
endTime = time.time()
print('read_csv cost {:.2f}s'.format(endTime-beginTime))

df_train.drop(columns=['source'], axis=1, inplace=True)
print(df_train.describe())

# 训练模型的过程
if True:
    beginTime = time.time()
    # 拆分更多特征
    if True:
        # df_train['car_serie'] = df_train.apply(lambda row: parse_car_serie(row['version']), axis=1)
        # df_train.drop(df_train[df_train['car_serie'] == '-'].index, inplace=True)
        df_train['car_displacement'] = df_train.apply(lambda row: parse_car_displacement(row['version']), axis=1)
        # df_train['car_version'] = df_train.apply(lambda row: parse_car_version(row['version']), axis=1)
        # 由下面的相关性热力图可以看出，car_year和sale_days与其他的变量的相关性不大，因此可以删除之
        # df_train['car_year'] = df_train.apply(lambda row: parse_car_year(row['version']), axis=1)
        df_train['sale_date'] = df_train.apply(lambda  row : deal_sale_date(row['sale_date']), axis=1)
        df_train['car_state'] = df_train.apply(lambda row : cal_car_state(row['fix_record']), axis=1)
        df_train['car_age'] = df_train.apply(lambda row : cal_car_age(row['first_licence']), axis=1)
        all_data_na = (df_train.isnull().sum() / len(df_train)) * 100
        all_data_na = all_data_na.drop(all_data_na[all_data_na == 0].index).sort_values(ascending=False)
        missing_data = pd.DataFrame({'Missing Ratio': all_data_na})
        print(missing_data)

        quit()
        # df_train['sale_days'] = df_train.apply(lambda row : cal_sale_days(row['add_date'], row['sale_date']), axis=1)
        df_train.drop(columns=['fix_record', 'first_licence', 'unique_id', 'source', 'sale_date', 'add_date', 'version'], axis=1, inplace=True)

    # 离群点处理
    if True:
        # fig, ax = plt.subplots()
        # ax.scatter(x=df_train['new_price'], y=df_train['current_price'])
        # plt.ylabel('current_price', fontsize=13)
        # plt.xlabel('new_price', fontsize=13)
        # plt.show()
        df_train = df_train.drop(df_train[(df_train['new_price']>4500000) | (df_train['current_price']>3000000)].index)
        # fig, ax = plt.subplots()
        # ax.scatter(x=df_train['new_price'], y=df_train['current_price'])
        # plt.ylabel('current_price', fontsize=13)
        # plt.xlabel('new_price', fontsize=13)
        # plt.show()

    # 分析因变量current_price
    if False:
        # target_var_distribution(df_train, 'current_price')
        # 呈正偏态，进行log转换
        df_train['current_price'] = np.log1p(df_train['current_price'])
        # target_var_distribution(df_train, 'current_price')
        # target_var_distribution(df_train, 'new_price')
        # 呈正偏态，进行log转换
        df_train['new_price'] = np.log1p(df_train['new_price'])
        # target_var_distribution(df_train, 'new_price')

    # 缺失值处理
    if True:
        all_data_na = (df_train.isnull().sum() / len(df_train)) * 100
        all_data_na = all_data_na.drop(all_data_na[all_data_na == 0].index).sort_values(ascending=False)
        missing_data = pd.DataFrame({'Missing Ratio': all_data_na})
        print(missing_data)

        # 显示缺失值的比例
        # f, ax = plt.subplots(figsize=(15, 12))
        # plt.xticks()
        # sns.barplot(x=all_data_na.index, y=all_data_na)
        # plt.xlabel('Features', fontsize=15)
        # plt.ylabel('Percent of missing values', fontsize=15)
        # plt.title('Percent missing data by feature', fontsize=15)
        # plt.show()

        # df_train.drop(df_train[df_train['car_year'].isnull()].index, inplace=True)
        df_train.drop(df_train[df_train['brand'].isnull()].index, inplace=True)
        df_train.drop(df_train[df_train['car_displacement'].isnull()].index, inplace=True)
        # df_train['sale_days'].fillna(df_train['sale_days'].median(), inplace=True)
        # df_train['car_displacement'].fillna(df_train['car_displacement'].mode(), inplace=True)

        all_data_na = (df_train.isnull().sum() / len(df_train)) * 100
        all_data_na = all_data_na.drop(all_data_na[all_data_na == 0].index).sort_values(ascending=False)
        missing_data = pd.DataFrame({'Missing Ratio': all_data_na})
        print(missing_data)

    # 数据相关性
    if False:
        # 选出只有整数和浮点数的columns
        num_trainData = df_train.select_dtypes(include=['int64', 'float64'])
        # 计算各列与current_price的相关性
        traindata_corr = num_trainData.corr()['current_price'][:-1]
        golden_feature_list = traindata_corr[abs(traindata_corr) > 0].sort_values(ascending = False)
        print("Below are {} correlated values with current_price:\n{}".format(len(golden_feature_list), golden_feature_list))
        # 创建一个热点图，以明确观察与current_price的相关性
        traindata_corr_heatmap = num_trainData.corr()
        cols = traindata_corr_heatmap.nlargest(10, 'current_price')['current_price'].index
        cm = np.corrcoef(num_trainData[cols].values.T)
        sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f',
                    annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values)
        plt.show()

        # 可以看出car_year和sale_days与其他数据的相关性都不大，可以删除之
        # df_train.drop(columns=['car_year', 'sale_days'], axis=1, inplace=True)

    # 数值类型变量的偏度
    if False:
        numeric_feats = df_train.dtypes[df_train.dtypes != "object"].index
        numeric_feats = numeric_feats.drop('transfer_times')
        skewed_feats = df_train[numeric_feats].apply(lambda x: skew(x.dropna())).sort_values(ascending=False)
        print("\nSkew in numerical features: \n")
        skewness = pd.DataFrame({'Skew' :skewed_feats})
        print(skewness)

        # target_var_distribution(df_train, 'sale_days')
        # target_var_distribution(df_train, 'mailage')
        # target_var_distribution(df_train, 'car_state')
        # target_var_distribution(df_train, 'car_age')
        # target_var_distribution(df_train, 'car_year')

        skewness = skewness[abs(skewness) > 0.5]
        print("There are {} skewed numerical features to Box Cox transform".format(skewness.shape[0]))
        print(skewness)
        from scipy.special import boxcox1p
        skewed_features = skewness.index
        lam = 0.15
        for feat in skewed_features:
            df_train[feat] = boxcox1p(df_train[feat], lam)

        # target_var_distribution(df_train, 'car_year')
        # target_var_distribution(df_train, 'car_displacement')
        # target_var_distribution(df_train, 'sale_days')
        # target_var_distribution(df_train, 'mailage')
        # target_var_distribution(df_train, 'car_state')
        # target_var_distribution(df_train, 'car_age')


    # 类别变量，get_dummies
    if False:
        df_train = pd.get_dummies(df_train)
        print(df_train.shape)

    endTime = time.time()
    print('preprocessing cost {:.2f}s'.format(endTime-beginTime))


    beginTime = time.time()

    y = df_train['current_price']
    categorical_features = df_train.select_dtypes(include=['object']).columns
    numerical_features = df_train.select_dtypes(exclude=['object']).columns
    numerical_features = numerical_features.drop('current_price')
    train_num = df_train[numerical_features]
    train_cat = df_train[categorical_features]
    skewness = train_num.apply(lambda x: skew(x))
    skewness = skewness[abs(skewness) > 0.5]
    print(skewness)
    skewed_features = skewness.index
    train_num[skewed_features] = np.log1p(train_num[skewed_features])
    train_cat = pd.get_dummies(train_cat)
    train = pd.concat([train_num, train_cat], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(train, y, test_size=0.3, random_state=0)
    print("X_train : " + str(X_train.shape))
    print("X_test : " + str(X_test.shape))
    print("y_train : " + str(y_train.shape))
    print("y_test : " + str(y_test.shape))

    from sklearn.model_selection import cross_val_score
    def rmse_cv(model):
        rmse = np.sqrt(-cross_val_score(model, X_train, y_train, scoring="neg_mean_squared_error", cv=10))
        return (rmse)

    # Standardize numerical features
    stdSc = StandardScaler()
    X_train.loc[:, numerical_features] = stdSc.fit_transform(X_train.loc[:, numerical_features])
    X_test.loc[:, numerical_features] = stdSc.transform(X_test.loc[:, numerical_features])

    # 随机森林
    if False:
        from sklearn.ensemble import RandomForestRegressor
        rfr = RandomForestRegressor()
        rfr.fit(X_train, y_train)
        y_train_pred = rfr.predict(X_train)
        y_test_pred = rfr.predict(X_test)

        from sklearn.metrics import mean_squared_error
        forest_mse = mean_squared_error(y_train, y_train_pred)
        forest_rmse = np.sqrt(forest_mse)
        print('forest_rmse {:.2f}'.format(forest_rmse))

        forest_rmse_scores = rmse_cv(rfr)
        print(forest_rmse_scores)
        print('forest_rmse_scores mean {:.2f}'.format(forest_rmse_scores.mean()))
        print('forest_rmse_scores std {:.2f}'.format(forest_rmse_scores.std()))

        # Plot residuals
        plt.scatter(y_train_pred, y_train_pred - y_train, c="blue", marker="s", label="Training data")
        plt.scatter(y_test_pred, y_test_pred - y_test, c="lightgreen", marker="s", label="Validation data")
        plt.title("Random Forest regression")
        plt.xlabel("Predicted values")
        plt.ylabel("Residuals")
        plt.legend(loc="upper left")
        plt.hlines(y=0, xmin=0, xmax=50, color="red")
        plt.show()

        # Plot predictions
        plt.scatter(y_train_pred, y_train, c="blue", marker="s", label="Training data")
        plt.scatter(y_test_pred, y_test, c="lightgreen", marker="s", label="Validation data")
        plt.title("Random Forest regression")
        plt.xlabel("Predicted values")
        plt.ylabel("Real values")
        plt.legend(loc="upper left")
        plt.plot(c="red")
        plt.show()

        # 保存模型参数
        save_model(rfr, 'rfr')

    from scipy.stats import skew
    from sklearn.model_selection import cross_val_score, train_test_split
    from sklearn.metrics import mean_squared_error, make_scorer
    from sklearn.linear_model import RidgeCV, LassoCV, ElasticNetCV

    # Ridge模型
    if False:
        ridge = RidgeCV(alphas=[0.01, 0.03, 0.06, 0.1, 0.3, 0.6, 1, 3, 6, 10, 30, 60])
        ridge.fit(X_train, y_train)
        alpha = ridge.alpha_
        print("Best alpha :", alpha)  # 0.1

        print("Try again for more precision with alphas centered around " + str(alpha))
        ridge = RidgeCV(alphas=[alpha * .6, alpha * .65, alpha * .7, alpha * .75, alpha * .8, alpha * .85,
                                alpha * .9, alpha * .95, alpha, alpha * 1.05, alpha * 1.1, alpha * 1.15,
                                alpha * 1.25, alpha * 1.3, alpha * 1.35, alpha * 1.4],
                        cv=10)
        ridge.fit(X_train, y_train)
        alpha = ridge.alpha_
        print("Best alpha :", alpha)  # 0.13999999999999999

        y_train_rdg = ridge.predict(X_train)
        y_test_rdg = ridge.predict(X_test)

        from sklearn.metrics import mean_squared_error
        ridge_mse = mean_squared_error(y_train, y_train_rdg)
        ridge_rmse = np.sqrt(ridge_mse)
        print('ridge_rmse {:.2f}'.format(ridge_rmse))

        ridge_rmse_scores = rmse_cv(ridge)
        print(ridge_rmse_scores)
        print('ridge_rmse_scores mean {:.2f}'.format(ridge_rmse_scores.mean()))
        print('ridge_rmse_scores std {:.2f}'.format(ridge_rmse_scores.std()))


    # Lasso模型
    if True:
        lasso = LassoCV(alphas=[0.0001, 0.0003, 0.0006, 0.001, 0.003, 0.006, 0.01, 0.03, 0.06, 0.1, 0.3, 0.6, 1],
                        max_iter=1000, cv=10)
        lasso.fit(X_train, y_train)
        alpha = lasso.alpha_
        print("Best alpha :", alpha)

        print("Try again for more precision with alphas centered around " + str(alpha))
        lasso = LassoCV(alphas=[alpha * .6, alpha * .65, alpha * .7, alpha * .75, alpha * .8,
                                alpha * .85, alpha * .9, alpha * .95, alpha, alpha * 1.05,
                                alpha * 1.1, alpha * 1.15, alpha * 1.25, alpha * 1.3, alpha * 1.35,
                                alpha * 1.4],
                        max_iter=50000, cv=10)
        lasso.fit(X_train, y_train)
        alpha = lasso.alpha_
        print("Best alpha :", alpha)

        y_train_las = lasso.predict(X_train)
        y_test_las = lasso.predict(X_test)

        from sklearn.metrics import mean_squared_error
        lasso_mse = mean_squared_error(y_train, y_train_las)
        lasso_rmse = np.sqrt(lasso_mse)
        print('lasso_rmse {:.2f}'.format(lasso_rmse))

        lasso_rmse_scores = rmse_cv(lasso)
        print(lasso_rmse_scores)
        print('lasso_rmse_scores mean {:.2f}'.format(lasso_rmse_scores.mean()))
        print('lasso_rmse_scores std {:.2f}'.format(lasso_rmse_scores.std()))


    endTime = time.time()
    print('Random Forest cost {:.2f}s'.format(endTime-beginTime))
quit()




# 预测数据
def predict_data(data):
    # 更多特征
    # data['car_serie'] = data.apply(lambda row: parse_car_serie(row['version']), axis=1)
    # data.drop(data[data['car_serie'] == '-'].index, inplace=True)
    data['car_displacement'] = data.apply(lambda row: parse_car_displacement(row['version']), axis=1)
    # data['car_version'] = data.apply(lambda row: parse_car_version(row['version']), axis=1)
    data['sale_date'] = data.apply(lambda row: deal_sale_date(row['sale_date']), axis=1)
    data['car_state'] = data.apply(lambda row: cal_car_state(row['fix_record']), axis=1)
    data['car_age'] = data.apply(lambda row: cal_car_age(row['first_licence']), axis=1)
    data.drop(columns=['fix_record', 'first_licence', 'unique_id', 'source', 'sale_date', 'add_date', 'version'],
              axis=1, inplace=True)
    #缺失值处理
    data.drop(data[data['brand'].isnull()].index, inplace=True)
    data.drop(data[data['car_displacement'].isnull()].index, inplace=True)
    # log mailage,new_price,transfer_times,car_displacement,car_state,car_age
    categorical_features = data.select_dtypes(include=['object']).columns
    numerical_features = data.select_dtypes(exclude=['object']).columns
    pred_num = data[numerical_features]
    pred_cat = data[categorical_features]

    log_features = ['mailage','new_price','transfer_times','car_displacement','car_state','car_age']
    pred_num[log_features] = np.log1p(pred_num[log_features])
    pred_cat = pd.get_dummies(pred_cat)
    pred = pd.concat([pred_num, pred_cat], axis=1)

    model = load_model('rfr')
    predict_prices = model.predict(pred)
    print(predict_prices)

# pred_data = pd.read_csv(r'./data/pred_test.csv', low_memory=False)
# predict_data(pred_data)




# 线性回归模型
if False:
    df_train = pd.get_dummies(df_train)
    y = df_train['current_price']
    X_train, X_test, y_train, y_test = train_test_split(df_train, y, test_size=0.3, random_state=0)

    from sklearn.linear_model import Ridge, RidgeCV, ElasticNet, LassoCV, LassoLarsCV
    from sklearn.model_selection import cross_val_score

    def rmse_cv(model):
        rmse= np.sqrt(-cross_val_score(model, X_train, y_train, scoring="neg_mean_squared_error", cv = 5))
        return(rmse)

    model_ridge = Ridge()
    alphas = [0.05, 0.1, 0.3, 1, 3, 5, 10, 15, 30, 50, 75]
    cv_ridge = [rmse_cv(Ridge(alpha = alpha)).mean()
                for alpha in alphas]
    cv_ridge = pd.Series(cv_ridge, index = alphas)
    cv_ridge.plot(title = "Validation - Just Do It")
    plt.xlabel("alpha")
    plt.ylabel("rmse")
    plt.show()

    print(cv_ridge.min())
    model_lasso = LassoCV(alphas = [1, 0.1, 0.001, 0.0005]).fit(X_train, y)
    print(rmse_cv(model_lasso).mean())
    coef = pd.Series(model_lasso.coef_, index = X_train.columns)
    print("Lasso picked " + str(sum(coef != 0)) + " variables and eliminated the other " +  str(sum(coef == 0)) + " variables")
    imp_coef = pd.concat([coef.sort_values().head(10), coef.sort_values().tail(10)])
    plt.rcParams['figure.figsize'] = (8.0, 10.0)
    imp_coef.plot(kind = "barh")
    plt.title("Coefficients in the Lasso Model")
    plt.show()

    plt.rcParams['figure.figsize'] = (6.0, 6.0)
    preds = pd.DataFrame({"preds":model_lasso.predict(X_train), "true":y})
    preds["residuals"] = preds["true"] - preds["preds"]
    preds.plot(x = "preds", y = "residuals",kind = "scatter")
    plt.show()


# 多栈模型拟合
from scipy.stats import skew
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV, ElasticNetCV

if True:
    y = df_train['current_price']
    categorical_features = df_train.select_dtypes(include=['object']).columns
    numerical_features = df_train.select_dtypes(exclude=['object']).columns
    numerical_features = numerical_features.drop('current_price')
    train_num = df_train[numerical_features]
    train_cat = df_train[categorical_features]
    skewness = train_num.apply(lambda x: skew(x))
    skewness = skewness[abs(skewness) > 0.5]
    skewed_features = skewness.index
    train_num[skewed_features] = np.log1p(train_num[skewed_features])
    train_cat = pd.get_dummies(train_cat)
    train = pd.concat([train_num, train_cat], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(train, y, test_size=0.3, random_state=0)
    print("X_train : " + str(X_train.shape))
    print("X_test : " + str(X_test.shape))
    print("y_train : " + str(y_train.shape))
    print("y_test : " + str(y_test.shape))

    scorer = make_scorer(mean_squared_error, greater_is_better=False)

    def rmse_cv_train(model):
        # rmse = np.sqrt(-cross_val_score(model, X_train, y_train, scoring=scorer, cv=10))
        rmse = np.sqrt(-cross_val_score(model, X_train, y_train, scoring="neg_mean_squared_error", cv=10))
        return (rmse)

    def rmse_cv_test(model):
        # rmse = np.sqrt(-cross_val_score(model, X_test, y_test, scoring=scorer, cv=10))
        rmse = np.sqrt(-cross_val_score(model, X_train, y_train, scoring="neg_mean_squared_error", cv=10))
        return (rmse)

    # Standardize numerical features
    # stdSc = StandardScaler()
    # X_train.loc[:, numerical_features] = stdSc.fit_transform(X_train.loc[:, numerical_features])
    # X_test.loc[:, numerical_features] = stdSc.transform(X_test.loc[:, numerical_features])

    beginTime = time.time()
    if False:
        # Linear Regression
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        # save_model(lr, 'linear_regression_without_regularization')

        # Look at predictions on training and validation set
        print("RMSE on Training set :", rmse_cv_train(lr).mean())
        print("RMSE on Test set :", rmse_cv_test(lr).mean())
        y_train_pred = lr.predict(X_train)
        y_test_pred = lr.predict(X_test)

        # Plot residuals
        plt.scatter(y_train_pred, y_train_pred - y_train, c="blue", marker="s", label="Training data")
        plt.scatter(y_test_pred, y_test_pred - y_test, c="lightgreen", marker="s", label="Validation data")
        plt.title("Linear regression")
        plt.xlabel("Predicted values")
        plt.ylabel("Residuals")
        plt.legend(loc="upper left")
        plt.hlines(y=0, xmin=0, xmax=50, color="red")
        plt.show()

        # Plot predictions
        plt.scatter(y_train_pred, y_train, c="blue", marker="s", label="Training data")
        plt.scatter(y_test_pred, y_test, c="lightgreen", marker="s", label="Validation data")
        plt.title("Linear regression")
        plt.xlabel("Predicted values")
        plt.ylabel("Real values")
        plt.legend(loc="upper left")
        plt.plot( c="red")
        plt.show()
    endTime = time.time()
    print('Linear Regression without regularization cost {:.2f}s'.format(endTime - beginTime))

    if False:
        model = load_model('linear_regression_without_regularization')
        X_test['result'] = model.predict(X_test)
        print(X_test.head())
        quit()

    beginTime = time.time()
    if True:
        # 2* Ridge
        ridge = RidgeCV(alphas=[0.01, 0.03, 0.06, 0.1, 0.3, 0.6, 1, 3, 6, 10, 30, 60])
        ridge.fit(X_train, y_train)
        alpha = ridge.alpha_
        print("Best alpha :", alpha)        # 0.1

        print("Try again for more precision with alphas centered around " + str(alpha))
        ridge = RidgeCV(alphas=[alpha * .6, alpha * .65, alpha * .7, alpha * .75, alpha * .8, alpha * .85,
                                alpha * .9, alpha * .95, alpha, alpha * 1.05, alpha * 1.1, alpha * 1.15,
                                alpha * 1.25, alpha * 1.3, alpha * 1.35, alpha * 1.4],
                        cv=10)
        ridge.fit(X_train, y_train)
        alpha = ridge.alpha_
        print("Best alpha :", alpha)        # 0.13999999999999999

        print("Ridge RMSE on Training set :", rmse_cv_train(ridge).mean())
        print("Ridge RMSE on Test set :", rmse_cv_test(ridge).mean())
        y_train_rdg = ridge.predict(X_train)
        y_test_rdg = ridge.predict(X_test)

        # Plot residuals
        plt.scatter(y_train_rdg, y_train_rdg - y_train, c="blue", marker="s", label="Training data")
        plt.scatter(y_test_rdg, y_test_rdg - y_test, c="lightgreen", marker="s", label="Validation data")
        plt.title("Linear regression with Ridge regularization")
        plt.xlabel("Predicted values")
        plt.ylabel("Residuals")
        plt.legend(loc="upper left")
        plt.hlines(y=0, xmin=10.5, xmax=13.5, color="red")
        plt.show()

        # Plot predictions
        plt.scatter(y_train_rdg, y_train, c="blue", marker="s", label="Training data")
        plt.scatter(y_test_rdg, y_test, c="lightgreen", marker="s", label="Validation data")
        plt.title("Linear regression with Ridge regularization")
        plt.xlabel("Predicted values")
        plt.ylabel("Real values")
        plt.legend(loc="upper left")
        plt.plot([10.5, 13.5], [10.5, 13.5], c="red")
        plt.show()

        # Plot important coefficients
        coefs = pd.Series(ridge.coef_, index=X_train.columns)
        print("Ridge picked " + str(sum(coefs != 0)) + " features and eliminated the other " + \
              str(sum(coefs == 0)) + " features")
        imp_coefs = pd.concat([coefs.sort_values().head(10),
                               coefs.sort_values().tail(10)])
        imp_coefs.plot(kind="barh")
        plt.title("Coefficients in the Ridge Model")
        plt.show()
    endTime = time.time()
    print('Linear Regression with Ridge regularization (L2 penalty) cost {:.2f}s'.format(endTime - beginTime))

    beginTime = time.time()
    if True:
        lasso = LassoCV(alphas=[0.0001, 0.0003, 0.0006, 0.001, 0.003, 0.006, 0.01, 0.03, 0.06, 0.1, 0.3, 0.6, 1],
                        max_iter=1000, cv=10)
        lasso.fit(X_train, y_train)
        alpha = lasso.alpha_
        print("Best alpha :", alpha)

        print("Try again for more precision with alphas centered around " + str(alpha))
        lasso = LassoCV(alphas=[alpha * .6, alpha * .65, alpha * .7, alpha * .75, alpha * .8,
                                alpha * .85, alpha * .9, alpha * .95, alpha, alpha * 1.05,
                                alpha * 1.1, alpha * 1.15, alpha * 1.25, alpha * 1.3, alpha * 1.35,
                                alpha * 1.4],
                        max_iter=50000, cv=10)
        lasso.fit(X_train, y_train)
        alpha = lasso.alpha_
        print("Best alpha :", alpha)

        print("Lasso RMSE on Training set :", rmse_cv_train(lasso).mean())
        print("Lasso RMSE on Test set :", rmse_cv_test(lasso).mean())
        y_train_las = lasso.predict(X_train)
        y_test_las = lasso.predict(X_test)

        # Plot residuals
        plt.scatter(y_train_las, y_train_las - y_train, c="blue", marker="s", label="Training data")
        plt.scatter(y_test_las, y_test_las - y_test, c="lightgreen", marker="s", label="Validation data")
        plt.title("Linear regression with Lasso regularization")
        plt.xlabel("Predicted values")
        plt.ylabel("Residuals")
        plt.legend(loc="upper left")
        plt.hlines(y=0, xmin=10.5, xmax=13.5, color="red")
        plt.show()

        # Plot predictions
        plt.scatter(y_train_las, y_train, c="blue", marker="s", label="Training data")
        plt.scatter(y_test_las, y_test, c="lightgreen", marker="s", label="Validation data")
        plt.title("Linear regression with Lasso regularization")
        plt.xlabel("Predicted values")
        plt.ylabel("Real values")
        plt.legend(loc="upper left")
        plt.plot([10.5, 13.5], [10.5, 13.5], c="red")
        plt.show()

        # Plot important coefficients
        coefs = pd.Series(lasso.coef_, index=X_train.columns)
        print("Lasso picked " + str(sum(coefs != 0)) + " features and eliminated the other " + \
              str(sum(coefs == 0)) + " features")
        imp_coefs = pd.concat([coefs.sort_values().head(10),
                               coefs.sort_values().tail(10)])
        imp_coefs.plot(kind="barh")
        plt.title("Coefficients in the Lasso Model")
        plt.show()
    endTime = time.time()
    print('Linear Regression with Lasso regularization (L1 penalty) cost {:.2f}s'.format(endTime - beginTime))












quit()

# 前100行
if False:
    pd.set_option('max_columns',100)
    pd.set_option('max_rows',100)
    # print(df_train.head(100))
    # print(pd.get_dummies(df_train).head())

# 相关性
if False:
    # 选出只有整数和浮点数的columns
    num_trainData = df_train.select_dtypes(include=['int64', 'float64'])
    # 计算各列与current_price的相关性
    traindata_corr = num_trainData.corr()['current_price'][:-1]
    golden_feature_list = traindata_corr[abs(traindata_corr) > 0].sort_values(ascending = False)
    print("Below are {} correlated values with SalePrice:\n{}".format(len(golden_feature_list), golden_feature_list))
    # 创建一个热点图，以明确观察与current_price的相关性
    traindata_corr_heatmap = num_trainData.corr()
    cols = traindata_corr_heatmap.nlargest(10, 'current_price')['current_price'].index
    cm = np.corrcoef(num_trainData[cols].values.T)
    sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f',
                annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values)
    plt.show()

def distplot(var, p1=True, p2=True):
    if p1:
        sns.distplot(df_train[var], color='b', bins=100)
        plt.show()
        probmap = stats.probplot(df_train[var], plot=plt)
        plt.show()

    if p2:
        # 用log使数据波动呈正态分布
        sns.distplot(np.log(df_train[var]), color='r', bins=100)
        plt.show()
        res = stats.probplot(np.log(df_train[var]), plot=plt)
        plt.show()

# 直方图
if False:
    distplot('current_price')
    distplot('new_price')
    distplot('car_state')
    distplot('transfer_times', p2=False)
    distplot('mailage')

# 统计类别数据
if False:
    pd.set_option('max_rows',1000)
    print(df_train['brand'].value_counts())
    print('-'*100)
    print(df_train['version'].value_counts())
    print('-'*100)
    print(df_train['color'].value_counts())
    print('-'*100)
    print(df_train['area'].value_counts())

# 对类别数据进行编码
from sklearn.preprocessing import LabelEncoder
if False:
    lb = LabelEncoder()
    lb.fit(list(df_train['color'].values))
    df_train['color'] = lb.transform(list(df_train['color'].values))
    print(df_train.head(10))


quit()

fix_map = {}
for record in df_train['fix_record']:
    if isinstance(record, str) is False:
        continue
    record_list = record.split('|')
    for r in record_list:
        if r in fix_map:
            fix_map[r] += 1
        else:
            fix_map[r] = 1

print('-'*100)
print(fix_map)
print('-'*100)

for r, n in fix_map.items():
    print(r, '----', n)

quit()
# print(df_train.columns)
# print(df_train['current_price'].describe())
# sns.distplot(df_train['current_price'])
# plt.show()
# print("Skewness: %f" % df_train['current_price'].skew())    # 5.656039
# print("Kurtosis: %f" % df_train['current_price'].kurt())    # 75.526008

# var = 'mailage'
# data = pd.concat([df_train['current_price'], df_train[var]], axis=1)
# data.plot.scatter(x=var, y='current_price')
# plt.show()

# var = 'transfer_times'
# data = pd.concat([df_train['current_price'], df_train[var]], axis=1)
# 看看散点图
# data.plot.scatter(x=var, y='current_price')
# plt.show()
# 看看箱图
# f, ax = plt.subplots(figsize=(8, 6))
# fig = sns.boxplot(x=var, y='current_price', data=data)
# plt.show()


# corrmat = df_train.corr()
# f, ax = plt.subplots(figsize=(12, 9))
# sns.heatmap(corrmat, vmax=.8, square=True)
# plt.show()

# corrmat = df_train.corr()
# k = 5 #number of variables for heatmap
# cols = corrmat.nlargest(k, 'current_price')['current_price'].index
# cm = np.corrcoef(df_train[cols].values.T)
# sns.set(font_scale=1.25)
# hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values)
# plt.show()


# var = 'new_price'
# data = pd.concat([df_train['current_price'], df_train[var]], axis=1)
# data.plot.scatter(x=var, y='current_price')
# plt.show()

df_X = df_train.drop('current_price', axis=1)
df_Y = df_train['current_price']
quantity = [attr for attr in df_X.columns if df_X.dtypes[attr] != 'object']
quality = [attr for attr in df_X.columns if df_X.dtypes[attr] == 'object']

melt_X = pd.melt(df_X, value_vars=quantity)
print(melt_X.head())
print(melt_X.tail())















# print(df_train.head())
# print(df_train['current_price'].describe())
# tmp = df_train[df_train['fix_record'].isnull().values==True][['brand', 'current_price', 'unique_id', 'version', 'first_licence', 'mailage']]
# print(tmp.head())

# print(sns.distplot(df_train['current_price']))
# print('skewness: {0}, kurtosis: {1}'.format(df_train['current_price'].skew(), df_train['current_price'].kurt()))


# na_count = df_train.isnull().sum().sort_values(ascending=False)
# na_rate = na_count / len(df_train)
# na_data = pd.concat([na_count,na_rate],axis=1,keys=['count','ratio'])
# print(na_data.head(20))

# tmp = df_train[df_train['sale_date'].values==r'\N']


# '''
#         'host':'192.168.56.102',
#         'port':3306,
#         'user':'root',
#         'password':'123',
#         'db':'graduation_project',
#         'charset':'utf8'
# '''
#
# conn = pymysql.connect(host='192.168.56.102', port=3306, user='root', password='123',
#                                       db='graduation_project', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
# cursor = conn.cursor()
# sql = r"select dealer_id, sales_price, publish_date, end_date from car_price, car_dealer where car_price.dealer_id=car_dealer.id and carid='124231' and province='广东'"
# sql = r"select avg(sales_price) as avg_price, province from car_price, car_dealer where car_price.dealer_id=car_dealer.id and carid='124231' group by province"
# train = pd.read_sql(sql, conn)
# df = pd.DataFrame(train)
#
# print('-------------------------------')
# print(train.shape)
# print(df)
#
# condition_pivot = train.pivot_table(index='province', values='avg_price')
# condition_pivot.plot(kind='bar', color='b')
# plt.xlabel('Province')
# plt.ylabel('Avg Price')
# plt.ylim(40000, 50000)
# plt.xticks(rotation=90)
# plt.show()



"""
select * from (select 'brand', 'unique_id', 'version', 'first_licence', 'mailage', 'new_price', 'current_price', 'source', 'area', 'color', 'transfer_times', 'add_date', 'fix_record', 'sale_date'
union select brand, unique_id, version, first_licence, mailage, new_price, current_price, source, area, color, transfer_times, add_date, fix_record, sale_date from car) b
into outfile '/var/lib/mysql-files/test.csv' fields terminated by ',' lines terminated by '\n';
"""

