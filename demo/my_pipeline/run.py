import logging
import os

from .steps import load, clean, filter
from .settings import DataPaths


def run(input_dataset, output_dataset):
    logging.info("Starting pipeline")
    df = load.load(input_dataset)
    df = clean.clean(df)
    df = filter.filter(df)
    save(df, output_dataset)
    logging.info("Pipeline finished")


def save(df, path):
    logging.info("Saving dataframe to path: " + path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)


if __name__ == "__main__":
    format = " | ".join(["%(asctime)s", "%(levelname)s", "%(filename)s", "%(message)s"])
    logging.basicConfig(format=format, level=logging.DEBUG)
    run(DataPaths.input_dataset, DataPaths.output_dataset)
