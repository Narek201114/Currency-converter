import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_URL = "https://open.er-api.com/v6/latest/"

@app.route('/', methods=['GET', 'POST'])
def convert_currency():
    result = None
    error = None
    
    # Ընդլայնված արտարժույթների և թանկարժեք մետաղների ցանկ
    currencies = {
        "USD": "ԱՄՆ դոլար ($)",
        "EUR": "Եվրո (€)",
        "GBP": "Բրիտանական ֆունտ (£)",
        "AMD": "Հայկական դրամ (֏)",
        "RUB": "Ռուսական ռուբլի (₽)",
        "GEL": "Վրացական լարի (₾)",
        "JPY": "Ճապոնական իեն (¥)",
        "CAD": "Կանադական դոլար (CA$)",
        "AUD": "Ավստրալիական դոլար (A$)",
        "CHF": "Շվեյցարական ֆրանկ (CHF)",
        "CNY": "Չինական յուան (¥)",
        "AED": "ԱՄԷ դիրհամ (AED)",
        "GOLD_GRAM": "Ոսկի (1 գրամ - USD)",
        "SILVER_GRAM": "Արծաթ (1 գրամ - USD)"
    }
    
    amount = 1.0
    from_curr = "USD"
    to_curr = "AMD"

    if request.method == 'POST':
        try:
            raw_amount = request.form.get('amount', '1').replace(',', '.')
            amount = float(raw_amount)
            from_curr = request.form.get('from_curr', 'USD')
            to_curr = request.form.get('to_curr', 'AMD')

            if from_curr == to_curr:
                result = amount
            else:
                # Եթե մետաղ է մասնակցում փոխարկմանը
                # Մոտավոր միջին գները 1 գրամի համար (կարող ենք ստանալ կամ ֆիքսված մոտավոր բազայով հաշվել, քանի որ մետաղների անվճար API-ները հաճախ սահմանափակ են)
                metal_prices_usd = {
                    "GOLD_GRAM": 85.0,   # Մոտավոր գին 1 գրամ ոսկու համար ԱՄՆ դոլարով (կարող է դինամիկ թարմացվել)
                    "SILVER_GRAM": 1.0   # Մոտավոր գին 1 գրամ արծաթի համար ԱՄՆ դոլարով
                }

                # Ստանում ենք ստանդարտ արտարժույթների փոխարժեքները USD-ի նկատմամբ
                response = requests.get(f"{API_URL}USD", timeout=5)
                data = response.json()
                rates = data.get("rates", {})
                rates["USD"] = 1.0
                rates["GOLD_GRAM"] = metal_prices_usd["GOLD_GRAM"]
                rates["SILVER_GRAM"] = metal_prices_usd["SILVER_GRAM"]

                # Հաշվարկ կատարելու համար
                # Նախ փոխարկում ենք 'from_curr'-ը USD-ի
                if from_curr in ["GOLD_GRAM", "SILVER_GRAM"]:
                    value_in_usd = amount * metal_prices_usd[from_curr]
                else:
                    # USD-ի նկատմամբ կուրսը
                    rate_from = rates.get(from_curr, 1)
                    value_in_usd = amount / rate_from

                # Հետո USD-ից փոխարկում ենք 'to_curr'
                if to_curr in ["GOLD_GRAM", "SILVER_GRAM"]:
                    result = round(value_in_usd / metal_prices_usd[to_curr], 4)
                else:
                    rate_to = rates.get(to_curr, 1)
                    result = round(value_in_usd * rate_to, 2)

        except Exception as e:
            error = f"Խնդրում եմ մուտքագրել ճիշտ թիվ: {e}"

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
