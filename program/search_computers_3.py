import argparse
import csv
import datetime
from os.path import join
import sys

import constants
import utils

def searchComputersLocally(serverHostname, baseAgent, basePattern, baseDatetime):
    def isAgentAndPatternFine(agent, pattern):
        return (
            utils.isAgentValid(agent) and
            utils.isPatternValid(pattern) and
            utils.isAgentNewerOrTheSame(agent, baseAgent) and
            utils.isPatterNewerOrTheSame(pattern, basePattern)
        )

    def isOfflineForLongTime(offlineDateTimeStr):
        if offlineDateTimeStr == "無":
            return False

        offlineDateStr, offlineTimeStr = offlineDateTimeStr.split(" ")
        offlineYearStr, offlineMonthStr, offlineDayStr = offlineDateStr.split("/")
        offlineHourStr, offlineMinuteStr = offlineTimeStr.split(":")
        offlineYear = int(offlineYearStr)
        offlineMonth = int(offlineMonthStr)
        offlineDay = int(offlineDayStr)
        offlineHour = int(offlineHourStr)
        offlineMinute = int(offlineMinuteStr)
        offlineDatetime = datetime.datetime(offlineYear, offlineMonth, offlineDay, offlineHour, offlineMinute)

        timedelta = baseDatetime - offlineDatetime
        return timedelta.days >= 14

    searchResults = []
    with open(join("../data/input/simplified-data", serverHostname.lower() + ".csv"), mode = "r", encoding = "big5", newline = "") as computerFile:
        reader = csv.DictReader(computerFile)
        for computer in reader:
            computer_hostname = computer["hostname"].upper()
            computer_ip = computer["ip"]
            computer_os = computer["os"]
            computer_agent = computer["agent"]
            computer_pattern = computer["pattern"]
            computer_offline_datetime = computer["offline_datetime"]
            if isOfflineForLongTime(computer_offline_datetime):
                continue

            isMatch = False
            if "Server" in computer_os:
                if not (
                    isAgentAndPatternFine(computer_agent, computer_pattern)
                ):
                    isMatch = True
            else:
                if utils.isBbLevelAgency(computer_hostname, computer_ip) and not (
                    isAgentAndPatternFine(computer_agent, computer_pattern)
                ):
                    isMatch = True

            if isMatch:
                searchResult = dict(computer)
                searchResult["server"] = serverHostname
                searchResults.append(searchResult)

    return searchResults

def searchComputers(baseAgent, basePattern, baseDatetime):
    searchResults = []
    for serverHostname in constants.serverHostnames:
        localSearchResults = searchComputersLocally(serverHostname, baseAgent, basePattern, baseDatetime)
        searchResults.extend(localSearchResults)

    return searchResults

def writeSearchResults(searchResults):
    with open(join("../data/output", "search-results-3.csv"), mode = "w", encoding = "big5", newline = "") as computerFile:
        writer = csv.DictWriter(computerFile, fieldnames = constants.fieldnames)
        writer.writeheader()
        for searchResult in searchResults:
            writer.writerow(searchResult)

def main(args):
    base_agent = args.base_agent
    base_pattern = args.base_pattern
    base_datetime = args.base_datetime

    if base_agent is None:
        print("need to provide a security agent version as a base")
        sys.exit(0)
    if base_pattern is None:
        print("need to provide a virus pattern version as a base")
        sys.exit(0)

    if base_datetime is None:
        print("need to provide a date and a time as a base")
        sys.exit(0)

    if not utils.isAgentValid(base_agent):
        print("invalid security agent version")
        sys.exit(0)
    if not utils.isPatternValid(base_pattern):
        print("invalid virus pattern version")
        sys.exit(0)

    searchResults = searchComputers(base_agent, base_pattern, base_datetime)
    if len(searchResults) == 0:
        print("no results match your search criteria")
        sys.exit(0)

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
    parser.add_argument("--base-agent", metavar = "[base-agent]", help="oldest acceptable security agent version")
    parser.add_argument("--base-pattern",  metavar = "[base-pattern]", help="oldest acceptable virus pattern version")
    parser.add_argument('--base-datetime', type=datetime.datetime.fromisoformat, metavar = "[base-datetime]", help="ISO format: [YYYY-MM-DD]T[HH:mm:ss]")

    main(parser.parse_args())
