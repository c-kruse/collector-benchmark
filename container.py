#! /usr/bin/env python

import argparse

from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container


class ZapListener(MessagingHandler):
    def __init__(self, server):
        super(ZapListener, self).__init__()
        self.server = server
        self.address = "zap"

    def on_start(self, event):
        conn = event.container.connect(self.server)
        event.container.create_receiver(conn, self.address)

    def on_message(self, event):
        print(event.message.body)

class ZapSender(MessagingHandler):
    def __init__(self, server, data):
        super(ZapSender, self).__init__()
        self.server = server
        self.address = "zap"
        self.data = data

    def on_start(self, event):
        conn = event.container.connect(self.server)
        event.container.create_sender(conn, self.address)

    def on_sendable(self, event):
        event.sender.send(Message(body=self.data))
        event.connection.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', help="address", required=True)
    parser.add_argument('-p', '--payload', help="data to send")
    args = parser.parse_args()
    if args.payload:
        Container(ZapSender(args.address, args.payload)).run()
    else:
        Container(ZapListener(args.address)).run()
