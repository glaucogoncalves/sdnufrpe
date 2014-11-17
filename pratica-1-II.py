#Exercise of the course Advanced Topics in Computer Networks at UFRPE/Brazil 
#Author: Kleber Leal and Glauco Goncalves, PhD

import atexit
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import info,setLogLevel
from mininet.node import RemoteController

net = None

global Switches
Switches = {}
'''
Links: Dictionary where the key is a 2-uple of switches and it indicates if a L$
Ex:
{
        ('0_0_0','0_0_1'): True,
        ('0_0_1','0_1_2'): False
}
'''
global Links
Links = {}

'''
checkingInterval: the time interval (in seconds) for computing energy consumpti$
'''

def setLinkStatus(sw1, sw2, on):
        '''
        sw1, sw2: switches that are at the borders of the link to be turned on/$
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

        pass


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


def createTopo():
        topo=Topo()

        #Create Nodes
        topo.addHost("h1")
        topo.addHost("h2")
        topo.addHost("h3")
        topo.addHost("h4")
        topo.addSwitch('s1')
        topo.addSwitch('s2')
        topo.addSwitch('s3')

        #Create links
        topo.addLink('s1','s2')
        topo.addLink('s1','s3')
        topo.addLink('h1','s2')
        topo.addLink('h2','s2')
        topo.addLink('h3','s3')
        topo.addLink('h4','s3')
        return topo

def startNetwork():
        topo = createTopo()
        global net
        net = Mininet(topo=topo, autoSetMacs=True)
        net.start()
        #CLI(net)
	print topo.links(True)
	for i in  topo.links(True):
		Links[i] = True
	print topo.switches(True)
        for i in  topo.switches(True):
                Switches[i] = True
	setSwitchStatus('s3',False)
	net.pingAll()
	setSwitchStatus('s3',True)
	net.pingAll()
	

def stopNetwork():
        if net is not None:
                net.stop()

if __name__ == '__main__':
        atexit.register(stopNetwork)
        setLogLevel('info')
        startNetwork()
	

