from flask import (Flask, Blueprint, render_template,request)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bp = Blueprint('app', __name__)

# Banco de dados (Database)

user = 'cybybdou'
password = 'y-uJ7MUNigdcKOAaFRl-1gPGpYSNDs_C'
host = 'motty.db.elephantsql.com'
database = 'cybybdou'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secreta'

db = SQLAlchemy(app)

# Modelo
class Artistas(db.Model):
  # db.Integer = int / serial
  id = db.Column(db.Integer, primary_key = True)
  # db.String = varchar --- nullable = not null
  nome = db.Column(db.String(50), nullable = False)
  imagem_url = db.Column(db.String(255), nullable = False)

  # self = a própria tabela / a própria classe Filmes do python
  # aqui estamos declarando que um novo filme deve obedecer as especificações declaradas acima
  def __init__(self, nome, imagem_url):
    self.nome = nome
    self.imagem_url = imagem_url

  @staticmethod
  def read_all():
    # SELECT * from artistas order by id asc;
    return Artistas.query.order_by(Artistas.id.asc()).all()
    # SELECT * from artistas;
    #return Artistas.query.all()

  @staticmethod
  def read_single(artista_id):
    # SELECT * from artistas where id = <id_de_um_artista>;
    return Artistas.query.get(artista_id)
  
  def save(self): 
    db.session.add(self) # estamos adicionando as informações passadas no form (Nome, url) p/ o Banco de Dados (utilizando sessão)
    db.session.commit()

  def update(self, new_data):
    self.nome = new_data.nome
    self.imagem_url = new_data.imagem_url
    self.save()

  def delete(self):
    db.session.delete(self) # estamos removendo as informações de um filme do banco de dados
    db.session.commit()
  


@bp.route('/')
def home():
  return render_template('index.html')

@bp.route('/read')
def listar_artistas():
  artistas = Artistas.read_all()

  return render_template('listar-artistas.html', listaDeArtistas=artistas) # Passando para dentro do nosso HTML os dados da minha listagem de filmes!!!!

@bp.route('/read/<artista_id>')
def lista_detalhe_artista(artista_id):
  artista = Artistas.read_single(artista_id)

  return render_template('read_single.html', artista=artista)

  #Rota do Create

@bp.route('/create', methods=('GET', 'POST'))
def create():

  id_atribuido = None
#Como o método utilizado no formulário é POST, pegamos os valores dos campos
  if request.method =='POST':
    form=request.form
    artista = Artistas(form['nome'],form['imagem_url']) 
    artista.save()
    id_atribuido=artista.id
  return render_template('create.html', id_atribuido=id_atribuido)

#Rota do Update

@bp.route('/update/<artista_id>',methods=('GET', 'POST'))
def update(artista_id):
  sucesso = None
  artista = Artistas.read_single(artista_id)  

  if request.method =='POST':
    form=request.form

    new_data= Artistas(form['nome'],form['imagem_url']) 

    artista.update(new_data)

    sucesso = True

  return render_template('update.html', artista=artista, sucesso=sucesso)


@bp.route('/delete/<artista_id>') # Rota de confirmação de Delete (pedir para o usuario confirmar se ele realmente quer deletar o filme selecionado)
def delete(artista_id):
  artista = Artistas.read_single(artista_id)

  return render_template('delete.html', artista=artista)


@bp.route('/delete/<artista_id>/confirmed') # Rota que realiza de fato a deleção do filme selecionado e mostra o HTML de SUCESSO
def delete_confirmed(artista_id):
  sucesso = None

  artista = Artistas.read_single(artista_id)

  if artista:
    artista.delete()

    sucesso = True

  return render_template('delete.html', sucesso=sucesso)



@bp.route('/usuario')
def usuario():
  
  return render_template('usuario.html')



# Pega os dados do blueprint da nossa aplicação (nome do app e as rotas) e registra dentro do app do Flask
app.register_blueprint(bp)


if __name__ == '__main__':
  app.run(debug=True)
