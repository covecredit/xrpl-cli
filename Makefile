all: xrpl-cli

xrpl-cli: xrplcli.py xrpl-cli.c
	cython --embed -o xrpl-cli.c xrplcli.py
	gcc -Os -I /usr/include/python3.10 -o xrpl-cli xrpl-cli.c -lpython3.10 -lpthread -lm -lutil -ldl

clean: 
	rm -rf xrpl-cli
