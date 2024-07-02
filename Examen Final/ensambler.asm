.data
    msg1:    .asciiz "El número es menor que 10
"
    msg2:    .asciiz "El número es mayor o igual que 10
"
    msg3:    .asciiz "El número no es mayor que 0
"
    sumResult: .asciiz "Resultado de suma: "
    newLine: .asciiz "
"
    hola: .asciiz "HOLA
"

.text
.globl main

main:
    li $t0, 5
    li $t1, 6

    move $a0, $t0
    move $a1, $t1
    jal suma
    move $s0, $v0

    li $v0, 4
    la $a0, sumResult
    syscall

    li $v0, 1
    move $a0, $s0
    syscall

    li $v0, 4
    la $a0, newLine
    syscall

    la $a0, hola
    syscall

    move $a0, $s0
    jal verificar_numero

    li $t2, 1
loop:
    li $v0, 1
    move $a0, $t2
    syscall

    li $v0, 4
    la $a0, newLine
    syscall

    addi $t2, $t2, 1
    bne $t2, 6, loop

    li $v0, 10
    syscall

suma:
    add $v0, $a0, $a1
    jr $ra

verificar_numero:
    li $t0, 5
    move $a0, $t0
    bgtz $a0, verificar_menor
    j menor_cero

verificar_menor:
    li $t3, 10
    blt $a0, $t3, menor_que
    j mayor_que

menor_que:
    li $v0, 4
    la $a0, msg1
    syscall
    j end_if

mayor_que:
    li $v0, 4
    la $a0, msg2
    syscall
    j end_if

menor_cero:
    li $v0, 4
    la $a0, msg3
    syscall

end_if:
    jr $ra
