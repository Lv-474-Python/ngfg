"""
Sockets module
"""
from app import SOCKETIO

@SOCKETIO.on('connect')
def test_connect():
    print("someone connected")
    #emit('after connect',  {'data':'Lets dance'})
