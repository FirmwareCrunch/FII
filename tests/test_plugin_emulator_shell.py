################################################################################
#
# Copyright 2022-2025 Vincent Dary
#
# This file is part of FII.
#
# FII is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation
# , either version 3 of the License, or (at your option) any later version.
#
# FII is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# FII. If not, see <https://www.gnu.org/licenses/>.
#
################################################################################

from io import StringIO

import pytest
from unittest.mock import patch

from .fixtures.fixture_utils import temp_named_txt_file

from FII.plugins.emulator_shell import ShellPluginsContext
from FII.core.plugin import PluginManager


def test_plugin_context_repr():
    pc = ShellPluginsContext()
    setattr(pc, 'test_attr', 4)
    assert pc.__repr__() == "test_attr : <class 'int'>"


@pytest.mark.parametrize(
    'temp_named_txt_file', [['plugin_emulator_shell: {}', '.yaml']],
    indirect=['temp_named_txt_file'])
def test_load_plugin_emulator_shell(temp_named_txt_file, capsys):
    pl = PluginManager()
    pl.load_plugin_by_config_file(temp_named_txt_file.name)

    assert pl.plugins_context.get('plugin_emulator_shell') is not None

    with patch('sys.stdin', StringIO('quit\n')):
        pl.plugins_context.program_entry()

    assert capsys.readouterr().out == '\nFII >>> '
