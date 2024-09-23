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

from typing import Dict, Any, cast

from unicorn import Uc
from unicorn.unicorn_const import UC_HOOK_INTR

from FII.unicorn.arm.arm_generic_core import UnicornArmGenericCore
from FII.unicorn.arm.pl190 import UnicornArmPl190
from FII.core.emulator_types import AddressSpace
from FII.core.plugin import (
    FiiPlugin, FiiPluginContext, Requirement,
    PLUGIN_PRIORITY_LEVEL_BUILTIN_L3)


class PluginUnicornArmPl190(FiiPlugin):
    NAME = 'plugin_unicorn_arm_pl190'
    LOADING_PRIORITY = PLUGIN_PRIORITY_LEVEL_BUILTIN_L3
    REQUIREMENTS = [Requirement('unicorn_uc', Uc)]
    OPTIONAL_REQUIREMENTS = [
        Requirement('unicorn_arm_generic_core', UnicornArmGenericCore),
        Requirement('emulator_address_space', AddressSpace)
    ]
    CONFIG_SCHEMA = {
        NAME: {
            'type': 'dict',
            'schema': {
                'base_address': 'DEF_INT64',
            }
        }
    }

    def plugin_load(
        self,
        init_context: FiiPluginContext,
        plugin_config: dict,
        requirements: Dict[str, Any],
        optional_requirements: Dict[str, Any]
    ):
        uc = cast(Uc, requirements['unicorn_uc'])
        pl190_base_addr = plugin_config['base_address']
        auto_map = True

        for begin, end, _ in uc.mem_regions():
            if (pl190_base_addr >= begin
                    and pl190_base_addr+UnicornArmPl190.MEM_MAP_SIZE-1 <= end):
                auto_map = False

        pl190 = UnicornArmPl190(uc, pl190_base_addr, auto_map)
        uc.hook_add(UC_HOOK_INTR, pl190.reset_handler, begin=1, end=0)

        if cpu := optional_requirements.get('unicorn_arm_generic_core', None):
            pl190.set_nvicfiq_high_callback(cpu.set_fiq_mode)
            pl190.set_nvicirq_high_callback(cpu.set_irq_mode)

        if ((address_space := optional_requirements.get('emulator_address_space'))
                and auto_map):
            address_space = cast(AddressSpace, address_space)
            address_space.memory_regions.append(pl190.mem_region)

        init_context.add('unicorn_arm_pl190', pl190)
