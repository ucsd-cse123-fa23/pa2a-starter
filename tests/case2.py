from test_base import *
import unittest
import random

class Test1(CSE123TestBase):
    
    def setUp(self):
        self.setUpEnvironment(build=False)
        # Any other initialization goes here

    def tearDown(self):
        self.tearDownEnvironment()
        # Any other cleanup goes here

    def test_case(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
