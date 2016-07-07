# -*- coding: utf-8 -*-
import unittest
import codetoname


class TestCrawler(unittest.TestCase):
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

    def test_crawler(self):
        self.assertTrue(codetoname.crawler.Crawler())
