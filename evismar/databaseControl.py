import atexit
import time
import random
import os
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import info,setLogLevel
from mininet.node import Controller
from functools import partial
from mininet.node import RemoteController
from mininet.util import irange,dumpNodeConnections
from mininet.link import TCLink
import MySQLdb




class databaseControl:
	global SwitchesCore
	global SwitchesAgregation
	global SwitchesEdge
	global SwitchesOff
	global SwitchesON
	
	SwitchesCore = {}
	SwitchesAgregation = {}
	SwitchesEdge = {}
	
	SwitchesOff = []
	SwitchesON = []

	def __init__(self, sc = {},sa = {},se = {}):
		SwitchesCore = sc
		SwitchesAgregation = sa
		SwitchesEdge = se		

		[db,cursor] = self.connectDB();
		
		
		'''=====================================================Inicio Core=========================================================='''
		SC = SwitchesCore.values()	
		for pair in SC:
			print pair
		
			swtParts = pair.split(",")

			swtParts1 = swtParts[0].split("_")
			swtName1 = "00-00-00-0"+swtParts1[0]+"-0"+swtParts1[1]+"-0"+swtParts1[2]
			
			swtParts2 = swtParts[1].split("_")
			swtName2 = "00-00-00-0"+swtParts2[0]+"-0"+swtParts2[1]+"-0"+swtParts2[2]

			sql = "SELECT * FROM `sdn`.`stats` WHERE `stats`.`switch` = '"+str(swtName1)+"' ORDER BY `stats`.`time` DESC LIMIT 10;"
			print sql
			cursor.execute(sql)
				
			try:
				# Execute the SQL command
				cursor.execute(sql)
				# Fetch all the rows in a list of lists.
				results1 = cursor.fetchall()
			except:
				print "Error: unable to fecth data"
				
			sql = "SELECT * FROM `sdn`.`stats` WHERE `stats`.`switch` = '"+str(swtName2)+"' ORDER BY `stats`.`time` DESC LIMIT 40;"
			print sql
			cursor.execute(sql)
				
			try:
				# Execute the SQL command
				cursor.execute(sql)
				# Fetch all the rows in a list of lists.
				results2 = cursor.fetchall()
			except:
				print "Error: unable to fecth data"
				
				
			counter = 0	
			sum = 0
			for row in results1:
				sum += results2[counter][3] + row[3] + results2[counter][4] + row[4]
				counter+= 1
			
			print ("TAMANHO DAS SOMAS DOS DADOS TRANSMITIDOS CORE")
			print sum
			if sum < 	500000000:
				SwitchesOff.append(swtParts[0])
				print ("Deligar "+ swtParts[0])	
			elif sum > 	1000000000:
				SwitchesON.append(swtParts[0])
				print ("LIGAR "+ swtParts[0])				
		

				
		

			'''=====================================================Inicio Agregation=========================================================='''	
	
		SA = SwitchesAgregation.values()
		for pair in SA:
			print pair
		
			swtParts = pair.split(",")

			swtParts1 = swtParts[0].split("_")
			swtName1 = "00-00-00-0"+swtParts1[0]+"-0"+swtParts1[1]+"-0"+swtParts1[2]
			
			swtParts2 = swtParts[1].split("_")
			swtName2 = "00-00-00-0"+swtParts2[0]+"-0"+swtParts2[1]+"-0"+swtParts2[2]

			sql = "SELECT * FROM `sdn`.`stats` WHERE `stats`.`switch` = '"+str(swtName1)+"' ORDER BY `stats`.`time` DESC LIMIT 10;"
			print sql
			cursor.execute(sql)
				
			try:
				# Execute the SQL command
				cursor.execute(sql)
				# Fetch all the rows in a list of lists.
				results1 = cursor.fetchall()
			except:
				print "Error: unable to fecth data"
				
			sql = "SELECT * FROM `sdn`.`stats` WHERE `stats`.`switch` = '"+str(swtName2)+"' ORDER BY `stats`.`time` DESC LIMIT 40;"
			print sql
			cursor.execute(sql)
				
			try:
				# Execute the SQL command
				cursor.execute(sql)
				# Fetch all the rows in a list of lists.
				results2 = cursor.fetchall()
			except:
				print "Error: unable to fecth data"
				
				
			counter = 0	
			sum = 0
			for row in results1:
				sum += results2[counter][3] + row[3] + results2[counter][4] + row[4]
				counter+= 1
			
			print ("TAMANHO DAS SOMAS DOS DADOS TRANSMITIDOS AGREGACAO")
			print sum
			if sum < 	500000000:
				SwitchesOff.append(swtParts[0])
				print ("Deligar "+ swtParts[0])					
			elif sum > 	1000000000:
				SwitchesON.append(swtParts[0])
				print ("LIGAR "+ swtParts[0])		

	
	
		'''=====================================================Fim Agregation=========================================================='''		
		cursor.close()
		db.close()
	def getSwitchesOff(self):
		return SwitchesOff
		
	def getSwitchesON(self):
		return SwitchesON
		
	def connectDB(self):
		db = MySQLdb.connect(host="localhost", # your host, usually localhost
						 user="root", # your username
						  passwd="sdn2014", # your password
						  db="sdn") # name of the data base

		# you must create a Cursor object. It will let
		#  you execute all the queries you need
		cur = db.cursor() 

		# Use all the SQL you like
		#cur.execute("SELECT * FROM stats")

	    # print all the first cell of all the rows
		#for row in cur.fetchall() :
		#  print row

		return [db,cur]	
		
	''' Queries
	SELECT * FROM sdn.switch_energy where switch = '00-00-00-04-02-01';
	SELECT * FROM sdn.switch_energy where switch = '00-00-00-04-02-02';
	'''
		

		
		
		
		
		
		
		
		