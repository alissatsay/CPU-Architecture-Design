# 16-bit Logisim CPU - Assembler / Linker
Author – Alissa Tsay*  
This Python assembler converts a assembly language for a custom 16-bit
Logisim CPU into a loadable ROM image (.hex).
* **Input** — *.asm* file with labels & comments  
* **Output** — *.hex* file accepted by Logisim
* **ISA** — 12 instructions, 8-bit data path, 16-bit fixed-length words  
## 1 · Instruction format
| Assembly line (syntax)                                     | 16-bit Instruction Word layout |
|------------------------------------------------------------|--------------------------------|
| **add/and/or/sub $rd, $rs, $rt** | **ri + opcode**&nbsp;(4) &#124; **$rs**&nbsp;(4) &#124; **$rt**&nbsp;(4) &#124; **$rd**&nbsp;(4) |
| **addi/andi/ori/subi $rd, $rs, imm** | **ri + opcode** &#124; **$rs** &#124; **imm** &#124; **$rd** |
| **lw/sw $rd, imm4($rs)**               | **ri + opcode** &#124; **$rs** &#124; **imm** &#124; **$rd** |
| **beq $rs, $rt, imm**               | **ri + opcode** &#124; **$rs** &#124; **imm4** &#124; **$rt** |
| **j label/imm**               | **ri + opcode** &#124; **absolute address** |

### Opcode map

| Mnemonic | ri + opcode | Encoded fields (11-0) |
|----------|-------------|-----------------------|
| add  rd, rs, rt | 0000 | rs rt rd |
| and  rd, rs, rt | 0001 | rs rt rd |
| or   rd, rs, rt | 0010 | rs rt rd |
| sub  rd, rs, rt | 0011 | rs rt rd |
| addi rd, rs, imm | 1000 | rs imm rd |
| andi rd, rs, imm | 1001 | rs imm rd |
| ori  rd, rs, imm | 1010 | rs imm rd |
| subi rd, rs, imm | 1011 | rs imm rd |
| lw   rd, imm4(rs) | 1100 | rs imm rd |
| sw   rd, imm4(rs) | 1101 | rs imm rd |
| beq  rs, rt, off | 1110 | rs off rt |
| j    addr/label   | 1111 | 12-bit absolute address |

**imm** range = −8 … +7.

## 2 Assembly syntax

```asm
# comment lines start with '#'

main:   addi $1, $0, 7      # rd, rs, imm
        sw   $1, 0($0)
        j    main

### Quick Reference

* Registers: `$0` … `$15`  
* Labels: end with `:` (case-sensitive)  
* Immediates: decimal (`-3`, `42`) or hex (`0x2A`)

```

### 3 Assembler Algorithm

**Pass 1:**  Strip comments, collect labels
**Pass 2:**  For each instruction: parse => encode 16-bit binary =>`bs2hex` => hex list 
The script writes "v2.0 raw" to the top of every output file so Logisim accepts it directly.

### 4 Usage
Navigate to the testing.py file. Run the tests.

### 6 · File Overview
| File                   | Purpose                                                         |
|------------------------|-----------------------------------------------------------------|
| assemblerAT.py | Finished assembler / linker                                    |
| hf.py                | Helper functions `int2bs` (int to binary string) and `bs2hex`    |
| testing.py                | file with the code for all testing cases    |
| test_files                | asm and hex test files    |
| README.md            |                                                     |