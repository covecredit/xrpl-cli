all: xrpl-cli manpage/xrpl-cli.1

xrpl-cli: xrplcli.py xrpl-cli.c
	cython --embed -o xrpl-cli.c xrplcli.py
	gcc -Os -I /usr/include/python3.10 -o xrpl-cli xrpl-cli.c -lpython3.10 -lpthread -lm -lutil -ldl 

manpage/xrpl-cli.1: manpage/xrpl-cli.1.md 
	pandoc manpage/xrpl-cli.1.md -s -t man -o manpage/xrpl-cli.1

clean: 
	rm -rf xrpl-cli
	rm -rf manpage/xrpl-cli.1
