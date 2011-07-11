import socket
import paramiko
import os
import sys
import getpass

def auth_r(hostname, username, transport):
    default_path = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
    """
    path = raw_input('RSA key [%s]: ' % default_path)
    if len(path) == 0:
        path = default_path
    """
    try:
	key = paramiko.RSAKey.from_private_key_file(path)
    except paramiko.PasswordRequiredException:
	password = getpass.getpass('RSA key password: ')
	key = paramiko.RSAKey.from_private_key_file(path, password)
    transport.auth_publickey(username, key)


def auth_p(hostname, username, password, transport):
    transport.auth_password(username, password)



def connect_r(hostname, username):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))
    t = paramiko.Transport(sock)
    t.start_client()
    try:
	keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    except IOError:
	print '*** Unable to open host keys file'
        keys = {}
    #check server's host key 
    key = t.get_remote_server_key()
    if not keys.has_key(hostname):
        print '*** WARNING: Unknown host key!'
    elif not keys[hostname].has_key(key.get_name()):
        print '*** WARNING: Unknown host key!'
    elif keys[hostname][key.get_name()] != key:
        print '*** WARNING: Host key has changed!!!'
        sys.exit(1)
    else:
	print '*** Host key OK.'
    auth_r(hostname, username, t)
    if not t.is_authenticated():
        print '*** Authentication failed. :('
        t.close()
        sys.exit(1)
    return t

def connect_p(hostname, username, password):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))
    t = paramiko.Transport(sock)
    t.start_client()
    try:
        keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    except IOError:
        print '*** Unable to open host keys file'
        keys = {}
    #check server's host key 
    key = t.get_remote_server_key()
    if not keys.has_key(hostname):
        print '*** WARNING: Unknown host key!'
    elif not keys[hostname].has_key(key.get_name()):
        print '*** WARNING: Unknown host key!'
    elif keys[hostname][key.get_name()] != key:
        print '*** WARNING: Host key has changed!!!'
        sys.exit(1)
    else:
        print '*** Host key OK.'
    auth_p(hostname, username, password, t)
    if not t.is_authenticated():
        print '*** Authentication failed. :('
        t.close()
        sys.exit(1)
    return t

def scp_to_r(hostname, username, remote_path, local_path):	
    t = connect_r(hostname, username)
    scp_channel = t.open_session()
    
    #step of copy
    f = file(local_path, 'rb')
    scp_channel.exec_command('scp -v -t %s\n' % '/'.join(remote_path.split('/')[:-1]))
    scp_channel.send('C%s %d %s\n' % (oct(os.stat(local_path).st_mode)[-4:], os.stat(local_path)[6], remote_path.split('/')[-1]))
    scp_channel.sendall(f.read())
    f.close()
    
    scp_channel.close()
    t.close()

def scp_from_r(hostname, username, local_path, remote_path):
    t = connect_r(hostname, username)
    scp_channel = t.open_session()
    
    #step of copy
    f = file(remote_path, 'rb')
    scp_channel.exec_command('scp -v -t %s\n' % '/'.join(local_path.split('/')[:-1]))
    scp_channel.send('C%s %d %s\n' % (oct(os.stat(remote_path).st_mode)[-4:], os.stat(remote_path)[6], local_path.split('/')[-1]))
    scp_channel.sendall(f.read())
    f.close()
    
    scp_channel.close()
    t.close()



def scp_to_p(hostname, username, password, remote_path, local_path):
    t = connect_p(hostname, username, password)
    scp_channel = t.open_session()
    
    #step of copy
    f = file(local_path, 'rb')
    scp_channel.exec_command('scp -v -t %s\n' % '/'.join(remote_path.split('/')[:-1]))
    scp_channel.send('C%s %d %s\n' % (oct(os.stat(local_path).st_mode)[-4:], os.stat(local_path)[6], remote_path.split('/')[-1]))
    scp_channel.sendall(f.read())
    f.close()
    
    scp_channel.close()
    t.close()


def scp_from_p(hostname, username, password, local_path, remote_path):
    t = connect_p(hostname, username, password)
    scp_channel = t.open_session()

    #step of copy
    f = file(remote_path, 'rb')
    scp_channel.exec_command('scp -v -t %s\n' % '/'.join(local_path.split('/')[:-1]))
    scp_channel.send('C%s %d %s\n' % (oct(os.stat(remote_path).st_mode)[-4:], os.stat(remote_path)[6], local_path.split('/')[-1]))
    scp_channel.sendall(f.read())
    f.close()
    
    scp_channel.close()
    t.close()


