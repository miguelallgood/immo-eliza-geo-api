from fastapi import FastAPI
from predict import Item, predict

app = FastAPI()

@app.get("/")
async def root():
    """Root endpoint returning a simple message indicating that the server is alive."""
    return {"message": "alive"}

@app.post("/predict/")
async def predict_price(item: Item):
    """Endpoint for predicting the price of an item.

    Parameters:
        item (Item): An instance of the Item class containing the features of the item.

    Returns:
        dict: A dictionary containing the prediction and status code.
            - 'prediction': The predicted price.
            - 'status_code': HTTP status code indicating success (200) or failure (404).
    """
    prediction = predict(item)
    status_code = 200 if prediction else 404  # Set status code based on prediction availability
    return {"prediction": prediction, "status_code": status_code}
