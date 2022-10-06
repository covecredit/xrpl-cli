xrpl-cli security information
=============================
This file is a list of known security issues, weaknesses and ways to
report future ones. 

The current xrpl-cli is using Python (we may change in the future) and
as such is subject to some constraints on how it handles "sensitive" 
information on a multi-user system. If you provide a seed on the command
line, it can retain in the device command history, the process list and
other places you may not wish to have your seed. We are aware of this 
issue and will provide a security fix for it as the tool matures, for 
development purposes and using this code please treat as experimental
with known issues. To prevent this being a concern if you must use
this tool on mainnet in its current form, you can unset your HISTFILE 
and ensure that your host is ONLY used by your user. 

If you have vulnerabilities to report in this software, please contact
info@hacker.house who manage the project security requirements. 
