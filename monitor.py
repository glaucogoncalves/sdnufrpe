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

log = core.getLogger()

def _timer_func ():
  for connection in core.openflow._connections.values():
    connection.send(of.ofp_stats_request(body=of.ofp_port_stats_request()))
  log.info("Sent %i flow/port stats request(s)", len(core.openflow._connections))

def _handle_portstats_received (event):
  stats = flow_stats_to_list(event.stats)
  for i in stats:
    log.info(i['port_no'])
  #log.info("PortStatsReceived from %s: %s",dpidToStr(event.connection.dpid), stats)

def launch ():
  # attach handsers to listners
  core.openflow.addListenerByName("PortStatsReceived",_handle_portstats_received) 

  # timer set to execute every five seconds
  Timer(5, _timer_func, recurring=True)
