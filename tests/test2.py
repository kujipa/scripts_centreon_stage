#!/usr/bin/python3
#-*- coding: utf-8 -*-

# connaitre le nombre de lignes
f1 = open("instructions.txt","r")
nbrl = 0
for line in f1:
	nbrl += 1
f1.close()

g = open("instructions.txt","r")
i = 0
while i < nbrl:
	b = g.readline()
	if b[0] != '#':
		c = b.split()	
		print(c)
	i += 1
