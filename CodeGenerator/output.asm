.data
newline: .asciiz "\n"
i: .word 0
j: .word 0
num: .word 0
a: .space 80


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
    # Allocate space for 1 local variables
    subu $sp, $sp, 4
    # Save parameter num
    sw $a0, -8($fp)
    li $t0, 1
    # assign value to i
    sw $t0, -12($fp)
L0:
    # local var i
    lw $t0, -12($fp)
    move $t2, $t0
    # local var num
    lw $t0, -8($fp)
    slt $t0, $t2, $t0
    beqz $t0, L1
    # local var num
    lw $t0, -8($fp)
    move $t4, $t0
    # local var i
    lw $t0, -12($fp)
    sub $t0, $t4, $t0
    move $t4, $t0
    li $t0, 1
    add $t0, $t4, $t0
    # assign value to j
    sw $t0, -16($fp)
    li $t0, 1
    # assign value to k
    sw $t0, -20($fp)
L2:
    # local var k
    lw $t0, -20($fp)
    move $t2, $t0
    # local var j
    lw $t0, -16($fp)
    slt $t0, $t2, $t0
    beqz $t0, L3
    # local var k
    lw $t0, -20($fp)
    move $t4, $t0
    li $t0, 1
    add $t0, $t4, $t0
    move $t3, $t0
    addi $t3, $t3, -1
    sll $t3, $t3, 2
    la $t1, a
    add $t1, $t1, $t3
    lw $t0, 0($t1)
    move $t2, $t0
    # local var k
    lw $t0, -20($fp)
    move $t3, $t0
    addi $t3, $t3, -1
    sll $t3, $t3, 2
    la $t1, a
    add $t1, $t1, $t3
    lw $t0, 0($t1)
    slt $t0, $t2, $t0
    beqz $t0, L4
    # local var k
    lw $t0, -20($fp)
    move $t3, $t0
    addi $t3, $t3, -1
    sll $t3, $t3, 2
    la $t1, a
    add $t1, $t1, $t3
    lw $t0, 0($t1)
    # assign value to t
    sw $t0, -24($fp)
    # local var k
    lw $t0, -20($fp)
    move $t3, $t0
    addi $t3, $t3, -1
    sll $t3, $t3, 2
    la $t1, a
    add $t1, $t1, $t3
    move $s0, $t1
    # local var k
    lw $t0, -20($fp)
    move $t4, $t0
    li $t0, 1
    add $t0, $t4, $t0
    move $t3, $t0
    addi $t3, $t3, -1
    sll $t3, $t3, 2
    la $t1, a
    add $t1, $t1, $t3
    lw $t0, 0($t1)
    # assign value to a[index]
    sw $t0, 0($s0)
    # local var k
    lw $t0, -20($fp)
    move $t4, $t0
    li $t0, 1
    add $t0, $t4, $t0
    move $t3, $t0
    addi $t3, $t3, -1
    sll $t3, $t3, 2
    la $t1, a
    add $t1, $t1, $t3
    move $s0, $t1
    # local var t
    lw $t0, -24($fp)
    # assign value to a[index]
    sw $t0, 0($s0)
    j L5
L4:
    li $t0, 0
    # assign value to t
    sw $t0, -24($fp)
L5:
    # local var k
    lw $t0, -20($fp)
    move $t4, $t0
    li $t0, 1
    add $t0, $t4, $t0
    # assign value to k
    sw $t0, -20($fp)
    j L2
L3:
    # local var i
    lw $t0, -12($fp)
    move $t4, $t0
    li $t0, 1
    add $t0, $t4, $t0
    # assign value to i
    sw $t0, -12($fp)
    j L0
L1:
    # Procedure exit
    move $sp, $fp
    lw $fp, 4($sp)
    lw $ra, 0($sp)
    addu $sp, $sp, 8
    jr $ra
main:
    # Setup stack frame
    subu $sp, $sp, 4
    sw $ra, 0($sp)  # Save return address
    # Read integer input
    li $v0, 5
    syscall
    sw $v0, num
    li $t0, 1
    # assign value to i
    sw $t0, i
L6:
    lw $t0, i
    move $t2, $t0
    lw $t0, num
    move $t4, $t0
    li $t0, 1
    add $t0, $t4, $t0
    slt $t0, $t2, $t0
    beqz $t0, L7
    # Read integer input
    li $v0, 5
    syscall
    sw $v0, j
    lw $t0, i
    move $t3, $t0
    addi $t3, $t3, -1
    sll $t3, $t3, 2
    la $t1, a
    add $t1, $t1, $t3
    move $s0, $t1
    lw $t0, j
    # assign value to a[index]
    sw $t0, 0($s0)
    lw $t0, i
    move $t4, $t0
    li $t0, 1
    add $t0, $t4, $t0
    # assign value to i
    sw $t0, i
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
    li $t0, 1
    # assign value to i
    sw $t0, i
L8:
    lw $t0, i
    move $t2, $t0
    lw $t0, num
    move $t4, $t0
    li $t0, 1
    add $t0, $t4, $t0
    slt $t0, $t2, $t0
    beqz $t0, L9
    lw $t0, i
    move $t3, $t0
    addi $t3, $t3, -1
    sll $t3, $t3, 2
    la $t1, a
    add $t1, $t1, $t3
    lw $t0, 0($t1)
    # Write integer output
    move $a0, $t0
    li $v0, 1
    syscall
    la $a0, newline
    li $v0, 4
    syscall
    lw $t0, i
    move $t4, $t0
    li $t0, 1
    add $t0, $t4, $t0
    # assign value to i
    sw $t0, i
    j L8
L9:
    # Program exit
    lw $ra, 0($sp)  # Restore return address
    addu $sp, $sp, 4
    li $v0, 10
    syscall
