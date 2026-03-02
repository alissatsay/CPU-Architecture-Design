
        lw   $1, 0($0)        # R1 = MEM[0]
        addi $2, $0, 3        # R2 = 3
loop:
        subi $1, $1, 1        # R1--
        beq  $1, $0, exit     # done if R1==0
        sw   $1, 0($0)        # MEM[0] = R1
        j    loop
exit:
        sw   $2, 1($0)        # MEM[1] = 3
        add  $0, $0, $0       # NOP – halt
