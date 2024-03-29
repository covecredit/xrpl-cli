# xrpl-cli
Command-line utilities for working with the XRPL blockchain. 
xrpl-cli is to the XRPL blockchain what curl / wget are to the 
web. A simple command line interface for performing common operations 
such as creating wallets, using faucets, minting NFT's, trading tokens, 
querying nodes, managing accounts and signatures. 

# Install
The following commands can be used to install the Python requirements to run.

````
pip3 install -r requirements.txt
python3 xrpl-cli.py --help  
````

# Examples
The following examples can be used to test the xrpl-cli application. 

```
python3 xrpl-cli.py --network 2 --account rsUjg5ekUMpoJG8NgabUz3WCkpgrkmVUZe
python3 xrpl-cli.py --account rEx2PsuEurkNQwQbiCeoj1rdAjzu1gX3XF --network 3 -l
python3 xrpl-cli.py -g -n 2 -t abcdef -l
```

The last command will generate a wallet via faucet on the test network and
mint the NFT string "abcdef" and then list the wallet contents to verify the NFT.

# Docker

You can run this utility within a Docker container to ease configuration and use.

```
docker build -t xrpl-cli .
docker run xrpl-cli
docker run xrpl-cli -n 2 -g 
```

# Dependancies
The following packages are commonly required on Ubuntu based distributions and
should be installed before creating a compiled version. 

```
apt-get install build-essential python3 pandoc python3-dev cython3 python3-pip
```

# Compile

You can create a stand-alone xrpl-cli (dynamic) binary for xrpl-cli using Cython.

```
make
```

# Security
This program is under active development and should not be used on mainnet
until it reaches a stable release. For all currently known security issues
and details on where to report security vulnerablities, read SECURITY.md.
