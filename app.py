from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metadata.db'  # Example SQLite URI
db = SQLAlchemy(app)

class Metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object_name = db.Column(db.String(100))
    listeria = db.Column(db.String(20))
    apc = db.Column(db.String(20))
    salmonella = db.Column(db.String(20))
    date_of_sample = db.Column(db.String(20))
    time_of_sample = db.Column(db.String(20))
    type_of_sample = db.Column(db.String(100))
    comment = db.Column(db.Text)

@app.route('/store_metadata', methods=['POST'])
def store_metadata():
    if request.method == 'POST':
        data = request.json
        metadata = Metadata(
            object_name=data.get('object_name', ''),
            listeria=data.get('listeria', ''),
            apc=data.get('apc', ''),
            salmonella=data.get('salmonella', ''),
            date_of_sample=data.get('date_of_sample', ''),
            time_of_sample=data.get('time_of_sample', ''),
            type_of_sample=data.get('type_of_sample', ''),
            comment=data.get('comment', '')
        )
        db.session.add(metadata)
        db.session.commit()
        return 'Metadata stored successfully', 200
    else:
        return 'Method not allowed', 405

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/metadata')
def show_metadata():
    metadata = Metadata.query.all()
    return render_template('metadata.html', metadata=metadata)

# Route to delete metadata record
@app.route('/delete_metadata/<int:id>', methods=['DELETE'])
def delete_metadata(id):
    metadata = Metadata.query.get(id)
    if metadata:
        db.session.delete(metadata)
        db.session.commit()
        return 'Metadata deleted successfully', 200
    else:
        return 'Metadata not found', 404

# Route to edit metadata record
@app.route('/edit_metadata/<int:id>', methods=['PUT'])
def edit_metadata(id):
    if request.method == 'PUT':
        metadata = Metadata.query.get(id)
        if metadata:
            data = request.json
            metadata.object_name = data.get('object_name', metadata.object_name)
            metadata.listeria = data.get('listeria', metadata.listeria)
            metadata.apc = data.get('apc', metadata.apc)
            metadata.salmonella = data.get('salmonella', metadata.salmonella)
            metadata.date_of_sample = data.get('date_of_sample', metadata.date_of_sample)
            metadata.time_of_sample = data.get('time_of_sample', metadata.time_of_sample)
            metadata.type_of_sample = data.get('type_of_sample', metadata.type_of_sample)
            metadata.comment = data.get('comment', metadata.comment)
            db.session.commit()
            return 'Metadata updated successfully', 200
        else:
            return 'Metadata not found', 404
    else:
        return 'Method not allowed', 405

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,host='0.0.0.0',port='5500')
