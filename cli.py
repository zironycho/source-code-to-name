import click
from getpass import getpass

from codetoname.crawler import Crawler


@click.command()
@click.option('--begin', default=0, help='begin index of page')
@click.option('--end', default=1, help='end index of page')
@click.option('--size', default=-1, help='size of page')
def cli_crawler(begin, end, size):
    account = input('Github account or email: ')
    password = getpass('Github password: ')

    begin = max(0, begin)
    if size <= 0:
        client = Crawler(account=account, password=password, page_num=begin)
    else:
        client = Crawler(account=account, password=password, page_num=begin, page_size=size)

    for i in range(begin, end):
        client.next()
