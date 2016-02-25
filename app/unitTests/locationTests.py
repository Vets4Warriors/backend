from requests import get, put, post, delete
import unittest
import app

class AddTest(unittest.TestCase):
    def setUp(self):
        super(AddTest, self).setUp()

    def tearDown(self):
        super(AddTest, self).tearDown()

    def doCleanups(self):
        return super(AddTest, self).doCleanups()


if __name__ == '__main__':
    unittest.main()
