#!/bin/bash

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

# IPY_TEST_SIMPLE_PROMPT=1 Force IPython to use input than readline.
IPY_TEST_SIMPLE_PROMPT=1 pytest \
  --cov-report html \
  --cov="FII.core" \
  --cov="FII.unicorn" \
  --cov="FII.plugins" \
  -s -v "${@}"

rm -rf .pytest_cache
