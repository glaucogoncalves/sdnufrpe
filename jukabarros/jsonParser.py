import json
import MySQLdb


lista = [{'rx_over_err': 0, 'tx_dropped': 0, 'rx_packets': 36236, 'rx_frame_err': 0, 'rx_bytes': 665300570, 'tx_errors': 0, 'rx_crc_err': 0, 'collisions': 0, 'rx_errors': 0, 'tx_bytes': 588119150, 'rx_dropped': 0, 'tx_packets': 35738, 'port_no': 3}, {'rx_over_err': 0, 'tx_dropped': 0, 'rx_packets': 70074, 'rx_frame_err': 0, 'rx_bytes': 1952444298, 'tx_errors': 0, 'rx_crc_err': 0, 'collisions': 0, 'rx_errors': 0, 'tx_bytes': 4264901488L, 'rx_dropped': 0, 'tx_packets': 104473, 'port_no': 1}, {'rx_over_err': 0, 'tx_dropped': 0, 'rx_packets': 40454, 'rx_frame_err': 0, 'rx_bytes': 1147059402, 'tx_errors': 0, 'rx_crc_err': 0, 'collisions': 0, 'rx_errors': 0, 'tx_bytes': 1457984684, 'rx_dropped': 0, 'tx_packets': 64069, 'port_no': 4}, {'rx_over_err': 0, 'tx_dropped': 0, 'rx_packets': 103862, 'rx_frame_err': 0, 'rx_bytes': 3706232166L, 'tx_errors': 0, 'rx_crc_err': 0, 'collisions': 0, 'rx_errors': 0, 'tx_bytes': 1160060154, 'rx_dropped': 0, 'tx_packets': 46786, 'port_no': 2}, {'rx_over_err': 0, 'tx_dropped': 0, 'rx_packets': 0, 'rx_frame_err': 0, 'rx_bytes': 0, 'tx_errors': 0, 'rx_crc_err': 0, 'collisions': 0, 'rx_errors': 0, 'tx_bytes': 0, 'rx_dropped': 0, 'tx_packets': 0, 'port_no': 65534}]

def insertDB(dpid, stats, time):
    [db,cur] = connectDB();
    print dpid
    for i in stats:
        rx_bytes = i['rx_bytes']
        tx_bytes = i['tx_bytes']
        port_no = i['port_no']
        sql = "INSERT INTO `sdn`.`stats` (`switch`, `rx_bytes`, `tx_bytes`, `port_no`, `time`) VALUES ('"+str(dpid)+"', "+str(rx_bytes)+", "+str(tx_bytes)+", "+str(port_no)+","+time+");"
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


#insertDB("00-00-00-03-03-01", lista, "2")
#connectDB()
