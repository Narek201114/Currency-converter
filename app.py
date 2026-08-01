import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Օգտագործում ենք ավելի հուսալի և անվճար API
API_URL = "https://open.er-api.com/v6/latest/"

@app.route('/', methods=['GET', 'POST'])
def convert_currency():
    result = None
    error = None
    
    currencies = ["USD", "EUR", "GBP", "AMD", "RUB", "GEL", "JPY", "CAD", "AUD"]
    
    amount = 1000.0
    from_curr = "USD"
    to_curr = "AMD"

    if request.method == 'POST':
        try:
            # Փոխարինում ենք ստորակետը կետով, եթե օգտատերը ստորակետ է գրել
            raw_amount = request.form.get('amount', '1').replace(',', '.')
            amount = float(raw_amount)
            from_curr = request.form.get('from_curr', 'USD')
            to_curr = request.form.get('to_curr', 'AMD')

            if from_curr == to_curr:
                result = amount
            else:
                response = requests.get(f"{API_URL}{from_curr}", timeout=5)
                data = response.json()
                
                if data.get("result") == "success" and "rates" in data and to_curr in data["rates"]:
                    rate = data["rates"][to_curr]
                    result = round(amount * rate, 2)
                else:
                    error = "Տվյալների ստացման սխալ կամ անհասանելի արժույթ:"
        except Exception as e:
            error = f"Խնդրում եմ մուտքագրել ճիշտ թիվ:"

    return render_template(
        'converter.html',
        currencies=currencies,
        result=result,
        amount=amount,
        from_curr=from_curr,
        to_curr=to_curr,
        error=error
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
