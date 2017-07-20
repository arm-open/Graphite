#!/usr/bin/env python3
"""
---------------------------------------------------------------------------------
Takes user sessions off Google Analytics API and Puts a bar graph into a PDF File
Uses Python3 Written by Arian Moslem
---------------------------------------------------------------------------------
"""
import argparse
import os
import sys
import subprocess
import click
import httplib2
from apiclient.discovery import build
from oauth2client import client, file, tools
from jinja2 import Environment, FileSystemLoader

# GLOBALS
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
CLIENT_SECRETS_PATH = ''  # Path to client_secrets.json file.
VIEW_ID = ''


def initialize_analyticsreporting():
    """Initializes the analyticsreporting service object.

    Returns:
      analytics an authorized analyticsreporting service object.
    """
    # Parse command-line arguments.
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[tools.argparser])
    flags = parser.parse_args([])

    # Set up a Flow object to be used if we need to authenticate.
    flow = client.flow_from_clientsecrets(
        CLIENT_SECRETS_PATH, scope=SCOPES,
        message=tools.message_if_missing(CLIENT_SECRETS_PATH))

    # Prepare credentials, and authorize HTTP object with them.
    # If the credentials don't exist or are invalid run through the native client
    # flow. The Storage object will ensure that if successful the good
    # credentials will get written back to a file.
    storage = file.Storage('analyticsreporting.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)
    http = credentials.authorize(http=httplib2.Http())

    # Build the service object.
    analytics = build('analytics', 'v4', http=http,
                      discoveryServiceUrl=DISCOVERY_URI)

    return analytics


def get_report(analytics, days, metric, dimension=''):
    # Use the Analytics Service Object to query the Analytics Reporting API V4.
    if dimension:
        return analytics.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': VIEW_ID,
                        'dateRanges': [{'startDate': days + 'daysAgo', 'endDate': 'today'}],
                        'metrics': [{'expression': 'ga:' + metric}],
                        'dimensions': [{'name': 'ga:' + dimension}]
                    }]
            }
        ).execute()

    else:
        return analytics.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': VIEW_ID,
                        'dateRanges': [{'startDate': days + 'daysAgo', 'endDate': 'today'}],
                        'metrics': [{'expression': 'ga:' + metric}]
                    }]
            }
        ).execute()


def get_report_end(analytics, days, metric, dimension=''):
    # Use the Analytics Service Object to query the Analytics Reporting API V4.
    if dimension:
        return analytics.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': VIEW_ID,
                        'dateRanges': [{'startDate': days + 'daysAgo', 'endDate': str(int(days) - 1) + 'daysAgo'}],
                        'metrics': [{'expression': 'ga:' + metric}],
                        'dimensions': [{'name': 'ga:' + dimension}]
                    }]
            }
        ).execute()

    else:
        return analytics.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': VIEW_ID,
                        'dateRanges': [{'startDate': days + 'daysAgo', 'endDate': str(int(days) - 1) + 'daysAgo'}],
                        'metrics': [{'expression': 'ga:' + metric}]
                    }]
            }
        ).execute()


def return_response_dimension(response):
    """Parses and prints the Analytics Reporting API V4 response
       Returns a dictionary of all the values"""

    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get(
            'metricHeader', {}).get('metricHeaderEntries', [])
        rows = report.get('data', {}).get('rows', [])

        returned = []
        for row in rows:
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])
            for i, values in enumerate(dateRangeValues):
                #returned.append(zip(dimensions, values.get('values')))
                d = {}
                d[dimensions[0]] = values.get('values')[0]
                returned.append(d)

            '''
      for header, dimension in zip(dimensionHeaders, dimensions):
        print(header + ': ' + dimension)

      for i, values in enumerate(dateRangeValues):
        print('Date range (' + str(i) + ')')
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          print(metricHeader.get('name') + ': ' + value)
      '''

        return returned


def return_response(response):
    """Parses and prints the Analytics Reporting API V4 response
       Returns a dictionary of all the values"""

    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get(
            'metricHeader', {}).get('metricHeaderEntries', [])
        rows = report.get('data', {}).get('rows', [])

        for row in rows:
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])
            for i, values in enumerate(dateRangeValues):
                return values.get('values')

        return


