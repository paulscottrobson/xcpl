; *****************************************************************************
; *****************************************************************************
;
;		Name:		sourcore.asm
;		Purpose:	Main command decoder and execution for Sour16
;					(not Miscellaneous functions, though decoded here)
;		Date: 		4th June 2020
;		Author:		Paul Robson (paul@robsons.org.uk)
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
		lda 	(pctr) 						; copy the first byte in
		sta 	Vars,X
		ldy 	#1
		lda 	(pctr),y 					; copy the second byte in
		sta 	Vars+1,X
		jmp 	Sour16NextSkip2 			; return skipping 2.

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
CLWI0:		
		ldy 	#1
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
		lda 	(pctr) 						; copy address to temp0
		sta 	temp0
		ldy 	#1
		lda 	(pctr),y
		sta 	temp0+1
		;
		lda 	(temp0) 					; read LSB
		sta 	Vars,x
		;
		lda 	(temp0),y 					; read and save MSB
		sta 	Vars+1,x
		;
		jmp 	Sour16NextSkip2

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
		ldy 	#1 							; write MSB
		sta 	(Vars),y
		clc
		lda 	Vars 						; bump by 2
		adc 	#2
		sta 	Vars
		bcc 	CSIANoCarry 				; carry to MSB
		inc 	Vars+1
CSIANoCarry:		
		jmp 	Sour16NextSkip2

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


