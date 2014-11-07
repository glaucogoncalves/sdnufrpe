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

from dctopo import FatTreeTopo

net = None

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
