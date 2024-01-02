from django.test import TestCase

import unittest
import os
from utils import Logger

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.log_file = 'test_logfile.log'
        self.logger = Logger(log_file=self.log_file)
        
    def test_log_entry(self):
        message = 'Test log entry'
        
        # Проверка записи в лог
        self.logger.log_entry(message)
        self.assertTrue(os.path.exists(self.log_file))

        # Проверка, что запись в лог содержит указанное сообщение
        with open(self.log_file, 'r') as log_file:
            log_content = log_file.read()
            self.assertIn(message, log_content)

if __name__ == '__main__':
    unittest.main()
