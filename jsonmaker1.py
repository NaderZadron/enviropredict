import os
import pandas as pd
import json
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

def predict_pollution(dates, state):
    # Load the data
    df = pd.read_csv('Air_ML/cleaned_data_air.csv')  # Assuming the CSV is in the 'Air_ML' folder
    us_states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
    
    # Initialize an empty dictionary to store the predictions
    predictions = {}

    # Load the model
    if state.lower() == 'all':
        states = us_states
    else:
        states = [state]

    for state in states:
        model_path = 'Air_ML/my_model'+state+'.h5'
        if os.path.exists(model_path):
            model = load_model(model_path)
            # Define the scaler
            scaler = MinMaxScaler()
            # Filter data for a specific state
            df_state = df[df['State'] == state]

            # Convert 'Date_Local' to datetime and extract the year, month, and day as integers
            df_state['Date_Local'] = pd.to_datetime(df_state['Date_Local'], format='%Y-%m-%d')
            df_state.loc[:, 'Year'] = df_state['Date_Local'].dt.year  # Corrected usage of .loc
            df_state.loc[:, 'Month'] = df_state['Date_Local'].dt.month
            df_state.loc[:, 'Day'] = df_state['Date_Local'].dt.day

            # Define the features
            X = df_state[['Year', 'Month', 'Day']]

            # Fit the scaler
            scaler.fit(X)

            # Prepare the dates
            dates = pd.to_datetime(dates, format='%m/%Y')
            future = np.array([[date.year, date.month, 1] for date in dates])
            future_normalized = scaler.transform(future)
            future_normalized = np.reshape(future_normalized, (future_normalized.shape[0], 1, future_normalized.shape[1]))

            # Use the model to make a prediction
            forecast = model.predict(future_normalized)

            # Store the prediction in the dictionary
            predictions[state] = {dates[i].strftime("%m/%Y"): float(y[0]) for i, y in enumerate(forecast)}
        else:
            predictions[state] = "N/A"

    # Convert the dictionary to a .geojson file
    with open('airPredictions.geojson', 'w') as f:
        json.dump(predictions, f)

# Call the function
predict_pollution(['02/2024', '03/2024', '04/2024','05/2024','06/2024','07/2024','08/2024','09/2024','10/2024','11/2024','12/2024','01/2025','02/2024'],'All')