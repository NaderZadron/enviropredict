from flask import Flask, jsonify
from water import get_water_results
from air import get_air_results
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/api')
def hello():
    return 'Hello, World!'

@app.route('/api/water-results')
def water_results():
    arg = 'This is an arg from water API'
    result = get_water_results(arg)
    # result to UI = {"result": "This is the result for water: This is an arg from water API"}
    return jsonify({'result': result})

@app.route('/api/air-results')
def air_results():
    arg = 'This is an arg from Air API'
    result = get_air_results(arg)
    # result to UI = {"result": "This is the result for air: This is an arg from Air API"}
    return jsonify({'result': result})

port = int(os.getenv("PORT", 3000))
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
