#!/usr/bin/python
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
        global next_step
        next_step = False
        accept_challenge(obj['data']['board_id'])
    elif 'your_turn' in message:
        global next_step
        next_step = move_figure
        board_id = obj['data']['board_id']
        turn_token = obj['data']['turn_token']

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def menu():
    username = str(raw_input('Username: '))
    password = str(raw_input('Password: '))
    return username, password

def register():
    print '\n** Register **'
    username, password = menu()
    global next_step
    next_step = login
    ws.send(json.dumps({"action":"register","data":{"username":username,"password":password}}))

def login():
    print '\n** Login **'
    username, password = menu()
    global next_step
    next_step = challenge
    ws.send(json.dumps({"action":"login","data":{"username":username,"password":password}}))

def challenge():
    global next_step
    next_step = False
    print '\n** Challenge **'
    username = str(raw_input('Username: '))
    ws.send(json.dumps({"action":"challenge","data":{"username":username}}))

def accept_challenge(board_id):
    raw_input('\nPress Enter to accept challenge... ')
    ws.send(json.dumps({"action":"accept_challenge","data":{"board_id":board_id}}))

def move_figure(board_id, turn_token):
    from_row = randint(1, 8)
    from_col = randint(1, 8)
    to_row = randint(1, 8)
    to_col = randint(1, 8)
    print 'Figure is moved'
    ws.send(json.dumps({"action": "move", "data": {"board_id": board_id, "from_row": from_row, "from_col": from_col, "to_row": to_row, "turn_token": turn_token, "to_col": to_col}}))

next_step = register
board_id = ''
turn_token = ''
# from_row = ''
# from_col = ''
# to_row = ''
# to_col = ''

def on_open(ws):
    def run(*args):
        while True:
            time.sleep(1)
            raw_input('Press Enter to continue...')
            if next_step: next_step()
            # time.sleep(1)
        ws.close()
        print "thread terminating..."
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://0.0.0.0:5000/service",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open

    ws.run_forever()
