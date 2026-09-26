import sys
import json #
import subprocess #to run commands, needed for detection of software and hardware
import os
import rich #to color print statemets

def get_gpu_info():
    result = subprocess.run(["lspci"], capture_output=True, text=True)
    output = result.stdout

    gpus = []

    for line in output.splitlines():
        if "VGA" in line:
            if "NVIDIA" in line:
                model = line.split('[')[-1].split(']')[0]
                gpus.append({'Vendor': 'NVIDIA', 'Model': model})
            elif "AMD" in line:
                model = line.split('[')[-1].split(']')[0]
                gpus.append({'Vendor': 'AMD', 'Model': model})
            elif "Intel" in line:
                model = line.split('[')[-1].split(']')[0]
                gpus.append({'Vendor': 'Intel', 'Model': model})
            pass
    return gpus

def get_cpu_info():
    cpu_result = subprocess.run(["lscpu"], capture_output=True, text=True)
    cpu_output = cpu_result.stdout

    cpu = ""

    for line in cpu_output.splitlines():
        if "Model name" in line:
            model = line.split(':')[-1].strip()
            cpu = model
    return cpu

def get_distro_info():
    if not os.path.exists('/etc/os-release'):
        return None

    info = {}

    with open('/etc/os-release') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                info[key] = value
    return info


distro_info = get_distro_info()
distro_name = distro_info.get('ID', '').strip('"')
gpu_info = get_gpu_info()
cpu_info = get_cpu_info()

distro_print = (f"Distribution: {distro_name.capitalize()}")
rich.print(f"[bold red]Distribution:[/bold red] [green]{distro_name.capitalize()}[/green]")
rich.print(f"[purple]{"-"* (len(distro_print))}[/purple]")


cpu_print = (f"CPU: {cpu_info}")
rich.print(f"[bold red]CPU:[/bold red] [green]{cpu_info}[/green]")
rich.print(f"[purple]{"-"* (len(cpu_print))}[/purple]")

for i, gpu in enumerate(gpu_info, start=1):
    gpus_print = f"GPU{i}: {gpu['Vendor']}, {gpu['Model']}"
    rich.print(f"[bold red]GPU{i}:[/bold red] [green]{gpu['Vendor']}[/green], [green]{gpu['Model']}[/green]")
    rich.print(f"[purple]{"-"* (len(gpus_print))}[/purple]")
