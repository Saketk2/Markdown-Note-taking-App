import logging
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
import language_tool_python
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['documents'] = 'uploads/documents'
app.config['database'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.string(200), nullable= False)
    data = db.Column(db.LargeBinary, nullable=False)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/grammar', methods = ['POST'])
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
    return render_template('suggestions.html', corr=corr, sugs=sugs, name=name)

@app.route('/save', methods = ['POST'])
def save():
    file = request.file['curr']
    if file:
        filename = secure_filename(file.name)
        data = file.read()
        duplicate = File(name=filename, data=data)
        db.session.add(duplicate)
        db.session.commit()
        return "Sucess!"
    return "Something went wrong:("

if __name__ == '__main__':
    app.run(debug=True)

