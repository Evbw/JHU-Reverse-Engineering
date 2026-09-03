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
        mov eax, [VALUE_A]
        mov ecx, [VALUE_B]
        mov [VALUE_A], ecx
        mov [VALUE_B], eax
        push dword [VALUE_B]
        push dword [VALUE_A]
        push msgPrompt
        call printf
        add esp, 12

        xor ebx, ebx
        int 0x80