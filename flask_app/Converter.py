from flask import Flask, render_template, request
from pycbrf.toolbox import ExchangeRates
from datetime import datetime

app = Flask(__name__)

cur_list = ['AUD', 'AZN', 'GBP', 'AMD', 'BYN', 'BGN', 'BRL', 'HUF', 'HKD', 'DKK', 'USD', 'EUR', 'INR', 'KZT', 'CAD',
 'KGS', 'CNY', 'MDL', 'NOK', 'PLN', 'RON', 'XDR', 'SGD', 'TJS', 'TRY', 'TMT', 'UZS', 'UAH', 'CZK', 'SEK', 'CHF',
 'ZAR', 'KRW', 'JPY']


def to_rur(amount, cur):
    date_now = datetime.strftime(datetime.now(), "%Y-%m-%d")
    rates = ExchangeRates(date_now)
    rate = float(rates[cur].value)
    return amount * rate


@app.route("/convert", methods=['GET', 'POST'])
def convert():

    if request.method == "POST":
        try:
            cur = request.form['pair']
            amount = float(request.form['amount'])
            converted_value = to_rur(amount, cur)
        except Exception:
            amount = 0.0
            converted_value = 0.0
        return render_template("Converter.html",
                               converted_value='%.2f' % (converted_value, ),
                               amount='%.2f' % (amount,), cur_list=cur_list, cur=cur)
    else:
        return render_template("Converter.html", cur_list=cur_list)


if __name__ == '__main__':
    app.run(debug=True)
