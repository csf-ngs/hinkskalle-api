#!/usr/bin/env python

"""Tests for `hinkskalle_api` package."""


import unittest
from click.testing import CliRunner

from hinkskalle_api import cli


class TestCli(unittest.TestCase):
    def test_help(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'hinkskalle_api.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
