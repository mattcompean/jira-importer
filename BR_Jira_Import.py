import sys
import tarfile
import os.path

APPLICATION_TOKEN = ''
TEMP_DIRECTORY = 'H:/Work/Python/temp'

def extractTar(tarPath):
    print("Extracting " + tarPath + " to " + TEMP_DIRECTORY)
    tar = tarfile.open(tarPath)
    tar.extractall(TEMP_DIRECTORY)
    tar.close()

def main(argv):
    brTar = ''
    argLen = len(sys.argv)

    if argLen > 0 and argLen <= 2:
        brTar = argv[1]
    else:
        print("Usage: BR_Jira_Impoty.py <Path to Bug Report Tar>")
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
    
