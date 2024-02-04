from flask import Flask, jsonify
from water import get_water_results
from air import get_air_results

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

if __name__ == '__main__':
    app.run(port=3000, debug=True)
