from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metadatum.db'  # Example SQLite URI
db = SQLAlchemy(app)

class Metadatum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object_name = db.Column(db.String(100))
    listeria = db.Column(db.String(20))
    apc = db.Column(db.String(20))
    salmonella = db.Column(db.String(20))
    date_of_sample = db.Column(db.String(20))
    time_of_sample = db.Column(db.String(20))
    type_of_sample = db.Column(db.String(100))  # Add type_of_sample column
    comment = db.Column(db.Text)

@app.route('/store_metadata', methods=['POST'])
def store_metadata():
    if request.method == 'POST':
        data = request.json
        metadatum = Metadatum(
            object_name=data.get('object_name', ''),
            listeria=data.get('listeria', ''),
            apc=data.get('apc', ''),
            salmonella=data.get('salmonella', ''),
            date_of_sample=data.get('date_of_sample', ''),
            time_of_sample=data.get('time_of_sample', ''),
            type_of_sample=data.get('type_of_sample', ''),  # Get type_of_sample from data
            comment=data.get('comment', '')
        )
        db.session.add(metadatum)
        db.session.commit()
        return 'Metadata stored successfully', 200
    else:
        return 'Method not allowed', 405

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

