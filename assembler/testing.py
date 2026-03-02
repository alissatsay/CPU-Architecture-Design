## This file contains all of the tests I ran on my assembler. 

from assemblerAT import AssemblyToHex

AssemblyToHex("test_files/test1.asm", "test_files/test1.hex")
AssemblyToHex("test_files/test2.asm", "test_files/test2.hex")
AssemblyToHex("test_files/Basic-LW-SW-rev.asm", "test_files/Basic-LW-SW-rev.hex")
AssemblyToHex("test_files/Basic-R-Type-rev2.asm", "test_files/Basic-R-Type-rev2.hex")
AssemblyToHex("test_files/testbranch.asm", "test_files/testbranch.hex")
AssemblyToHex("test_files/testjump-absolute.asm", "test_files/testjump-absolute.hex")