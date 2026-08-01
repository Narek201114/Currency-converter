import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Անվճար API փոխարժեքների համար
API_URL = "https://api.frankfurter.app/latest"

@app.route('/', methods=['GET', 'POST'])
def convert_currency():
    result = None
    error = None
    
    # Հասանելի արտարժույթների ցանկ
    currencies = ["USD", "EUR", "GBP", "AMD", "RUB", "GEL", "JPY", "CAD", "AUD"]
    
    amount = 1.0
    from_curr = "USD"
    to_curr = "AMD"

    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount', 1))
            from_curr = request.form.get('from_curr', 'USD')
            to_curr = request.form.get('to_curr', 'AMD')

            if from_curr == to_curr:
                result = amount
            else:
                # Հարցում ենք ուղարկում API-ին
                response = requests.get(f"{API_URL}?from={from_curr}&to={to_curr}", timeout=5)
                data = response.json()
                
                if "rates" in data and to_curr in data["rates"]:
                    rate = data["rates"][to_curr]
                    result = round(amount * rate, 2)
                else:
                    error = "Տվյալների ստացման սխալ:"
        except Exception as e:
            error = f"Սխալ տեղի ունեցավ: {e}"

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
