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

from typing import Dict
import logging
from datetime import datetime


class FiiLogger:
    def __init__(self):
        filename = datetime.now().strftime('log-%Y-%m-%d-%H-%M-%S.txt')
        logging.basicConfig(
            filename=filename, filemode='a', level=logging.INFO,
            format='%(asctime)s:%(msecs)03d : %(levelname)s : %(name)s '
                   ': %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger('FII.logger')
        self.logger.info('Logger activated.')

    @staticmethod
    def configure_loggers(loggers_level_config: Dict[str, str] = None):
        logger = logging.getLogger('FII.logger')

        if loggers_level_config is not None:
            for logger_name, level in loggers_level_config.items():
                if logger_name == 'FII' or logger_name.startswith('FII.'):
                    name = logger_name
                elif logger_name == 'root':
                    name = None
                else:
                    name = logger_name

                logger.info(f'set logging level to {level} for logger {name}.')
                logging.getLogger(name).setLevel(level)
