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

import logging

import pytest

from .fixtures.fixture_utils import temp_named_txt_file

from FII.core.logger import FiiLogger


def test_FII_logger_active_level(caplog):
    caplog.set_level(logging.INFO)
    FiiLogger.configure_loggers({'FII.tests': 'INFO'})
    logging.getLogger('FII.tests').info('test log msg')
    assert caplog.record_tuples[-1] == ('FII.tests', logging.INFO,
                                        'test log msg')


def test_FII_logger_deactivate_level(caplog):
    caplog.set_level(logging.INFO)
    FiiLogger.configure_loggers({'FII.tests': 'ERROR'})
    logging.getLogger('FII.tests').info('test log msg')
    for log in caplog.record_tuples:
        assert log[0] != 'FII.tests'
