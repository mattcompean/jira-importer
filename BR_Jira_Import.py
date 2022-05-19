from array import array
import sys
import tarfile
import os
import json
from jira import JIRA
from jira import Issue
from jira import JIRAError

APPLICATION_TOKEN = ''
JIRA_HOSTNAME = 'https://jira.atlassian.com'
DEFAULT_OUTPUT_DIRECTORY = 'H:/Work/Python/temp'

class BugReport:
    def __init__(self):
        self.projectName = "ESAGE"
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

def extractTar(tarPath, outputDirPath):
    print("Extracting " + tarPath + " to " + outputDirPath)
    tar = tarfile.open(tarPath)
    tar.extractall(outputDirPath)
    tar.close()

def getReportPaths(outputDirPath):
    print("Getting list of bug reports")

    reportPaths:array
    for dir in os.scandir(outputDirPath):
        fullPath = os.path.join(outputDirPath, dir)
        if os.path.isdir(fullPath):
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
        if file.path.endswith(".png") or file.path.endswith(".jpg") or file.path.endswith(".jpeg"):
            jiraClient.add_attachment(issue, attachment=file.path)

def importToJira(outputDirPath):
    try:
        jiraClient = JIRA(server=JIRA_HOSTNAME, token_auth=APPLICATION_TOKEN)
    except JIRAError as err:
        print("Error: An exception occured while attempting to authenticate the Jira Client: " + err.text)
        exit(1)

    reportPaths = getReportPaths(outputDirPath)

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
                    issue = jiraClient.create_issue(project=br.project, summary=br.summary, description=br.description, 
                        fundingsource=br.fundingsource, affectedVersion=br.affectedVersion, type=br.type, originator=br.originator, issueCategory=br.category)
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

    jiraClient.close()


def main(argv):
    print("Starting Bug Report Importer...")
    brTar = ''
    outputDir = ''
    argLen = len(sys.argv)

    # Note: See if there are any core python libraries that let you play with CLI arguments
    if argLen == 2:
        brTar = argv[1]
    elif argLen == 3:
        brTar = argv[1]
        outputDir = argv[2]
    else:
        print("Usage: BR_Jira_Import.py <Path to Bug Report Tar> <Optional tar extraction output path>")
        sys.exit(1)

    # Use default location if the user didn't enter a path
    if not outputDir:
        outputDir = DEFAULT_OUTPUT_DIRECTORY

    if brTar.endswith('.tar', '.tar.gz', '.tgz', '.gz'):
        if os.path.exists(brTar):
            extractTar(brTar, outputDir)
        else:
            print("Error: " + brTar + " does not exist")
            sys.exit(1)
    else:
        print("Error: Bug Report archive must be in .tar|.tar.gz|.tgz|.gz format")
        sys.exit(1)
    
    importToJira(outputDir)
