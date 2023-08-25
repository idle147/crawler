import json
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.json_model import QJsonModel


class TestRetry(unittest.TestCase):

    def setUp(self):
        self.json_info = """{
                "name": "suncoreY",
                "age": 25,
                "address": {
                    "state": "中国",
                    "city": "广东广州"
                },
                "phoneNumber": [
                    {
                        "type": "home",
                        "number": "123456"
                    },
                    {
                        "type": "company",
                        "number": "654321"
                    }
                ]
            }"""
        self.model = QJsonModel()

    def tearDown(self):
        self.model.clear()

    def test_load(self):
        document = json.loads(self.json_info)
        self.assertTrue(self.model.load(document))

    def test_sort(self):
        document = json.loads(self.json_info)
        self.model.load(document)
        self.assertEqual(json.dumps(self.model.json(), sort_keys=True),
                         json.dumps(document, sort_keys=True))
