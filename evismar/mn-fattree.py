import atexit
import time
import random
import os
from databaseControl import databaseControl
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

from threading import Timer

from dctopo import FatTreeTopo

net = None
SwitchesConsumption = {}
SwitchesPower = {}
LinksPower = {}

SwitchesCore = {}
SwitchesAgregation = {}
SwitchesEdge = {}

global currentTimee
currentTime = 0


def setLinkStatus(sw1, sw2, on):
	''' 
	sw1, sw2: switches that are at the borders of the link to be turned on/off 
	on: - if True link lnk must be turned ON
	    - if False link lnk must be turned OFF
	'''
	if on:
		net.configLinkStatus(sw1,sw2,'up')
	else:
		net.configLinkStatus(sw1,sw2,'down')
	
	if (sw1,sw2) in Links:
		Links[(sw1,sw2)] = on
        elif (sw2,sw1) in Links:
                Links[(sw2,sw1)] = on

def listSwitchLinks(sw):
	keyLists = Links.keys()
	linkList = []

	for i in keyLists:
                if i[0] == sw:
			linkList.append(i)
                elif i[1] == sw:
			linkList.append(i)

	return linkList

def setSwitchStatus(sw, on):
        '''
        sw = switch to be turned on/off
        on = - if True switch sw must be turned ON
             - if False switch sw must be turned OFF
        '''
        ''' Insert your code here '''
	
	linkList = listSwitchLinks(sw)
	for j in linkList:
		setLinkStatus(j[0],j[1],on)

        Switches[sw] = on;
	
def getLinkStatus(sw1, sw2):
	''' 
	sw1, sw2: switches that are at the borders of the link to be checked
	'''
	return Links[(sw1,sw2)]

def getSwitchStatus(sw):
	''' 
	sw = switch to be turned checked
	'''
	return Switches[sw]

''' 
Switches: Dictionary where each element indicates if a Switch is ON (True) or OFF (False)
Ex:
{
	'0_0_0': True,
	'0_0_1': False
}
'''
global Switches
Switches = {}
''' 
Links: Dictionary where the key is a 2-uple of switches and it indicates if a Link is ON (True) or OFF (False)
Ex:
{
	('0_0_0','0_0_1'): True,
	('0_0_1','0_1_2'): False
}
'''
global Links
Links = {}

''' 
checkingInterval: the time interval (in seconds) for computing energy consumption
'''
global checkingInterval
checkingInterval = 5


def calcEnergy():
	''' 
	This function calculates the energy wasted by each switch in the network
	'''
	'''Programming next call of this function'''
	t = Timer(checkingInterval, calcEnergy, ())
	t.daemon = True
	t.start()

	powerList = SwitchesPower.items()
	#print("===============CALCULATING ENERGY===============")
	result = 0
	global currentTime
	currentTime = currentTime + checkingInterval
	for i in powerList:
		if not Switches[i[0]]:
			switchPower = 0
		else:
			linkList = listSwitchLinks(i[0])

			portPower = 0
			for j in linkList:
				if Links[j]:
					portPower += LinksPower[j]*checkingInterval/3600.0
			                insertPortDB(j[0],j[1], portPower, currentTime)

				else:
			                insertPortDB(j[0],j[1] ,0, currentTime)
	
		
			switchPower = (i[1]*(checkingInterval/3600.0))+portPower	
		

		#print ("Switch "+ i[0]+" =  "+str(switchPower)+" Wh") 
		insertSwtDB(i[0], switchPower, currentTime)
		SwitchesConsumption[i[0]] = switchPower

		result = result + switchPower

	#print ("*** Total wast = "+str(result)+" Wh")
			
	#t = Timer(checkingInterval, calcEnergy, ())
	#t.daemon = True
	#t.start()
	
	#Checa Os Switches que precisam ser desligados e desliga os que forem necessario
	if (currentTime%50 == 0):
		checkSwitches()
	else: print ("You shall not turn off")
def createTopo(k = 4):
	topo=FatTreeTopo(k)
	return topo

