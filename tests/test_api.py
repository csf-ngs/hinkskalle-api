import unittest
from unittest import mock
import os
import os.path
import tempfile

from hinkskalle_api import HinkApi

class TestApi(unittest.TestCase):
  def test_init(self):
    api = HinkApi(base='http://testha.se/', key='secret')
    self.assertEqual(api.base, 'http://testha.se')
  
  def test_config_file(self):
    with tempfile.TemporaryDirectory() as tmp_dir, mock.patch('hinkskalle_api.api.os.path.expanduser') as mock_exp:
      mock_exp.return_value = os.path.join(tmp_dir, 'test.yml')
      with open(mock_exp(), 'w') as tmpfh:
        tmpfh.write("hink_api_base: http://testha.se/\nhink_api_key: secret\n")
      api = HinkApi()
      self.assertEqual(api.base, 'http://testha.se')
      self.assertEqual(api.key, 'secret')
      mock_exp.assert_called_with('~/.hink_api.yml')

      with mock.patch.dict(os.environ, { 'HINK_API_CFG': '~/blubb.yml'}):
        api = HinkApi()
      mock_exp.assert_called_with('~/blubb.yml')

  
  def test_config_env(self):
    with mock.patch.dict(os.environ, { 'HINK_API_BASE': 'http://testha.se', 'HINK_API_KEY': 'secret'}):
      api = HinkApi()
      self.assertEqual(api.base, 'http://testha.se')
      self.assertEqual(api.key, 'secret')
    
  def test_no_config(self):
    with tempfile.TemporaryDirectory() as tmp_dir, mock.patch('hinkskalle_api.api.os.path.expanduser') as mock_exp:
      mock_exp.return_value = os.path.join(tmp_dir, 'test.yml')
      with self.assertRaisesRegex(FileNotFoundError, r'/test\.yml'):
        api = HinkApi()

    with tempfile.TemporaryDirectory() as tmp_dir, mock.patch('hinkskalle_api.api.os.path.expanduser') as mock_exp:
      mock_exp.return_value = os.path.join(tmp_dir, 'test.yml')
      with open(mock_exp(), 'w') as tmpfh:
        tmpfh.write("oink: http://testha.se/\ngrunz: secret\n")
      with self.assertRaisesRegex(Exception, r'Please configure'):
        api = HinkApi()

  def test_make_headers(self):
    api = HinkApi(base='http://testha.se', key='secret')
    self.assertDictEqual(api._make_headers({ 'bla': 'fasel'}), { 'bla': 'fasel', 'Authorization': 'Bearer secret'})