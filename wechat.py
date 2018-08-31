import itchat

itchat.auto_login(hotReload=True)

for friend in itchat.get_friends():
    print(friend)

# itchat.send('hello, aaaaa~~~', toUserName='@68e1939df79244308fb75b7a5ced3255')
