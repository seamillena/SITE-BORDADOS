from flask import Flask, flash,  get_flashed_messages, render_template, request, redirect, session, url_for, make_response, send_from_directory, Response
from flask_mysqldb import MySQL # type: ignore
from collections import defaultdict
from dotenv import load_dotenv # type: ignore
import pymysql # type: ignore
import uuid
import os
from werkzeug.utils import secure_filename
import random
import string
from datetime import datetime, timedelta
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import re
from itsdangerous import URLSafeTimedSerializer
from bson.regex import Regex # type: ignore
import smtplib
from flask import jsonify
from pymongo import MongoClient # type: ignore
from email.message import EmailMessage
import smtplib
from email.mime.text import MIMEText
from rapidfuzz import fuzz # type: ignore
from unidecode import unidecode # type: ignore




load_dotenv()  # Carrega o .env

# CONFIGURAÇÕES


chave_confirmacao = os.getenv('chave_confirmacao')

s = URLSafeTimedSerializer(os.getenv('chave_confirmacao'))


#DEF CONFIGURAÇÕES E SUPORTE

app = Flask(__name__)




conexao = mysql.connector.connect(
    host='localhost',
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)


mongo_uri = os.getenv("MONGO_URI")
mongo_db_nome = os.getenv("MONGO_DB")
mongo_collection_nome = os.getenv("MONGO_COLLECTION")

cliente_mongo = MongoClient(mongo_uri)
mongo_db = cliente_mongo[mongo_db_nome]
colecao_detalhes = mongo_db[mongo_collection_nome]

app.config['UPLOAD_FOLDER'] = 'static/imagens'

app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key_here')

mysql = MySQL(app)

def enviar_email(email):
    cur = conexao.cursor()
    cur.execute("SELECT codigo_email FROM login JOIN usuarios ON login.email = usuarios.email  WHERE login.email = %s", (email,))
    resultado = cur.fetchone()
    codigo_email = resultado[0]
    cur.close()

    email_principal = os.getenv("meu_email")
    senha_app = os.getenv("senha_app")
    link = f"http://127.0.0.1:5000/cadastro?email={email}&codigo_email={codigo_email}&menu=confirmar_email"

    msg = MIMEText(
    "Seu código de verificação é: {}\nClique no link para confirmar seu e-mail: {}" \
    " Este código expira em uma (1) hora!".format(codigo_email, link))

    msg["Subject"] = "CÓDIGO DE VERIFICAÇÃO - O ASTRONAUTA BORDADOS "
    msg["From"] = email_principal
    msg["To"] = email

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()  # inicia conexão segura
        smtp.login(email_principal, senha_app)
        smtp.send_message(msg)
    

def get_id():
    cur = conexao.cursor()
    cur.execute("SELECT MAX(id) FROM bordados")
    resultado = cur.fetchone()
    id_atual = resultado[0] if resultado[0] is not None else 0
    cur.close()
    id = id_atual + 1
    return id

def gerar_codigo_pedido(tamanho=10):
    caracteres = string.ascii_uppercase + string.digits
    codigo = ''.join(random.choices(caracteres, k=tamanho))
    return codigo

def gerar_publicacao(tamanho=15):
    caracteres = string.ascii_uppercase + string.digits
    publicacao = ''.join(random.choices(caracteres, k=tamanho))
    return publicacao

def gerar_codigo_email(tamanho=6):
    caracteres = string.ascii_uppercase + string.digits
    codigo_email = ''.join(random.choices(caracteres, k=tamanho))
    return codigo_email

@app.route('/user')
def user():
    usuario_id = request.cookies.get("usuario_id")
    return f"<p>Usuário ID: {usuario_id}</p>"

def notificacao_carrinho():
    id_usuario = request.cookies.get('usuario_id')
    if not id_usuario:
        return False 
    usuario = 'usuario'
    cur = conexao.cursor()
    cur.execute("SELECT COUNT(*) FROM carrinhos WHERE id_usuario = %s AND usuario = %s", (id_usuario, usuario,))
    count = cur.fetchone()[0]
    cur.close()

    return count > 0 

def notificacao_carrinho_cliente():
    id_usuario = request.cookies.get('usuario_id')
    if not id_usuario:
        return False
    usuario = session.get('usuario')
    cur = conexao.cursor()
    cur.execute("SELECT COUNT(*) FROM carrinhos WHERE id_usuario = %s AND usuario = %s", (id_usuario, usuario))
    count = cur.fetchone()[0]
    cur.close()

    return count > 0 

def get_contatos():
    cur = conexao.cursor()
    cur.execute("SELECT * FROM contatos")
    dados = cur.fetchall()
    colunas = [desc[0]for desc in cur.description]
    cur.close()

    contatos = [dict(zip(colunas, linha)) for linha in dados]

    return contatos

@app.context_processor
def inject_contatos():
    return {'contatos' :get_contatos()}

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

def verificar_admin():
    usuario = session.get('usuario')
    if 'usuario' not in session:
        return False

    
    cur = conexao.cursor()
    cur.execute("SELECT tipo FROM usuarios WHERE usuario = %s", (usuario,))
    resultado = cur.fetchone()
    cur.close()

    return resultado and resultado[0] == 'administrador'

def verificar_cliente():
    if 'usuario' not in session:
        return False

    usuario = session.get('usuario')
    cur = conexao.cursor()
    cur.execute("SELECT tipo FROM usuarios WHERE usuario = %s", (usuario,))
    resultado = cur.fetchone()
    cur.close()

    return resultado and resultado[0] == 'cliente'


def codigo_senha(senha):
    return generate_password_hash(senha)


def verificar_senha(senha_hash,senha):
    return check_password_hash(senha_hash,senha)


def verificar_usuario(usuario):
    cur = conexao.cursor()
    cur.execute("SELECT usuario FROM usuarios WHERE usuario = %s", (usuario,))
    resultado = cur.fetchone()
    cur.close()
    if not resultado:
        return False
    else:
        return resultado[0]

def verificar_tentativas(usuario):
    cur = conexao.cursor()
    cur.execute("SELECT login.tentativas FROM login JOIN usuarios ON login.email = usuarios.email WHERE usuarios.usuario = %s", (usuario,))
    resultado = cur.fetchone()
    cur.close()
    if resultado:
        return resultado[0]
    else:
        return 0

def usuario_existente(usuario):
    cur = conexao.cursor()
    cur.execute("SELECT usuario FROM usuarios WHERE usuario = %s", (usuario,))
    resultado = cur.fetchone()
    cur.close()
    return resultado
    
def email_cadastrado(email):
    cur = conexao.cursor()
    cur.execute("SELECT email FROM usuarios WHERE email = %s", (email,))
    resultado = cur.fetchone()
    cur.close()
    if resultado:
        return resultado[0]
    

def usuario_valido(usuario):
    return re.match(r'^[a-zA-Z0-9._-]+$', usuario) is not None

@app.route('/verificar_email', methods=['GET','POST'])
def verificar_email():
    email = request.form.get('email')
    codigo_email = gerar_codigo_email()
    hora = datetime.now()
    
    cur = conexao.cursor()
    cur.execute('UPDATE login SET codigo_email = %s, hora = %s WHERE email = %s',(codigo_email, hora, email,))
    conexao.commit()
    cur.close()

    enviar_email(email)
    mensagem = 'Email de confirmação enviado!'
    return render_template('cadastro.html', mensagem=mensagem)


@app.route('/login', methods=['GET', 'POST'])
def login():
    mensagem = None
    usuario = ''
    senha = ''
    if request.method== 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if usuario == '':
            mensagem = "Informe o usuário para efetuar login"

        if usuario and not senha:
            mensagem = "Insira a senha para efetuar login"

        else:    
            if verificar_tentativas(usuario) >= 5:
                mensagem = "Muitas tentativas, verifique sua conta para concluir login"
                cur = conexao.cursor()
                cur.execute('UPDATE login JOIN usuarios ON login.email = usuarios.email SET login.verificado = 0 WHERE usuarios.usuario = %s',(usuario,))
                conexao.commit()
                cur.close()
            else:
                if verificar_usuario(usuario):
                    cur = conexao.cursor()
                    cur.execute("SELECT senha FROM usuarios WHERE usuario = %s", (usuario,))
                    resultado = cur.fetchone()
                    senha_hash = resultado[0]
                    cur.close()

                    if verificar_senha(senha_hash, senha):
                        session['usuario'] = usuario
                        cur = conexao.cursor()
                        cur.execute("UPDATE login JOIN usuarios ON login.email = usuarios.email SET login.tentativas = 0 WHERE usuarios.usuario = %s", (usuario,))
                        conexao.commit()
                        cur.close()
                        return redirect(url_for('inicio'))
                    else:
                        cur = conexao.cursor()
                        cur.execute("UPDATE login JOIN usuarios on login.email = usuarios.email SET tentativas = tentativas + 1 WHERE usuario = %s", (usuario,))
                        conexao.commit()
                        cur.close()

                        cur = conexao.cursor()
                        cur.execute("SELECT tentativas FROM login JOIN usuarios on login.email = usuarios.email WHERE usuario = %s", (usuario,))
                        tentativas = cur.fetchone()[0]
                        cur.close()
                        mensagem = "Senha incorreta. Tentativas restantes: {}".format(5 - tentativas)

                    
                if not verificar_usuario(usuario):
                    mensagem = "usuario não cadastrado"
                

    return render_template('login.html', mensagem=mensagem, usuario=usuario)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    mensagem = None
    usuario=''
    menu = request.args.get('menu')
    codigo_email = gerar_codigo_email()
    if request.method == 'POST':
        
        usuario = request.form.get('novo_usuario')
        senha = request.form.get('nova_senha')
        confirmar_senha = request.form.get('confirmar_senha')
        nome = request.form.get('novo_nome')
        sobrenome = request.form.get('novo_sobrenome')
        telefone = request.form.get('novo_telefone')
        email = request.form.get('novo_email')
        confirmar_email = request.form.get('confirmar_email')
        senha_codificada = codigo_senha(senha)

        if usuario_existente(usuario):
            mensagem = 'Usuario existente'
            return render_template('cadastro.html', mensagem = mensagem)
        
        if email_cadastrado(email):
            mensagem = 'Este email já foi cadastrado'
            return render_template('cadastro.html', mensagem = mensagem)
               

        if senha != confirmar_senha:
            mensagem = 'Senhas não conferem'
            return render_template('cadastro.html', mensagem = mensagem)
        
        if not usuario_valido(usuario):
            mensagem = 'Usuario inválido'
            return render_template('cadastro.html', mensagem = mensagem)
        if email != confirmar_email:
            mensagem = 'Emails não conferem'
            return render_template('cadastro.html', mensagem = mensagem)
        else:
            hora = datetime.now()
            cur = conexao.cursor()    
            cur.execute("INSERT INTO usuarios (usuario, senha, nome, sobrenome, telefone, email, tipo) VALUES (%s, %s, %s, %s, %s, %s, 'cliente')", (usuario, senha_codificada, nome, sobrenome, telefone, email,))
            conexao.commit()
            cur.close()
            
            cur = conexao.cursor()
            cur.execute("INSERT INTO login(email, codigo_email, hora) VALUES(%s,%s,%s)",(email, codigo_email, hora,))
            conexao.commit()
            cur.close()
            mensagem = 'Cadastro realizado com sucesso'

            cur = conexao.cursor()
            cur.execute("SELECT email FROM usuarios where usuario = %s", (usuario,))
            resultado = cur.fetchone()
            email = resultado[0]
            enviar_email(email)
            cur.close()
            return render_template('cadastro.html', menu='cadastrado')

    email = request.args.get('email')
    codigo_email = request.args.get('codigo_email')

    return render_template('cadastro.html', mensagem=mensagem, menu=menu, email=email, codigo_email=codigo_email)



