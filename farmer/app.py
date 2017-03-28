from flask import Flask, request, redirect
from twilio import twiml

app = Flask(__name__)

# Try adding your own number to this list!
callers = {
    "+14158675309": "Curious George",
    "+14158675310": "Boots",
    "+14158675311": "Virgil",
}

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond and greet the caller by name."""

    from_number = request.values.get('Body', None)
    if from_number == 'Hello':
        message = "thanks for the message!"
    else:
        message = "Monkey, thanks for the message!"

    resp = twiml.Response()
    resp.message(message)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)