.data
newline: .asciiz "\n"
z: .word 0
x: .word 0
num: .word 0
a: .word 0


.text
.globl main
# Entry point
j main
# Program: bubble
q:
    # Setup stack frame
    subu $sp, $sp, 8
    sw $ra, 0($sp)  # Save return address
    sw $fp, 4($sp)  # Save frame pointer
    move $fp, $sp   # Setup new frame pointer
    lw $t0, i
    li $t0, 1
    sw $t0, i
L0:
    lw $t0, i
    move $t2, $t0
    lw $t0, num
    slt $t0, $t2, $t0
    beqz $t0, L1
    lw $t0, j
    lw $t0, num
    move $t2, $t0
    lw $t0, i
    sub $t0, $t2, $t0
    move $t2, $t0
    li $t0, 1
    add $t0, $t2, $t0
    sw $t0, j
    lw $t0, k
    li $t0, 1
    sw $t0, k
L2:
    lw $t0, k
    move $t2, $t0
    lw $t0, j
    slt $t0, $t2, $t0
    beqz $t0, L3
    # Global array access a[...]
    la $t1, a
    lw $t0, k
    move $t2, $t0
    li $t0, 1
    add $t0, $t2, $t0
    sll $t0, $t0, 2
    add $t1, $t1, $t0
    lw $t0, 0($t1)
    move $t2, $t0
    # Global array access a[...]
    la $t1, a
    lw $t0, k
    sll $t0, $t0, 2
    add $t1, $t1, $t0
    lw $t0, 0($t1)
    slt $t0, $t2, $t0
    beqz $t0, L4
    lw $t0, t
    # Global array access a[...]
    la $t1, a
    lw $t0, k
    sll $t0, $t0, 2
    add $t1, $t1, $t0
    lw $t0, 0($t1)
    sw $t0, t
    # Global array access a[...]
    la $t1, a
    lw $t0, k
    sll $t0, $t0, 2
    add $t1, $t1, $t0
    lw $t0, 0($t1)
    # Global array access a[...]
    la $t1, a
    lw $t0, k
    move $t2, $t0
    li $t0, 1
    add $t0, $t2, $t0
    sll $t0, $t0, 2
    add $t1, $t1, $t0
    lw $t0, 0($t1)
    sw $t0, a
    # Global array access a[...]
    la $t1, a
    lw $t0, k
    move $t2, $t0
    li $t0, 1
    add $t0, $t2, $t0
    sll $t0, $t0, 2
    add $t1, $t1, $t0
    lw $t0, 0($t1)
    lw $t0, t
    sw $t0, a
    j L5
L4:
    lw $t0, t
    li $t0, 0
    sw $t0, t
L5:
    lw $t0, k
    lw $t0, k
    move $t2, $t0
    li $t0, 1
    add $t0, $t2, $t0
    sw $t0, k
    j L2
L3:
    lw $t0, i
    lw $t0, i
    move $t2, $t0
    li $t0, 1
    add $t0, $t2, $t0
    sw $t0, i
    j L0
L1:
    # Procedure exit
    move $sp, $fp   # Restore stack pointer
    lw $fp, 4($sp)  # Restore frame pointer
    lw $ra, 0($sp)  # Restore return address
    addu $sp, $sp, 8
    jr $ra          # Return to caller
main:
    # Setup stack frame
    subu $sp, $sp, 4
    sw $ra, 0($sp)  # Save return address
    # Read integer input
    li $v0, 5
    syscall
    sw $v0, num
    lw $t0, z
    li $t0, 1
    sw $t0, z
L6:
    lw $t0, z
    move $t2, $t0
    lw $t0, num
    slt $t0, $t2, $t0
    beqz $t0, L7
    # Read integer input
    li $v0, 5
    syscall
    sw $v0, x
    # Global array access a[...]
    la $t1, a
    lw $t0, z
    sll $t0, $t0, 2
    add $t1, $t1, $t0
    lw $t0, 0($t1)
    lw $t0, x
    sw $t0, a
    lw $t0, z
    lw $t0, z
    move $t2, $t0
    li $t0, 1
    add $t0, $t2, $t0
    sw $t0, z
    j L6
L7:
    # Call to procedure q
    # Save temporary registers
    subu $sp, $sp, 40
    sw $t0, 0($sp)
    sw $t1, 4($sp)
    sw $t2, 8($sp)
    sw $t3, 12($sp)
    sw $t4, 16($sp)
    sw $t5, 20($sp)
    sw $t6, 24($sp)
    sw $t7, 28($sp)
    sw $t8, 32($sp)
    sw $t9, 36($sp)
    lw $t0, num
    move $a0, $t0
    jal q
    # Restore temporary registers
    lw $t0, 0($sp)
    lw $t1, 4($sp)
    lw $t2, 8($sp)
    lw $t3, 12($sp)
    lw $t4, 16($sp)
    lw $t5, 20($sp)
    lw $t6, 24($sp)
    lw $t7, 28($sp)
    lw $t8, 32($sp)
    lw $t9, 36($sp)
    addu $sp, $sp, 40
    lw $t0, z
    li $t0, 1
    sw $t0, z
L8:
    lw $t0, z
    move $t2, $t0
    lw $t0, num
    slt $t0, $t2, $t0
    beqz $t0, L9
    # Global array access a[...]
    la $t1, a
    lw $t0, z
    sll $t0, $t0, 2
    add $t1, $t1, $t0
    lw $t0, 0($t1)
    # Write integer output
    move $a0, $t0
    li $v0, 1
    syscall
    la $a0, newline
    li $v0, 4
    syscall
    lw $t0, z
    lw $t0, z
    move $t2, $t0
    li $t0, 1
    add $t0, $t2, $t0
    sw $t0, z
    j L8
L9:
    # Program exit
    lw $ra, 0($sp)  # Restore return address
    addu $sp, $sp, 4
    li $v0, 10
    syscall