#DEF USUÁRIOS
@app.route('/confirmar_email', methods=['GET', 'POST'])
def confirmar_email():
    menu = 'confirmar_email'
    codigo_email = request.form.get('codigo_email')
    email = request.form.get('email')

    cur = conexao.cursor()
    cur.execute('SELECT verificado FROM login WHERE email = %s', (email,))
    verificado = cur.fetchone()
    cur.close()

    if verificado[0] ==1:
        mensagem_verificado = 'Este email já foi verificado.'

    else:

        cur = conexao.cursor()
        cur.execute('SELECT codigo_email FROM login WHERE email = %s AND hora > NOW() - INTERVAL 1 HOUR', (email,))
        resultado = cur.fetchone()
        cur.close()
        

        if resultado and resultado[0] == codigo_email:
            cur = conexao.cursor()
            cur.execute("UPDATE login SET verificado = 1 WHERE email = %s", (email,))
            conexao.commit()
            
            cur.execute('SELECT usuario FROM usuarios WHERE email = %s',(email,))
            usuario = cur.fetchone()[0]  # Pega apenas o nome do usuário
            cur.close()
            return render_template('login.html', usuario=usuario)
        
        else:
            mensagem = 'Código expirado.'
        return render_template('cadastro.html', menu=menu, mensagem=mensagem, email=email)

    return render_template('cadastro.html', menu=menu, mensagem_verificado=mensagem_verificado, email=email)



@app.route('/')
def inicio():
    cur = conexao.cursor()
    cur.execute("SELECT * FROM iniciodb")
    dados = cur.fetchall()
        
    cur.execute("SHOW COLUMNS FROM iniciodb")
    colunas = [col[0] for col in cur.fetchall()]
    
    cur.close()

    iniciodb = [dict(zip(colunas, linha)) for linha in dados]
    item_carrinho = notificacao_carrinho()
    tipo = 'usuario'
   
    if verificar_admin():
        tipo = 'administrador'

    if verificar_cliente():
       tipo = 'cliente'

    return render_template('inicio.html', iniciodb=iniciodb, item_carrinho=item_carrinho, tipo=tipo)


@app.route('/catalogo')
def catalogo():
    tema = request.args.get('tema')
    pesquisa = request.args.get('pesquisa', '')
    pesquisa_normalizada = unidecode(pesquisa.lower())
    
    cur = conexao.cursor()
    cur.execute("SELECT * FROM bordados ORDER BY id ASC")
    dados = cur.fetchall()
    cur.close()

    cur = conexao.cursor()
    cur.execute("SHOW COLUMNS FROM bordados")
    colunas = [col[0] for col in cur.fetchall()]
    cur.close()

    bordados = [dict(zip(colunas, linha)) for linha in dados]

    documentos = colecao_detalhes.find({}, {"id": 1, "descricao": 1, "temas": 1})

    ids_com_descricao = set()
    temas_por_id = {}
    lista_temas = set()

    for doc in documentos:
        doc_id = doc["id"]
        descricao = doc.get("descricao", "")

        # Se descricao for lista, junta tudo numa string só
        if isinstance(descricao, list):
            descricao = " ".join(descricao)

        texto = unidecode(descricao.lower())

        temas = doc.get("temas", [])
        if isinstance(temas, str):
            temas = [t.strip() for t in temas.split(',')]
        temas = [t for t in temas if isinstance(t, str)]
        temas_normalizados = [unidecode(t.lower()) for t in temas]

        descricao_match = fuzz.partial_ratio(pesquisa_normalizada, texto) >= 70
        temas_match = any(fuzz.partial_ratio(pesquisa_normalizada, tema) >= 70 for tema in temas_normalizados)

        if descricao_match or temas_match:
            ids_com_descricao.add(doc_id)

        temas_cap = [t.capitalize() for t in temas]
        temas_por_id[doc_id] = temas_cap
        lista_temas.update(temas_cap)

    temas_ordenados = sorted(lista_temas)

    bordados_filtrados = []
    for bordado in bordados:
        bordado_id = bordado["id"]
        temas_do_bordado = temas_por_id.get(bordado_id, [])
        bordado["temas"] = temas_do_bordado

        if pesquisa:
            if bordado_id in ids_com_descricao:
                bordados_filtrados.append(bordado)
        elif not tema or tema.lower() == "todos":
            bordados_filtrados.append(bordado)
        elif any(tema.lower() == t.lower() for t in temas_do_bordado):
            bordados_filtrados.append(bordado)

    item_carrinho = notificacao_carrinho()

    tipo = 'usuario'
    if verificar_admin():
        tipo = 'administrador'
    if verificar_cliente():
        tipo = 'cliente'

    return render_template('catalogo.html',
                           bordados=bordados_filtrados,
                           temas_ordenados=temas_ordenados,
                           tema_atual=tema,
                           item_carrinho=item_carrinho,
                           tipo=tipo,
                           pesquisa=pesquisa)



@app.route('/detalhes/<int:id>')
def detalhes(id):

    tema = request.args.get('tema') 
    if not tema:
        tema = 'todos'

    cur = conexao.cursor()
    cur.execute("SELECT * FROM bordados WHERE id = %s", (id,))
    resultado = cur.fetchone()
    cur.close()

    cur = conexao.cursor()
    cur.execute("SHOW COLUMNS FROM bordados")
    colunas = [col[0] for col in cur.fetchall()]
    cur.close()
    
    cur = conexao.cursor()
    cur.execute("SELECT * FROM bordados ORDER BY id ASC")
    bordados_com_tema = cur.fetchall()
    cur.close()

    if resultado:
        bordado = dict(zip(colunas, resultado))
        item_carrinho = notificacao_carrinho()

        # Pega os detalhes do Mongo pelo id do bordado
        detalhes_mongo = colecao_detalhes.find_one({"id": id})

        # Monta a lista de imagens
        imagens = []

        # Imagem principal (SQL)
        if bordado.get("imagem"):
            imagens.append(bordado["imagem"])

        # Imagens extras (MongoDB)
        if detalhes_mongo and detalhes_mongo.get("imagens_extras"):
            extras = detalhes_mongo["imagens_extras"]
            if isinstance(extras, str):
                extras = [i.strip() for i in extras.split(',') if i.strip()]
            imagens.extend(extras)

        # Adiciona ao objeto bordado
        bordado["imagens"] = imagens
        

        if tema.lower() != "todos":
            bordados_com_tema_filtrados = []
            for b in bordados_com_tema:
                mongo = colecao_detalhes.find_one({"id": b[0]}, {"temas": 1})
                if mongo and "temas" in mongo:
                    if any(tema.lower() == t.lower() for t in mongo["temas"]):
                        bordados_com_tema_filtrados.append(b)
            bordados_com_tema = bordados_com_tema_filtrados
            documentos_filtrados = list(colecao_detalhes.find(
                {"temas": {"$regex": f"^{tema}$", "$options": "i"}},
                {"id": 1}
            ))
        else:
            documentos_filtrados = list(colecao_detalhes.find({}, {"id": 1}))

        bordado_ids = [doc["id"] for doc in documentos_filtrados]

        current_index = bordado_ids.index(id)
        
        cur = conexao.cursor()
        cur.execute("SELECT * FROM bordados ORDER BY nome ASC")
        dados = cur.fetchall()
        cur.close()
    
        bordados = [dict(zip(colunas, linha)) for linha in dados]

        next_id = bordado_ids[(current_index + 1) % len(bordado_ids)]
        prev_id = bordado_ids[(current_index - 1) % len(bordado_ids)]
        tipo = 'usuario'
    
        if verificar_admin():
            tipo ='administrador'
        if verificar_cliente():
            tipo = 'cliente'

        mongo_detalhes = colecao_detalhes.find_one({"id": id})
        detalhes_bordados = mongo_detalhes.get("descricao", []) if mongo_detalhes else []


        if isinstance(detalhes_bordados, str):
            detalhes_bordados = [d.strip() for d in detalhes_bordados.split(",") if d.strip()]
        

        return render_template('detalhes.html',bordados=bordados, tipo=tipo, bordado=bordado, tema=tema, next_id=next_id, prev_id=prev_id, item_carrinho=item_carrinho,detalhes_bordados=detalhes_bordados)
        

