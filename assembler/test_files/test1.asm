
start:
    add  $1, $0, $0      # R1 = 0
    addi $1, $1, 5       # R1 = 5
    andi $2, $1, 3       # R2 = 1
    ori  $3, $2, 8       # R3 = 9
    subi $4, $3, 2       # R4 = 7
    j    done            # skip the next add
nop_label:
    add  $5, $5, $5      # (never executed)
done:
    add  $0, $0, $0      # NOP
