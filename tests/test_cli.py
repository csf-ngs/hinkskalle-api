#!/usr/bin/env python

"""Tests for `hinkskalle_api` package."""


import unittest
from click.testing import CliRunner
from unittest import mock

from hinkskalle_api import cli
import re
import os


class TestCli(unittest.TestCase):
  def test_help(self):
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.cli)
    self.assertEqual(result.exit_code, 0)
    help_result = runner.invoke(cli.cli, ['--help'])
    self.assertEqual(help_result.exit_code, 0)
    self.assertRegexpMatches(help_result.output, r'--help\s+Show this message and exit.')

  @mock.patch.dict(os.environ, { 'HINK_API_BASE': 'http://testha.se', 'HINK_API_KEY': 'secret'})
  def test_push(self):
    runner = CliRunner()
    with mock.patch('hinkskalle_api.api.HinkApi.push_file') as mock_push:
      result = runner.invoke(cli.cli, ['push', 'testhase', 'testhase:v1'], catch_exceptions=False)
    self.assertEqual(result.exit_code, 0)

  @mock.patch.dict(os.environ, { 'HINK_API_BASE': 'http://testha.se', 'HINK_API_KEY': 'secret'})
  def test_push_exclude(self):
    runner = CliRunner()
    with mock.patch('hinkskalle_api.api.HinkApi.push_file') as mock_push:
      result = runner.invoke(cli.cli, ['push', 'testhase', 'testhase:v1', '--exclude', 'oink'], catch_exceptions=False)
    self.assertEqual(result.exit_code, 0)
    mock_push.assert_called_with(entity=None, collection='default', container='testhase', tag='v1', progress=True, filename='testhase', excludes=[re.compile('oink')])
  
  @mock.patch.dict(os.environ, { 'HINK_API_BASE': 'http://testha.se', 'HINK_API_KEY': 'secret'})
  def test_push_exclude_file(self):
    runner = CliRunner()
    with mock.patch('hinkskalle_api.api.HinkApi.push_file') as mock_push, runner.isolated_filesystem():
      with open('excludes', 'w') as ofh:
        ofh.write("oink\n")
        ofh.write("# something\n")
        ofh.write(".*\n")
      result = runner.invoke(cli.cli, ['push', 'testhase', 'testhase:v1', '--exclude-file', 'excludes'], catch_exceptions=False)
    self.assertEqual(result.exit_code, 0)
    mock_push.assert_called_with(entity=None, collection='default', container='testhase', tag='v1', progress=True, filename='testhase', excludes=[re.compile('oink'), re.compile('.*')])
