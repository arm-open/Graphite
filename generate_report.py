import click

useremail = ''
userpassword = ''

@click.command()
@click.argument('pdfname')
@click.option('--email', help='Google Analytics Email')
@click.option('--password', help='Google Analytics Password')
def importArgs(pdfname, email, password):
    global useremail 
    useremail = email
    global userpassword
    userpassword = password
    click.echo(pdfname)
    #printEmail()
    #printPwd()

''''
def printEmail():
    click.echo('%s' % useremail)

def printPwd():
    click.echo('%s' % userpassword)
'''

if __name__ == '__main__':
    importArgs()
