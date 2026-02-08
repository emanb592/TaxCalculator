
from flask import Flask, request, jsonify, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

@app.route("/", methods=['GET'])
def home():
  print('home')
  return render_template("index.html")





@app.route("/api/calcTax", methods=["POST"])
def calcTax():
    data = request.get_json(silent=True)

    # check input exists
    if not data or "a" not in data or "b" not in data or "c" not in data:
        return jsonify({"error1": "Income can not be blank"}), 400

    # check input is numeric
    try:
        a = float(data["a"])  # employment
        b = float(data["b"])  # savings
        c = float(data["c"])  # bonus
    except (ValueError, TypeError):
        return jsonify({"error4": "All incomes must be numbers"}), 400

    # check positive
    if a < 0 or b < 0 or c < 0:
        return jsonify({"error2": "Please provide positive income"}), 400

    # R1
    tax_on_employment = 0.20 * a

    # R2
    tax_on_savings = 0.0 if b <= 1000 else 0.15 * (b - 1000)



    # R3 (bonus rate depends on employment income)
    if a < 25000:
        rate = 0.20
    elif a <= 50000:
        rate = 0.40
    else:
        rate = 0.45

    tax_on_bonus = rate * c

    return jsonify({
        "taxOnEmployment": {"value": round(tax_on_employment, 2)},
        "taxOnSavings": {"value": round(tax_on_savings, 2)},
        "taxOnBonus": {"value": round(tax_on_bonus, 2)}
    }), 200


@app.route('/confirm', methods=["GET"])
def confirm_page():
     print('confirm')
     return render_template("confirm.html")

  
@app.route("/api/saveTax", methods=["POST"])
def save_incomes():
  data = request.get_json(silent=True)
  
  print('save')

  try:
    a = float(data["a"])
    b = float(data["b"])
    c = float(data["c"])


    print(a, b)
    # this is where we save the inputs in a db
    import db_incomeManager
    db_incomeManager.addIncomes(1, a, b)

    if a < 0 or b < 0:
      return jsonify({"error2": "Please provide positive income"}), 400
  
    if b < 1000:
      return jsonify({"taxIncome": 20/100*a, "taxSavings": 0, "message":"Saved"}), 200
    
    return jsonify({"taxIncome": 20/100*a, "taxSavings": 15/100*(b-1000), "message":"Saved"}), 200
    
  
  except (ValueError, TypeError):
    return jsonify({"error": "Error saving"}), 400


if __name__ == "__main__":
    app.run(debug=True)
