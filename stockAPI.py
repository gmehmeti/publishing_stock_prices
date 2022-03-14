from operator import gt
from fastapi import FastAPI, Query
import main

# python -m pip install pipreqs
# python -m  pipreqs.pipreqs --force
# python -m pip install pandas
# uvicorn stockAPI:app --reload

app = FastAPI()

@app.get("/")
def home():
    return {"Home":"Welcome to the Stock price API"}

@app.get("/get-stock-by-serialno")
def get_stock_by_serialno(serialNo: str = Query(None, description="Serial No", min_length=3),
                          date_input: str = Query(None, description="Date Input", min_length=3)):
    result = main.get_stock_by_serialno(serialNo, date_input)
    return result


@app.get("/get-stock-price")
def get_stock_price(serialNo: str = Query(None, description="Serial No", min_length=3),
                    date_input: str = Query(
                        None, description="Date Input", min_length=3),
                    take: int = Query(None, description="Take rows", gt=0)):
    result = main.get_stock_price(serialNo, date_input, take)
    return result


@app.get("/get-stock-by-no")
def get_stock_price_by_no(No: int = Query(None, description="Unique No", gt=0)):
    result = main.get_stock_by_no(No)
    return result