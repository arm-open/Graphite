# Graphite [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) ![Version](https://img.shields.io/badge/version-v.0.1.17-blue.svg)
A simple tool for scraping google analytics and generating a meaningful report from our usage data.

![ScreenShot](http://i.imgur.com/eXdtzwQ.png)

<!-- toc -->

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  * [Signature / Name](#signature--name)

<!-- tocstop -->

# Requirements

```
- python 3
- phantomjs (v2 or higher works; make sure it's installed globally with npm/yarn)
- pip (python 3 found at https://pypi.udo pip uninstall graphython.org/pypi/pip)

```
# Installation

Make sure you have phantomjs installed (you can use npm or yarn)

`npm install -g phantomjs-prebuilt`

It's best to have this installed in your python user directory with the `--user` option on pip. 

`pip install --user graphite-analytics`

In order for this script to work properly, you must export the following environment variables
```
VIEW_ID
CLIENT_SECRETS_PATH
```

To get these variables:
```
**NOTE; When prompted click Furnish a new private key and for the Key type select JSON, and save the generated key as client_secrets.json; you will need it later**
1. Go to https://console.developers.google.com/permissions/serviceaccounts
2. Click create service accoun``t
```
![ScreenShot](https://i.imgur.com/NTYgQ7o.png)
```
3. In the Create service account window, type a name for the service account, and select Furnish a new private key. Then click Create.
4. Your new public/private key pair is generated and downloaded to your machine; it serves as the only copy of this key. You are responsible for storing it securely.
```
![ScreenShot](https://i.imgur.com/zVPRCcH.png)
```
5. Make sure you have your client_secrets.json file and set its path in the CLIENT_SECRETS_PATH environment variable
6. For your VIEW_ID you can find it under https://ga-dev-tools.appspot.com/account-explorer/, so set the VIEW_ID environmental variable with the #.
```

If you decide not to use environment variables, I have added `--secretpath` and `--viewid` command line options. 

# Usage

If you have installed this with the sudo command, and have set environment variables run:

`sudo -E graphite-analytics`

If you don't have any environment variables set, simply remove the -E option and use the `--secretpath` and `--viewid` options to specify the client secrets path location and your viewid

If you have installed this with the `--user` option on pip, you can just run

`graphite-analytics` 

And an analytics.png file will be generated similar to the screenshot of the example output.

## Signature / Name

If you want a signature / your name added, I have added an `--name` option.
