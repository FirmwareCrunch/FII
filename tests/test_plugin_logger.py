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

from FII.core.plugin import PluginManager


@pytest.mark.parametrize(
    'temp_named_txt_file',
    [['plugin_logger:\n'
      ' loggers_level_config:\n'
      '     FII.tests: INFO\n', '.yaml']],
    indirect=['temp_named_txt_file'])
def test_load_plugin_logger(temp_named_txt_file):
    PluginManager().load_plugin_by_config_file(temp_named_txt_file.name)
