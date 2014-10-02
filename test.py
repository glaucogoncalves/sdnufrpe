import atexit
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

        s1 = topo.addSwitch('s1')
        s2 = topo.addSwitch('s2')
        s3 = topo.addSwitch('s3')
        s4 = topo.addSwitch('s4')
        topo.addLink(s1, s2)
        topo.addLink(s2, s3)
        topo.addLink(s3, s4)
        topo.addLink(s4, s1)
        h1 = topo.addHost('h1')
        h2 = topo.addHost('h2')
        h3 = topo.addHost('h3')
        h4 = topo.addHost('h4')
        topo.addLink(h1, s1)
        topo.addLink(h2, s2)
        topo.addLink(h3, s3)
        topo.addLink(h4, s4)

	return topo

def startNetwork():
	topo = createTopo()
	global net
	net = Mininet( topo=topo, controller=None)
        net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=6633 )
	net.start()
	CLI(net)

def stopNetwork():
	if net is not None:
		net.stop()

if __name__ == '__main__':
	atexit.register(stopNetwork)
	setLogLevel('info')
	startNetwork()
