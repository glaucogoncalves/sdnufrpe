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
        swCore2 = topo.addSwitch('s2')
        swCore3 = topo.addSwitch('s3')
        swCore4 = topo.addSwitch('s4')

        ## Ajuste do parametro de fanout da rede
        fanout1  = 2
	fanout2  = 8 

        # Switches counter
        lastSW = 5
        lastHost = 1

        # Aggregation switches loop
        for i in irange (1, fanout2):
                swAggregL = topo.addSwitch('s%s' % lastSW)
                
		if i % 2 == 0:
			topo.addLink(swCore3, swAggregL)
                	topo.addLink(swCore4, swAggregL)
                else:
			topo.addLink(swCore1, swAggregL)
                	topo.addLink(swCore2, swAggregL)
                lastSW += 1

                # Edge switches loop
                for j in irange (1, fanout1):
			                               				                
    		                	        
			if i % 2 == 1:
				swEdge = topo.addSwitch('s%s' % lastSW)
	
				topo.addLink(swAggregL, swEdge)
	                	lastSW += 1
			else:
				if j % 2 == 1:
#					swEdge2 = topo.addSwitch('s%s' % (lastSW-1))
					topo.addLink(swAggregL, swEdge)
				else:
					swEdge2 = topo.addSwitch('s%s' % (lastSW-3))
					topo.addLink(swAggregL, swEdge2)

                        # Hosts loop
                        for k in irange (1, fanout1):
				if j % 2 == 1:
	                                host = topo.addHost('h%s' % lastHost)
        	                        topo.addLink(swEdge, host)
                	                lastHost += 1
	
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
