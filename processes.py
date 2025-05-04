import psutil

SUSPICIOUS = {"procmon.exe", "ida.exe", "ollydbg.exe"}

def check_processes():
    found = []
    for p in psutil.process_iter(['name','exe']):
        try:
            if p.info['name'] and p.info['name'].lower() in SUSPICIOUS:
                found.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return found
