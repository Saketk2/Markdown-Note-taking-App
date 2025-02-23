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
        print(request.files)
        f = request.files.get('curr')
        name = f.filename
        file_path = os.path.join(app.config['documents'], name)
        f.save(file_path)
        return render_template('acknowledgement.html', n=name)

@app.route('/grammar')
def grammer():
    tool = language_tool_python.LanguageTool('en-US')
    file = request.files.get('curr')
    name = file.filename
    file_path = os.path.join(app.config['documents'], name)
    file.save(file_path)
    with open(file_path, 'r') as c:
        lines = c.readlines()
    corr = []
    sugs = []
    for line in lines:
        sugs.append(tool.check(line))
        corr.append(tool.correct(line))
    return render_template('suggestions.html', corr=corr, sugs=sugs)

if __name__ == '__main__':
    app.run(debug=True)

