import os
import yaml
from flask import Flask, render_template, jsonify, \
                                request, Response, redirect, url_for, session

from service.vpn import Vpn

app = Flask(__name__)
app.secret_key = 'eipohgoo4rai0uf5ie1oshahmaeF'
configs = yaml.load(open('config.yml'))

vpn = Vpn(configs['vpn']['host'], configs['vpn']['user'], configs['vpn']['key_path'])

def validate_session(session):
    if session.get('username'):
        return True
    else:
        return False


@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    error  = ''
    if request.method == 'POST':
        try:
            attempted_username = request.form['username']
            attempted_password = request.form['password']
            
            #Realizar query para pegar o usuario na base.
            if attempted_username == str(os.environ.get('APP_USER')) and attempted_password == str(os.environ.get('APP_PASS')):
                session['username'] = request.form['username']
                return redirect(url_for('get_index'))
                #URL_FOR expects the name of the function
            else:
                error = 'Usuario ou Senha invalidos'
                print (error)
                return render_template("login.html", error=error)
        except Exception as e:
            print (e)
            error = 'Usuario ou Senha invalidos'
            return render_template("login.html", error=error)
    else:
        return render_template("login.html", error=error)

@app.route('/logout/', methods=['POST', 'GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login_page'))

@app.route('/', methods=['GET'])
def get_index():
    if validate_session(session):
        return render_template('index.html')
    return redirect(url_for('login_page'))

@app.route('/get_users', methods=['GET'])
def mostrar_usuarios():
    if validate_session(session):
        logged = vpn.logged_users()
        print (logged)
        return render_template('users.html', dict_users=logged)
    return redirect(url_for('login_page'))

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if validate_session(session):
        if request.method == 'GET':
            return render_template('add_user.html')
        elif request.method == 'POST':
            #Adicionar usuario
            username = request.values.get('usuario')
            user_add = vpn.adicionar_user(username)
            if user_add:
                print (user_add)
                #Content to Download
                return Response(user_add, mimetype='application/text', headers={'Content-Disposition':'attachment;filename={}.ovpn'.format(username)})
            else:
                return "Erro"
    return redirect(url_for('login_page'))

@app.route('/remove_user', methods=['GET', 'POST'])
def remove_user():
    if validate_session(session):
        if request.method == 'GET':
            usuarios = vpn.list_existing_users(configs['openvpn']['pki_folder'])
            return render_template('remove_user.html', users=usuarios)
        elif request.method == 'POST':
            user_remove = vpn.remover_user(request.values.get('my_user'), configs['openvpn']['pki_folder'])
            return redirect(url_for('remove_user'))
    return redirect(url_for('login_page'))
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')