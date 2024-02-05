# water.py
import json

def get_water_results(Date, State):
    # Load the predictions from the .geojson file
    with open('waterPredictions.geojson', 'r') as f:
        predictions = json.load(f)

    # Check if the state exists in the predictions
    if State in predictions:
        # Check if the date exists in the state's predictions
        if Date in predictions[State]:
            # Get the prediction for the date
            predicted_pollution = predictions[State][Date]
        else:
            predicted_pollution = "N/A"
    else:
        predicted_pollution = "N/A"

    result = f"This is the result for water: {predicted_pollution}"
    return result
