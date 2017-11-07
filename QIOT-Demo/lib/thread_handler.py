#!/usr/bin/env python

from threading import Event, Thread


def call_me_again(interval, function, *args):
    stopped = Event()

    def loop():
        while not stopped.wait(interval):
            function(*args)

    Thread(target=loop).start()
    return stopped.set
