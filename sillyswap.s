.text

main:
    LDR r0, =prompt
	BL printf
    LDR r0, =prompt2
	BL printf
    BLE swap
    LDR r0, =ouput
	BL printf
    
swap:
    LDR r1, VALUE_C
    LDR r2, VALUE_A
    LDR r3, VALUE_B
    MOV r1, r2
    MOV r2, r3
    MOV r3, r1
    
data:

    prompt: .asciz "VALUE_A is: %d. VALUE_B is: %d.\n\n"
    prompt2: .asciz "Performing swap now.\n\n"
    VALUE_A: .word 1
    VALUE_B: .word 2
    VALUE_C: .word 0
    output: .asciz "VALUE_A is: %d. VALUE_B is: %d.\n\n"