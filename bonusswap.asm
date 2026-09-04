[BITS 32]

section .data
        VALUE_A dd 1            ;I gotta have something!
        VALUE_B dd 2

section .text
global main

main:
        xchg eax, [VALUE_A]
        xchg eax, [VALUE_B]
        xchg eax, [VALUE_A]
        ret