@click.command()
@click.option('--name', default='', help='Your/Company/Etc name for the signature')
@click.option('--secretpath', default='', help='Client Secrets Path')
@click.option('--viewid', default='', help='View Id')
def main(name, secretpath, viewid):
    #THE PATH OF THE FILE DIRECTORY
    dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'
    cwd = os.getcwd()
    # ERROR CHECKING & SETTING UP OUR GLOBAL VARIABLES
    global CLIENT_SECRETS_PATH
    if "CLIENT_SECRETS_PATH" in os.environ:
        CLIENT_SECRETS_PATH = os.environ["CLIENT_SECRETS_PATH"]
    elif secretpath:
        CLIENT_SECRETS_PATH = secretpath
    else:
        print("Please set the environment variable CLIENT_SECRETS_PATH, which is the path and including the client secrets .json file or use the \"--secretpath <path>\" option to list it's path")
        sys.exit(1)

    global VIEW_ID
    if "VIEW_ID" in os.environ:
        VIEW_ID = os.environ["VIEW_ID"]
    elif viewid:
        VIEW_ID = viewid
    else:
        print("Please set the environment variable VIEW_ID or use the \"--viewid <id>\" option to list it's VIEW ID")
        sys.exit(1)

    copysecrets = subprocess.run(["cp " + CLIENT_SECRETS_PATH + " client_secrets.json"], shell=True)
    CLIENT_SECRETS_PATH = "client_secrets.json"
    """
    DATA TO BE PASSED INTO THE HTML DOCUMENT
    INITALIZING OUR ANALYTICS REPORTING
    """
    analytics = initialize_analyticsreporting()
    # Total Number of sessions for past 30 days
    response = get_report(analytics, '30', 'sessions')
    sessionNum = return_response(response)
    sessionNum = sessionNum[0]
    # Total Number of users in the past 30 days
    response = get_report(analytics, '30', 'users')
    userNum = return_response(response)
    userNum = userNum[0]
    # Total Number of pageviews in the past 30 days
    response = get_report(analytics, '30', 'pageviews')
    pageViews = return_response(response)
    pageViews = pageViews[0]
    # Bounce rate % in the past 30 days
    response = get_report(analytics, '30', 'bounceRate')
    bounceRate = return_response(response)
    bounceRate = bounceRate[0]
    # Sessions over past 30 days on per day basis
    sessionCount = []
    for i in range(1, 31):
        response = get_report_end(analytics, str(i), 'sessions')
        sessionCounter = return_response(response)
        if not sessionCounter:
            sessionCount.append(0)
        else:
            sessionCounter = sessionCounter[0]
            sessionCount.append(int(sessionCounter))
    # Channels that are driving enagement
    response = get_report(analytics, '30', 'sessions',
                          'acquisitionTrafficChannel')
    sessionChannels = return_response_dimension(response)
    response = get_report(analytics, '30', 'pageviews',
                          'acquisitionTrafficChannel')
    pageviewChannels = return_response_dimension(response)
    # Device Type Distribution in the past 30 days
    response = get_report(analytics, '30', 'sessions', 'deviceCategory')
    deviceTypes = return_response_dimension(response)
    # Average Session Length for past 30 days
    response = get_report(analytics, '30', 'sessions', 'sessionDurationBucket')
    sessionDuration = return_response_dimension(response)
    # Top Countries by sessions for past 30 days
    response = get_report(analytics, '30', 'sessions', 'country')
    countryPerSession = return_response_dimension(response)
    countryPerSession = countryPerSession[0:20]
    countryperSession = countryPerSession[::-1]

    """
    LOADED UP JINJA ENVIRONMENT, WILL BE PASSING DATA INTO IT
    WILL RENDER A rendered.html DOCUMENT WITH ALL THE DATA PASSED INTO IT
    """
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
    rendered_output = j2_env.get_template('templates/html/render.html').render(
        number_of_sessions=sessionNum,
        number_of_users=userNum,
        number_of_pageViews=pageViews,
        bounce_rate_percentage=bounceRate[0:4],
        daily_sessions=sessionCount,
        engagement_session_channels=sessionChannels,
        engagement_pageview_channels=pageviewChannels,
        device_types=deviceTypes,
        session_duration=sessionDuration,
        country_per_session=countryPerSession,
        signature_name = name
        )
    # Rendered file which will receive output written to it and then closed up
    try:
        os.remove(dir_path + 'templates/html/rendered.html')
    except OSError:
        pass

    renderedFile = open(dir_path + "templates/html/rendered.html", "a")
    renderedFile.write(rendered_output)
    renderedFile.close()
    #Running phantomjs then exitting
    os.chdir(dir_path)
    phantomout = subprocess.run(["phantomjs --ignore-ssl-errors=true capture.js"], shell=True, cwd=dir_path)
    subprocess.run(["mv analytics.png " + cwd], shell=True)

if __name__ == '__main__':
    main()
