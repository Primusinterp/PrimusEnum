import subprocess
import argparse
import re
import os

parser = argparse.ArgumentParser(description='PrimusinterpEnum  ')
parser.add_argument('-u', type=str, required=False, help='Input the target URL -eg https://www.facebook.com/')
parser.add_argument('-i', type=str, required=False, help='Input the target IP -eg http://10.10.194.158/')

#Varibels
args = parser.parse_args()
pwd = os.getcwd()
info_dir ='infodump'
loot_dir ='loot'
dirsearch_dir = '/opt/dirsearch'
curl_dir = 'curl_sites'
ferox_name = 'feroxbuster'

#Dependecies
try:
    print(r"""
  _____      _                     ______
 |  __ \    (_)                   |  ____|
 | |__) | __ _ _ __ ___  _   _ ___| |__   _ __  _   _ _ __ ___
 |  ___/ '__| | '_ ` _ \| | | / __|  __| | '_ \| | | | '_ ` _ \
 | |   | |  | | | | | | | |_| \__ \ |____| | | | |_| | | | | | |
 |_|   |_|  |_|_| |_| |_|\__,_|___/______|_| |_|\__,_|_| |_| |_|""")
    print('\n')
    print('[+] Installing Dependecies. . .')
    dep_dir = os.path.isdir(dirsearch_dir)
    #print(dep_dir
    if dep_dir == False:
        install_dirsearch = ["git", "clone", "https://github.com/maurosoria/dirsearch.git", "/opt/dirsearch"]
        subprocess.run(install_dirsearch)
    else:
        print(f'[+] The directory {dirsearch_dir} already exists. . . Moving on')

    ferox_check = subprocess.call(["which", ferox_name,], stdout=subprocess.DEVNULL)
    if ferox_check != 0:
        print(f"{ferox_name} not installed!")
        install_cmd=["apt", "install", ferox_name]
        subprocess.run(install_cmd)
    print(f'[+] All Dependecies are installed. . . Moving on','\n')
except:
    print(f'[+] Error in installing Dependecies. . . Please try a manual install')

if args.u:
    #Regex
    full_URL = args.u
    print(f'[+] Enumerating: {full_URL}')
    re_URL = re.findall('\w+\:\/\/\w+\.(\w+)\.\w+\/', args.u)
    #print(re_URL)
    top_dir =(' '.join(re_URL))

    #obtain IP from domain name - used for nmap
    re_ping_url = re.findall('\w+\:\/\/\w+\.(\w+\.\w+)\/', full_URL)
    ping_url = ' '.join(re_ping_url)
    ping_cmd = ["ping","-c","1", ping_url]
    res = subprocess.run(ping_cmd, capture_output=True)
    re_ip = re.findall('(\d+\.\d+\.\d+\.\d+)', str(res))



    print('[+] Creating file structure. . .')

    #Create directory for info and loot
    def create_dir(p):
        isdir = os.path.isdir(p)
        #print(isdir)
        if isdir == False:
            print(f'[+] Creating folder in {pwd} for infodump & loot. . . ')
            try:
                os.mkdir(p)
            except OSError:
                print ("[+] Creation of the directory %s failed" % p)
            else:
                print ("[+] Successfully created the directory %s " % p)
        else:
            print(f'The directory {p} already exists. . . Please remove old results and try again')
    create_dir(top_dir)


    #Sub directory creation
    #print('\n')
    os.chdir(top_dir)
    pwd = os.getcwd()
    print('[+] Creating sub directories. . .')
    create_dir(info_dir)
    create_dir(loot_dir)
    os.chdir(info_dir)
    pwd = os.getcwd()
    create_dir(curl_dir)

    print('\n')
    print('#'*100)
    print('[+] Starting web enum. . .')
    print('#'*100)
    print('\n')

    #NMAP enumeration
    print(f'[+] Starting NMAP enumeration of: {full_URL}. . . output to nmap_scan.txt')
    print('[+] Iniating with aggressive scan of target. . .')
    nmap_cmd = ["nmap", "-A", "-T4", "-vv", ''.join(re_ip[0])]
    subprocess.run(nmap_cmd)

    #Starting enumeration - whatweb
    print('[+] Identifying web technologies. . . output to > whatweb.txt')
    f = open("whatweb.txt", "w")
    whatweb_cmd = ["whatweb", full_URL]
    subprocess.run(whatweb_cmd, stdout=f)

    #Starting feroxbuster and dirsearch
    print('[+] Started directory busting. . . output to > ferox.txt & dir.txt')
    ferox_cmd = ["feroxbuster", "-u", full_URL,"-C","401,403,404" ,"-o", "ferox.txt" ]
    subprocess.run(ferox_cmd)
    dirsearch_cmd =["python3", "/opt/dirsearch/dirsearch.py", "-u", full_URL, "-o", "dir.txt"]
    subprocess.run(dirsearch_cmd)


    #Curl enumeration
    os.chdir(curl_dir)
    print(f'[+] Curling the sites: {full_URL}. . . output to curl_sites')
    curl_cmd = ["curl", "-i",full_URL, "-o", f"{full_URL.txt}"]
    subprocess.run(curl_cmd)
    with open(f'{pwd}/dir.txt','r') as c_dir:
        sub_domains = c_dir.read()
        re_sub_domains = re.findall(r'\b200\b\s+\d+\w+\s+(.+)', sub_domains)
        for i in re_sub_domains:
            n = re.findall(r'.\/\/\d+\.\d+\.\d+\.\d+/(\w+)', i)
            curl_cmd = ["curl", "-i", ''.join(i), "-o",f"{''.join(n)}.txt" ]
            subprocess.run(curl_cmd)

    print('\n')
    print('#'*100)
    print(f'[+] Enumeration finished, go to {top_dir} for scan results ')
    print('#'*100)
    print('\n')


