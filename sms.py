import twilio
from flask import Markup

API_VERSION = '2010-04-01'
ACCOUNT_SID = 'AC...'
ACCOUNT_TOKEN = '...'
# Outgoing Caller ID previously validated with Twilio
CALLER_ID = 'NNNNNNNNNN'
account = twilio.Account(ACCOUNT_SID, ACCOUNT_TOKEN)

def build_sms(text):
    return """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Sms>%s</Sms>
</Response>
""" % (Markup.escape(text))

def send_sms(to, text):
    """We use Twilio's python libraries to send SMS.  Taken directly
     from:
     https://github.com/twilio/twilio-python/blob/master/examples/example-rest.py"""
    global account

    d = {
        "From" : CALLER_ID,
        "To" : to,
        "Body" : text
        }

    try:
        account.request('/%s/Accounts/%s/SMS/Messages' % \
                            (API_VERSION, ACCOUNT_SID), "POST", d)
    except Exception, e:
        open('error', 'w').write(e.read())
