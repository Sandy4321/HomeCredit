import argparse
import lightgbm
import mlflow

from util import seed_everything, read_file_with_dtypes

def parse_args():
    parser = argparse.ArgumentParser(description='Baseline')
    parser.add_argument('--objective', action='store', type=str, default='binary')
    parser.add_argument('--device', action='store', type=str, default='gpu')
    return parser.parse_args()

def main():
    # Train
    df_train = read_file_with_dtypes('../data/01_labelencoding/application_train.csv')
    x_train = df_train.drop('TARGET', axis=1)
    y_train = df_train['TARGET']
    train_set = lightgbm.Dataset(x_train, y_train)

    args = parse_args()
    params = vars(args)
    mlflow.log_params(params)

    eval_hist = lightgbm.cv(params, train_set, metrics='auc')
    for i, metric in enumerate(eval_hist['auc-mean']):
        mlflow.log_metric('auc', metric, step=i)

    # Predict
    df_test = read_file_with_dtypes('../data/01_labelencoding/application_test.csv')
    x_test = df_test
    model = lightgbm.train(params, train_set)
    y_pred = model.predict(x_test)
    df_submission = x_test[['SK_ID_CURR']].copy()
    df_submission['TARGET'] = y_pred

    path = '../submission/02_baseline.csv'
    df_submission.to_csv(path, index=False)
    mlflow.log_artifact(path)

if __name__ == "__main__":
    seed_everything()
    mlflow.set_tracking_uri('../logs/mlruns')
    mlflow.set_experiment('HomeCredit')
    with mlflow.start_run(run_name='baseline') as run:
        main()
