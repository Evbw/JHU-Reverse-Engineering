[BITS 32]

section .data
        msgPrompt db "VALUE_A is: %d. VALUE_B is: %d.", 10, 0
        msgPrompt2 db "Performing swap now.", 10, 0
        VALUE_A dd 1
        VALUE_B dd 2
        VALUE_C dd 0

section .text
global main
extern printf

main:
        push ebp
        mov ebp, esp
        push dword [VALUE_B]
        push dword [VALUE_A]
        push msgPrompt
        call printf
        add esp, 12

        push msgPrompt2
        call printf
        add esp, 4
        xor eax, eax
        ret

;swap:
;    LDR r1, VALUE_C
;    LDR r2, VALUE_A
;    LDR r3, VALUE_B
;    MOV r1, r2
;    MOV r2, r3
;    MOV r3, r1
