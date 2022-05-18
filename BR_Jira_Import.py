from array import array
from genericpath import isdir
import sys
import tarfile
import os
import json
from jira import JIRA
from jira import Issue
from jira import JIRAError

APPLICATION_TOKEN = ''
JIRA_HOSTNAME = 'https://jira.atlassian.com'
OUTPUT_DIRECTORY = 'H:/Work/Python/temp'

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
    print("Extracting " + tarPath + " to " + OUTPUT_DIRECTORY)
    tar = tarfile.open(tarPath)
    tar.extractall(OUTPUT_DIRECTORY)
    tar.close()

def getReportPaths():
    print("Getting list of bug reports")

    reportPaths:array
    for dir in os.scandir(OUTPUT_DIRECTORY):
        fullPath = os.path.join(OUTPUT_DIRECTORY, dir)
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

def attachScreenShots(jiraClient:JIRA, reportPath, issue:Issue):
    print("Adding screen shots as attachments to issue " + issue.id)
    for file in os.scandir(reportPath):
        if file.path.endswith(".png") or file.path.endswith(".jpg"):
            jiraClient.add_attachment(issue, attachment=file.path)

def importToJira():
    try:
        jiraClient = JIRA(server=JIRA_HOSTNAME, token_auth=APPLICATION_TOKEN)
    except JIRAError as err:
        print("Error: An exception occured while attempting to authenticate the Jira Client: " + err.text)
        exit(1)

    reportPaths = getReportPaths()

    if len(reportPaths) > 0:
        reportPaths.sort()
    else:
        print("Error: Could not get list of bug reports")
        exit(1)

    for reportPath in reportPaths:
        for file in os.scandir(reportPath):
            if file.path.endswith(".json"):
                try:
                    br:BugReport = parseReport(file.path)
                    issue = jiraClient.create_issue(project=br.project, summary=br.summary, description=br.description)
                    print("Created issue: " + issue.id)
                    comment = "Log Locations: " + reportPath + "/" + br.tsdLocation + ", " + reportPath + "/" + br.logLocation + ", " + reportPath + "/" + br.commLocation
                    jiraClient.add_comment(issue, comment)
                    attachScreenShots(jiraClient, reportPath, issue)
                except JIRAError as err:
                    print("Error: An exception occured while creating an issue: " + err.text)
                    exit(1)

                # TODO: 
                # Add function to create a better formatted summarry
                # Get relative paths for the log files
                # Fill out the rest of the issue fields and transition the issue into next state if necessary

    jiraClient.close()


def main(argv):
    print("Starting Bug Report Importer...")
    brTar = ''
    argLen = len(sys.argv)

    if argLen > 0 and argLen <= 2:
        brTar = argv[1]
    else:
        print("Usage: BR_Jira_Import.py <Path to Bug Report Tar>")
        sys.exit(1)

    if brTar.endswith('.tar', '.tar.gz', '.tgz', '.gz'):
        if os.path.exists(brTar):
            extractTar(brTar)
        else:
            print("Error: " + brTar + " does not exist")
            sys.exit(1)
    else:
        print("Error: Bug Report archive must be in .tar|.tar.gz|.tgz|.gz format")
        sys.exit(1)
    
    importToJira()
