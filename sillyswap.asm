[BITS 32]

section .data
        msgPrompt db "VALUE_A is: %d. VALUE_B is: %d.", 0
        msgPrompt2 db "Performing swap now.", 0
        VALUE_A .long 1
        VALUE_B .long 2
        VALUE_C .long 0

section .text

main:
    mov ecx, msgPrompt


swap:
    LDR r1, VALUE_C
    LDR r2, VALUE_A
    LDR r3, VALUE_B
    MOV r1, r2
    MOV r2, r3
    MOV r3, r1
