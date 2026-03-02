#  Assembler / Linker for the 16-bit Logisim CPU
#  Author : Alissa Tsay         │

import sys
from hf import int2bs, bs2hex   

_OPCODES = {
    'add' : '0000',  'and' : '0001',  'or'  : '0010',  'sub' : '0011',
    'addi': '1000',  'andi': '1001',  'ori' : '1010',  'subi': '1011',
    'lw'  : '1100',  'sw'  : '1101',  'beq' : '1110',  'j'   : '1111',
}


def REG(tok: str) -> str:
    """'$13' -> '1101' (4-bit register index)."""
    num = int(tok[1:])         
    return int2bs(str(num), 4)

def IMM4(tok: str) -> str:
    """Signed 4-bit immediate (two’s complement)."""
    return int2bs(tok, 4)

def ADDR(val) -> str:
    """12-bit absolute jump address."""
    return int2bs(str(int(val)), 12)


def _strip_comment(line: str) -> str:
    return line.split('#', 1)[0]

def _first_pass(lines):
    """Returns (cleaned_lines, label_table)."""
    labels, cleaned, pc = {}, [], 0
    for raw in lines:
        line = _strip_comment(raw).strip()
        if not line:
            continue
        if ':' in line:                       
            lbl, after = line.split(':', 1)
            labels[lbl.strip()] = pc
            line = after.strip()
            if not line:                     
                continue
        cleaned.append(line)
        pc += 1
    return cleaned, labels


def ConvertAssemblyToMachineCode(inline: str,
                                 labels: dict,
                                 pc: int) -> str:
    """
    Convert one cleaned assembly line to a 16-bit binary string.
    Called by AssemblyToHex during the second pass.
    """
    words = inline.replace(',', ' ').split()
    op = words[0].lower()
    if op not in _OPCODES:
        raise ValueError(f'Unknown opcode “{op}” at PC={pc}')

    t_bit, op3 = _OPCODES[op][0], _OPCODES[op][1:]

    if t_bit == '0':
        rd, rs, rt = REG(words[1]), REG(words[2]), REG(words[3])
        return t_bit + op3 + rs + rt + rd

    if op in ('addi', 'andi', 'ori', 'subi'):
        rd, rs, imm = REG(words[1]), REG(words[2]), IMM4(words[3])
        return t_bit + op3 + rs + imm + rd  
    
    if op in ('lw', 'sw'):
        rd, off_rs = REG(words[1]), words[2] 
        off, base  = off_rs.split('(')        
        rs = REG(base[:-1])
        return t_bit + op3 + rs + IMM4(off) + rd 

    if op == 'beq':
        rs, rt, tgt = REG(words[1]), REG(words[2]), words[3]
        offset = (labels[tgt] - (pc + 1)) if tgt in labels else int(tgt, 0)
        return t_bit + op3 + rs + IMM4(str(offset)) + rt

    if op == 'j':
        target = words[1]
        if target in labels:            
            dest = labels[target]
        else:
            try:                        
                dest = int(target, 0)
            except ValueError:
                raise ValueError(f'Undefined label “{target}” at line {pc}') from None
        return t_bit + op3 + ADDR(dest)


    raise ValueError(f'Unhandled instruction “{inline}”')


def AssemblyToHex(infilename: str, outfilename: str):
    """
    Two-pass translation: (1) build symbol table  (2) emit hex ROM image.
    """
    with open(infilename) as f:
        raw_lines = [l.rstrip('\n') for l in f]

    clean_lines, labels = _first_pass(raw_lines)

    hex_lines = []
    for pc, line in enumerate(clean_lines):
        binstr = ConvertAssemblyToMachineCode(line, labels, pc)
        hex_lines.append(bs2hex(binstr).zfill(4))

    with open(outfilename, "w") as out:
        out.write("v2.0 raw\n")         
        out.write("\n".join(hex_lines))
        out.write("\n")   

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('usage: python assemblerAT.py inputfile.asm outputfile.hex')
        sys.exit(1)

    infile, outfile = sys.argv[1], sys.argv[2]
    AssemblyToHex(infile, outfile)
