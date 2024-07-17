#USE THIS FILE FOR ALL DATA MANIPULATION RELATED FUNCTION
import os
import pandas as pd
from pathlib import Path
import streamlit as st

def load_file(path: str) -> pd.DataFrame:

    filename = os.path.basename(path)
    file_extension = os.path.splitext(filename)[1]
    with open(path, "rb") as f:
        if file_extension == ".csv":
            dataset = pd.read_csv(f) #pickle.load(f)
        elif file_extension == ".xlsx":
            dataset = pd.read_excel(f) #pickle.load(f)
        else:
            raise ValueError("Unsupported file format")
        return dataset


@st.cache_data
def load_data(folder: str) -> pd.DataFrame:
    all_datasets = [load_file(file) for file in Path(folder).iterdir()]
    df = pd.concat(all_datasets)
    return df
