import paramiko

def connect_ssh(host, username, key, command):
    """
        Executar comando remotos em servidores linux
    """
    try:
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print (host, username, key, command)
        client.connect(host, username=username, key_filename=key, timeout=2)
        print ("Conectou")
        stdin, stdout, stderr = client.exec_command(command)
        print (stdin, stdout, stderr)
        stdout = stdout.readlines()
        client.close()
        return stdout
    except Exception as e:
        print ("Erro problema de conexao {}".format(e))
        return None