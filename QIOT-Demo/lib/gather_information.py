#!/usr/bin/env python3
import argparse
import subprocess
import json

"""
A quick script to grab information from a raspberry pi
Krishna Bhattarai
QuantumIOT
Jan 2017
"""


class RaspberryPi:
    def __init__(self):
        pass

    def execute(self, command):
        return subprocess.getoutput(command)

    def get_memory_info(self):
        total_memory = float(self.execute("cat /proc/meminfo | grep MemTotal | awk '{print $2/1024}'"))
        free_memory = float(self.execute("cat /proc/meminfo | grep MemFree | awk '{print $2/1024}'"))
        available_memory = float(self.execute("cat /proc/meminfo | grep MemAvailable | awk '{print $2/1024}'"))
        buffers = float(self.execute("cat /proc/meminfo | grep Buffers | awk '{print $2/1024}'"))
        cache = float(self.execute("cat /proc/meminfo | grep Cached | awk 'NR==1' | awk '{print $2/1024}'"))
        dirty = float(self.execute("cat /proc/meminfo | grep Dirty | awk '{print $2/1024}'"))
        active = float(self.execute("cat /proc/meminfo | grep 'Active' | awk 'NR==1' | awk '{print $2/1024}'"))

        inactive = float(self.execute("cat /proc/meminfo | grep 'Inactive' | awk 'NR==1' | awk '{print $2/1024}'"))

        memory_split = {'arm': float(self.execute("vcgencmd get_mem arm | awk -F'=' '{print $2}' | sed s'/.$//' ")),
                        'gpu': float(self.execute("vcgencmd get_mem gpu | awk -F'=' '{print $2}' | sed s'/.$//' "))}

        return {"total_memory": total_memory, "free_memory": free_memory, "available_memory": available_memory,
                "buffers": buffers, "cache": cache, "dirty": dirty, "active": active, "inactive": inactive,
                "memory_split": memory_split}

    def get_system_info(self):
        hostname = self.execute('hostname')
        uptime = self.execute('uptime -p')
        hardware = self.execute("cat /proc/cpuinfo | grep Hardware | awk '{print $3}'")
        revision = self.execute("cat /proc/cpuinfo | grep Revision | awk '{print $3}'")
        model_name = self.execute("cat /proc/cpuinfo | grep 'model name' | cut -d' ' -f 3- | awk 'NR==1'")
        serial_number = self.execute("cat /proc/cpuinfo | grep Serial | awk '{print $3}'")
        mac_address = self.execute("cat /sys/class/net/eth0/address")
        kernel = self.execute('uname -mrs')

        return {"kernel": kernel, "hostname": hostname, "uptime": uptime, "hardware": hardware, "revision": revision,
                "model_name": model_name, "serial_number": serial_number, "mac_address": mac_address}

    def get_display_info(self):
        name = self.execute("tvservice -n | awk -F'=' '{print $2}'")
        if name:
            status = self.execute('tvservice -s').strip()
        else:
            name = None
            status = None
        return {"name": name, "status": status}

    def get_network_info(self):
        wifis = self.execute('iwlist wlan0 scan | grep ESSID').strip().split('\n')
        iproute = self.execute('ip route').strip().split('\n')
        arp = self.execute('arp -an').strip().split('\n')
        ipaddress = self.execute("ip addr | grep -Po '(?!(inet 127.\d.\d.1))(inet \K(\d{1,3}\.){3}\d{1,3})'")
        netstat = self.execute('netstat -rn').strip().split('\n')
        return {"ssids": wifis, 'ip_route': iproute, "arp": arp, "netstat": netstat,
                "ipaddres": ipaddress}

    def get_disk_stats(self):
        df = self.execute('df -h').strip().split('\n')
        vmstat = self.execute('vmstat').strip().split('\n')
        return {"df": df, "vmstat": vmstat}

    def get_temperature(self):
        cpu_temperature = float(self.execute("cat /sys/class/thermal/thermal_zone0/temp | awk '{print $1/1000}'"))
        gpu_temperature = float(self.execute("vcgencmd measure_temp | awk -F'=' '{print $2}' | sed s'/..$//' "))
        return {"cpu": cpu_temperature, "gpu": gpu_temperature}

    def get_voltages(self):
        core_voltage = self.execute("vcgencmd measure_volts core | awk -F'=' '{print $2}' | sed s'/.$//' ")
        sdram_c_voltage = self.execute("vcgencmd measure_volts sdram_c | awk -F'=' '{print $2 }' | sed s'/.$//' ")
        sdram_i_voltage = self.execute("vcgencmd measure_volts sdram_i | awk -F'=' '{print $2 }' | sed s'/.$//' ")
        sdram_p_voltage = self.execute("vcgencmd measure_volts sdram_p | awk -F'=' '{print $2 }' | sed s'/.$//' ")
        return {"core_voltage": core_voltage,
                "sdram_c_voltage": sdram_c_voltage,
                "sdram_i_voltage": sdram_i_voltage,
                "sdram_p_voltage": sdram_p_voltage}

    def get_clock_frequencies(self):
        cpu_current = float(self.execute("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"))
        cpu_max = float(self.execute("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq"))
        cpu_min = float(self.execute("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq"))
        arm = self.execute("vcgencmd measure_clock arm")
        core = self.execute("vcgencmd measure_clock core")
        h264 = self.execute("vcgencmd measure_clock h264")
        isp = self.execute("vcgencmd measure_clock isp")
        v3d = self.execute("vcgencmd measure_clock v3d")
        uart = self.execute("vcgencmd measure_clock uart")
        pwm = self.execute("vcgencmd measure_clock pwm")
        emmc = self.execute("vcgencmd measure_clock emmc")
        pixel = self.execute("vcgencmd measure_clock pixel")
        vec = self.execute("vcgencmd measure_clock vec")

        hdmi = self.execute("vcgencmd measure_clock hdmi")
        dpi = self.execute("vcgencmd measure_clock dpi")
        return {"cpu": {"current": cpu_current, "min": cpu_min, "max": cpu_max},
                "arm": arm,
                "core": core,
                "h264_": h264,
                "isp": isp,
                "v3d": v3d,
                "uart": uart,
                "pwm": pwm,
                "emmc": emmc,
                "pixel": pixel,
                "vec": vec,
                "hdmi": hdmi,
                "dpi": dpi}

    def get_essentials(self):
        return {
            'display': self.get_display_info(),
            'temperature': self.get_temperature(),
            'memory': {"free": float(self.execute("cat /proc/meminfo | grep MemFree | awk '{print $2/1024}'")),
                       "cache": float(self.execute("cat /proc/meminfo | grep Cached | awk 'NR==1' | awk '{print $2/1024}'")),
                       "dirty": float(self.execute("cat /proc/meminfo | grep Dirty | awk '{print $2/1024}'"))},
            'network': self.execute("ip addr | grep -Po '(?!(inet 127.\d.\d.1))(inet \K(\d{1,3}\.){3}\d{1,3})'")
        }

    def gather_all_info(self):
        return {
            'system': self.get_system_info(),
            'memory': self.get_memory_info(),
            'display': self.get_display_info(),
            'network': self.get_network_info(),
            'clock': self.get_clock_frequencies(),
            'voltages': self.get_voltages(),
            'temperature': self.get_temperature(),
            'disk': self.get_disk_stats(),
        }