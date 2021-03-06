"""
集計特徴量

featuretoolsを利用して作成した集計特徴量を用いてLightGBMで予測を行う。
"""

import argparse
import joblib

from util import run_lgb

def parse_args():
    parser = argparse.ArgumentParser(description='featuretools')
    parser.add_argument('--seed', action='store', type=int, default=1234)
    parser.add_argument('--objective', action='store', type=str, default='binary')
    parser.add_argument('--n_estimators', action='store', type=int, default=10000)
    parser.add_argument('--early_stopping', action='store', type=int, default=100)
    parser.add_argument('--device', action='store', type=str, default='gpu')
    return parser.parse_args()

def main():
    args = parse_args()
    feature_matrix = joblib.load('../data/02_featuretools/feature_matrix.joblib')
    app_train = feature_matrix.dropna(subset=['TARGET'])
    app_test = feature_matrix[feature_matrix['TARGET'].isnull()].drop('TARGET', axis=1)
    run_lgb(args, app_train, app_test, '12_featuretools')


if __name__ == "__main__":
    main()
