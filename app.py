from flask import Flask, jsonify, request
from water import get_water_results
from air import get_air_results
from dotenv import load_dotenv
import os
import geopandas as gpd
import json
import geojson
from flask_cors import CORS


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api')
def hello():
    return 'Hello, World!'

@app.route('/api/predict')
def air_results():
    geojson_path = './us-state-boundaries.geojson'
    gdf = gpd.read_file(geojson_path)
    date = request.args.get('date')
    
    predicted_air_data_path = './airPredictions2.json'
    predicted_air_data = load_json_file(predicted_air_data_path)

    predicted_water_data_path = './waterPredictions.json'
    predicted_water_data = load_json_file(predicted_water_data_path)

    features_with_values = []
    for feature in gdf.iterfeatures():
        state_name = feature['properties']['name']
        air_value = next((item['Data'] for item in predicted_air_data if item['State'] == state_name and item['Date'] == date), None)
        water_value = next((item['Data'] for item in predicted_water_data if item['State'] == state_name and item['Date'] == date), None)

        feature['properties']['air'] = air_value
        feature['properties']['water'] = water_value

        features_with_values.append(feature)


    feature_collection = geojson.FeatureCollection(features_with_values)
    return jsonify(feature_collection)

@app.route('/api/current')
def current():
    geojson_path = './us-state-boundaries.geojson'
    gdf = gpd.read_file(geojson_path)

    current_air_data_path = './currentAir.json'
    current_water_data_path = './currentWater.json'
    current_air_data = load_json_file(current_air_data_path)
    current_water_data = load_json_file(current_water_data_path)

    features_with_values = []
    for feature in gdf.iterfeatures():
        state_name = feature['properties']['name']
        water_value = next((item['Data'] for item in current_water_data if item['State'] == state_name), None)
        air_value = next((item['Data'] for item in current_air_data if item['State'] == state_name), None)

        feature['properties']['water'] = water_value
        feature['properties']['air'] = air_value

        features_with_values.append(feature)

    feature_collection = geojson.FeatureCollection(features_with_values)
    return jsonify(feature_collection)




def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

port = int(os.getenv("PORT", 3001))
# port = 3002
print(port)
if __name__ == '__main__':
    # Use Gunicorn to run the Flask app
    from gunicorn.app.base import BaseApplication

    class FlaskApplication(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super(FlaskApplication, self).__init__()

        def load_config(self):
            for key, value in self.options.items():
                if key in self.cfg.settings and value is not None:
                    self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    options = {
        'bind': f'0.0.0.0:{port}',  # Bind to the provided Render port
        'workers': 1,  # Adjust the number of worker processes as needed
    }

    FlaskApplication(app, options).run()
