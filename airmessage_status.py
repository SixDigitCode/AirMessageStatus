import os
import requests

#System-specific info (CHANGE THESE)
router_ip_addr = "192.168.1.1"
remote_address = "myairmessageserver.example.com" #This is your remote (DynDNS/No-IP/DDNS) address for your server. Can also be your NGrok address or similar
airmessage_port = "1359" #(default = 1359)

#Generic info (You probably won't need to change these)
internet_test_addr = "1.1.1.1"

def ping_remote(remote_ip):
        response = os.system("ping -c 1 "+remote_ip+" > /dev/null")
        return (response == 0)

def ping_router():
        return ping_remote(router_ip_addr)

def ping_remote_address():
        return ping_remote(remote_address)

def ping_internet_test():
        return ping_remote(internet_test_addr)

def check_if_server_running():
        res = os.system("pgrep AirMessage")
        return res != 256

def check_if_port_reachable():
        headers = {
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'Origin': 'https://www.portchecktool.com',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'Referer': 'https://www.portchecktool.com/',
                'Accept-Language': 'en-US,en;q=0.9',
                'dnt': '1',
                'sec-gpc': '1',
        }

        data = {
                'port': airmessage_port,
                'submit': 'Check your port'
        }

        response = requests.post('https://www.portchecktool.com/', headers=headers, data=data)
        return "<strong>Success!</strong>" in response.text

def print_status(status_name, check_function):
        print(u"\u25CC"+" "+status_name, end="\r", flush=True)
        if (check_function()):
                print('\033[92m'+u"\u2713"+" "+status_name+' [OK] \033[0m')
        else:
                print('\033[91m'+u"\u2715"+" "+status_name+' [FAILED] \033[0m')
print("========= SERVER STATUS AND INFO =========\n")

print("Public IP Address: "+requests.get('https://api.ipify.org').text)
print("Forwarding Address: "+remote_address)
print("\nStatus:")

print_status("AirMessage Server Running?",check_if_server_running)
print_status("Router reachable?",ping_router)
print_status("Internet reachable?",ping_internet_test)
print_status("Port forwarding working?",check_if_port_reachable)
print_status(remote_address+" reachable?",ping_remote_address)

print("\nPress any key to exit...")
input()