@app.route('/atualizar_carrinho', methods=['POST'])
def atualizar_carrinho():

    id_bordado = request.form.get('id')
    id_usuario = request.cookies.get('usuario_id')
    usuario = 'usuario'
    if not id_usuario:
        id_usuario = str(uuid.uuid4())
        response = make_response(redirect(url_for('detalhes', id=id_bordado)))
        response.set_cookie('usuario_id', id_usuario)
        return response

    cur = conexao.cursor()
    cur.execute("SELECT quantidade FROM carrinhos WHERE id_usuario = %s AND id_bordado = %s AND usuario = %s", (id_usuario, id_bordado, usuario))
    resultado = cur.fetchone()
    cur.close()

    if resultado:
        cur = conexao.cursor()
        cur.execute("UPDATE carrinhos SET quantidade = quantidade + 1 WHERE id_usuario = %s AND id_bordado = %s AND usuario =%s", (id_usuario, id_bordado, usuario))
        conexao.commit()
        cur.close()

    else:
        cur = conexao.cursor()
        cur.execute("INSERT INTO carrinhos (id_usuario, id_bordado, usuario, quantidade) VALUES (%s, %s, %s, 1)", (id_usuario, id_bordado, usuario))
        conexao.commit()
        cur.close()    

    return redirect(url_for('detalhes', id=id_bordado))

@app.route('/esvaziar_carrinho', methods=['POST'])
def esvaziar_carrinho():
    id_usuario = request.cookies.get('usuario_id')
    if not id_usuario:
        return redirect(url_for('carrinho'))
    usuario = 'usuario'
    
    cur = conexao.cursor()
    cur.execute("DELETE FROM carrinhos WHERE id_usuario = %s AND usuario =%s", (id_usuario, usuario))
    conexao.commit()
    cur.close()

    return redirect(url_for('carrinho'))

@app.route('/remover_item', methods=['POST'])
def remover_item():
    id_usuario = request.cookies.get('usuario_id')
    id_bordado = request.form.get('id')
    usuario = 'usuario'
    if not id_usuario or not id_bordado:
        return redirect(url_for('carrinho'))

    cur = conexao.cursor()
    cur.execute("DELETE FROM carrinhos WHERE id_usuario = %s AND id_bordado = %s AND usuario = %s", (id_usuario, id_bordado, usuario))
    conexao.commit()
    cur.close()

    return redirect(url_for('carrinho'))

@app.route('/quantidade', methods=['POST'])
def quantidade():
    id_usuario = request.cookies.get('usuario_id')
    if not id_usuario:
        return redirect(url_for('carrinho'))

    cur = conexao.cursor()
    cur.execute("SELECT id_bordado FROM carrinhos WHERE id_usuario = %s AND usuario = %s", (id_usuario, usuario))
    dados = cur.fetchall()
    cur.close()

    usuario = 'usuario'
    for linha in dados:
        id_bordado = linha[0]
        campo_quantidade = f'quantidade_{id_bordado}'
        nova_quantidade = request.form.get(campo_quantidade)

        if nova_quantidade and nova_quantidade.isdigit() and int(nova_quantidade) > 0:
            cur = conexao.cursor()
            cur.execute("UPDATE carrinhos SET quantidade = %s WHERE id_usuario = %s AND id_bordado = %s AND usuario = %s",(int(nova_quantidade), id_usuario, id_bordado, usuario))
            conexao.commit()
            cur.close()

    return redirect(url_for('carrinho'))


@app.route('/realizar_pedido', methods=['POST'])
def realizar_pedido():
    id_usuario = request.cookies.get('usuario_id')
    if not id_usuario:
        return redirect(url_for('carrinho'))
    
    usuario ='usuario'
    
    cur = conexao.cursor()
    cur.execute("SELECT c.id_bordado, c.quantidade, b.preco, b.imagem, b.nome, b.tamanho FROM carrinhos c JOIN bordados b ON c.id_bordado = b.id WHERE c.id_usuario = %s AND usuario = %s", (id_usuario, usuario))
    dados = cur.fetchall()
    cur.close()

    for linha in dados:
        id_bordado = linha[0]
        campo_quantidade = f'quantidade_{id_bordado}'
        quantidade = request.form.get(campo_quantidade)

        if quantidade and quantidade.isdigit() and int(quantidade) > 0:
            quantidade_int = int(quantidade)
            cur.execute("UPDATE carrinhos SET quantidade = %s WHERE id_usuario = %s AND id_bordado = %s AND usuario = %s", (quantidade_int, id_usuario, id_bordado, usuario))
            conexao.commit()

    cur = conexao.cursor()
    cur.execute("SELECT c.id_bordado, c.quantidade, b.preco, b.imagem, b.nome, b.tamanho FROM carrinhos c JOIN bordados b ON c.id_bordado = b.id WHERE c.id_usuario = %s AND usuario = %s", (id_usuario, usuario))
    dados_atualizados = cur.fetchall()
    cur.close()

    bordados = []
    for linha in dados_atualizados:
        bordados.append({
            'id': linha[0],
            'quantidade': linha[1],
            'preco': linha[2],
            'imagem': linha[3],
            'nome': linha[4],
            'descricao': linha[5]
        })

    valor_total = sum(item['preco'] * item['quantidade'] for item in bordados)

    return render_template('realizar-pedido.html', bordados=bordados, valor_total=valor_total)

