from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()

def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(BASE_DIR, "..", "data")

    files = os.listdir(path)
    all_data = []

    for file in files:
        if file.endswith(".csv"):
            df_temp = pd.read_csv(os.path.join(path, file))
            df_temp['source_file'] = file
            all_data.append(df_temp)

    df = pd.concat(all_data, ignore_index=True)

    df = df.iloc[2:].copy()
    df.reset_index(drop=True, inplace=True)

    df.rename(columns={
        'Unnamed: 2': 'Crop',
        'Kharif': 'Kharif_Area',
        'Unnamed: 5': 'Kharif_Production',
        'Rabi': 'Rabi_Area',
        'Unnamed: 8': 'Rabi_Production'
    }, inplace=True)

    df = df[['Crop', 'Kharif_Area', 'Kharif_Production',
             'Rabi_Area', 'Rabi_Production', 'source_file']]

    df = df[df['Crop'].notna()]

    for col in ['Kharif_Area', 'Kharif_Production', 'Rabi_Area', 'Rabi_Production']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    invalid = ['Crops', 'Area', 'Production', 'Productivity']
    df = df[~df['Crop'].isin(invalid)]

    df = df[
        ~df['Crop'].astype(str)
        .str.replace('.', '', regex=False)
        .str.isnumeric()
    ]

    df['Crop'] = df['Crop'].str.strip().str.lower()

    df['Kharif_Production'] = df['Kharif_Production'].fillna(0)
    df['Rabi_Production'] = df['Rabi_Production'].fillna(0)

    df['Total_Production'] = df['Kharif_Production'] + df['Rabi_Production']
    df['Year'] = df['source_file'].str.extract(r'(\d{4})')

    return df


df_clean = load_data()


@app.get("/")
def home():
    return {"message": "Crop Dashboard API running"}


@app.get("/data")
def get_data():
    return df_clean.to_dict(orient="records")


@app.get("/year-trend")
def year_trend():
    trend = df_clean.groupby('Year')['Total_Production'].sum()
    return trend.to_dict()


@app.get("/season")
def season():
    return {
        "kharif": float(df_clean['Kharif_Production'].sum()),
        "rabi": float(df_clean['Rabi_Production'].sum())
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/year/{year}")
def get_year_data(year: str):
    data = df_clean[df_clean['Year'] == year]

    total = data['Total_Production'].sum()
    kharif = data['Kharif_Production'].sum()
    rabi = data['Rabi_Production'].sum()

    return {
        "year": year,
        "total": float(total),
        "kharif": float(kharif),
        "rabi": float(rabi)
    }