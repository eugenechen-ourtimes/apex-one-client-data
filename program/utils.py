import socket
import struct

def isAgentValid(agent):
    try:
        v1, v2, v3 = agent.split(".")
        v1 = int(v1)
        v2 = int(v2)
        v3 = int(v3)
        return v1 >= 0 and v2 >= 0 and v3 >= 0
    except:
        return False

def isPatternValid(pattern):
    try:
        v1, v2, v3 = pattern.split(".")
        v1 = int(v1)
        v2 = int(v2)
        v3 = int(v3)
        return v1 >= 0 and v2 >= 0 and v3 >= 0
    except:
        return False

def isAgentNewerOrTheSame(agent1, agent2):
    v11, v12, v13 = agent1.split(".")
    v21, v22, v23 = agent2.split(".")
    v11 = int(v11)
    v12 = int(v12)
    v13 = int(v13)
    v21 = int(v21)
    v22 = int(v22)
    v23 = int(v23)

    if v11 > v21:
        return True
    if v11 < v21:
        return False

    if v12 > v22:
        return True
    if v12 < v22:
        return False

    return v13 >= v23

def isPatterNewerOrTheSame(pattern1, pattern2):
    v11, v12, v13 = pattern1.split(".")
    v21, v22, v23 = pattern2.split(".")
    v11 = int(v11)
    v12 = int(v12)
    v21 = int(v21)
    v22 = int(v22)

    if v11 > v21:
        return True
    if v11 < v21:
        return False

    return v12 >= v22


def isEdub(hostname, ip):
    return (
        hostname.startswith("EDUB")
    ) or (
        ip.startswith("172.20.12.") or
        ip.startswith("172.20.23.") or
        ip.startswith("172.20.35.") or
        ip.startswith("172.20.37.") or
        ip.startswith("172.20.38.") or
        ip.startswith("172.20.40.") or
        ip.startswith("172.20.41.") or
        ip.startswith("172.20.42.")
    )

def isPlbu(hostname, ip):
    return False

def isLabu(hostname, ip):
    return (
        hostname.startswith("LABU") or
        hostname.startswith("LAND")   
    ) or (
        ip.startswith("192.168.215.") or
        ip.startswith("192.168.216.") or
        ip.startswith("192.168.217.")
    )

def isLtbu(hostname, ip):
    return False

def isDabu(hostname, ip):
    return (
        hostname.startswith("DABU") or
        hostname.startswith("IFMC")
    ) or (
        ip.startswith("192.168.86.") or
        ip.startswith("192.168.137.") or
        ip.startswith("192.168.138.")
    )

def isTcpl(hostname, ip):
    return False

def isBbLevelAgency(hostname, ip):
    return (
        isEdub(hostname, ip) or
        isPlbu(hostname, ip) or
        isLabu(hostname, ip) or
        isLtbu(hostname, ip) or
        isDabu(hostname, ip) or
        isTcpl(hostname, ip)
    )


def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]

def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))
