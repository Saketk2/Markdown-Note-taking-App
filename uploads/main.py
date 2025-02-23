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
    tool = language_tool_python.LanguageTool('en-US')
    file = open('/' + filename)
    lines = file.readlines
    corr = []
    sugs = []
    for line in lines:
        sugs.append(tool.check(line))
        corr.append(tool.correct(line))
    return render_template('suggestions.html', {corr, sugs})

if __name__ == '__main__':
    app.run(debug=True)

