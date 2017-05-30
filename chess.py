#!/usr/bin/python
import os
import websocket
import thread
import time
import pdb
import json
from random import randint


def on_message(ws, message):
    print '\n'
    print message
    obj = json.loads(message)
    if 'ask_challenge' in message:
        accept_challenge(obj['data']['board_id'])
    elif 'your_turn' in message:
        board_id = obj['data']['board_id']
        turn_token = obj['data']['turn_token']
        move_figure(board_id, turn_token)


def on_error(ws, error):
    print error


def on_close(ws):
    print "### closed ###"


def connect():
    print '\n** connect **'
    ws.send(json.dumps({"action":"connect","data":{"auth_token":auth_token}}))


def challenge():
    print '\n** Challenge **'
    username = str(raw_input('Username: '))
    ws.send(json.dumps({"action":"challenge","data":{"username":username}}))


def accept_challenge(board_id):
    print '\nPress Enter to accept challenge... '
    ws.send(json.dumps({"action":"accept_challenge","data":{"board_id":board_id}}))


def move_figure(board_id, turn_token):
    from_row = randint(1, 8)
    from_col = randint(1, 8)
    to_row = randint(1, 8)
    to_col = randint(1, 8)
    print 'Figure is moved'
    ws.send(json.dumps({"action": "move", "data": {"board_id": board_id, "from_row": from_row, "from_col": from_col, "to_row": to_row, "turn_token": turn_token, "to_col": to_col}}))


auth_token = os.environ['AUTH_TOKEN']
board_id = ''
turn_token = ''


def on_open(ws):
    connect()


if __name__ == "__main__":
    websocket.enableTrace(True)
    # local: ws://0.0.0.0:5000/service
    # qa: wss://mega-chess-qa.herokuapp.com/service
    # production: wss://mega-chess.herokuapp.com/service
    ws = websocket.WebSocketApp(
        "wss://mega-chess.herokuapp.com/service",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever(
        ping_interval=10,  # seconds
    )
