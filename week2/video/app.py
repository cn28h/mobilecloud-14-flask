#!/usr/bin/env python
# The MIT License (MIT)
# Copyright (c) 2014 John Valko
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

from flask import Flask, request, Response, redirect, url_for, abort
from flask.ext.script import Manager
from threading import Lock

app = Flask(__name__)
manager = Manager(app)

class Video(object):
    def __init__(self, name, url, duration):
        self.name, self.url, self.duration = name, url, int(duration)

video_list = []
video_lock = Lock()

@app.route('/')
def index():
    # The only interesting bits of this example are at /video, so redirect
    # anybody who visits / there.
    return redirect(url_for('video'))

def add_video_from_post(form):
    try:
        name     = form.get('name', '').strip()
        url      = form.get('url', '').strip()
        duration = form.get('duration', '').strip()

        if len(name) < 1 or len(url) < 10 or len(duration) < 1 or \
                int(duration) <= 0:
            raise ValueError('Input validation failed')

        v = Video(name, url, duration)
        with video_lock:
            video_list.append(v)
    except ValueError:
        abort(400)

@app.route('/video', methods=('GET', 'POST'))
def video():
    rsp = ''
    if request.method == 'POST':
        add_video_from_post(request.form)
        rsp = 'Video added!\n'

    with video_lock:
        rsp += '\n'.join('{}: {}'.format(v.name, v.url) for v in video_list)
    return Response(rsp, mimetype='text/plain')

@app.route('/view/video', methods=('GET', 'POST'))
def view_video():
    rsp = '''<!doctype html><html><body>'''
    if request.method == 'POST':
        add_video_from_post(request.form)
        rsp += 'Video added!<br>\n'

    rsp += '''
          <form name='formvideo' method='POST' target='_self'>
            <fieldset><legend>Video Data</legend>
            <table><tr>
            <td><label for='name'>Name:&nbsp;</label></td>
            <td><input type='text' name='name' id='name' size='64' maxlength='64' /></td>
            </tr><tr>
            <td><label for='url'>URL:&nbsp;</label></td>
            <td><input type='text' name='url' id='url' size='64' maxlength='256' /></td>
            </tr><tr>
            <td><label for='duration'>Duration:&nbsp;</label></td>
            <td><input type='text' name='duration' id='duration' size='16' maxlength='16' /></td>
            </tr><tr>
            <td style='text-align: right;' colspan=2><input type='submit' value='Add Video' /></td>
            </tr></table></fieldset></form>'''

    with video_lock:
        rsp += '\n'.join('{}: {}<br />'.format(v.name, v.url) for v in video_list)

    return rsp + '</body></html>'

if __name__ == '__main__':
    manager.run()
