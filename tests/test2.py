#!/usr/bin/python3
#-*- coding: utf-8 -*-

# structure switch
def nolla():
	print('')

def yksi():
	print('"values":"{}"'.format(values[0]))

def kaksi():
	print('"values":"{};{}"'.format(values[0],values[1]))

def kolme():
	print('"values":"{};{};{}"'.format(values[0],values[1],values[2]))

options = {0 : nolla, 1 : yksi , 2 : kaksi , 3 : kolme }


g = open("instructions.txt","r")
i = 0
while i < nbrl: 
	c = g.readline().split()
	objet = c[0]
	action = c[1]
	values = c[2:]

	r = sess.post('http://192.168.10.218/centreon/api/index.php?action=action&object=centreon_clapi', 
		headers={"centreon-auth-token": token, 'Content-Type': 'application/json'}, 
		json={"action":"{}".fomat(action), "object":"{}".format(objet), options[len(values)]() }
		)
	print(r.text)
	i++
