"""
 Run server.
"""
from app import APP, SOCKETIO


if __name__ == "__main__":
    import eventlet
    eventlet.monkey_patch()
    SOCKETIO.run(APP, host='ngfg.com', port=8000, debug=True)
    # APP.run(host='ngfg.com', port=8000, debug=True)
