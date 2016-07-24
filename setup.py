from setuptools import setup, find_packages

setup(
    name='codetoname',
    version='0.1',
    py_modules=find_packages(),
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        codetoname-crawler=cli:cli_crawler
        codetoname-total-repo=cli:cli_total_repos
        codetoname-total-feat=cli:cli_total_features
        codetoname-first-words=cli:cli_report_first_words
    ''',
)
