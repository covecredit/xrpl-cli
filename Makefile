all: xrpl-cli manpage/xrpl-cli.1

xrpl-cli: xrplcli.py xrpl-cli.c
	pip3 install -r requirements.txt
	cython3 --embed -o xrpl-cli.c xrplcli.py
	gcc -Os -I /usr/include/python3.11 -o xrpl-cli xrpl-cli.c -lpython3.11 -lpthread -lm -lutil -ldl 

manpage/xrpl-cli.1: manpage/xrpl-cli.1.md 
	pandoc manpage/xrpl-cli.1.md -s -t man -o manpage/xrpl-cli.1

clean: 
	rm -rf xrpl-cli
	rm -rf manpage/xrpl-cli.1
