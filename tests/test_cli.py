#!/usr/bin/env python

"""Tests for `hinkskalle_api` package."""


import unittest
from click.testing import CliRunner

from hinkskalle_api import cli


class TestCli(unittest.TestCase):
    def test_help(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.cli)
        self.assertEqual(result.exit_code, 0)
        help_result = runner.invoke(cli.cli, ['--help'])
        self.assertEqual(help_result.exit_code, 0)
        self.assertRegexpMatches(help_result.output, r'--help\s+Show this message and exit.')
