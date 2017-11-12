from flask import *
import flask
import json
from parser import parseSentence
app = Flask(__name__)

app.debug = True
@app.route('/send_sms',methods=["POST"])
def send_sms():
    print(request.data)
    req_dict = json.load(request.data)
    parseSentence(req_dict["sms_body"],'INR')
    return jsonify(resp)
app.run(port=9000)
