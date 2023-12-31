from distutils.command.config import config
from http import client
from get_data import read_params
import argparse
import mlflow
from mlflow.tracking import MlflowClient
from pprint import pprint
import joblib
import os
import mlflow.sklearn


def log_production_model(config_path):
    config=read_params(config_path)
    mlflow_config=config["mlflow_config"]
    model_name=mlflow_config["registered_model_name"]
    remote_server_uri=mlflow_config["remote_server_uri"]
    mlflow.set_tracking_uri(remote_server_uri)
    runs=mlflow.search_runs([1])
    lowest=runs["metrics.mae"].sort_values(ascending=True)[0]
    lowest_run_id=runs[runs["metrics.mae"]==lowest]["run_id"][0]
    client=MlflowClient()
    for mv in client.search_model_versions(f"name='{model_name}'"):
        mv=dict(mv)
        if mv["run_id"]==lowest_run_id:
            current_version=mv["version"]
            logged_model=mv["source"]
            pprint(mv, indent=4)

            client.transition_model_version_stage(name=model_name, version=current_version, stage="Production")

        else:
            current_version=mv["version"]
            client.transition_model_version_stage(name=model_name, version=current_version, stage="Staging")
    
    load_model=mlflow.pyfunc.log_model(logged_model)
    model_path=config["model_dir"]
    os.system(f"attrib +h {model_path}")
    file_ = open(model_path, "wb")


    joblib.dump(load_model, model_path)
    


if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args=args.parse_args()
    log_production_model(config_path=parsed_args.config)