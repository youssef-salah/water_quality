
from flask import Flask, request, jsonify, make_response
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
quality_predict = joblib.load('Water_Quality_final.joblib')
print(type(quality_predict))

@app.route('/water_quality', methods=['POST', 'GET'])
def handle_data():
   try:

      if request.method == 'POST':
         jdata = request.json
         jdata_df = pd.DataFrame([jdata])
         
      elif request.method == 'GET':
         # Get parameters from query string
         params = ["ph", "Hardness","Solids"
                   ,"Chloramines" , "Sulfate" ,
                     "Conductivity" , "Organic_carbon" ,
                     "Trihalomethanes" , "Turbidity"]
         jdata = {param : float (request.args.get(param , 0)) for param in params}
         jdata_df = pd.DataFrame([jdata])

      # Call predict on the model, reshape for single sample
      predicted_water_quality = quality_predict.predict(jdata_df)
      predicted_water_quality = predicted_water_quality.tolist()

# Create response with CORS headers
      response = make_response(jsonify({'Potability': predicted_water_quality[0]}))
      response.headers['Access-Control-Allow-Origin'] = '*'
      response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
      response.headers['Access-Control-Allow-Methods'] = 'GET, POST'

      return response

   except Exception as e :
      response = make_response(jsonify({'error' : str(e)}), 400)

      return response

if __name__ == '__main__':
 app.run(debug=True, host='0.0.0.0', port=3000)



