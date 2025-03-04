import logging
import markdown
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
import language_tool_python
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['documents'] = 'uploads/documents'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_name.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable= False)
    data = db.Column(db.LargeBinary, nullable=False)

with app.app_context():
    db.create_all()

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

@app.route('/save', methods=['POST'])
def save():
    filename = request.form.get('name')

    if filename:
        file_path = os.path.join(app.config['documents'], filename)
        
        with open(file_path, 'r') as file_data:
            data = file_data.read()
        
        temp = data.encode('utf-8')
        duplicate = File(name=filename, data=temp)
        db.session.add(duplicate)
        db.session.commit()
        
        return render_template('options.html')
    
    return "Something went wrong", 400

@app.route('/saved')
def saved():
    notes = File.query.all()
    return render_template('saved.html', notes=notes)

@app.route('/convert', methods = ['POST'])
def convert():
    filename = request.form.get('name')

    if filename:
        file_path = os.path.join(app.config['documents'], filename)
        
        with open(file_path, 'r') as file_data:
            temp = file_data.read()
        
        tempHtml = markdown.markdown(temp, extensions = ['extra'])
        soup = BeautifulSoup(tempHtml, "html.parser")
        final = soup.prettify()

        return render_template('convert.html', final=final)



if __name__ == '__main__':
    app.run(debug=True)

