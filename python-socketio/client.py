#!/usr/bin/env python3

import sys
import inspect
from os import getenv, path

import socketio


current_dir = path.dirname(
    path.abspath(
        inspect.getfile(inspect.currentframe())
    )
)
parent_dir = path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from helpers.utils import timing, byte_to_text, \
    get_time, get_memory_usage, generate_bytes_data  # noqa


HOST = getenv('HOST', '0.0.0.0')
PORT = getenv('PORT', 7642)
NAMESPACE = '/ns'


sio = socketio.Client()


@timing
def send(message):
    print('.' * 70)
    print('Sending data at {}'.format(get_time()))
    normal_mem_usage = get_memory_usage()
    msg_size = len(message)
    print(
        'Packet size in bytes: {} ({})'.format(
            msg_size,
            byte_to_text(msg_size)
        )
    )
    print('Normal memory usage:', byte_to_text(normal_mem_usage, 5))

    sio.emit('message', message, namespace=NAMESPACE)

    sending_mem_usage = get_memory_usage()
    print(
        'Memory usage while sending:',
        byte_to_text(sending_mem_usage, 5)
    )


@sio.on('connect', namespace=NAMESPACE)
def on_connect():
    k = 1
    while k <= 24:
        size = 2 ** k
        data = generate_bytes_data(size)
        send(data)
        k += 1


def init():
    try:
        sio.connect('ws://{}:{}'.format(
            HOST, PORT
        ), namespaces=[NAMESPACE])
        sio.wait()
    except Exception as err:
        print('Error while trying to start socket client:')
        print(err)


if __name__ == '__main__':
    init()
