from flask import Flask, request, render_template

import requests


# this data is fetched from the IBM watson cloud service

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "sDmBUiS7WqdiqKsseDQlnfI86XrlgF_w9NZpdiVwNziF"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={
                               "apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/parameters')
def parameters():
    return render_template('parameters.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        my_dict = request.form

        area_type = str(my_dict['areatype'])
        location = float(my_dict['location'])
        roomsize = float(my_dict['roomsize'])
        sqftarea = float(my_dict['sqftarea'])
        washrooms = float(my_dict['washrooms'])
        balcony = float(my_dict['balcony'])

        input_features = [[area_type, location, roomsize,
                           sqftarea, washrooms, balcony]]

        # input = ["area_type","location","size","total_sqft","bath","balcony"]

        payload_scoring = {"input_data": [{"fields": [
            ["area_type", "location", "size", "total_sqft", "bath", "balcony"]], "values": input_features}]}

        response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/e96f36c2-d525-4f61-8b19-4ebf3b1bb5ab/predictions?version=2021-04-09',
                                         json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})

        print("Scoring response")
        predictions = response_scoring.json()
        print(predictions)
        # return render_template('predict.html')

        # {'predictions': [{'fields': ['prediction'], 'values': [[73.1356229374655]]}]}
        final_price = predictions['predictions'][0]['values'][0][0]

        final_price = round(final_price, 2)
        # print(f' The value is : {final_price}')

        return render_template('show.html', inf=final_price)
    return render_template('predict.html')


if __name__ == "__main__":
    app.run(debug=True)
