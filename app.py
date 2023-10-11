from flask import Flask, render_template, request
from requests import get

app = Flask(__name__)

BASE_URL = "https://free.currconv.com/"
API_KEY = "57af6107d5a124698e14"

@app.route('/')
def index():
    currencies = get_currencies()
    return render_template('index.html', currencies=currencies)

@app.route('/convert', methods=['POST'])
def convert():
    currency1 = request.form['currency1'].upper()
    currency2 = request.form['currency2'].upper()
    amount = float(request.form['amount'])
    converted_amount = calculate_conversion(currency1, currency2, amount)
    return render_template('result.html', currency1=currency1, currency2=currency2, amount=amount, converted_amount=converted_amount)

def get_currencies():
    endpoint = f"api/v7/currencies?apiKey={API_KEY}"
    url = BASE_URL + endpoint
    data = get(url).json()['results']

    data = list(data.items())
    data.sort()

    return data

def calculate_conversion(currency1, currency2, amount):
    endpoint = f"api/v7/convert?q={currency1}_{currency2}&compact=ultra&apiKey={API_KEY}"
    url = BASE_URL + endpoint
    data = get(url).json()

    if len(data) == 0:
        return None

    rate = list(data.values())[0]
    converted_amount = rate * amount
    return converted_amount

if __name__ == '__main__':
    app.run(debug=True)
