""" Testting parse_html function """
from unittest import TestCase
from unittest.mock import patch
import unittest
from faker import Faker

import main


class TestParseHTML(TestCase):
    """ Testing parse_html and other functions """

    def test_open_tag_process(self):
        """ Testing open_tags_process on small data """
        main.open_tags_count = {}
        main.open_tag_process('h1')
        main.open_tag_process('h1')
        open_tags_count = main.open_tag_process('a')
        self.assertEqual(open_tags_count, {'h1': 2, 'a': 1})

    def test_data_process(self):
        """ Testing data_process with Faker """
        fake = Faker(locale="Ru_ru")
        content = [fake.text(100) for _ in range(10)]
        content.append(fake.text(500))

        for _content in content:
            max_len = main.data_process(_content)

        self.assertEqual(max_len, len(content[-1]))

    def test_close_tag_process(self):
        """ Testing close_tags_process on small data """
        main.open_tags_count = {}
        main.open_tag_process('h1')
        main.open_tag_process('h1')
        main.open_tag_process('a')
        self.assertEqual(main.close_tag_process(), 'h1')

    @patch('main.open_tag_process', return_value=None)
    @patch('main.data_process', return_value=None)
    @patch('main.close_tag_process', return_value=None)
    def test_parse_html(self, otag_mock, data_mock, ctag_mock):
        """ Testing parse_html using mocks and Faker """
        fake = Faker()

        content = fake.text(100)

        html_str = content
        tags = []
        for _ in range(10):
            tag_text = fake.text(5)
            tags.append(tag_text)
            html_str = f"<{tag_text}>{html_str}</{tag_text}>"

        data = {tags[0]: [content]}
        for tag in tags[1:]:
            data = {tag: [data]}

        json = main.parse_html(html_str, otag_mock, data_mock, ctag_mock)

        self.assertEqual(otag_mock.call_count, 10)
        self.assertEqual(data_mock.call_count, 2*10+1)
        self.assertEqual(ctag_mock.call_count, 10)
        self.assertEqual(json, [data])


if __name__ == "__main__":
    unittest.main()
