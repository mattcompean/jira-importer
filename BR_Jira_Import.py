from array import array
from genericpath import isdir
import sys
import tarfile
import os
from tempfile import tempdir
from jira import JIRA

APPLICATION_TOKEN = ''
TEMP_DIRECTORY = 'H:/Work/Python/temp'

#TODO add all necessary fields from bug report file
class BugReport:
    def __init__(self):
        self.issueNumber = ""
        self.component = ""

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

def importToJira():
    jiraClient = JIRA('https://jira.atlassian.com', token_auth=APPLICATION_TOKEN)
    reportPaths = getReportPaths()

    if len(reportPaths) > 0:
        reportPaths.sort()
    else:
        print("Error: Could not get list of bug reports")
        exit(1)


def main(argv):
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
