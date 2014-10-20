import atexit
import time
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import info,setLogLevel
from mininet.node import Controller
from functools import partial
from mininet.node import RemoteController
from mininet.util import irange,dumpNodeConnections

net = None

def createTopo():
	topo=Topo()

        swCore1 = topo.addSwitch('s1')
	
	k = 4
	numCoreSwitch = (k/2)**2
	numPod = k

	listaSwitch = []

	switchNum = 1

	numAggSwitch = k/2
	numEdgeSwitch = k/2
	
	numHost = (k/2)**2
	lastHost = 1

	for i in irange(1,numCoreSwitch):
		swCore = topo.addSwitch('s%s'% switchNum)
		listaSwitch.append(swCore)
		switchNum += 1
	
	listaPod = []
	
	for j in irange(1, numPod):
		numCore = 0
		listSwAgg = []
		for l in irange(1,numAggSwitch):
			swAgg = topo.addSwitch('s%s' % switchNum)
			listSwAgg.append(swAgg)
			for m in irange(1,k/2):
				topo.addLink(swAgg, listaSwitch[numCore])
				numCore += 1
			
			switchNum += 1
		
		listSwEdge = []		
		for n in irange(1, numEdgeSwitch):
			swEdge = topo.addSwitch('s%s' % switchNum)
			listSwEdge.append(swEdge)
			numAgg = 0
			for o in irange(1,k/2):
				topo.addLink(swEdge,listSwAgg[numAgg])
				numAgg += 1
			
			switchNum += 1
		
		for p in range(0, numHost):
			swHost = topo.addHost('h%s' % lastHost)
			lastHost += 1
			q = p/(k/2)
			topo.addLink(swHost, listSwEdge[q])
	
	return topo

def startNetwork():
	topo = createTopo()
	global net
	net = Mininet( topo=topo, controller=None)
        net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=6633 )
	net.start()
	time.sleep(20)
	CLI(net)

def stopNetwork():
	if net is not None:
		net.stop()

if __name__ == '__main__':
	atexit.register(stopNetwork)
	setLogLevel('info')
	startNetwork()
