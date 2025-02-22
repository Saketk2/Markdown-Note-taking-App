import logging
from flask import Flask, render_template, request
import os
import language_tool_python
app = Flask(__name__)
app.config['documents'] = 'uploads/documents'

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/success', methods = ['POST'])
def sucess():
    if request.method == 'POST':
        f = request.files['file']
        name = f.filename
        f.save(f.filename, app.config['documents'])
        return render_template('acknowledgement.html', name)

@app.route('/grammar')
def grammer(filename):
    file = open('/' + filename)
    lines = file.readlines






if __name__ == '__main__':
    app.run(debug=True)

