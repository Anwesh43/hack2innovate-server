from flask import *
import flask
import json
from parser import parseSentence
from utils import get_currency
app = Flask(__name__)

app.debug = True
@app.route('/send_sms',methods=["POST"])
def send_sms():
    print(request.data)
    req_dict = request.form
    amt,credit,currency,card,ac,typ = parseSentence(req_dict["sms_message"],get_currency())
    relevant = True
    personal_account = True
    credit_category = False
    if(credit == 'credit'):
        credit_category = True
    if(card == '9999'):
        personal_account = False
    data = {"relevant":relevant,"expense":amt,"type":typ,"currency":currency,"credit_category":credit_category,"personal_account":personal_account}
    return jsonify(data)
app.run(port=9000)
