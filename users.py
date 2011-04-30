from flask import Markup
import redis
import sys
from sms import send_sms, build_sms

try:
    r = redis.Redis(host='localhost', port=6379, db=0)
except:
    print "Cannot connect to redis server.  Exiting..."
    sys.exit(0)

def connect(number):
    """Add @number to the set of waiting callers."""
    r.sadd('waiting', number)
    ok = linkup()
    if not ok:
        return build_sms("Please wait, you will be connected to a random person...")
    return ""

def disconnect(number):
    """Remove @number from the set of waiting callers."""
    r.srem('waiting', number)
    peer = r.get(number)
    r.delete(number)
    if peer:
        r.delete(peer)
        send_sms(peer, "Your peer disconnected.")
    return build_sms("You've been disconnected and will no longer receive messages.")

def refresh(number):
    """Refresh the chat session to connect to another random person."""
    disconnect(number)
    return connect(number)

def call(number):
    """@number wishes to share the number with the other person."""
    if not r.exists(number):
        return build_sms("Error: You haven't connected to anyone yet.")
    peer_number = r.get(number)
    send_sms(peer_number, "The other person has shared their number: %s" % (number))
    return ""

def msg(number, text):
    """Message @number's peer"""
    peer = r.get(number)
    if peer is None:
        return (number, "Error: not connected, or your earlier peer disconnected. Refresh to chat again!")
    return (peer, "Stranger: " + text)

def stats(number):
    """Implement your favourite stats here. :-)"""
    pass

def linkup():
    """Links up two random people from the waiting list."""
    num_waiting = r.scard('waiting')
    if num_waiting < 2:
        # Cannot link up
        return False
    num1 = r.spop('waiting')
    num2 = r.spop('waiting')
    # our routing table
    r.set(num1, num2)
    r.set(num2, num1)
    text = "You're now connected to a random stranger!"
    send_sms(num1, text)
    send_sms(num2, text)
    return True
