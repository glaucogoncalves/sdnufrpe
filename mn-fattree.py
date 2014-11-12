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

from threading import Timer

from dctopo import FatTreeTopo

net = None

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

def setSwitchStatus(sw, on):
	''' 
	sw = switch to be turned on/off 
	on = - if True switch sw must be turned ON
	     - if False switch sw must be turned OFF
	'''
	''' Insert your code here '''
	
	keyLists = Links.keys()
	
	for i in keyLists:
		if i[0] == sw:
			setLinkStatus(i[0],i[1],on)
		elif i[1] == sw:
			setLinkStatus(i[0],i[1],on)

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
	print("===============CALCULATING ENERGY===============")
	''' Insert your code here '''
	t = Timer(checkingInterval, calcEnergy, ())
	t.daemon = True
	t.start()

def createTopo(k = 4):
	topo=FatTreeTopo(k)
	return topo

def startNetwork():
	k = 4
	testTime = 120
	#numberOfSwitches = k**2 + (k/2)**2
	numberOfHosts = (k**3)/4
	numberOfHostsPerPod = (k/2)**2
	numberOfPods = numberOfSwitchesPerPod = k
	#numberOfCoreSwitches = (k/2)**2

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

	''' Initialize here the Switches and Links dicts '''
	''' Insert your code here '''

        for i in  topo.links(True):
                Links[i] = True
        for i in  topo.switches(True):
                Switches[i] = True





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

	print("Iniciando POX")
	#os.system('/home/mininet/pox/pox.py samples.spanning_tree 2>/dev/null &')
	os.system('/home/mininet/pox/pox.py riplpox.riplpox --topo=ft,4 --routing=hashed  2>/tmp/teste &')

	time.sleep(30)

	''' Starting computing energy function'''
	calcEnergy()

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
		time.sleep(interval)
		overallDuration = overallDuration + interval
		testCount = testCount + 1
	print("Tempo de teste atingido. Terminando testes...")
	print("Resultados disponiveis em /tmp/pratica-fat_results.")
	#CLI(net)
	os.system("kill -15 `ps -ef | grep pox | egrep -v grep | awk '{print $2}'`")
	os.system("kill -15 `ps -ef | grep iperf | egrep -v grep | awk '{print $2}'`")
	net.stop()

def stopNetwork():
	if net is not None:
		net.stop()

if __name__ == '__main__':
	atexit.register(stopNetwork)
	setLogLevel('info')
	startNetwork()
