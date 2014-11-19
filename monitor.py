# Copyright 2012 James McCauley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Turns your complex OpenFlow switches into stupid hubs.
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
from pox.lib.recoco import Timer
from pox.openflow.of_json import *
import MySQLdb

log = core.getLogger()
global tempo
tempo = 5

def _timer_func ():
  for connection in core.openflow._connections.values():
    connection.send(of.ofp_stats_request(body=of.ofp_port_stats_request()))
  log.info("Sent %i flow/port stats request(s)", len(core.openflow._connections))

def _handle_portstats_received (event):
  stats = flow_stats_to_list(event.stats)
  #global tempo
  print "TEMPOOOO: "+str(tempo)
  tempo += 5
  insertDB(dpidToStr(event.connection.dpid),stats,tempo)
  #for i in stats:
   # log.info(i['port_no'])
  #log.info("PortStatsReceived from %s: %s",dpidToStr(event.connection.dpid), stats)

def launch ():
  # attach handsers to listners
  core.openflow.addListenerByName("PortStatsReceived",_handle_portstats_received)
  print "TEMPOOOO: "+str(tempo)
  # timer set to execute every five seconds
  Timer(5, _timer_func, recurring=True)


# MYSQL 
def insertDB(dpid, stats, tempo):
    [db,cur] = connectDB();
    for i in stats:
        rx_bytes = i['rx_bytes']
        tx_bytes = i['tx_bytes']
        port_no = i['port_no']
        sql = "INSERT INTO `sdn`.`stats` (`switch`, `rx_bytes`, `tx_bytes`, `port_no`, `time`) VALUES ('"+str(dpid)+"', "+str(rx_bytes)+", "+str(tx_bytes)+", "+str(port_no)+","+tempo+");"
        print sql
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
   # cur.execute("SELECT * FROM stats")

    # print all the first cell of all the rows
 #   for row in cur.fetchall() :
  #      print row

    return [db,cur]
