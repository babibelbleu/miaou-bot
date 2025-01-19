from flask import Flask

app = Flask(__name__)

@app.route('/webhook/user_goes_live/<user_id>')
def user_goes_live(user_id):
    return "yay"
