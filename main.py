from flask import Flask,render_template,redirect,request,session
import razorpay

app = Flask(__name__)
app.secret_key= "This_is_a_secret_key"
client = razorpay.Client(auth=("rzp_test_I4RI6OLrPcJeSM", "O0bjtxZVNQNNLbrLwOfL6p4E"))

@app.route('/', methods=["POST","GET"])
def index():
    if request.method == "POST":
        amount = request.form.get("amount")
        if not  amount:
            return "Amount cannot be empty !!", 400
        try:
            amount = float(amount)
            session['amount'] = amount
        except ValueError:
            return "Enter an Valid Amount", 400
        amount = amount * 100
        data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        pdata=[amount, payment["id"]]
        return render_template('index.html', pdata=pdata)
    if request.method == "GET":
        return render_template('index.html')

@app.route('/thank-you')
def thankyou():
    amount = session['amount'] or None
    return f"Thank You for Your Donation of {int(amount)} rupees"

@app.route('/success', methods=["POST"])
def success():
    pid=request.form.get("razorpay_payment_id")
    ordid=request.form.get("razorpay_order_id")
    sign=request.form.get("razorpay_signature")
    print(f"The payment id : {pid}, order id : {ordid} and signature : {sign}")
    params={
    'razorpay_order_id': ordid,
    'razorpay_payment_id': pid,
    'razorpay_signature': sign
    }
    final=client.utility.verify_payment_signature(params)
    if final == True:
        return redirect("/thank-you", code=301, )
    return "Something Went Wrong Please Try Again"

if __name__ == "__main__":
    app.run(debug=True)