# PrimusEnum
This is a script made for automating some of the scans in the enumeration phase when testing a web application or doing a CTF. The scrip will create a file structure and output the different results to their own .txt or folder.

***This is a work in progress script***

## Dependcies 
The most important dependencies should be installed automatically - if it fails try a manual install, the following tools have been used in the script:
```
NMAP
feroxbuster
dirsearch.py
curl
```

# Usage:
*Script must be run a sudo*

The script can handle two types of input, either `https://www.test.com/` with the argument `-u`or use the `-i` argument with `https://10.10.10.10/`

*Examples*

`-u` argument
```
sudo python3 PrimusEnum.py -u https://www.test.com/  
```
`-i` argument 
```
sudo python3 PrimusEnum.py -i http://10.10.10.10/  
```