@app.route('/finalizar_pedido', methods=['POST'])
def finalizar_pedido():
    nome = request.form.get('nome_cliente')
    telefone = request.form.get('tel_cliente')
    email = request.form.get('email_cliente')
    status = 'Pendente'
    data_pedido = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    id_usuario = request.cookies.get('usuario_id')
    codigo_pedido = gerar_codigo_pedido()

    cur = conexao.cursor()
    cur.execute("SELECT b.id, b.tamanho, c.quantidade FROM bordados b JOIN carrinhos c ON b.id = c.id_bordado WHERE c.id_usuario = %s", (id_usuario,))
    bordados = cur.fetchall()
    cur.close()

    for linha in bordados:
        id_bordado = str(linha[0])
        quantidade = int(linha[2])  
        descricao = request.form.get(f'descricao_{id_bordado}')
        fotos = request.files.getlist(f'fotos_{id_bordado}')

        fotos_salvas = []
        for imagem in fotos:
            if imagem and imagem.filename != '':
                nome_foto = secure_filename(imagem.filename)
                caminho_foto = os.path.join('static/imagens', nome_foto)
                imagem.save(caminho_foto)
                fotos_salvas.append(nome_foto)
        
        imagens_string = ','.join(fotos_salvas) if fotos_salvas else None

        cur = conexao.cursor()
        cur.execute("INSERT INTO pedidos (fotos, descricao, data_pedido, nome_cliente, tel_cliente, email_cliente, status_pedido, codigo_pedido, id_bordado, quantidade) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (imagens_string, descricao, data_pedido, nome, telefone, email, status, codigo_pedido, id_bordado, quantidade,))
        conexao.commit()
        cur.close()

    cur = conexao.cursor()
    cur.execute("DELETE FROM carrinhos WHERE id_usuario = %s", (id_usuario,))
    conexao.commit()
    cur.close()

    codigo_pedido = request.form.get('codigo_pedido', codigo_pedido)
    
    return redirect('/info-pedido' + f'/{codigo_pedido}')


@app.route('/info-pedido/<codigo_pedido>')
def info_pedido(codigo_pedido):
    cur = conexao.cursor()
    cur.execute("""
          SELECT p.*, p.id_bordado, p.codigo_pedido, p.nome_cliente, p.tel_cliente, p.fotos,
               p.email_cliente, p.status_pedido, p.data_pedido, p.descricao AS pedido_descricao, p.quantidade,
               b.id AS bordado_id, b.imagem, b.preco, b.tamanho AS bordado_tamanho
        FROM pedidos p
        JOIN bordados b ON p.id_bordado = b.id
        WHERE p.codigo_pedido = %s
    """, (codigo_pedido,))
    dados = cur.fetchall()
    cur.close()

    if not dados:
        return "Pedido não encontrado", 404

    colunas = [desc[0] for desc in cur.description]
    pedidos = [dict(zip(colunas, linha)) for linha in dados]

    total = sum(p['preco'] * p['quantidade'] for p in pedidos)
    data_pedido = pedidos[0]['data_pedido']

    
    return render_template('info-pedido.html', pedidos=pedidos, codigo_pedido=codigo_pedido, total=total, data_pedido=data_pedido)

@app.route('/carrinho')
def carrinho():
    id_usuario = request.cookies.get('usuario_id')
    item_carrinho = notificacao_carrinho()
    usuario = 'usuario'
    
    cur = conexao.cursor()
    cur.execute("""
        SELECT b.*, c.quantidade
        FROM carrinhos c
        JOIN bordados b ON c.id_bordado = b.id
        WHERE c.id_usuario = %s AND usuario = %s
    """,(id_usuario, usuario,))
    dados = cur.fetchall()
    cur.close()

    cur = conexao.cursor()
    cur.execute("SHOW COLUMNS FROM bordados")
    colunas_bordados = [col[0] for col in cur.fetchall()]
    cur.close()

    colunas = colunas_bordados + ['quantidade']
    bordados = [dict(zip(colunas, linha)) for linha in dados]

    valor_total = 0
    for item in bordados:
        preco = float(item.get('preco', 0))
        quantidade = int(item.get('quantidade', 1))
        valor_total += preco * quantidade
    

    tipo = 'usuario'
    if verificar_cliente():
        tipo = 'cliente'
    return render_template('carrinho.html',tipo=tipo, item_carrinho=item_carrinho, bordados=bordados, valor_total=valor_total)

@app.route('/pedidos/', methods=['GET', 'POST'])
def pedidos():
    termo_busca = ''
    pedidos = []
    codigo_pedido = request.args.get('codigo_pedido', '')
    tipo = 'usuario'

    if request.method == 'POST':
        termo_busca = request.form.get('termo_busca')
        if termo_busca:

            cur = conexao.cursor()
            cur.execute("""
                SELECT p.*, p.id_bordado, p.codigo_pedido, p.nome_cliente, p.tel_cliente, p.fotos,
                    p.email_cliente, p.status_pedido, p.data_pedido, p.descricao AS pedido_descricao, p.quantidade,
                    b.id AS bordado_id, b.imagem, b.preco, b.tamanho AS bordado_tamanho
                FROM pedidos p
                JOIN bordados b ON p.id_bordado = b.id
                WHERE p.codigo_pedido = %s
            """,(termo_busca,))
            resultados = cur.fetchall()
            cur.close()

            if resultados:
                colunas = [desc[0] for desc in cur.description]
                pedidos = [dict(zip(colunas, linha)) for linha in resultados]
            
    
    if verificar_admin():
        return pedidosadm()
    
    if verificar_cliente():

        usuario = session.get('usuario')

        cur = conexao.cursor()
        cur.execute("SELECT email FROM usuarios WHERE usuario = %s", (usuario,))
        resultado = cur.fetchone()
        cur.close()

        if resultado:
            email_usuario = resultado[0]
        else:
            email_usuario = None

        cur = conexao.cursor()
        cur.execute("""
            SELECT p.*, p.id_bordado, p.codigo_pedido, p.nome_cliente, p.tel_cliente, p.fotos,
                p.email_cliente, p.status_pedido, p.data_pedido, p.descricao AS pedido_descricao, p.quantidade,
                b.id AS bordado_id, b.imagem, b.preco, b.tamanho AS bordado_tamanho
            FROM pedidos p
            JOIN bordados b ON p.id_bordado = b.id
            WHERE p.usuario = %s OR p.email_cliente = %s
        """,(usuario, email_usuario))
        resultados = cur.fetchall()
        cur.close()

        if resultados:
            colunas = [desc[0] for desc in cur.description]
            pedidos = [dict(zip(colunas, linha)) for linha in resultados]
 
        item_carrinho = notificacao_carrinho_cliente()
        tipo = 'cliente'
        return render_template('pedidos.html', tipo =tipo, pedidos=pedidos, usuario=usuario, item_carrinho=item_carrinho)

    return render_template('pedidos.html',tipo=tipo, pedidos=pedidos, termo=codigo_pedido)


@app.route('/excluir_pedido/<codigo_pedido>', methods=['POST'])
def excluir_pedido(codigo_pedido):
    cur = conexao.cursor()
    cur.execute("DELETE FROM pedidos WHERE codigo_pedido = %s", (codigo_pedido,))
    conexao.commit()
    cur.close()
    return redirect(url_for('pedido'))


@app.route('/editar-pedido/<codigo_pedido>', methods=['GET', 'POST'])
def editar_pedido(codigo_pedido):
    cur = conexao.cursor()
    cur.execute("""
        SELECT p.*, b.imagem, b.preco, b.tamanho AS bordado_tamanho
        FROM pedidos p
        JOIN bordados b ON p.id_bordado = b.id
        WHERE p.codigo_pedido = %s
    """,(codigo_pedido,))
    resultado = cur.fetchone()
    colunas = [desc[0] for desc in cur.description]
    pedido = dict(zip(colunas, resultado))
    cur.close()

    if not resultado:        
        return "Pedido não encontrado.", 404

    # Se o pedido não estiver pendente, bloqueia a edição
    if pedido['status_pedido'].lower() != 'pendente':
        cur.close()
        return "Este pedido não pode mais ser editado. Ele está " + pedido['status_pedido'] + ". Entre em contato com O ASTRONAUTA BORDADOS PARA REALIZAR ALTERAÇÕES.", 404

    # Se for POST e status for pendente, permite atualizar
    if request.method == 'POST':
        novo_nome = request.form.get('nome_cliente')
        novo_email = request.form.get('email_cliente')
        nova_descricao = request.form.get('descricao')
        novo_tel = request.form.get('tel_cliente')
        
        cur = conexao.cursor()
        cur.execute("""
            UPDATE pedidos
            SET nome_cliente = %s, email_cliente = %s, descricao = %s, tel_cliente = %s
            WHERE codigo_pedido = %s
        """, (novo_nome, novo_email, nova_descricao, novo_tel, codigo_pedido))
        conexao.commit()
        cur.close()

        return redirect(url_for('pedido', codigo_pedido=codigo_pedido)) 

    return render_template('editar-pedido.html', pedido=pedido)


@app.route('/mural', methods=['GET', 'POST'])
def mural():
    tipo = 'usuario'
    item_carrinho = notificacao_carrinho()
    
    cur = conexao.cursor()
    cur.execute("""
        SELECT m.publicacao, m.usuario, m.fotos, m.curtidas, m.legendas, m.data_publicacao, m.hora_publicacao,
               u.foto, u.nome, u.sobrenome
        FROM mural m
        JOIN usuarios u ON m.usuario = u.usuario
        ORDER BY m.data_publicacao DESC, m.hora_publicacao DESC
    """)
    mural_dados = cur.fetchall()
    colunas_mural = ['publicacao', 'usuario', 'fotos', 'curtidas', 'legendas', 'data_publicacao', 'hora_publicacao',
                     'foto', 'nome', 'sobrenome']
    cur.close()

    publicacoes_vistas = set()
    mural = []
    for linha in mural_dados:
        item = dict(zip(colunas_mural, linha))
        if item['publicacao'] not in publicacoes_vistas:
            mural.append(item)
            publicacoes_vistas.add(item['publicacao'])

    # Buscar comentários para cada publicação
    comentarios_por_post = {}
    cur = conexao.cursor()
    cur.execute("SHOW COLUMNS FROM comentarios")
    colunas_coment = [col[0] for col in cur.fetchall()]
    cur.close()

    for item in mural:
        publicacao = item['publicacao']
        cur = conexao.cursor()
        cur.execute("""
            SELECT * FROM comentarios WHERE publicacao = %s ORDER BY data_comentario DESC, hora_comentario DESC
        """, (publicacao,))
        dados_coment = cur.fetchall()
        comentarios_por_post[publicacao] = [dict(zip(colunas_coment, linha)) for linha in dados_coment]
        cur.close()

    if verificar_admin():
        tipo = 'administrador'

        if request.method == 'POST':
            legenda = request.form.get('legenda')
            usuario = session.get('usuario')
            fotos_arquivos = request.files.getlist('fotos')
            fotos_nomes = []

            for foto in fotos_arquivos:
                if foto and foto.filename:
                    nome_arquivo = f"mural_{datetime.now().strftime('%Y%m%d%H%M%S')}_{foto.filename}"
                    caminho = os.path.join('static/imagens/', nome_arquivo)
                    foto.save(caminho)
                    fotos_nomes.append(nome_arquivo)

            fotos = ','.join(fotos_nomes)
            curtidas = 0
            publicacao = gerar_publicacao()
            agora = datetime.now()
            
            cur = conexao.cursor()
            cur.execute("""
                INSERT INTO mural (publicacao, usuario, fotos, curtidas, legendas, data_publicacao, hora_publicacao)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (publicacao, usuario, fotos, curtidas, legenda, agora.date(), agora.time()))
            conexao.commit()
            cur.close()

    if verificar_cliente():
        tipo = 'cliente'

        if request.method == 'POST':
            legenda = request.form.get('legenda')
            usuario = session.get('usuario')
            fotos_arquivos = request.files.getlist('fotos')
            fotos_nomes = []

            for foto in fotos_arquivos:
                if foto and foto.filename:
                    nome_arquivo = f"mural_{datetime.now().strftime('%Y%m%d%H%M%S')}_{foto.filename}"
                    caminho = os.path.join('static/imagens/', nome_arquivo)
                    foto.save(caminho)
                    fotos_nomes.append(nome_arquivo)

            fotos = ','.join(fotos_nomes)
            curtidas = 0
            publicacao = gerar_publicacao()
            agora = datetime.now()

            cur = conexao.cursor()
            cur.execute("""
                INSERT INTO mural (publicacao, usuario, fotos, curtidas, legendas, data_publicacao, hora_publicacao)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (publicacao, usuario, fotos, curtidas, legenda, agora.date(), agora.time()))
            conexao.commit()
            cur.close()


        
    return render_template('mural.html', item_carrinho=item_carrinho, mural = mural, comentarios_por_post=comentarios_por_post, tipo=tipo)


@app.route('/comentarios', methods=['POST'])
def comentarios():
    publicacao = request.form.get('publicacao')
    
    cur = conexao.cursor()
    cur.execute("""
        SELECT * FROM comentarios WHERE publicacao = %s ORDER BY data_comentario DESC, hora_comentario DESC
    """, (publicacao,))
    dados = cur.fetchall()
    cur.close()

    cur = conexao.cursor()
    cur.execute("SHOW COLUMNS FROM comentarios")
    colunas = [col[0] for col in cur.fetchall()]
    cur.close()

    comentarios = [dict(zip(colunas, linha)) for linha in dados]

    return render_template('comentarios.html', comentarios=comentarios, publicacao=publicacao)


@app.route('/excluir_imagem_extra', methods=['POST'])
def excluir_imagem_extra():
    id = int(request.form.get('id'))  # Garante que o ID seja inteiro
    imagem_excluir = request.form.get('imagem')

    # Busca o documento correspondente no MongoDB
    bordado_mongo = colecao_detalhes.find_one({"id": id})

    if bordado_mongo and 'imagens_extras' in bordado_mongo:
        imagens = bordado_mongo['imagens_extras']

        # Remove a imagem da lista
        novas_imagens = [img for img in imagens if img != imagem_excluir]

        # Atualiza o documento no MongoDB
        colecao_detalhes.update_one(
            {"id": id},
            {"$set": {"imagens_extras": novas_imagens}}
        )

    return redirect(url_for('editar_bordado', id=id))  # nome da sua função de edição



@app.context_processor
def foto_perfil():
    usuario = session.get('usuario')
    
    if not usuario:
        return dict(foto='user.png')

    cur = conexao.cursor()
    cur.execute("SELECT foto FROM usuarios WHERE usuario = %s", (usuario,))
    resultado = cur.fetchone()
    cur.close()

    if resultado:
        return dict(foto=resultado[0])
    else:
        return dict(foto='user.png')


@app.context_processor
def nome():
    usuario = session.get('usuario')
    print('Usuário da sessão:', usuario)

    if not usuario:
        return dict(nome='', sobrenome='')

    cur = conexao.cursor()
    cur.execute("SELECT nome FROM usuarios WHERE usuario = %s", (usuario,))
    resultado = cur.fetchone()
    cur.close()

    print('Resultado da consulta SQL:', resultado)

    if resultado:
        return dict(nome=resultado[0])
    else:
        return dict(nome='')
    
@app.context_processor
def sobrenome():
    usuario = session.get('usuario')
    print('Usuário da sessão:', usuario)

    if not usuario:
        return dict(nome='', sobrenome='')

    cur = conexao.cursor()
    cur.execute("SELECT sobrenome FROM usuarios WHERE usuario = %s", (usuario,))
    resultado = cur.fetchone()
    cur.close()

    print('Resultado da consulta SQL:', resultado)

    if resultado:
        return dict(sobrenome=resultado[0])
    else:
        return dict(sobrenome='')
    
@app.context_processor
def usuario():
    usuario = session.get('usuario')

    cur = conexao.cursor()
    cur.execute("SELECT usuario FROM usuarios WHERE usuario = %s", (usuario,))
    resultado = cur.fetchone()
    cur.close()

    if resultado:
        return dict(usuario=resultado[0])
    else:
        return dict(usuario='')

#DEF CLIENTES

@app.route('/perfil')
def perfil():
    tipo = 'cliente'
    if verificar_admin():
        tipo = 'administrador'
    if not usuario():
        return redirect('/login')
  
    return render_template('perfil.html', tipo=tipo)


@app.route('/editar_perfil_adm/', methods=['POST'])
def editar_perfil_adm():
    usuario = session.get('usuario')
    if not verificar_admin():
        return redirect('/login')

    novo_nome = request.form['nome']
    novo_sobrenome = request.form['sobrenome']
    novo_usuario = request.form['usuario']
    
    senha_atual_form = request.form.get('senha_atual')
    nova_senha = request.form.get('nova_senha')
    foto = request.files.get('imagem')

    mensagem = None

    cur = conexao.cursor()
    cur.execute("SELECT senha, foto FROM usuarios WHERE usuario = %s", (usuario,))
    resultado = cur.fetchone()
    cur.close()
    if not resultado:
        mensagem = 'Usuário não encontrado.'
        
        return render_template('perfil.html', mensagem=mensagem, usuario=usuario, nome=session.get('nome'), sobrenome=session.get('sobrenome'), foto=session.get('foto'))

    senha_armazenada, foto_atual = resultado

    if novo_usuario != usuario:
        cur = conexao.cursor()
        cur.execute("SELECT id FROM usuarios WHERE usuario = %s", (novo_usuario,))
        resultado2 = cur.fetchone()
        cur.close()

        if resultado2:
            mensagem = 'Este nome de usuário já está em uso. Escolha outro.'

            return render_template('perfil.html', mensagem=mensagem, usuario=usuario, nome=session.get('nome'), sobrenome=session.get('sobrenome'), foto=session.get('foto'))
    
    if nova_senha:
        if not senha_atual_form:
            mensagem = 'Digite sua senha atual para alterar a senha.'

            return render_template('perfil.html', mensagem=mensagem, usuario=usuario, nome=session.get('nome'), sobrenome=session.get('sobrenome'), foto=session.get('foto'))

        if senha_atual_form != senha_armazenada:
            mensagem = 'Senha atual incorreta.'
            
            return render_template('perfiladn.html', mensagem=mensagem, usuario=usuario, nome=session.get('nome'), sobrenome=session.get('sobrenome'), foto=session.get('foto'))

        senha_para_salvar = nova_senha
    else:
        senha_para_salvar = senha_armazenada

    # Verificar a foto
    if foto and foto.filename:
        nova_foto = secure_filename(foto.filename)
        foto.save(os.path.join('static/imagens', nova_foto))
    else:
        nova_foto = foto_atual

    cur = conexao.cursor()
    cur.execute("""
        UPDATE usuarios 
        SET nome = %s, sobrenome = %s, foto = %s, senha = %s, usuario = %s 
        WHERE usuario = %s
    """,(novo_nome, novo_sobrenome, nova_foto, senha_para_salvar, novo_usuario, usuario))
    conexao.commit()
    cur.close()

    session['usuario'] = novo_usuario
    session['nome'] = novo_nome
    session['sobrenome'] = novo_sobrenome
    session['foto'] = nova_foto

    mensagem = 'Perfil atualizado com sucesso!'
  

    return render_template('perfil.html', mensagem=mensagem, usuario=novo_usuario, nome=novo_nome, sobrenome=novo_sobrenome, foto=nova_foto)


@app.route('/excluir_publicacao/<publicacao>', methods=['POST'])
def excluir_publicacao(publicacao):
    if 'usuario' not in session:
        return redirect('/login')

    usuario = session.get('usuario')

    cur = conexao.cursor()
    cur.execute("SELECT tipo FROM usuarios WHERE usuario = %s", (usuario,))
    resultado = cur.fetchone()
    cur.close()

    tipo = resultado[0] if resultado else None
    if tipo == 'administrador':
        cur = conexao.cursor()
        cur.execute("DELETE FROM comentarios WHERE publicacao = %s", (publicacao,))
        conexao.commit()
        cur.close()

        cur = conexao.cursor()
        cur.execute("DELETE FROM mural WHERE publicacao = %s", (publicacao,))
        conexao.commit()
        cur.close()

    else:
        cur = conexao.cursor()
        cur.execute("SELECT * FROM mural WHERE publicacao = %s AND usuario = %s", (publicacao, usuario))
        resultado = cur.fetchone()
        cur.close()
        if resultado:
            cur = conexao.cursor()
            cur.execute("DELETE FROM comentarios WHERE publicacao = %s", (publicacao,))
            conexao.commit()
            cur.close()    

            cur = conexao.cursor()
            cur.execute("DELETE FROM mural WHERE publicacao = %s", (publicacao,))
            conexao.commit()
            cur.close()

    return redirect(request.referrer)


@app.route('/excluir_comentario/<int:id>', methods=['POST'])
def excluir_comentario(id):
    if 'usuario' not in session:
        return redirect('/login')

    usuario = session['usuario']
    

    # Se for administrador, pode excluir qualquer comentário
    if session.get('tipo') == 'administrador':
        cur = conexao.cursor()
        cur.execute("DELETE FROM comentarios WHERE id = %s", (id,))
        conexao.commit()
        cur.close()
    else:
        cur = conexao.cursor()
        cur.execute("SELECT * FROM comentarios WHERE id = %s AND usuario = %s ", (id, usuario))
        resultado = cur.fetchone()
        cur.close()
        if resultado:
            cur = conexao.cursor()
            cur.execute("DELETE FROM comentarios WHERE id = %s ", (id,))
            conexao.commit()
            cur.close()

    return redirect(request.referrer)



@app.route('/excluir_pedido_cliente/<codigo_pedido>', methods=['POST'])
def excluir_pedido_cliente(codigo_pedido):
    if not verificar_cliente():
        return redirect('/login')
    
    id_bordado = request.form.get('id_bordado')
    usuario = session.get('usuario')
    cur = conexao.cursor()
    cur.execute("DELETE FROM pedidos WHERE codigo_pedido = %s AND id_bordado = %s AND usuario = %s ", (codigo_pedido, id_bordado, usuario))
    conexao.commit()
    cur.close()
    return redirect(url_for('pedido_cliente'))


@app.route('/editar-pedido-cliente/<codigo_pedido>', methods=['GET', 'POST'])
def editar_pedido_cliente(codigo_pedido):
    if not verificar_cliente():
        return redirect('/login')

    if request.method == 'POST':
        novo_nome = request.form.get('nome_cliente')
        novo_email = request.form.get('email_cliente')
        nova_descricao = request.form.get('descricao')
        novo_tel = request.form.get('tel_cliente')
        
        cur = conexao.cursor()
        cur.execute("""
            UPDATE pedidos
            SET nome_cliente = %s, email_cliente = %s, descricao = %s, tel_cliente = %s
            WHERE codigo_pedido = %s
        """, (novo_nome, novo_email, nova_descricao, novo_tel, codigo_pedido))
        conexao.commit()
        cur.close()
        
        return redirect(url_for('pedido_cliente', codigo_pedido=codigo_pedido)) 

    else:
        cur = conexao.cursor()
        cur.execute("""
            SELECT p.*, b.imagem, b.preco, b.tamanho AS bordado_tamanho
            FROM pedidos p
            JOIN bordados b ON p.id_bordado = b.id
            WHERE p.codigo_pedido = %s
        """,(codigo_pedido,))
        resultado = cur.fetchone()
        colunas = [desc[0] for desc in cur.description]
        pedido = dict(zip(colunas, resultado))
        cur.close()
        
        if not resultado:

            return "Pedido não encontrado.", 404

    return render_template('editar-pedido-cliente.html', pedido=pedido)

@app.route('/publicacao-cliente', methods=['GET', 'POST'])
def publicacao_cliente():
    if usuario in session:
        return redirect('/login')

    if request.method == 'POST':
        legenda = request.form.get('legenda')
        usuario = session.get('usuario')
        fotos_arquivos = request.files.getlist('fotos')  # Nome do campo no form
        fotos_nomes = []
        
        # Salvar fotos na pasta static/imagens/mural
        for foto in fotos_arquivos:
            if foto and foto.filename:  # Verifica se o arquivo foi enviado
                nome_arquivo = f"mural_{datetime.now().strftime('%Y%m%d%H%M%S')}_{foto.filename}"
                caminho = os.path.join('static/imagens/', nome_arquivo)
                foto.save(caminho)
                fotos_nomes.append(nome_arquivo)

        fotos = ','.join(fotos_nomes)  # Salvar no banco como string separada por vírgula
        curtidas = 0
        comentarios = ''
        publicacao = gerar_publicacao()
        agora = datetime.now()
        data_publicacao = agora.date()
        hora_publicacao = agora.time()

        cur = conexao.cursor()
        cur.execute("""
            INSERT INTO mural (publicacao, usuario, fotos, curtidas, legendas, comentarios, data_publicacao, hora_publicacao)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (publicacao, usuario, fotos, curtidas, legenda, comentarios, data_publicacao, hora_publicacao))
        conexao.commit()
        cur.close()

        return redirect(request.referrer)

    return redirect(request.referrer,mural = mural)

@app.route('/curtir', methods=['POST'])
def curtir():
    
    publicacao = request.form.get('publicacao')
    usuario = session['usuario']

    cur = conexao.cursor()
    cur.execute("""
        SELECT * FROM curtidas WHERE usuario = %s AND publicacao = %s
    """, (usuario, publicacao))
    curtida_existente = cur.fetchone()
    cur.close()

    if curtida_existente:
        cur = conexao.cursor()
        cur.execute("""
            UPDATE mural SET curtidas = curtidas - 1 WHERE publicacao = %s
        """, (publicacao,))
        conexao.commit()
        cur.close()
        
        cur = conexao.cursor()
        cur.execute("""
            DELETE FROM curtidas WHERE usuario = %s AND publicacao = %s
        """, (usuario, publicacao))
        conexao.commit()
        cur.close()
    else:
        cur = conexao.cursor()
        cur.execute("""
            UPDATE mural SET curtidas = curtidas + 1 WHERE publicacao = %s
        """, (publicacao,))
        conexao.commit()
        cur.close()

        cur = conexao.cursor()
        cur.execute("""
            INSERT INTO curtidas (usuario, publicacao) VALUES (%s, %s)
        """, (usuario, publicacao))
        conexao.commit()
        cur.close()

    return redirect(request.referrer)

@app.route('/comentario', methods=['POST'])
def comentario():
    
    comentario = request.form.get('comentario')
    usuario = session.get('usuario')
    publicacao = request.form.get('publicacao')
    agora = datetime.now()
    data_comentario = agora.date()
    hora_comentario = agora.time()

    cur = conexao.cursor()
    cur.execute("""
        INSERT INTO comentarios (comentario, usuario, publicacao, data_comentario, hora_comentario)
        VALUES (%s, %s, %s, %s, %s)
    """, (comentario, usuario, publicacao, data_comentario, hora_comentario))
    conexao.commit()
    cur.close()

    return redirect(request.referrer or '/mural')


@app.route('/excluir_imagem_extra_cliente', methods=['POST'])
def excluir_imagem_extra_cliente():
    id = request.form.get('id')
    imagem_excluir = request.form.get('imagem')

    cur = conexao.cursor()
    cur.execute("SELECT * FROM bordados WHERE id = %s", (id,))
    bordado = cur.fetchone()
    cur.close()

    if bordado:
        imagens = bordado[4].split(',') if bordado[4] else []
        imagens = [img.strip() for img in imagens if img.strip() != imagem_excluir]
        nova_string = ','.join(imagens)

        cur = conexao.cursor()
        cur.execute("UPDATE bordados SET imagens_extras = %s WHERE id = %s", (nova_string, id))
        conexao.commit()
        cur.close()

    return redirect(url_for('editar-bordado-cliente', id=id))


#DEF ADMINISTRADORES


@app.route('/excluir_pedidoadm/<codigo_pedido>', methods=['POST'])
def excluir_pedidoadm(codigo_pedido):
    if not verificar_admin():
        return redirect('/login')
    
    cur = conexao.cursor()
    cur.execute("DELETE FROM pedidos WHERE codigo_pedido = %s", (codigo_pedido,))
    conexao.commit()
    cur.close()
    return redirect(url_for('pedidos'))

@app.route('/muraladm', methods=['GET', 'POST'])
def muraladm():
    if not verificar_admin():
        return redirect('/login')
    

    if request.method == 'POST':
        legenda = request.form.get('legenda')
        usuario = session.get('usuario')
        fotos_arquivos = request.files.getlist('fotos')
        fotos_nomes = []

        for foto in fotos_arquivos:
            if foto and foto.filename:
                nome_arquivo = f"mural_{datetime.now().strftime('%Y%m%d%H%M%S')}_{foto.filename}"
                caminho = os.path.join('static/imagens/', nome_arquivo)
                foto.save(caminho)
                fotos_nomes.append(nome_arquivo)

        fotos = ','.join(fotos_nomes)
        curtidas = 0
        publicacao = gerar_publicacao()
        agora = datetime.now()

        cur = conexao.cursor()
        cur.execute("""
            INSERT INTO mural (publicacao, usuario, fotos, curtidas, legendas, data_publicacao, hora_publicacao)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (publicacao, usuario, fotos, curtidas, legenda, agora.date(), agora.time()))
        conexao.commit()
        cur.close()
    
    cur = conexao.cursor()
    cur.execute("""
        SELECT m.publicacao, m.usuario, m.fotos, m.curtidas, m.legendas, m.data_publicacao, m.hora_publicacao,
               u.foto, u.nome, u.sobrenome
        FROM mural m
        JOIN usuarios u ON m.usuario = u.usuario
        ORDER BY m.data_publicacao DESC, m.hora_publicacao DESC
    """)
    mural_dados = cur.fetchall()

    colunas_mural = ['publicacao', 'usuario', 'fotos', 'curtidas', 'legendas', 'data_publicacao', 'hora_publicacao',
                     'foto', 'nome', 'sobrenome']
    cur.close()

    # Filtrar duplicatas por publicacao manualmente
    publicacoes_vistas = set()
    mural = []
    for linha in mural_dados:
        item = dict(zip(colunas_mural, linha))
        if item['publicacao'] not in publicacoes_vistas:
            mural.append(item)
            publicacoes_vistas.add(item['publicacao'])

    # Buscar comentários para cada publicação
    comentarios_por_post = {}
    cur = conexao.cursor()
    cur.execute("SHOW COLUMNS FROM comentarios")
    colunas_coment = [col[0] for col in cur.fetchall()]
    cur.close()
    for item in mural:
        publicacao = item['publicacao']
        cur.execute("""
            SELECT * FROM comentarios WHERE publicacao = %s ORDER BY data_comentario DESC, hora_comentario DESC
        """, (publicacao,))
        dados_coment = cur.fetchall()
        comentarios_por_post[publicacao] = [dict(zip(colunas_coment, linha)) for linha in dados_coment]

    return render_template('muraladm.html', mural=mural, comentarios_por_post=comentarios_por_post)


@app.route('/configuracoes' , methods=['GET', 'POST'])
def configuracoes():
    if not verificar_admin():
        return redirect('/login')
    usuarios =''
    menu = 'contatos'
    if request.method == 'POST':
        menu = request.form.get('menu-conf')

        if menu =='menu-administradores':
            cur = conexao.cursor()
            cur.execute("SELECT * FROM usuarios where tipo ='administrador'")
            dados = cur.fetchall() 
            colunas = [desc[0] for desc in cur.description]
            cur.close()

            usuarios = [dict(zip(colunas, linha)) for linha in dados]

            return render_template('configuracoes.html', menu=menu, usuarios=usuarios)
        
        if menu =='clientes':
            cur = conexao.cursor()
            cur.execute("SELECT * FROM usuarios where tipo ='cliente'")     
            dados = cur.fetchall()   
            colunas = [desc[0] for desc in cur.description]
            cur.close()
            
            usuarios = [dict(zip(colunas, linha)) for linha in dados]
            return render_template('configuracoes.html', menu=menu, usuarios=usuarios)

        if menu =='contatos':
            cur = conexao.cursor()
            cur.execute("SELECT * FROM contatos")
            dados = cur.fetchall()
            colunas = [desc[0]for desc in cur.description]
            cur.close()

            contatos = [dict(zip(colunas, linha)) for linha in dados]

            return render_template('configuracoes.html', menu=menu,contatos=contatos)
            
    return render_template('configuracoes.html', menu=menu, usuarios=usuarios)    

@app.route('/editar-bordado/<int:id>', methods=['GET', 'POST'])
def editar_bordado(id):
    if not verificar_admin():
        return redirect('/login')
    
    # Buscar dados do MySQL
    cur = conexao.cursor()
    cur.execute("SELECT * FROM bordados WHERE id = %s", (id,))
    linha = cur.fetchone()
    cur.close()
    if not linha:
        return "Bordado não encontrado", 404

    cur = conexao.cursor()
    cur.execute("SHOW COLUMNS FROM bordados")
    colunas = [col[0] for col in cur.fetchall()]
    bordado = dict(zip(colunas, linha))
    cur.close()

    # Buscar dados do MongoDB
    detalhes_bordado = mongo_db['detalhes_bordados'].find_one({"id": id}) or {}
    
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        tamanho = request.form['tamanho']
        preco = request.form['preco']
        temas = request.form['temas']

        imagem = request.files.get('imagem')
        if imagem and imagem.filename:
            nome_imagem = secure_filename(imagem.filename)
            imagem.save(os.path.join('static/imagens', nome_imagem))
        else:
            nome_imagem = bordado['imagem']

        # Upload de imagens extras
        novas_imagens_extras = []
        imagens_extras = request.files.getlist('imagem_bordado_extra')
        for img in imagens_extras:
            if img and img.filename:
                nome_arquivo = secure_filename(img.filename)
                img.save(os.path.join('static/imagens', nome_arquivo))
                novas_imagens_extras.append(nome_arquivo)

        # Recuperar imagens antigas do MongoDB
        imagens_anteriores = detalhes_bordado.get("imagens_extras", [])
        if not isinstance(imagens_anteriores, list):
            imagens_anteriores = []

        # Juntar com as novas
        imagens_finais = imagens_anteriores + novas_imagens_extras

        # Atualizar SQL
        cur = conexao.cursor()
        cur.execute("""
            UPDATE bordados 
            SET nome = %s, tamanho = %s, preco = %s, imagem = %s 
            WHERE id = %s
        """, (nome, tamanho, preco, nome_imagem, id))
        conexao.commit()
        cur.close()

        # Atualizar MongoDB
        mongo_db['detalhes_bordados'].update_one(
            {'id': id},
            {'$set': {
                'descricao': descricao,
                'temas': temas,
                'imagens_extras': imagens_finais
            }},
            upsert=True
        )

        return redirect(url_for('detalhes', id=id))

    # Para GET: preparar dados para exibir no template

    # Processar descrição para o formulário
    descricao_valor = detalhes_bordado.get("descricao", "")
    if isinstance(descricao_valor, list):
        detalhes_texto = ", ".join(descricao_valor)
    else:
        detalhes_texto = str(descricao_valor)

    # Processar temas para o formulário
    temas_valor = detalhes_bordado.get("temas", "")
    if isinstance(temas_valor, list):
        detalhes_tema = ", ".join([str(t).strip().capitalize() for t in temas_valor])
    else:
        detalhes_tema = str(temas_valor).strip().capitalize()

    # Processar imagens extras para exibir
    imagens_extras = detalhes_bordado.get("imagens_extras", [])
    if not isinstance(imagens_extras, list):
        imagens_extras = []

    return render_template(
        'editar-bordado.html',
        bordado=bordado,
        detalhes_texto=detalhes_texto,
        detalhes_tema=detalhes_tema,
        imagens_extras=imagens_extras
    )

@app.route('/pedidosadm', methods=['GET', 'POST'])
def pedidosadm():
    if not verificar_admin():
        return redirect('/login')
    tipo = 'administrador'
    if request.method == 'POST':
        menu = request.form.get('menu-pedidos')
        if menu =='pendente':
            cur = conexao.cursor()

            cur.execute("""
                SELECT p.*, b.imagem, b.preco, b.tamanho, p.quantidade
                FROM pedidos p
                JOIN bordados b ON p.id_bordado = b.id
                WHERE p.status_pedido = 'Pendente'
            """)
            dados = cur.fetchall()
            colunas = [desc[0] for desc in cur.description]
            pedidos = [dict(zip(colunas, linha)) for linha in dados]
            codigo_pedido = request.args.get('codigo_pedido', '')
            cur.close()

            pedidos_agrupados = defaultdict(list)
            for pedido in pedidos:
                pedidos_agrupados[pedido['codigo_pedido']].append(pedido)

            pedidos_agrupados = list(pedidos_agrupados.items())
            total_pedidos = len(pedidos_agrupados)
            valor_pedidos = sum(pedido['preco'] * pedido['quantidade'] for pedido in pedidos)
            
            return render_template('pedidos.html',tipo=tipo, menu=menu, pedidos=pedidos, codigo_pedido=codigo_pedido, pedidos_agrupados=pedidos_agrupados, total_pedidos=total_pedidos, valor_pedidos=valor_pedidos)


        if menu =='processo':
            cur = conexao.cursor()

            cur.execute("""
                SELECT p.*, b.imagem, b.preco, b.tamanho, p.quantidade
                FROM pedidos p
                JOIN bordados b ON p.id_bordado = b.id
                WHERE p.status_pedido = 'Em Andamento'
            """)
            dados = cur.fetchall()
            colunas = [desc[0] for desc in cur.description]
            pedidos = [dict(zip(colunas, linha)) for linha in dados]
            codigo_pedido = request.args.get('codigo_pedido', '')
            cur.close()

            pedidos_agrupados = defaultdict(list)
            for pedido in pedidos:
                pedidos_agrupados[pedido['codigo_pedido']].append(pedido)

            pedidos_agrupados = list(pedidos_agrupados.items())
            total_pedidos = len(pedidos_agrupados)
            valor_pedidos = sum(pedido['preco'] * pedido['quantidade'] for pedido in pedidos)

            return render_template('pedidos.html', tipo=tipo, menu=menu, pedidos=pedidos, codigo_pedido=codigo_pedido, pedidos_agrupados=pedidos_agrupados, total_pedidos=total_pedidos, valor_pedidos=valor_pedidos)


        if menu =='finalizado':
            cur = conexao.cursor()

            cur.execute("""
                SELECT p.*, b.imagem, b.preco, b.tamanho, p.quantidade
                FROM pedidos p
                JOIN bordados b ON p.id_bordado = b.id
                WHERE p.status_pedido = 'Finalizado'
            """)
            dados = cur.fetchall()
            colunas = [desc[0] for desc in cur.description]
            pedidos = [dict(zip(colunas, linha)) for linha in dados]
            codigo_pedido = request.args.get('codigo_pedido', '')
            cur.close()

            pedidos_agrupados = defaultdict(list)
            for pedido in pedidos:
                pedidos_agrupados[pedido['codigo_pedido']].append(pedido)

            pedidos_agrupados = list(pedidos_agrupados.items())
            total_pedidos = len(pedidos_agrupados)
            valor_pedidos = sum(pedido['preco'] * pedido['quantidade'] for pedido in pedidos)

            return render_template('pedidos.html', tipo=tipo, menu=menu, pedidos=pedidos, codigo_pedido=codigo_pedido, pedidos_agrupados=pedidos_agrupados, total_pedidos=total_pedidos, valor_pedidos=valor_pedidos)
        
    menu ='pendente'
    
    cur = conexao.cursor()
    cur.execute("""
        SELECT p.*, b.imagem, b.preco, b.tamanho, p.quantidade
        FROM pedidos p
        JOIN bordados b ON p.id_bordado = b.id
        WHERE p.status_pedido = 'Pendente'
    """)
    dados = cur.fetchall()
    colunas = [desc[0] for desc in cur.description]
    pedidos = [dict(zip(colunas, linha)) for linha in dados]
    codigo_pedido = request.args.get('codigo_pedido', '')
    cur.close()

    pedidos_agrupados = defaultdict(list)
    
    for pedido in pedidos:
        pedidos_agrupados[pedido['codigo_pedido']].append(pedido)

    pedidos_agrupados = list(pedidos_agrupados.items())
    total_pedidos = len(pedidos_agrupados)
    valor_pedidos = sum(pedido['preco'] * pedido['quantidade'] for pedido in pedidos)

    
    return render_template('pedidos.html', tipo=tipo, menu=menu, valor_pedidos=valor_pedidos, total_pedidos=total_pedidos,codigo_pedido=codigo_pedido, pedidos_agrupados=pedidos_agrupados)

    

@app.route('/detalhe_pedido/<codigo_pedido>')
def detalhe_pedido(codigo_pedido):
    if not verificar_admin():
        return redirect('/login')

    cur = conexao.cursor()

    cur.execute("""
        SELECT p.*, p.id_bordado, p.codigo_pedido, p.nome_cliente, p.tel_cliente, p.fotos,
               p.email_cliente, p.status_pedido, p.data_pedido, p.descricao AS pedido_descricao, p.quantidade,
               b.id AS bordado_id, b.imagem, b.preco, b.tamanho AS bordado_tamanho
        FROM pedidos p
        JOIN bordados b ON p.id_bordado = b.id
        WHERE p.codigo_pedido = %s
    """, (codigo_pedido,))
    resultados = cur.fetchall()

    colunas = [desc[0] for desc in cur.description]
    pedidos = [dict(zip(colunas, linha)) for linha in resultados]
    menu = resultados[0][colunas.index('status_pedido')]
    cur.close()

    cur = conexao.cursor()
    cur.execute("SELECT id_bordado FROM pedidos WHERE codigo_pedido = %s", (codigo_pedido,))
    resultado = cur.fetchall()
    detalhes_pedido = []
    cur.close()
    if resultado:
        id_bordado = resultado[0]

        mongo_detalhes = colecao_detalhes.find_one({"id": id_bordado})

        detalhes_pedido = mongo_detalhes.get("descricao", []) if mongo_detalhes else []
    else:
        detalhes_pedido = []


    return render_template('detalhe_pedido.html', pedidos=pedidos, menu=menu, detalhes_pedido=detalhes_pedido)

@app.route('/status_pedido', methods=['POST'])
def status_pedido():
    if not verificar_admin():
        return redirect('/login')

    for key in request.form:
        if key.startswith("status"):
            novo_status = request.form[key]
            break
    else:
        return "Dados inválidos", 400

    codigo_pedido = request.form.get('codigo_pedido')
    if not codigo_pedido:
        return "Código do pedido não enviado", 400

    try:
        cur = conexao.cursor()
        cur.execute("UPDATE pedidos SET status_pedido = %s WHERE codigo_pedido = %s", (novo_status, codigo_pedido))
        conexao.commit()
        cur.close()

        return redirect(f'/pedidos?codigo_pedido={codigo_pedido}')
    except Exception as e:
        return f"Erro: {e}", 500


@app.route('/editar/<int:id>', methods=['POST'])
def editar_item(id):
    if not verificar_admin():
        return redirect('/login')

    novo_titulo = request.form['titulo']
    novo_texto = request.form['textos']
    imagem_arquivo = request.files.get('imagens')

    if imagem_arquivo and imagem_arquivo.filename != '':

        from werkzeug.utils import secure_filename
        nome_arquivo = secure_filename(imagem_arquivo.filename)
        caminho = os.path.join('static/imagens', nome_arquivo)
        imagem_arquivo.save(caminho)
        nova_imagem = nome_arquivo
    else:
        cur = conexao.cursor()
        cur.execute("SELECT imagens FROM iniciodb WHERE id = %s", (id,))
        resultado = cur.fetchone()
        nova_imagem = resultado[0]
        cur.close()

    cur = conexao.cursor()
    cur.execute("UPDATE iniciodb SET titulo = %s, textos = %s, imagens = %s WHERE id = %s",(novo_titulo, novo_texto, nova_imagem, id))
    conexao.commit()
    cur.close()

    return redirect('/')  

@app.route('/administradores' , methods=['GET', 'POST'])
def administradores():
    if not verificar_admin():
        return redirect('/login')
    
    
    cur = conexao.cursor()
    cur.execute("SELECT * FROM usuarios where tipo ='administrador'")
    dados = cur.fetchall() 

    colunas = [desc[0] for desc in cur.description]

    cur.close()

    usuarios = [dict(zip(colunas, linha)) for linha in dados]
    return render_template('administradores.html', usuarios=usuarios)


@app.route('/editar_contatos/<int:id>', methods=['POST'])
def editar_contatos(id):
    if not verificar_admin():
        return redirect('/login')
   
    novo_numero = request.form['numero']
    novo_email = request.form['email']
    novo_insta = request.form['insta']


    cur = conexao.cursor()
    cur.execute("UPDATE contatos SET numero = %s, email = %s, insta = %s WHERE id = %s",(novo_numero, novo_email, novo_insta, id))
    conexao.commit()
    cur.close()

    return redirect('/configuracoes') 

@app.route('/excluir_usuario', methods=['POST'])
def excluir_usuario():

   
    id = (request.form.get("id"))

    if not verificar_admin():
        return redirect('/login')
    
    else:
        if id == '1':

            cur = conexao.cursor()
            cur.execute("SELECT * FROM usuarios where tipo ='administrador'")
            dados = cur.fetchall() 
            colunas = [desc[0] for desc in cur.description]
            cur.close()

            usuarios = [dict(zip(colunas, linha)) for linha in dados]

            flash("Não é possível excluir o administrador principal")
            menu ='menu-administradores'
            return render_template('configuracoes.html',menu=menu, usuarios=usuarios)
        else:
        
            cur = conexao.cursor()
            cur.execute('SELECT email FROM usuarios WHERE id = %s',(id,))
            resultado = cur.fetchone()
            cur.close()
            if resultado:
                email = resultado[0]
            

                if email:
                    cur = conexao.cursor()
                    cur.execute('DELETE FROM login WHERE email = %s',(email,))
                    conexao.commit()
                    cur.close()
                    
                    cur = conexao.cursor()
                    cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
                    conexao.commit()
                    cur.close()
                    return redirect('/configuracoes')

    return redirect('/configuracoes')


@app.route('/adicionar-bordado', methods=['GET', 'POST'])
def adicionar_bordado():
    if not verificar_admin():
        return redirect('/login')
    
    if request.method == 'POST':

        nome = request.form['nome']
        tamanho = request.form['tamanho']
        preco = request.form['preco']
        temas = request.form['temas']
        imagem_bordado = request.files['imagem']
        descricao = request.form['descricao']

        imagem_bordado_extra = request.files.getlist('imagem_bordado_extra')
        imagens_extra_salvas = []
        
        for imagem in imagem_bordado_extra:
            if imagem.filename != '': 
                nome_arquivo_extra = secure_filename(imagem.filename)
                caminho_extra = os.path.join('static/imagens', nome_arquivo_extra)
                imagem.save(caminho_extra)
                imagens_extra_salvas.append(nome_arquivo_extra) 

        if imagem_bordado and imagem_bordado.filename != '':
            nome_arquivo = secure_filename(imagem_bordado.filename)
            caminho = os.path.join('static/imagens', nome_arquivo)
            imagem_bordado.save(caminho)
            nova_imagem = nome_arquivo
        else:
            nova_imagem = None

       
        novo_id = get_id()
        cur = conexao.cursor()
        cur.execute("INSERT INTO bordados (id, nome, tamanho, preco, imagem) VALUES (%s ,%s, %s, %s,%s)",(novo_id, nome, tamanho, preco, nova_imagem))
        conexao.commit()
        cur.close()
        documento = {
            "id": novo_id,
            "descricao": descricao,
            "temas": temas,
            "imagens_extras": imagens_extra_salvas       }

        colecao_detalhes.insert_one(documento)

        return redirect('/catalogo')

    cur = conexao.cursor()
    cur.execute("SELECT * FROM bordados")
    dados = cur.fetchall()
    cur.close()

    cur = conexao.cursor()
    cur.execute("SHOW COLUMNS FROM bordados")
    colunas = [col[0] for col in cur.fetchall()]
    cur.close()

    bordados = [dict(zip(colunas, linha)) for linha in dados]

    return render_template('adicionar-bordado.html', bordados=bordados)

@app.route('/confirmar_exclusao/<int:bordado_id>', methods=['POST'])
def confirmar_exclusao(bordado_id):
    if not verificar_admin():
        return redirect('/login')
   
    cur = conexao.cursor()
    cur.execute("DELETE FROM bordados WHERE id = %s",(bordado_id,))
    conexao.commit()
    cur.close()
    colecao_detalhes.delete_one({'id': bordado_id})

    return redirect('/catalogo') 

@app.route('/editar_perfil/', methods=['POST'])
def editar_perfil():
    usuario_atual = session.get('usuario')
    if not verificar_cliente():
        return redirect('/login')

    mensagem = None
    novo_nome = request.form['nome']
    novo_sobrenome = request.form['sobrenome']
    novo_usuario = request.form['usuario']

    senha_atual_form = request.form.get('senha_atual')
    nova_senha = request.form.get('nova_senha')
    foto = request.files.get('imagem')

    cur = conexao.cursor()

    # Primeiro busca o ID, senha e foto do usuário atual
    cur.execute("SELECT id, senha, foto FROM usuarios WHERE usuario = %s", (usuario_atual,))
    resultado = cur.fetchone()
    cur.close()

    if not resultado:
        mensagem = 'Usuário não encontrado.'
        return render_template('perfil.html', mensagem=mensagem, usuario=usuario_atual, nome=session.get('nome'), sobrenome=session.get('sobrenome'), foto=session.get('foto'))

    id_usuario, senha_armazenada, foto_atual = resultado

    
    if usuario_existente:
        mensagem = 'Este nome de usuário já está em uso. Escolha outro.'
        return render_template('perfil.html', mensagem=mensagem, usuario=usuario_atual, nome=session.get('nome'), sobrenome=session.get('sobrenome'), foto=session.get('foto'))

    # Se o usuário quiser trocar de senha, exigir confirmação da senha atual
    if nova_senha:
        if senha_atual_form != senha_armazenada:
            mensagem = 'Senha atual incorreta.'
            return render_template('perfil.html', mensagem=mensagem, usuario=usuario_atual, nome=session.get('nome'), sobrenome=session.get('sobrenome'), foto=session.get('foto'))
        senha_para_salvar = nova_senha
    else:
        senha_para_salvar = senha_armazenada

    # Foto de perfil
    if foto and foto.filename:
        nova_foto = secure_filename(foto.filename)
        foto.save(os.path.join('static/imagens', nova_foto))
    else:
        nova_foto = foto_atual

    cur = conexao.cursor()
    cur.execute("""
        UPDATE usuarios 
        SET nome = %s, sobrenome = %s, foto = %s, senha = %s, usuario = %s
        WHERE id = %s
    """,(novo_nome, novo_sobrenome, nova_foto, senha_para_salvar, novo_usuario, id_usuario))
    conexao.commit()
    cur.close()

    # Atualiza sessão
    session['usuario'] = novo_usuario
    session['nome'] = novo_nome
    session['sobrenome'] = novo_sobrenome
    session['foto'] = nova_foto

    mensagem = 'Perfil atualizado com sucesso!'
    return render_template('perfil.html', mensagem=mensagem, usuario=novo_usuario, nome=novo_nome, sobrenome=novo_sobrenome, foto=nova_foto)

if __name__ == "__main__":
    app.run(debug=True)