from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import desc


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
    equipamentos = Equipamento.query.all()
    un = db.session.query(Equipamento.nome).filter(True == True).order_by(desc(Equipamento.id)).first()
    uc = db.session.query(Equipamento.consumo).filter(True == True).order_by(desc(Equipamento.id)).first()
    sumcotv = db.session.query(func.sum(Equipamento.consumo)).filter(Equipamento.nome=='Televisão').first()
    sumtetv = db.session.query(func.sum(Equipamento.tempo)).filter(Equipamento.nome=='Televisão').first()
    medge = db.session.query(func.avg(Equipamento.consumo)).filter(Equipamento.nome=='Geladeira').first()
    medlr = db.session.query(func.avg(Equipamento.consumo)).filter(Equipamento.nome=='Lava Roupas').first()
    medmo = db.session.query(func.avg(Equipamento.consumo)).filter(Equipamento.nome=='Microondas').first()
    medac = db.session.query(func.avg(Equipamento.consumo)).filter(Equipamento.nome=='Ar Condicionado').first()
    return render_template('resp.html', un=un, uc=uc, sumcotv=sumcotv, sumtetv=sumtetv, equipamentos=equipamentos, medge=medge, medlr=medlr, medmo=medmo, medac=medac)
    

if __name__ =='__main__':
    db.create_all()
    app.run(debug=True)