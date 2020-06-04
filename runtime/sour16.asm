; *****************************************************************************
; *****************************************************************************
;
;		Name:		sour16.asm
;		Purpose:	Sour16 is the XCPL Runtime
;					It borrows some ideas, not code, from Apple ][ Sweet 16.
;					(It is useless as a general purpose 16 bit VM)
;		Date: 		4th June 2020
;		Author:		Paul Robson (paul@robsons.org.uk)
;
; *****************************************************************************
; *****************************************************************************

		* = $00

Vars:	.fill 	16*2 						; registers in low/high byte pairs
pctr:	.fill 	2							; address of current routine.
temp0:	.fill 	2

; *****************************************************************************
;
;								Entry point
;
; *****************************************************************************

		* = 	$1000
Sour16Base:		 							; starts with jump to run code/
		jmp 	RunProgram
		nop

StartVector:								; +4 is the start of the Sour16 code.
		.word 	TestCode,0 					

		* = $10E0
MiscellaneousHandler:
		.word 	$ABCD

; *****************************************************************************
; *****************************************************************************
;
;				Main codes. These are at 16 byte intervals
;
; *****************************************************************************
; *****************************************************************************

		* = Sour16Base+$100

Sour16RootCommandSet:

; *****************************************************************************
;
;							Handle Miscellaneous Opcodes
;
; *****************************************************************************

Command_Miscellaneous:
		bra 	MiscellaneousHandler

; *****************************************************************************
;
;							Load Constant to Register
;
; *****************************************************************************

		.align 	16

Command_LoadConst:		;; LDI @,#
		lda 	(pctr),y 					; copy the first byte in
		sta 	Vars,X
		iny
		lda 	(pctr),y 					; copy the second byte in
		sta 	Vars+1,X
Command_IncYNext:		
		iny
		jmp 	Sour16Next

; *****************************************************************************
;
;							Add Constant to Register
;
; *****************************************************************************

		.align 	16

Command_AddConst:		;; ADI @,#
		clc
		lda 	(pctr),y 					; first calculation, LSB
		adc 	Vars,X
		sta 	Vars,X
		iny
		lda 	(pctr),y 					; second calculation, LSB
		adc 	Vars+1,X
		sta 	Vars+1,X
		bra 	Command_IncYNext			; co-opt the end of load const.

; *****************************************************************************
;
;						Add Next Register to Register
;
; *****************************************************************************

		.align 	16

Command_AddRegister:	;; ADD @
		clc
		lda 	Vars,x
		adc 	Vars+2,x
		sta		Vars,x
		lda 	Vars+1,x
		adc 	Vars+3,x
		sta		Vars+1,x
		jmp 	Sour16Next

; *****************************************************************************
;
;						Sub Next Register from Register
;
; *****************************************************************************

		.align 	16

Command_SubRegister:	;; SUB @
		sec
		lda 	Vars,x
		sbc 	Vars+2,x
		sta		Vars,x
		lda 	Vars+1,x
		sbc 	Vars+3,x
		sta		Vars+1,x
		jmp 	Sour16Next

; *****************************************************************************
;
;						And Next Register into Register
;
; *****************************************************************************

		.align 	16

Command_AndRegister:	;; AND @
		lda 	Vars,x
		and 	Vars+2,x
		sta		Vars,x
		lda 	Vars+1,x
		and 	Vars+3,x
		sta		Vars+1,x
		jmp 	Sour16Next

; *****************************************************************************
;
;						Or Next Register into Register
;
; *****************************************************************************

		.align 	16

Command_OrRegister:	;; ORR @
		lda 	Vars,x
		ora 	Vars+2,x
		sta		Vars,x
		lda 	Vars+1,x
		ora 	Vars+3,x
		sta		Vars+1,x
		jmp 	Sour16Next

; *****************************************************************************
;
;						Xor Next Register into Register
;
; *****************************************************************************

		.align 	16

Command_XorRegister:	;; XOR @
		lda 	Vars,x
		eor 	Vars+2,x
		sta		Vars,x
		lda 	Vars+1,x
		eor 	Vars+3,x
		sta		Vars+1,x
		jmp 	Sour16Next

; *****************************************************************************
;
;						Byte store indirect Rn.L -> (R0)
;
; *****************************************************************************

		.align 	16

Command_StoreByteInd:	;; SBI @
		lda 	Vars,x 						; value to write
		sta 	(Vars) 						; store indirect via R0.
		jmp 	Sour16Next

; *****************************************************************************
;
;								Load Word Indirect
;
; *****************************************************************************

		.align 	16

Command_LoadWordInd:	;; LWI @
		stx 	CLWI0+1 					; set to load high byte

		phy 								; load the high byte to variable
		ldy 	#1
CLWI0:		
		lda 	($00),y 					; read the high byte.
		tay 								; put it in Y temporarily.
		bra 	CLBIEntrance 				; and do the low code

; *****************************************************************************
;
;								Load Byte Indirect
;
; *****************************************************************************

		.align 	16

Command_LoadByteInd:	;; LBI @
		phy  								; save Y
		ldy 	#0 							; zero high byte value.
		;
		;		Entering here, Y contains the loaded MSB/zero and Y pos is stacked.
		;
CLBIEntrance:
		stx 	CLBI0+1 					; set to load low byte
CLBI0:
		lda 	($00) 						; read the low byte.
		sta 	Vars,x 						; save it into the variable.
		sty 	Vars+1,x
		ply 								; restore Y
		jmp 	Sour16Next

; *****************************************************************************
;
;							Shift Register by Register
;
; *****************************************************************************

		.align 	16

Command_Shift: 			;; SHF @
		lda 	Vars+2,x 					; the LSB of the second register
		beq 	Shift_None 					; no shift
		bmi 	Shift_Right 				; is a signed value - is shift right logical
		bra 	Shift_Left 					; + is shift left logical.
Shift_None:
		jmp 	Sour16Next

; *****************************************************************************
;
;							Load Direct
;
; *****************************************************************************

		.align 	16

Command_LoadWordDirect: ;; LDR @,#
		lda 	(pctr),y 					; copy address to temp0
		iny
		sta 	temp0
		lda 	(pctr),y
		iny
		sta 	temp0+1
		;
		lda 	(temp0) 					; read LSB
		sta 	Vars,x
		;
		phy 								; read MSB
		ldy 	#1
		lda 	(temp0),y
		sta 	Vars+1,x
		ply

		jmp 	Sour16Next

; *****************************************************************************
;
;						Store Indirect via R0 and advance by 2
;
; *****************************************************************************

		.align 	16

Command_StoreIndirectAdvance: ;; SIA @
		lda 	Vars,X 						; get LSB and write out
		sta 	(Vars) 						; to R0
		lda 	Vars+1,X 					; get MSB
		phy 								; save program pos
		ldy 	#1 							; write MSB
		sta 	(Vars),y
		ply 								; restore program position
		clc
		lda 	Vars 						; bump by 2
		adc 	#2
		sta 	Vars
		bcc 	CSIANoCarry 				; carry to MSB
		inc 	Vars+1
CSIANoCarry:		
		jmp 	Sour16Next

; *****************************************************************************
;
;								Register shift code
;
; *****************************************************************************

Shift_Left:									; so if A = 2 do 2 shift lefts
		asl 	Vars,x
		rol 	Vars+1,x
		dec 	a
		bne 	Shift_Left
		jmp 	Sour16Next

Shift_Right:								; so if A = -2, e.g. $FE do 2 shift rights
		lsr 	Vars+1,x
		ror 	Vars,x
		inc 	a
		bne 	Shift_Right
		jmp 	Sour16Next

; *****************************************************************************
;
;							Run main program
;
; *****************************************************************************

RunProgram:
		ldx 	#$FF 						; reset stack
		txs
		lda 	StartVector 				; load the initial program counter value.
		sta 	pctr
		lda 	StartVector+1
		sta 	pctr+1
		ldy 	#0

; *****************************************************************************
;
;					Return here to execute next command
;
; *****************************************************************************

Sour16Next:
		.byte 	$FF
		lda 	(pctr),y 					; get the opcode 
		iny 								; skip the opcode.
		tax 								; save in X
		and 	#$F0
		sta 	S16NJmp+1 					; modify the jump address
		txa 			 					; get the opcode back from X
		and 	#15 						; index into the register block.
		asl 	a 							; (reg# x 2) is also in A. 
		tax
S16NJmp:
		jmp 	Sour16RootCommandSet



; 	0x Miscellaneous
;			jsr ret tests and branches code caller

;	1x Load Constant
;	2x Add Constant
; 	3x Add Register
; 	4x Sub Register
; 	5x And Register
; 	6x Or Register
; 	7x Xor Register
;	8x Store byte indirect
; 	9x Load Word Indirect
; 	Ax Load Byte Indirect
; 	Bx Shift bidirectional.
; 	Cx Load Direct
;	Dx Unused (at present)
; 	Ex Store Word Indirect Advance 
;	Fx Unused (at present)

TODO:

Implement:
;	* Misc 
; 	* External Multiply, Divide, Negate.

TestCode:
		.byte 	$10,$E0,$10
		.byte 	$12,$34,$FE
		.byte 	$E2


; Expr returns : Reference, Calculated value, Constant (one only), Test Result.
; Code passes base address of registers in A.


