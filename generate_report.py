#Import the rest here later
import click
from apiclient.discovery import build


#Global Variables to account for email and password
pdfToOpen = ''
aKey = ''
#API Service

#Instantiate a click command
@click.command()
@click.argument('pdfname')
@click.argument('apikey')
def importArgs(pdfname, apikey):
    global pdfToOpen
    pdfToOpen = pdfToOpen
    global akey
    aKey = apikey
    analytics_service = build('analytics', 'v3', developerKey = aKey)

if __name__ == '__main__':
    importArgs()

