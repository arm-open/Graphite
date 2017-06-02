"""
---------------------------------------------------------------------------------
Takes user sessions off Google Analytics API and Puts a bar graph into a PDF File
Uses Python2
Written by Arian Moslem
---------------------------------------------------------------------------------
"""

import argparse
import os
import sys

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools


def get_service(api_name, api_version, scope, key_file_location,
                service_account_email):
  """Get a service that communicates to a Google API.
  Args:
    api_name: The name of the api to connect to.
    api_version: The api version to connect to.
    scope: A list auth scopes to authorize for the application.
    key_file_location: The path to a valid service account p12 key file.
    service_account_email: The service account email address.
  Returns:
    A service that is connected to the specified API.
  """

  f = open(key_file_location, 'rb')
  key = f.read()  
  f.close()

  credentials = ServiceAccountCredentials.from_p12_keyfile(
              service_account_email, key_file_location, scopes=scope)


  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  service = build(api_name, api_version, http=http)

  return service

def get_first_profile_id(service):
  # Use the Analytics service object to get the first profile id.

  # Get a list of all Google Analytics accounts for this user
  accounts = service.management().accounts().list().execute()

  if accounts.get('items'):
    # Get the first Google Analytics account.
    account = accounts.get('items')[0].get('id')

    # Get a list of all the properties for the first account.
    properties = service.management().webproperties().list(
        accountId=account).execute()

    if properties.get('items'):
      # Get the first property id.
      property = properties.get('items')[0].get('id')

      # Get a list of all views (profiles) for the first property.
      profiles = service.management().profiles().list(
          accountId=account,
          webPropertyId=property).execute()

      if profiles.get('items'):
        # return the first view (profile) id.
        return profiles.get('items')[0].get('id')

  return None


def get_n_results(service, profile_id, n):
  # Use the Analytics Service Object to query the Core Reporting API
  # for the number of sessions within the past seven days.
  ndate = str(n)+'daysAgo'
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=ndate,
      end_date='today',
      metrics='ga:sessions').execute()



def main():
  # Define the auth scopes to request.
  scope = ['https://www.googleapis.com/auth/analytics.readonly']

  # Use the developer console and replace the values with your
  # service account email and relative location of your key file.
  if "GOOGLE_SERVICE_EMAIL" in os.environ:
      service_account_email = os.environ["GOOGLE_SERVICE_EMAIL"]
  else:
      print("Please set the environment variable GOOGLE_SERVICE_EMAIL, which is your google api service account email")
      sys.exit(1)

  if "KEY_FILE_LOCATION" in os.environ:
      key_file_location = os.environ["KEY_FILE_LOCATION"]

  else:
      print("Please set the environment variable KEY_FILE_LOCATION, which is the location to your .p12 client secrets file")
      sys.exit(1)

  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, key_file_location,
    service_account_email)
  profile = get_first_profile_id(service)
  xid7 = get_n_results(service, profile, 7)
  xid14 = get_n_results(service, profile, 14)
  xid21 = get_n_results(service, profile, 21)
  xid28 = get_n_results(service, profile, 28)
  xid35 = get_n_results(service, profile, 35)
  print(int(xid7.get('rows')[0][0]))
  print(int(xid14.get('rows')[0][0]))
  print(int(xid21.get('rows')[0][0]))
  print(int(xid28.get('rows')[0][0]))
  print(int(xid35.get('rows')[0][0]))


if __name__ == '__main__':
  main()
