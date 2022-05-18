from array import array
from genericpath import isdir
import sys
import tarfile
import os
import json
from jira import JIRA
from jira import Issue

APPLICATION_TOKEN = ''
JIRA_HOSTNAME = 'https://jira.atlassian.com'
TEMP_DIRECTORY = 'H:/Work/Python/temp'

class BugReport:
    def __init__(self):
        self.projectName = "SAGE"
        self.issueNumber = ""
        self.summary = ""
        self.project = ""
        self.assignee = ""
        self.originator = ""
        self.affectedVersion = ""
        self.stringName = ""
        self.fundingsource = ""
        self.model = ""
        self.component = ""
        self.type = ""
        self.description = ""
        self.priority = ""
        self.date = ""
        self.category = ""
        self.tsdLocation = ""
        self.logLocation = ""
        self.commLocation = ""
        self.attachments = ["", ""]

def extractTar(tarPath):
    print("Extracting " + tarPath + " to " + TEMP_DIRECTORY)
    tar = tarfile.open(tarPath)
    tar.extractall(TEMP_DIRECTORY)
    tar.close()

def getReportPaths():
    print("Getting list of bug reports")

    reportPaths:array
    for dir in os.scandir(TEMP_DIRECTORY):
        fullPath = os.path.join(TEMP_DIRECTORY, dir)
        if isdir(fullPath):
            reportPaths.append(fullPath)

    return reportPaths

def parseReport(reportPath):
    fstream = open(reportPath, "r")
    data = json.loads(fstream.read())
    fstream.close()
    bugReport = BugReport()

    bugReport.description = data["description"]
    bugReport.description = data["issueNumber"]
    bugReport.description = data["summary"]
    bugReport.description = data["project"]
    bugReport.description = data["assignee"]
    bugReport.description = data["originator"]
    bugReport.description = data["affectedVersion"]
    bugReport.description = data["stringName"]
    bugReport.description = data["fundingsource"]
    bugReport.description = data["model"]
    bugReport.description = data["component"]
    bugReport.description = data["type"]
    bugReport.description = data["priority"]
    bugReport.description = data["date"]
    bugReport.description = data["category"]
    bugReport.description = data["tsdLocation"]
    bugReport.description = data["logLocation"]
    bugReport.description = data["commLocation"]
    bugReport.description = data["attachments"]

    return bugReport

def attachScreenShots(jiraClient:JIRA, report, issue:Issue):
    for file in os.scandir(report):
        if file.path.endswith(".png") or file.path.endswith(".jpg"):
            jiraClient.add_attachment(issue, attachment=file.path)

def importToJira():
    jiraClient = JIRA(server=JIRA_HOSTNAME, token_auth=APPLICATION_TOKEN)
    reportPaths = getReportPaths()

    if len(reportPaths) > 0:
        reportPaths.sort()
    else:
        print("Error: Could not get list of bug reports")
        exit(1)

    for report in reportPaths:
        for file in os.scandir(report):
            if file.path.endswith(".json"):
                br:BugReport = parseReport(file.path)
                issue = jiraClient.create_issue(project=br.project, summary=br.summary, description=br.description)
                comment = "Log Locations: " + TEMP_DIRECTORY + "/" + br.tsdLocation + ", " + TEMP_DIRECTORY + "/" + br.logLocation + ", " + TEMP_DIRECTORY + "/" + br.commLocation
                jiraClient.add_comment(issue, comment)
                attachScreenShots(jiraClient, report, issue)


def main(argv):
    print("Starting Bug Report Importer...")
    brTar = ''
    argLen = len(sys.argv)

    if argLen > 0 and argLen <= 2:
        brTar = argv[1]
    else:
        print("Usage: BR_Jira_Import.py <Path to Bug Report Tar>")
        sys.exit(1)

    if brTar.endswith('.tar', '.tar.gz', '.tgz', '.gz') and os.path.exists(brTar):
        if os.path.exists(brTar):
            extractTar(brTar)
        else:
            print("Error: " + brTar + " does not exist")
            sys.exit(1)
    else:
        print("Error: Bug Report archive must be in .tar|.tar.gz|.tgz|.gz format")
        sys.exit(1)
    
    importToJira()
