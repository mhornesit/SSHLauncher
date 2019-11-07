import os
import sys
import json
import platform
import ctypes

for arg in sys.argv:
    if arg in ('-d', '--debug'):
        DEBUG = True
        break
    else:
        DEBUG = False

clear_command = "cls" if platform.system().lower()=="windows" else "clear"
escaped = False
while not escaped:
    restart = False
    servers = {}
    with open('servers.json', 'r') as config_file:
        raw_servers = json.loads(config_file.read())
        count = 0
        for name, raw_server in raw_servers.items():
            if name and name != 'template_server' and raw_server.get('ip'):
                count += 1
                server = raw_server.copy()
                server['name'] = name
                servers[str(count)] = server

    # read json file and put servers in dict with int as key
    print('Please select a server to connect to:')

    for key, server in servers.items():
        name = server.get('name') or server.get('ip')
        if name:
            print('    %s: %s' % (key, name))

    user_server = False
    while not user_server:
        user_server_key = input('')
        if user_server_key in servers:
            user_server = servers[user_server_key]
        else:
            print('Invalid server option. Please enter one of the listed server values')

    key = user_server.get('key')
    port = user_server.get('port')
    user = user_server.get('user')
    ip = user_server.get('ip')
    
    if not DEBUG:
            os.system(clear_command)  # Clear console
    
    while not escaped and not restart:

        terminal_type = user_server.get('terminal')
        
        if terminal_type == 'cmd' or not terminal_type:
            command = 'ssh '
            if key:
                command += '-i %s ' % key
            if port:
                command += '-p %s ' % port
            if user:
                command += '%s@' % user
            command += ip
            
            
        elif terminal_type == 'bash':
            command = 'bash -c "ssh '
            if key:
                command += '-i %s ' % key
            if port:
                command += '-P %s ' % port
            if user:
                command += '%s@' % user
            command += ip + '"'
        
        else:
            restart = True
            continue
        
        if DEBUG:
            print(command)
            
        # Execute command!
        os.system(command)
        
        if not DEBUG:
            os.system(clear_command)  # Clear console
        
        user_char = False
        while not user_char:
            print("Connection lost.  Press R to reconnect, C to choose a new connection, or N to quit... ")
            user_char = input('')
            if user_char:
                user_char = user_char.strip().lower()
                if user_char.lower() == 'r':
                    user_char = False
                    if not DEBUG:
                        os.system(clear_command)  # Clear console
                    break
                elif user_char.lower() == 'n':
                    escaped = True
                    if not DEBUG:
                        os.system(clear_command)  # Clear console
                    break
                elif user_char.lower() == 'c':
                    restart = True
                    if not DEBUG:
                        os.system(clear_command)  # Clear console
                    break
                else:
                    print("Invalid response.")
                    user_char = False
                    continue
            
