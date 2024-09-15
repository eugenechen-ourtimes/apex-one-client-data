import argparse
import csv
from os.path import join

import constants
import utils

def searchComputersLocally(serverHostname, hostname, ip, mac):
    searchResults = []
    with open(join("../data/input/simplified-data", serverHostname.lower() + ".csv"), mode = "r", encoding = "big5", newline = "") as computerFile:
        reader = csv.DictReader(computerFile)
        for computer in reader:
            computer_hostname = computer["hostname"]
            computer_ip = computer["ip"]
            computer_mac = computer["mac"]
            isHostnameMatch = hostname is None or computer_hostname.lower().startswith(hostname.lower())
            isIpMatch = ip is None or computer_ip.startswith(ip)
            isMacMatch = mac is None or computer_mac.lower().startswith(mac.lower())
            if isHostnameMatch and isIpMatch and isMacMatch:
                searchResult = dict(computer)
                searchResult["server"] = serverHostname
                searchResults.append(searchResult)

    return searchResults

def searchComputers(hostname, ip, mac):
    searchResults = []
    for serverHostname in constants.serverHostnames:
        localSearchResults = searchComputersLocally(serverHostname, hostname, ip, mac)
        searchResults.extend(localSearchResults)

    return searchResults

def writeSearchResults(searchResults):
    with open(join("../data/output", "search-results-2.csv"), mode = "w", encoding = "big5", newline = "") as computerFile:
        writer = csv.DictWriter(computerFile, fieldnames = constants.fieldnames)
        writer.writeheader()
        for searchResult in searchResults:
            writer.writerow(searchResult)

def main(args):
    hostname = args.hostname
    ip = args.ip
    mac = args.mac
    if hostname is None and ip is None and mac is None:
        print("need to provide a hostname, an IP address, or a MAC address")
        return 0

    searchResults = searchComputers(hostname, ip, mac)
    if len(searchResults) == 0:
        print("no results match your search criteria")
        return 0

    def ipKey(computer):
        return utils.ip2int(computer["ip"])

    def computerTypeKey(computer):
        if "Server" in computer["os"]:
            return 1
        return 2

    searchResults.sort(key = ipKey)
    searchResults.sort(key = computerTypeKey)

    writeSearchResults(searchResults)
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "search computers")
    parser.add_argument("--hostname", metavar = "[hostname]")
    parser.add_argument("--ip", metavar = "[ip]")
    parser.add_argument("--mac", metavar = "[mac]")

    main(parser.parse_args())
