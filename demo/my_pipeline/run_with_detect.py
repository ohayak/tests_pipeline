import logging
import os
from steps import load, clean, filter
from settings import DataPaths
from tdda.constraints.pd.constraints import detect_df

def my_detect_df(df, TDDA_FILE, *args, **kwargs):
    v = detect_df(df, TDDA_FILE, *args, **kwargs)
    if v.failures == 0:
        print('Correctly verified dataframe against constraints in %s.'
              % TDDA_FILE)
    else:
        print('*** Unexpectedly failed to verify dataframe against constraints'
              ' in %s.\nSomething is wrong!' % TDDA_FILE)
        print(v)

def run():
    logging.info("Starting pipeline")
    df = load.load(DataPaths.input_dataset)
    my_detect_df(df, 'data/constraints/embauche_loaded.tdda', outpath='data/output/embauche_loaded_fails.csv', per_constraint=True)
    df = clean.clean(df)
    my_detect_df(df, 'data/constraints/embauche_cleaned.tdda', outpath='data/output/embauche_cleaned_fails.csv', per_constraint=True)
    df = filter.filter(df)
    my_detect_df(df, 'data/constraints/embauche_filtered.tdda', outpath='data/output/embauche_filtered_fails.csv', per_constraint=True)
    save(df, DataPaths.output_dataset)
    logging.info("Pipeline finished")


def save(df, path):
    logging.info("Saving dataframe to path: " + path)
    os.makedirs(os.path.dirname(DataPaths.output_dataset), exist_ok=True)
    df.to_csv(DataPaths.output_dataset, index=False)


if __name__ == "__main__":
    format = " | ".join(["%(asctime)s", "%(levelname)s", "%(filename)s", "%(message)s"])
    logging.basicConfig(format=format, level=logging.DEBUG)
    run()
