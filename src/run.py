"""
 Run server.
"""
from app import APP, SOCKETIO


if __name__ == "__main__":
    SOCKETIO.run(APP, host='ngfg.com', port=8000, debug=True)
