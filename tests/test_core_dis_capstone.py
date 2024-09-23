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

from FII.core.dis_capstone import DisassemblerCapstone

from .fixtures.blobs import BlobArmEl32IncLoop
from .fixtures.fixture_utils import get_file_content


def test_disassembler_capstone_disassemble_mem_range():
    expected_listing = get_file_content(
        'outputs/dis_capstone_arm_el_32_inc_loop.txt').split('\n')
    dis = DisassemblerCapstone('arm:el:32:default')

    assert expected_listing == \
           dis.disassemble_mem_range(
               BlobArmEl32IncLoop.mapped_blobs[0]['blob'], 0x0, 0x18)
