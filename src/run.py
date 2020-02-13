"""
 Run server.
"""

from app import APP


if __name__ == "__main__":
    APP.run(host='ngfg.com', port=8000, debug=True)
