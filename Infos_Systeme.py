import psutil
import platform
import subprocess
import tkinter as tk
from tkinter import ttk

def get_system_info():
    os = platform.uname()
    user_name = psutil.users()[0].name
    os_version = f"{os.system} {os.release}"
    python_version = platform.python_version()
    cpu_architecture = platform.machine()
    return user_name, os_version, python_version, cpu_architecture

def get_memory_info():
    memory = psutil.virtual_memory()
    total = round(memory.total / (1024.0 ** 3), 2)
    available = round(memory.available / (1024.0 ** 3), 2)
    used = round(memory.used / (1024.0 ** 3), 2)
    percent = memory.percent
    return total, available, used, percent

def get_cpu_info():
    cpu = psutil.cpu_freq()
    current = cpu.current
    max_freq = cpu.max
    min_freq = cpu.min
    num_cores = psutil.cpu_count()
    return current, max_freq, min_freq, num_cores

def get_disk_info():
    disks = psutil.disk_partitions()
    disk_info = []
    for disk in disks:
        try:
            disk_usage = psutil.disk_usage(disk.mountpoint)
            total = round(disk_usage.total / (1024.0 ** 3), 2)
            free = round(disk_usage.free / (1024.0 ** 3), 2)
            used = round(disk_usage.used / (1024.0 ** 3), 2)
            percent = disk_usage.percent
            disk_info.append((disk.device, disk.fstype, total, free, used, percent))
        except PermissionError:
            pass
    return disk_info

def get_drivers():
    output = subprocess.check_output("driverquery", shell=True)
    output = output.decode("latin-1")
    drivers = [line.strip() for line in output.split("\n") if line.strip()]
    return drivers

def get_software():
    output = subprocess.check_output("wmic product get name", shell=True)
    output = output.decode("latin-1")
    software = [line.strip() for line in output.split("\n") if line.strip()]
    return software

def create_app():
    app = tk.Tk()
    app.title("Informations système")
    notebook = ttk.Notebook(app)
    notebook.pack(expand=True, fill=tk.BOTH)

    # Système
    system_frame = ttk.Frame(notebook)
    notebook.add(system_frame, text="Système")

    user_name, os_version, python_version, cpu_architecture = get_system_info()

    ttk.Label(system_frame, text=f"Nom d'utilisateur : {user_name}").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    ttk.Label(system_frame, text=f"Système d'exploitation : {os_version}").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    ttk.Label(system_frame, text=f"Version de Python : {python_version}").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    ttk.Label(system_frame, text=f"Architecture du processeur : {cpu_architecture}").grid(row=3, column=0, padx=10, pady=10, sticky="w")

    # Mémoire
    memory_frame = ttk.Frame(notebook)
    notebook.add(memory_frame, text="Mémoire")

    total, available, used, percent = get_memory_info()

    ttk.Label(memory_frame, text=f"Total : {total} GB").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    ttk.Label(memory_frame, text=f"Disponible : {available} GB").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    ttk.Label(memory_frame, text=f"Utilisé : {used} GB").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    ttk.Label(memory_frame, text=f"Pourcentage d'utilisation : {percent}%").grid(row=3, column=0, padx=10, pady=10, sticky="w")

    # CPU
    cpu_frame = ttk.Frame(notebook)
    notebook.add(cpu_frame, text="CPU")

    current, max_freq, min_freq, num_cores = get_cpu_info()

    ttk.Label(cpu_frame, text=f"Fréquence actuelle : {current:.2f} MHz").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    ttk.Label(cpu_frame, text=f"Fréquence maximale : {max_freq:.2f} MHz").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    ttk.Label(cpu_frame, text=f"Fréquence minimale : {min_freq:.2f} MHz").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    ttk.Label(cpu_frame, text=f"Nombre de coeurs : {num_cores}").grid(row=3, column=0, padx=10, pady=10, sticky="w")

    # Disques durs
    disk_frame = ttk.Frame(notebook)
    notebook.add(disk_frame, text="Disques durs")

    disk_info = get_disk_info()
    for i, (device, fstype, total, free, used, percent) in enumerate(disk_info):
        ttk.Label(disk_frame, text=f"Nom : {device}").grid(row=i * 5, column=0, padx=10, pady=10, sticky="w")
        ttk.Label(disk_frame, text=f"Système de fichiers : {fstype}").grid(row=i * 5 + 1, column=0, padx=10, pady=10, sticky="w")
        ttk.Label(disk_frame, text=f"Espace total : {total} GB").grid(row=i * 5 + 2, column=0, padx=10, pady=10, sticky="w")
        ttk.Label(disk_frame, text=f"Espace disponible : {free} GB").grid(row=i * 5 + 3, column=0, padx=10, pady=10, sticky="w")
        ttk.Label(disk_frame, text=f"Espace utilisé : {used} GB").grid(row=i * 5 + 4, column=0, padx=10, pady=10, sticky="w")
        ttk.Label(disk_frame, text=f"Pourcentage d'utilisation : {percent}%").grid(row=i * 5 + 5, column=0, padx=10, pady=10, sticky="w")

    # Pilotes
    drivers_frame = ttk.Frame(notebook)
    notebook.add(drivers_frame, text="Pilotes")
    
    drivers = get_drivers()
    
    drivers_listbox = tk.Listbox(drivers_frame, height=20, width=100)
    drivers_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    drivers_scrollbar = ttk.Scrollbar(drivers_frame, orient=tk.VERTICAL, command=drivers_listbox.yview)
    drivers_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    drivers_listbox.config(yscrollcommand=drivers_scrollbar.set)
    
    for driver in drivers:
        drivers_listbox.insert(tk.END, driver)
    
    # Logiciels
    software_frame = ttk.Frame(notebook)
    notebook.add(software_frame, text="Logiciels")
    
    software = get_software()
    
    software_listbox = tk.Listbox(software_frame, height=20, width=100)
    software_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    software_scrollbar = ttk.Scrollbar(software_frame, orient=tk.VERTICAL, command=software_listbox.yview)
    software_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    software_listbox.config(yscrollcommand=software_scrollbar.set)
    
    for s in software:
        software_listbox.insert(tk.END, s)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.mainloop()
