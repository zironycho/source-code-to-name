# -*- coding: utf-8 -*-
import unittest

import os

import codetoname


class TestCrawler(unittest.TestCase):
    def setUp(self):
        account = os.getenv('github_account', '')
        password = os.getenv('github_password', '')
        if account and password:
            self.crawler = codetoname.Crawler(index='codetoname-dev', page_size=3, account=account, password=password)
        else:
            self.crawler = codetoname.Crawler(index='codetoname-dev', page_size=3)

    def tearDown(self):
        self.crawler.delete_index()

    def test_fetch_github_repo_item(self):
        repos = self.crawler.fetch_github_repos()
        self.assertEqual(3, len(repos))
        self.assertIn('url', repos[0])
        self.assertIn('branch', repos[0])
        self.assertIn('github_id', repos[0])
        self.assertIn('fork', repos[0])

        next_repos = self.crawler.fetch_github_repos()
        self.assertEqual(3, len(next_repos))

        the_same = True
        for u in next_repos:
            if u not in repos:
                the_same = False
        self.assertFalse(the_same)

    def test_next(self):
        self.crawler.create_index()
        self.assertEqual(0, self.crawler.num_features())
        self.crawler.next()
        num_repos = self.crawler.num_repos()
        self.assertNotEqual(0, num_repos)
        self.crawler.next()
        self.assertLess(num_repos, self.crawler.num_repos())

    def test_num_repos(self):
        self.crawler.next()
        self.assertEqual(3, self.crawler.num_repos())
        self.crawler.next()
        self.assertLess(3, self.crawler.num_repos())

    def test_exist_repos(self):
        self.crawler.next()
        features = self.crawler.get_features()
        self.assertTrue(features)
        github_id = features[0]['repo']['github_id']
        print(github_id)
        self.assertTrue(self.crawler.exists_repos_in_database(github_id))


class TestCrawlerLimit(unittest.TestCase):
    def setUp(self):
        account = os.getenv('github_account', '')
        password = os.getenv('github_password', '')
        if account and password:
            self.crawler = codetoname.Crawler(index='codetoname-dev', account=account, password=password)
        else:
            self.crawler = codetoname.Crawler(index='codetoname-dev')

    def tearDown(self):
        self.crawler.delete_index()

    def test_fetch_more_than_1000(self):
        for i in range(35):
            self.assertEqual(30, len(self.crawler.fetch_github_repos()))
