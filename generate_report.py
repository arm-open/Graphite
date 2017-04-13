#!/usr/bin/python
#
# This file is part of ARM's analytics reporting which is released under the Apache 2 license.
# See file /LICENSE or go to https://github.com/ARM-open/analytics-reports arm for full license details.
# 


import click

# Usage: python generate report.py [ --name <output_filename> ]   



@click.command()
@click.option('--name', default='report.pdf', help='Name of output file.')
def run(name):
    click.echo('Hello %s!' % name)

if __name__ == '__main__':
    run()
