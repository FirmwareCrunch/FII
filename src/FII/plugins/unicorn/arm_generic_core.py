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

import unicorn

from FII.unicorn.arm.arm_generic_core import UnicornArmGenericCore
from FII.core.plugin import (
    FiiPlugin, FiiPluginContext, Requirement,
    PLUGIN_PRIORITY_LEVEL_BUILTIN_L2)


class PluginUnicornGenericArmCore(FiiPlugin):
    NAME = 'plugin_unicorn_arm_generic_core'
    LOADING_PRIORITY = PLUGIN_PRIORITY_LEVEL_BUILTIN_L2
    REQUIREMENTS = [Requirement('unicorn_uc', unicorn.Uc)]
    CONFIG_SCHEMA = {
        NAME: {
            'type': 'dict',
            'schema': {
                'high_vector_support': {'type': 'boolean', 'default': True},
                'high_vector': {'type': 'boolean', 'default': False},
            }
        }
    }

    def plugin_load(
        self,
        plugins_context: FiiPluginContext,
        plugin_config: dict,
        requirements: Dict[str, Any],
        optional_requirements: Dict[str, Any]
    ):
        uc = requirements.get('unicorn_uc')
        arm_core = UnicornArmGenericCore(uc, **plugin_config)
        plugins_context.add('unicorn_arm_generic_core', arm_core)
