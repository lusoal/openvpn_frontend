import yaml
from flask import Flask, render_template, jsonify, request, Response, redirect, url_for

from service.vpn import Vpn

app = Flask(__name__)
configs = yaml.load(open('config.yml'))

vpn = Vpn(configs['vpn']['host'], configs['vpn']['user'], configs['vpn']['key_path'])

@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html')

@app.route('/get_users', methods=['GET'])
def mostrar_usuarios():
    logged = vpn.logged_users()
    print (logged)
    return render_template('users.html', dict_users=logged)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
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

@app.route('/remove_user', methods=['GET', 'POST'])
def remove_user():
    if request.method == 'GET':
        usuarios = vpn.list_existing_users(configs['openvpn']['pki_folder'])
        return render_template('remove_user.html', users=usuarios)
    elif request.method == 'POST':
        user_remove = vpn.remover_user(request.values.get('my_user'), configs['openvpn']['pki_folder'])
        return redirect(url_for('remove_user'))
        
        


#@app.route('/json')
#def retornar_json_usuarios():
#    network_obj = network.Network(configs['vpn']['host'], configs['vpn']['user'], configs['vpn']['key_path'])
#    logged_users = network_obj.logged_users()
#
#    return jsonify(logged_users)

    

if __name__ == '__main__':
    app.run()