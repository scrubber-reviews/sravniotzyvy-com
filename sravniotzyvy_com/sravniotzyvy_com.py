# -*- coding: utf-8 -*-

"""Main module."""
import re
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests.structures import CaseInsensitiveDict


class SravniOtzyvyCom:
    rating = None
    BASE_URL = 'https://sravniotzyvy.com'
    reviews = []

    def __init__(self, slug):
        self.session = requests.Session()
        self.slug = str(slug)
        self.rating = Rating()
        self.session.headers = CaseInsensitiveDict({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel'
                          ' Mac OS X x.y; rv:10.0)'
                          ' Gecko/20100101 Firefox/10.0',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'text/html; charset=utf-8'
        })

    def start(self):
        resp = self.session.get(urljoin(self.BASE_URL, self.slug) + '.html')
        resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.text, 'html.parser')
        self.rating.average_rating = self._convert_string_to_float(
            soup.select_one('div.summ>p').text)
        self.reviews = list(self._collect_reviews(soup))
        return self

    def _collect_reviews(self, soup):
        for review_soup in soup.find_all('div', id='comment'):
            new_review = Review()
            new_review.text = review_soup.text
            new_review.date = review_soup.parent \
                .select_one('span.dtreviewed').text
            if review_soup.parent['class'][1] == 'good':
                new_review.status = _StatusReview.positive
            else:
                new_review.status = _StatusReview.negative
            new_review.author.name = review_soup.parent \
                .select_one('span.reviewer').text
            yield new_review

    @staticmethod
    def _convert_string_to_float(text):
        text = text.replace(',', '.')
        try:
            return float(text)
        except ValueError:
            return float(re.findall("\d+\.\d+", text)[0])


class Rating:
    average_rating = None
    min_scale = 0.0
    max_scale = 5.0

    def get_dict(self):
        return {
            'average_rating': self.average_rating,
            'on_scale': self.min_scale,
            'max_scale': self.max_scale,
        }

    def __repr__(self):
        return '<{} из {}>'.format(self.average_rating, self.max_scale)


class Author:
    name = ''

    def get_name(self):
        return self.name

    def get_dict(self):
        return {
            'name': self.name
        }


class _StatusReview(Enum):
    negative = True
    positive = True


class Review:
    def __init__(self):
        self.text = ''
        self.date = ''
        self.author = Author()
        self.status = None
        self.rating = Rating()

    def get_dict(self):
        return {
            'text': self.text,
            'date': self.date,
            'status': self.status,
            'rating': self.rating.get_dict(),
            'author': self.author.get_dict(),
        }

    def __repr__(self):
        return '<{}: {} -> {}'.format(self.date,
                                      self.author.get_name(), self.status)


if __name__ == '__main__':
    prov = SravniOtzyvyCom('1711-rosenergobank-otzyvy')
    prov.start()
    for r in prov.reviews:
        print(r.get_dict())
