/*

 Copyright 2022-2025 Vincent Dary

 This file is part of FII.

 FII is free software: you can redistribute it and/or modify it under the terms
 of the GNU General Public License as published by the Free Software Foundation,
 either version 3 of the License, or (at your option) any later version.

 FII is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY
 ; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
 PARTICULAR PURPOSE. See the GNU General Public License for more details.

 You should have received a copy of the GNU General Public License along with
 FII. If not, see <https://www.gnu.org/licenses/>.

*/

.global __main__

.equ emu_start, __main__
.equ unmapped_addr, 0x00ff0000

__main__:
    mov r1, #0
    ldr r0, =unmapped_addr
    str r1, [r0]
emu_end:
    mov r0, r0
