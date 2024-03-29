import joblib
from sklearn.preprocessing import StandardScaler
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    number_rooms: float
    living_area: float
    garden_area: float
    number_facades: float
    Longitude: float
    Latitude: float    

def predict(item: Item) -> Optional[float]:
    # Load your trained model
    model = joblib.load('api/new_best_model.pkl')

    # Load your stored scaler
    scaler = joblib.load('api/new_input_scaler.pkl')

    # Define feature names
    feature_names = ['number_rooms', 'living_area', 'garden_area', 'number_facades', 'Longitude', 'Latitude']

    # Prepare input data
    input_data = [[item.number_rooms, item.living_area, item.garden_area, item.number_facades, item.Longitude, item.Latitude]]

    # Transform input data
    input_data_scaled = scaler.transform(input_data)

    # Set feature names on the model
    model.feature_names = feature_names

    # Make prediction
    prediction_scaled = model.predict(input_data_scaled)

    # Load the scaler used for 'price' during training
    price_scaler = joblib.load('api/new_target_scaler.pkl')

    # Inverse transform prediction
    prediction = price_scaler.inverse_transform(prediction_scaled.reshape(-1, 1))

    return prediction[0][0] if prediction else None
