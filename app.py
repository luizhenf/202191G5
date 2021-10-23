from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///equipamentos.sqlite3'
db = SQLAlchemy(app)

class Equipamento(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    consumo = db.Column(db.Integer, nullable=False)
    tempo = db.Column(db.Integer, nullable=False)

    def __init__(self, nome, consumo, tempo):
        self.nome = nome 
        self.consumo = consumo
        self.tempo = tempo 

@app.route("/")
def index():
    equipamentos = Equipamento.query.all()
    return render_template('index.html', equipamentos=equipamentos)

@app.route('/new', methods=['GET','POST'])
def new():
    if request.method == 'POST':
        equipamento = Equipamento(
            request.form['nome'],
            request.form['consumo'],
            request.form['tempo']
        )
        db.session.add(equipamento)
        db.session.commit()
    return render_template('new.html')

@app.route("/resp")
def resp():
    media = db.session.query(func.avg(Equipamento.consumo)).all()
    soma = db.session.query(func.sum(Equipamento.consumo)).all()
    return render_template('resp.html', media=media, soma=soma)
    

if __name__ =='__main__':
    db.create_all()
    app.run(debug=True)