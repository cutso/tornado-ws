#!/usr/bin/python
# coding: utf-8

import tornado.ioloop
import tornado.web
import tornado.websocket

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)

# we gonna store clients in dictionary..
clients = dict()

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        # self.write("This is your response")
        self.render('index.html')
        # self.finish()

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        self.keepconnection_alive = True
        clients[self.id] = {"id": self.id, "object": self}

    def on_message(self, message):        
        """
        when we receive some message we want some message handler..
        for this example i will just print message to console
        """
        if message == 'stop':
        	self.keepconnection_alive = False
        	self.on_close()
        	
        message = "Client %s received a message : %s" % (self.id, message)
        print message
        while self.keepconnection_alive:
        	myMessage = raw_input("Enter something: ")
        	self.write_message(u"You said: " + myMessage)
        
    def on_close(self):
    	self.keepconnection_alive = False
        if self.id in clients:
            del clients[self.id]

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/test/', WebSocketHandler),
])

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


    