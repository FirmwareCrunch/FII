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

from typing import Dict, Any

from FII.core.plugin import FiiPlugin, FiiPluginContext, Requirement


class CustomDependencyP5:
    pass


class PluginTestP5(FiiPlugin):
    NAME = 'plugin_test_p5'
    LOADING_PRIORITY = 2
    REQUIREMENTS = [Requirement('plugin_test_requirement', CustomDependencyP5)]
    CONFIG_SCHEMA = {
        NAME: {
            'type': 'dict',
            'required': False,
            'schema': {'activate': {'type': 'boolean'}}
        }
    }

    def plugin_load(
        self,
        plugins_context: FiiPluginContext,
        plugin_config: dict,
        requirements: Dict[str, Any],
        optional_requirements: Dict[str, Any]
    ):
        pass
