# -*- coding: utf-8 -*-
import unittest
import codetoname


class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.crawler = codetoname.Crawler(index='codetoname-dev', page_num=0, page_size=1)

    def tearDown(self):
        self.crawler.delete_index()

    def test_fetch_github_repos(self):
        repos = codetoname.crawler.fetch_github_repos('python', repo_page=0)
        self.assertEqual(10, len(repos))
        self.assertIn('url', repos[0])
        self.assertIn('branch', repos[0])
        self.assertIn('github_id', repos[0])
        self.assertIn('fork', repos[0])
        self.assertIn('https://github.com/jkbrzt/httpie.git', [r['url'] for r in repos])

        next_repos = codetoname.crawler.fetch_github_repos('python', repo_page=1, repo_size=15)

        the_same = True
        for u in next_repos:
            if u not in repos:
                the_same = False
        self.assertFalse(the_same)

    def test_next(self):
        self.crawler.create_index()
        self.assertEqual(0, self.crawler.num_features())
        self.crawler.next()
        num_features = self.crawler.num_features()
        self.assertNotEqual(0, num_features)
        self.crawler.next()
        self.assertLess(num_features, self.crawler.num_features())
