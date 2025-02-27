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

import pytest

from .fixtures.fixture_utils import temp_named_txt_file
from .fixtures.unicorn_utils import BinBlob2Emulator
from .fixtures.blobs import BlobArmEl32MultiBlock

from FII.core.plugin import PluginManager
from FII.plugins.emulator_shell import EmulatorShell


@pytest.mark.parametrize(
    'temp_named_txt_file', [['plugin_unicorn_dbg: {}', '.yaml']],
    indirect=['temp_named_txt_file'])
def test_load_plugin_unicorn_dbg_with_emulator_shell(temp_named_txt_file, capsys):
    pl = PluginManager()
    pl.plugins_context.add('emulator_shell', EmulatorShell())
    pl.plugins_context.add('unicorn_uc', BinBlob2Emulator(BlobArmEl32MultiBlock).uc)
    pl.load_plugin_by_config_file(temp_named_txt_file.name)
    assert pl.plugins_context.get('plugin_unicorn_dbg') is not None
