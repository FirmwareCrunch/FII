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

from typing import Union
import sys
import argparse
from importlib import metadata

from FII.core.logger import FiiLogger
from FII.core.plugin import PluginManager
from FII.frontend.jupyter.jupyter_console import jupyter_console


SUB_PARSER_EMU = 'emu'
SUB_PARSER_JUPITER_CONSOLE = 'jupiter-console'


def fii_emu(config: str, extra_plugin_path: Union[str, None] = None) -> None:
    FiiLogger()
    plugin_loader = PluginManager()
    plugin_loader.load_plugin_by_config_file(
        config, ([extra_plugin_path] if extra_plugin_path else []))

    if plugin_loader.plugins_context.program_entry:
        plugin_loader.plugins_context.program_entry()

    sys.exit(0)


def main() -> None:
    meta = metadata.metadata('FII')

    parser = argparse.ArgumentParser(
        prog=f'FII',
        description=f'Version {meta["Version"]} - {meta["Summary"]}',
        epilog='Emulation Framework for Firmware Analysis'
    )

    subparsers = parser.add_subparsers(required=True, dest='fii_subparser')

    ###################################
    # subparser emu
    ###################################
    parser_emu = subparsers.add_parser(
        SUB_PARSER_EMU, help='Run a FII emulation environment.')
    parser_emu.add_argument(
        '--config', required=True, help='YAML/JSON configuration file.')
    parser_emu.add_argument(
        '--extra-plugin-path', required=False, help='Extra plugin directory',
        default=None)

    ###################################
    # subparser jupiter-console
    ###################################
    parser_jupiter_console = subparsers.add_parser(
        SUB_PARSER_JUPITER_CONSOLE,
        help=(
            'Run and connect a Jupiter Console to a FII remote IPykernel. '
            'To work the remote FII instance must setup a '
            '"plugin_emulator_shell" with the "remote_ipykernel" option set to'
            ' true, and a "plugin_backend".'))
    parser_jupiter_console.add_argument(
        '--backend-ip', required=True, help='FII backend IP address.')
    parser_jupiter_console.add_argument(
        '--backend-port', required=True, help='FII backend port number.')

    ###################################
    # parsing
    ###################################
    script_args = parser.parse_args()

    if script_args.fii_subparser == SUB_PARSER_EMU:
        fii_emu(script_args.config, script_args.extra_plugin_path)
    elif script_args.fii_subparser == SUB_PARSER_JUPITER_CONSOLE:
        jupyter_console(script_args.backend_ip, script_args.backend_port)


if __name__ == '__main__':
    main()
