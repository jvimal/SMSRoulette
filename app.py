from flask import Flask, request, make_response
import users
from sms import build_sms, send_sms

app = Flask(__name__)

CONNECT_SYNONYMS = ['connect', 'conn', 'login', 'register']
DISCONNECT_SYNONYMS = ['disconnect', 'dc', 'logout']
REFRESH_SYNONYMS = ['refresh', 'reload']
CALL_SYNONYMS = ['call', 'share']
STATS_SYNONYMS = ['stats']

def make_sms_response(text):
    response = make_response(build_sms(text))
    response.headers['Content-Type'] = 'text/xml'
    return response

@app.route("/")
def index():
    return "SMSRoulette!"

@app.route("/sms", methods=['GET'])
def sms():
    if request.method != "GET":
        return make_sms_response("Invalid SMS.")

    # Get our parameters from the query string
    msg = request.args.get('Body')
    from_number = request.args.get('From')
    to_number = request.args.get('To')

    if not msg or not from_number or not to_number:
        return make_sms_response("Invalid SMS.")

    # Just to debug
    app.logger.warning("From: %s, To: %s, Message: %s\n" % (from_number, to_number, msg))
    cmd = msg.lower()
    if cmd in CONNECT_SYNONYMS:
        return users.connect(from_number)
    elif cmd in DISCONNECT_SYNONYMS:
        return users.disconnect(from_number)
    elif cmd in REFRESH_SYNONYMS:
        return users.refresh(from_number)
    elif cmd in CALL_SYNONYMS:
        return users.call(from_number)
    elif cmd in STATS_SYNONYMS:
        return users.stats(from_number)
    else:
        (peer_number, text) = users.msg(from_number, msg)
        send_sms(peer_number, text)
        return ""

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
