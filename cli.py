import sys
import click
import humanize

from getpass import getpass
from codetoname import log, report
from codetoname.crawler import Crawler

# hooking log
sys.excepthook = log.except_hooking


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


@click.command()
def cli_total_repos():
    print(humanize.intcomma(Crawler().num_repos()))


@click.command()
def cli_total_features():
    print(humanize.intcomma(Crawler().num_features()))


@click.command()
def cli_report_first_words():
    for word in report.first_words():
        print(word)