###############################################################################################################
elif args.i:
    #Regex
    full_URL = args.i
    print(f'[+] Enumerating {full_URL}')
    re_URL = re.findall('\w+\:\/\/(\d+\.\d+\.\d+\.\d+\/)', args.i)
    #print(re_URL)
    re_nmap_url = re.findall('(\d+\.\d+\.\d+\.\d+)', full_URL)
    top_dir =(' '.join(re_URL))


    print('[+] Creating file structure. . .')


    #Create directory for info and loot
    def create_dir(p):
        isdir = os.path.isdir(p)
        #print(isdir)
        if isdir == False:
            print(f'[+] Creating folder in {pwd} for infodump & loot. . . ')
            try:
                os.mkdir(p)
            except OSError:
                print ("[+] Creation of the directory %s failed" % p)
            else:
                print ("[+] Successfully created the directory %s " % p)
        else:
            print(f'The directory {p} already exists. . . Please remove old results and try again')
    create_dir(top_dir)



    #Sub directory creation
    #print('\n')
    os.chdir(top_dir)

    print('[+] Creating sub directories. . .')
    create_dir(info_dir)
    create_dir(loot_dir)
    os.chdir(info_dir)
    pwd = os.getcwd()
    create_dir(curl_dir)


    print('\n')
    print('#'*100)
    print('[+] Starting web enum. . .')
    print('#'*100)
    print('\n')

    #NMAP enumeration
    print(f'[+] Starting NMAP enumeration of: {full_URL}. . . output to nmap_scan.txt')
    print('[+] Iniating with aggressive scan of target. . .')
    nmap_cmd = ["nmap", "-A", "-T4", "-vv","-oN","nmap_scan.txt" ,''.join(re_nmap_url)]
    subprocess.run(nmap_cmd)

    print('\n')
    #Starting enumeration - whatweb
    print('[+] Identifying web technologies. . . output to > whatweb.txt')
    f = open("whatweb.txt", "w")
    whatweb_cmd = ["whatweb", full_URL]
    subprocess.run(whatweb_cmd, stdout=f)


    print('\n')
    #Starting feroxbuster and dirsearch
    print('[+] Started directory busting. . . output to > ferox.txt & dir.txt')
    ferox_cmd = ["feroxbuster", "-u", full_URL,"-C","401,403,404", "-o", "ferox.txt" ]
    subprocess.run(ferox_cmd)
    dirsearch_cmd =["python3", "/opt/dirsearch/dirsearch.py", "-u", full_URL, "-o", "dir.txt"]
    subprocess.run(dirsearch_cmd)

    #Curl enumeration
    os.chdir(curl_dir)
    print(f'[+] Curling the sites: {full_URL}. . . output to curl_sites')
    curl_cmd = ["curl", "-i", full_URL, "-o","homepage.txt"]
    subprocess.run(curl_cmd)
    with open(f'{pwd}/dir.txt','r') as c_dir:
        sub_domains = c_dir.read()
        re_sub_domains = re.findall(r'\b200\b\s+\d+\w+\s+(.+)', sub_domains)
        for i in re_sub_domains:
            n = re.findall(r'.\/\/\d+\.\d+\.\d+\.\d+/(\w+)', i)
            curl_cmd = ["curl", "-i", ''.join(i), "-o",f"{''.join(n)}.txt" ]
            subprocess.run(curl_cmd)



    print('\n')
    print('#'*100)
    print(f'[+] Enumeration finished, go to {top_dir} for scan results ')
    print('#'*100)
    print('\n')
