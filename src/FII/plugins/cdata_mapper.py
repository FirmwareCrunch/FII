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

from typing import Dict, Any, cast, List

import IPython
from IPython.core import magic
from IPython.core.magic_arguments import (
    argument, magic_arguments, parse_argstring)

from FII.core.emulator_types import (
    Architecture, AddressSpace, ADDRESS_FORMAT)
from FII.core.ctypes import (
    configure_ctypes, CTypesTranslator,
    CDataMemMapper, CDataMemMapEntry,
    CTYPES_TRANSLATOR_FLAVOR)
from FII.core.shell import register_alias
from .emulator_shell import EmulatorShell
from FII.core.plugin import (
    FiiPlugin, FiiPluginContext, Requirement,
    PLUGIN_PRIORITY_LEVEL_BUILTIN_L4)


class ShellCDataMemMapper:
    def __init__(self, cdata_mem_mapper: CDataMemMapper, address_formatter):
        self._cdata_mem_mapper = cdata_mem_mapper
        self._address_formatter = address_formatter

    def __getattr__(self, name: str):
        if cdata_entry := self._cdata_mem_mapper.get_cdata_mapping(name):
            return cdata_entry.cdata
        else:
            raise AttributeError(f'{name} attribute not found.')

    def __repr__(self):
        cdata_entries = self._cdata_mem_mapper.get_all_mapping()

        cdata_by_addr: Dict[int, List[CDataMemMapEntry]] = {}
        for _, cdata_entry in cdata_entries.items():
            cdata_by_addr.setdefault(cdata_entry.address, list())
            cdata_by_addr[cdata_entry.address].append(cdata_entry)

        buffer = list()
        for addr in sorted(cdata_by_addr):
            for entry in cdata_by_addr[addr]:
                buffer.append(f'{self._address_formatter(entry.address)} '
                              f': {entry.name} '
                              f': {str(entry.cdata.__class__._name_)}')

        return '\n'.join(buffer)


@IPython.core.magic.magics_class
class CDataMemMapperFrontend(IPython.core.magic.Magics):
    def __init__(
        self, cdata_mem_mapper: CDataMemMapper, emu_shell: EmulatorShell,
        address_formatter
    ):
        super(CDataMemMapperFrontend, self).__init__(shell=emu_shell.shell)
        self.cdata_memory_mapper = cdata_mem_mapper
        self.emu_shell = emu_shell
        emu_shell.register_magics(self)
        emu_shell.register_aliases(self)
        shell_cdata_mapper = ShellCDataMemMapper(
            cdata_mem_mapper, address_formatter)
        emu_shell.map_object_in_shell('cdata_mapping', shell_cdata_mapper)

    @magic_arguments()
    @argument('cdata_type', type=str, help='')
    @argument('cdata_name', type=str, help='')
    @argument('address', help='')
    @register_alias('bc')
    @IPython.core.magic.line_magic
    def map_cdata(self, line: str):
        args = parse_argstring(self.map_cdata, line)
        if isinstance(args.address, str):
            address = int(args.address, 16)
        else:
            address = args.address

        self.cdata_memory_mapper.map_cdata(
            args.ctype_name, args.cdata_name, address)


class PluginCDataMemoryMapper(FiiPlugin):
    NAME = 'plugin_c_data_memory_mapper'
    LOADING_PRIORITY = PLUGIN_PRIORITY_LEVEL_BUILTIN_L4
    REQUIREMENTS = [
        Requirement('emulator_address_space', AddressSpace),
        Requirement('emulator_arch', Architecture)]
    OPTIONAL_REQUIREMENTS = [Requirement('emulator_shell', EmulatorShell)]
    CONFIG_SCHEMA = {
        NAME: {
            'type': 'dict',
            'schema': {
                'ctypes_options': {'type': 'dict', 'default': {}},
                'ctypes_flavor': {
                    'type': 'string',
                    'allowed': ['pycparser', 'pycparserext_gnu'],
                    'default': 'pycparser'
                },
                'cdata_types_files': {
                    'type': 'list',
                    'schema': {'type': 'string'}, 'default': []
                },
                'cdata_mapping_files': {'type': 'list', 'default': []},
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
        arch = cast(Architecture, requirements['emulator_arch'])
        ctypes_arch = f'{arch.cpu_name}:{arch.endian}:{arch.mem_bit_size}'
        ctypes_options = plugin_config['ctypes_options']
        ctypes_flavor = CTYPES_TRANSLATOR_FLAVOR[plugin_config['ctypes_flavor']]

        ctypes_config = configure_ctypes(ctypes_arch, options=ctypes_options)
        ctt = CTypesTranslator(ctypes_config, ctypes_flavor)

        for cdata_type_file in plugin_config['cdata_types_files']:
            extra_cdata_types = ctt.translate_from_file(cdata_type_file)
            ctt.add_cdata_type(extra_cdata_types)

        cdata_mem_mapper = CDataMemMapper(
            requirements['emulator_address_space'], ctt.get_ctypes_config())

        for cdata_map_file in plugin_config['cdata_mapping_files']:
            cdata_mem_mapper.map_cdata_from_file(cdata_map_file)

        plugins_context.add('cdata_memory_mapper', cdata_mem_mapper)

        if emu_shell := optional_requirements.get('emulator_shell'):
            CDataMemMapperFrontend(
                cdata_mem_mapper, emu_shell,
                ADDRESS_FORMAT[arch.mem_bit_size])
