[BITS 32]

section .data
        msgPrompt db "The first value on the stack is: %d. The next value is: %d.", 10, 0
        msgPrompt2 db "Performing swap now.", 10, 0
        VALUE_A dd 1            ;Will push solely to guarantee values
        VALUE_B dd 2

section .text
global main
extern printf

main:
        push ebp
        mov ebp, esp
        push dword [VALUE_B]
        push dword [VALUE_A]    ;Set VALUE_A on top with VALUE_B below it
        push msgPrompt
        call printf
        add esp, 4

        push msgPrompt2
        call printf
        add esp, 4

        pop ebx                 ;Move VALUE_A to ebx
        pop ecx                 ;Move VALUE_B to ecx
        push ebx                ;Put VALUE_A on the stack
        push ecx                ;Put VALUE_B on th stack, in reverse.
        push msgPrompt
        call printf
        add esp, 12

        mov esp, ebp
        pop ebp
        xor eax, eax
        ret