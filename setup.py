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
    ''',
)
