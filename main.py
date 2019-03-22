import yaml
from flask import Flask, render_template, jsonify

import network

app = Flask(__name__)
configs = yaml.load(open('config.yml'))

@app.route('/', methods=['GET'])
def comando_executar():
    network_obj = network.Network(configs['vpn']['host'], configs['vpn']['user'], configs['vpn']['key_path'])
    logged_users = network_obj.logged_users()
    print (logged_users)

    return render_template('users.html', dict_users=logged_users)

@app.route('/json')
def comando_json():
    network_obj = network.Network(configs['vpn']['host'], configs['vpn']['user'], configs['vpn']['key_path'])
    logged_users = network_obj.logged_users()

    return jsonify(logged_users)

    

if __name__ == '__main__':
    app.run()