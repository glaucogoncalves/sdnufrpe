#Exercise of the course Advanced Topics in Computer Networks at UFRPE/Brazil
#Author: Kleber Leal and Glauco Goncalves, PhD

#!/bin/bash
echo "Iniciando o controlador remoto"
echo "Para interromper o controlador pressione Ctrl+C"
/home/mininet/pox/pox.py samples.spanning_tree >/dev/null 2>&1