def startNetwork():
	k = 6
	testTime = 300
	#numberOfSwitches = k**2 + (k/2)**2
	numberOfHosts = (k**3)/4
	numberOfHostsPerPod = (k/2)**2
	numberOfPods = numberOfSwitchesPerPod = k
	#numberOfCoreSwitches = (k/2)**2
	
	''' ===============================Gera os IDs dos Switches=================================='''
	print ("Switches de Agregacao e Ponta")
	for p in range(k):
		
		for s in range(k):
			if s%2 == 0:
				if s < k/2:
					swtcs = (str(p)+"_"+str(s)+"_"+str(1))
					for i in range(1,k/2):
						swtcs += ","+(str(p)+"_"+str(s+i)+"_"+str(1))
					SwitchesEdge[p+1] = swtcs

					
				else:
					swtcs = (str(p)+"_"+str(s)+"_"+str(1))
					for i in range(1,k/2):
						swtcs += ","+(str(p)+"_"+str(s+i)+"_"+str(1))
					SwitchesAgregation[p+1] = swtcs

	
	for pod in SwitchesAgregation:
		print SwitchesAgregation[pod]
	for pod in SwitchesEdge:
		print SwitchesEdge[pod]
	
	print ("Switches de Core")		
	
	
	for p in range(1,(k/2 + 1)):
		for s in range(1,(k/2 + 1)):
			if s%2 == 1:
				swtcs = (str(k)+"_"+str(p)+"_"+str(s))
				for i in range(1,k/2):
					swtcs += ","+(str(k)+"_"+str(p)+"_"+str(s+i))
				SwitchesCore[p] = swtcs
				
	for pod in SwitchesCore:
		print SwitchesCore[pod]
		
	
	'''============================================================================================'''
		
			
	topo = createTopo(k)
	global net
	net = Mininet( topo=topo, controller=None, link=TCLink)
        net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=6633 )
	net.start()
	random.seed(41241)
	
	# Configurando hosts
	hosts = 'h1'
	for a in range(2,numberOfHosts+1):
		b = ('h' + str(a))
		hosts = (hosts + ',' + b)
	exec('%s = net.hosts' % hosts)

	# Initialize here the Switches and Links dicts 
	# Insert your code here 

	
	for i in  topo.links(True):
		Links[i] = True
		LinksPower[i] = 0.5

	print topo.switches(True)
        for i in  topo.switches(True):
                Switches[i] = True
		SwitchesPower[i] = random.randint(100, 2000)
		SwitchesConsumption[i] = 0


	# Creating hosts
        hosts = []
        for host in range(1,numberOfHosts+1):
                hosts.append('h%s' % host)
        hosts.reverse()
	
	IPHosts = []
	for pod in range(0,numberOfPods):
		for edge in range(0,k/2):
			for host in range(1,numberOfHostsPerPod*2/k+1):
				hostID = hosts.pop()
				exec('%s.cmd("ifconfig %s-eth0 10.%s.%s.%s")' % (hostID,hostID,pod,edge,host))
				exec('%s.cmd("iperf -s &")' % hostID)
				IPHosts.append('10.%s.%s.%s' % (pod,edge,host))

	# Starting computing energy function
	calcEnergy()

	print("Iniciando POX")
	#os.system('/home/mininet/pox/pox.py samples.spanning_tree 2>/dev/null &')
	os.system('/home/mininet/pox/pox.py  misc.monitor riplpox.riplpox --topo=ft,4 --routing=hashed  2>/tmp/teste &')

	time.sleep(30)

	print("Apagando resultados anteriores...")
	os.system('if test -d /tmp/pratica-fat_results; then rm -rf /tmp/pratica-fat_results; fi')
	os.system('mkdir /tmp/pratica-fat_results')
	print("Iniciando testes...")

	overallDuration = 0
	testCount = 0
	while overallDuration <= testTime:
		HostServer = IPHosts[random.randrange(1,numberOfHosts)]
		HostClient = 'h%s' % random.randrange(1,numberOfHosts+1)
		interval = random.expovariate(1)
		duration = random.expovariate(0.2)
		print(interval,duration)
		print('Iniciando teste %s: Cliente: %s ; Servidor: %s' % (testCount,HostClient,HostServer))
		exec('%s.cmd("iperf -c %s --time %s >/tmp/pratica-fat_results/%s-%s.test &")' % (HostClient,HostServer,duration,testCount,HostClient))	
		#if overallDuration > 60:
		#	setSwitchStatus("4_1_1", False)
		time.sleep(interval)
		overallDuration = overallDuration + interval
		testCount = testCount + 1
	print("Tempo de teste atingido. Terminando testes...")
	print("Resultados disponiveis em /tmp/pratica-fat_results.")
	#CLI(net)
	os.system("kill -15 `ps -ef | grep pox | egrep -v grep | awk '{print $2}'`")
	os.system("kill -15 `ps -ef | grep iperf | egrep -v grep | awk '{print $2}'`")
	net.stop()
	
	
# MYSQL 
def insertSwtDB(switch,wh,tempo):
    [db,cur] = connectDB();
    
    swtParts = switch.split("_")
    swtName = "00-00-00-0"+swtParts[0]+"-0"+swtParts[1]+"-0"+swtParts[2]

    sql = "INSERT INTO `sdn`.`switch_energy` (`switch`, `time`, `wh`) VALUES ( '"+str(swtName)+"', "+str(tempo)+","+str(wh)+");"
    #print sql 
    cur.execute(sql)
    db.commit()

    cur.close()
    db.close()
         

def insertPortDB(switch1,switch2,wh,tempo):
    [db,cur] = connectDB();

    swtParts1 = switch1.split("_")
    swtName1 = "00-00-00-0"+swtParts1[0]+"-0"+swtParts1[1]+"-0"+swtParts1[2]

    swtParts2 = switch2.split("_")
    swtName2 = "00-00-00-0"+swtParts2[0]+"-0"+swtParts2[1]+"-0"+swtParts2[2]


    sql = "INSERT INTO `sdn`.`link_energy` (`switch_src`, `switch_dst`,`time`, `wh`) VALUES ( '"+str(swtName1)+"','"+str(swtName2)+"' ,"+str(tempo)+","+str(wh)+");"
    #print sql
    cur.execute(sql)
    db.commit()

    cur.close()
    db.close()

def connectDB():
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

def stopNetwork():
	if net is not None:
		net.stop()
		
def checkSwitches():
	dbControl = databaseControl(SwitchesCore, SwitchesAgregation, SwitchesEdge)
	SwtOff = dbControl.getSwitchesOff()
	SwtON = dbControl.getSwitchesON()
	for swt in SwtOff:
		setSwitchStatus(swt, False)
	for swt in SwtON:
		setSwitchStatus(swt, True)
if __name__ == '__main__':
	atexit.register(stopNetwork)
	setLogLevel('info')
	startNetwork()
