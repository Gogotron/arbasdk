#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Bridge for the Snap! visual programming language

    Provides a visual programming language to Arbalet for children or beginners

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
from bottle import Bottle, response, hook
from arbalet.application import Application
from webbrowser import open


class SnapServer(Application):
    def __init__(self, port, **kwargs):
        super(SnapServer, self).__init__(**kwargs)
        self.bottle = Bottle()
        self.port = int(port)
        self.route()

    def allow_cors(func):
        def wrapper(*args, **kwargs):
            response.headers['Access-Control-Allow-Origin'] = '*'  # All localhost ports would be safer
            return func(*args, **kwargs)
        return wrapper

    def route(self):
        self.bottle.route('/set_pixel/<h>/<w>/<color>', callback=self.set_pixel)
        self.bottle.route('/set_pixel_rgb/<h>/<w>/<r>/<g>/<b>', callback=self.set_pixel_rgb)
        self.bottle.route('/erase_all', callback=self.erase_all)

    def set_pixel(self, h, w, color):
        self.model.set_pixel(int(h)-1, int(w)-1, color)
        return ''

    @allow_cors
    def erase_all(self):
        self.model.set_all('black')
        return ''

    @allow_cors
    def set_pixel_rgb(self, h, w, r, g, b):
        def scale(v):
            return min(1., max(0, float(v)/100.))
        
        self.model.set_pixel(int(h)-1, int(w)-1, map(scale, [r, g, b]))
        return ''

    def run(self):
        open('http://snap.berkeley.edu/run')
        self.bottle.run(host='localhost', port=self.port)

