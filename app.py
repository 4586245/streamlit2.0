from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import os
import uvicorn
from random import uniform

app = FastAPI()

DATA_PATH = "insurance.csv"
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"{DATA_PATH} not found.")

df = pd.read_csv(DATA_PATH)


class MatchDataRequest(BaseModel):
    age: int
    bmi: float
    gender: str
    children: int
    smoke: str
    region: str


class AddDataRequest(BaseModel):
    age: int
    bmi: float
    sex: str
    children: int
    smoker: str
    region: str
    charges: float


@app.post("/submit_form")
def submit_form(data: MatchDataRequest):
    global df

    filtered_data = df[
        (df["age"] >= data.age - 10) & (df["age"] <= data.age + 10) &
        (df["bmi"] >= data.bmi - 10) & (df["bmi"] <= data.bmi + 10) &
        (df["sex"].str.lower() == data.gender.lower()) &
        (df["children"] == data.children) &
        (df["smoker"].str.lower() == data.smoke.lower()) &
        (df["region"].str.lower() == data.region.lower())
        ]

    if not filtered_data.empty:
        avg_charges = filtered_data["charges"].mean()
        return {
            "message": "Matching data found.",
            "average_charges": round(avg_charges, 2),
            "matches": filtered_data.to_dict(orient="records"),
        }
    else:
        min_charge = df["charges"].min()
        max_charge = df["charges"].max()
        random_charge = uniform(min_charge, max_charge)
        return {
            "message": "No matching data found. Returning a random charge.",
            "random_charge": round(random_charge, 2),
        }


@app.post("/add_data")
def add_data(data: AddDataRequest):
    global df
    new_row = {
        "age": data.age,
        "bmi": data.bmi,
        "sex": data.sex,
        "children": data.children,
        "smoker": data.smoker,
        "region": data.region,
        "charges": data.charges,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)
    return {"message": "Data added successfully!", "data": new_row}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
