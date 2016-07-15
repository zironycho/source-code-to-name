# -*- coding: utf-8 -*-
import unittest
import codetoname


class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.crawler = codetoname.Crawler(index='codetoname-dev', page_num=0, page_size=1)

    def tearDown(self):
        self.crawler.delete_index()

    def test_fetch_github_repos(self):
        repos = self.crawler.fetch_github_repos(page_size=10)
        self.assertEqual(10, len(repos))
        self.assertIn('url', repos[0])
        self.assertIn('branch', repos[0])
        self.assertIn('github_id', repos[0])
        self.assertIn('fork', repos[0])
        self.assertIn('https://github.com/jkbrzt/httpie.git', [r['url'] for r in repos])

        next_repos = self.crawler.fetch_github_repos()
        self.assertEqual(10, len(next_repos))

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

    def test_num_repos(self):
        self.crawler.next()
        self.assertEqual(1, self.crawler.num_repos())
        self.crawler.next()
        self.assertEqual(2, self.crawler.num_repos())

    def test_exist_repos(self):
        self.crawler.next()
        features = self.crawler.get_features()
        self.assertTrue(features)
        github_id = features[0]['repo']['github_id']
        print(github_id)
        self.assertTrue(self.crawler.exists_repos_in_database(github_id))
