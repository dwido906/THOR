;
; FREYA OS BOOTLOADER
; Assembly bootloader for FREYA - The Protector OS
; Written in x86_64 assembly for UEFI and BIOS compatibility
;

[BITS 16]
[ORG 0x7C00]

; FREYA Boot Signature
freya_signature db 'FREYA', 0

; Boot entry point
boot_start:
    ; Clear interrupts
    cli
    
    ; Set up segments
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00
    
    ; Clear screen
    mov ah, 0x00
    mov al, 0x03
    int 0x10
    
    ; Print FREYA boot banner
    mov si, freya_boot_banner
    call print_string
    
    ; Check if CPU supports long mode (64-bit)
    call check_long_mode
    jc no_long_mode_error
    
    ; Load FREYA kernel
    mov si, loading_kernel_msg
    call print_string
    
    ; Load kernel from disk
    call load_freya_kernel
    jc kernel_load_error
    
    ; Switch to protected mode
    call enter_protected_mode
    
    ; Jump to FREYA kernel
    jmp 0x08:protected_mode_entry

; Print string function
print_string:
    pusha
.loop:
    lodsb
    cmp al, 0
    je .done
    mov ah, 0x0E
    mov bh, 0
    int 0x10
    jmp .loop
.done:
    popa
    ret

; Check for long mode support
check_long_mode:
    pushfd
    pop eax
    mov ecx, eax
    xor eax, 1 << 21
    push eax
    popfd
    pushfd
    pop eax
    push ecx
    popfd
    cmp eax, ecx
    je .no_cpuid
    
    ; Check for extended CPUID
    mov eax, 0x80000000
    cpuid
    cmp eax, 0x80000001
    jb .no_long_mode
    
    ; Check for long mode
    mov eax, 0x80000001
    cpuid
    test edx, 1 << 29
    jz .no_long_mode
    
    clc
    ret

.no_cpuid:
.no_long_mode:
    stc
    ret

; Load FREYA kernel from disk
load_freya_kernel:
    ; Reset disk system
    mov ah, 0x00
    mov dl, 0x80
    int 0x13
    jc .error
    
    ; Read kernel sectors
    mov ah, 0x02        ; Read sectors
    mov al, 32          ; Number of sectors to read
    mov ch, 0           ; Cylinder
    mov cl, 2           ; Sector (start from 2, after bootloader)
    mov dh, 0           ; Head
    mov dl, 0x80        ; Drive
    mov bx, 0x1000      ; Load address
    int 0x13
    jc .error
    
    clc
    ret

.error:
    stc
    ret

; Enter protected mode
enter_protected_mode:
    ; Load GDT
    lgdt [gdt_descriptor]
    
    ; Enable protected mode
    mov eax, cr0
    or eax, 1
    mov cr0, eax
    
    ret

; Protected mode entry point
[BITS 32]
protected_mode_entry:
    ; Set up protected mode segments
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov esp, 0x90000
    
    ; Clear screen in protected mode
    mov edi, 0xB8000
    mov ecx, 80 * 25
    mov ax, 0x0F20
    rep stosw
    
    ; Print protected mode message
    mov esi, protected_mode_msg
    mov edi, 0xB8000
    call print_string_pm
    
    ; Set up long mode (64-bit)
    call setup_long_mode
    
    ; Jump to FREYA kernel
    mov eax, 0x1000
    jmp eax

; Print string in protected mode
print_string_pm:
    mov ah, 0x0F
.loop:
    lodsb
    cmp al, 0
    je .done
    stosw
    jmp .loop
.done:
    ret

; Setup long mode
setup_long_mode:
    ; Create page tables for long mode
    ; This is simplified - real implementation would be more complex
    
    ; Identity map first 2MB
    mov edi, 0x70000    ; PML4 table
    mov ecx, 0x71000    ; PDPT
    or ecx, 3           ; Present + writable
    mov [edi], ecx
    
    mov edi, 0x71000    ; PDPT
    mov ecx, 0x72000    ; Page directory
    or ecx, 3
    mov [edi], ecx
    
    mov edi, 0x72000    ; Page directory
    mov ecx, 0x83       ; 2MB page, present + writable
    mov [edi], ecx
    
    ; Enable PAE
    mov eax, cr4
    or eax, 1 << 5
    mov cr4, eax
    
    ; Set PML4 table
    mov eax, 0x70000
    mov cr3, eax
    
    ; Enable long mode
    mov ecx, 0xC0000080
    rdmsr
    or eax, 1 << 8
    wrmsr
    
    ; Enable paging
    mov eax, cr0
    or eax, 1 << 31
    mov cr0, eax
    
    ret

; Error handlers
no_long_mode_error:
    mov si, no_long_mode_msg
    call print_string
    jmp halt

kernel_load_error:
    mov si, kernel_error_msg
    call print_string
    jmp halt

halt:
    cli
    hlt
    jmp halt

; Global Descriptor Table
gdt_start:
gdt_null:
    dq 0

gdt_code:
    dw 0xFFFF       ; Limit low
    dw 0x0000       ; Base low
    db 0x00         ; Base middle
    db 10011010b    ; Access byte
    db 11001111b    ; Granularity
    db 0x00         ; Base high

gdt_data:
    dw 0xFFFF
    dw 0x0000
    db 0x00
    db 10010010b
    db 11001111b
    db 0x00

gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

; Boot messages
freya_boot_banner:
    db 13, 10
    db '    ========================================', 13, 10
    db '    ||          FREYA OS BOOT           ||', 13, 10
    db '    ||        The Protector OS          ||', 13, 10
    db '    ||   AI-Powered Security System     ||', 13, 10
    db '    ========================================', 13, 10
    db 13, 10
    db '    Initializing FREYA bootloader...', 13, 10, 0

loading_kernel_msg:
    db '    Loading FREYA kernel...', 13, 10, 0

protected_mode_msg:
    db 'FREYA: Protected mode active', 0

no_long_mode_msg:
    db '    ERROR: CPU does not support 64-bit mode!', 13, 10
    db '    FREYA requires x86_64 processor.', 13, 10, 0

kernel_error_msg:
    db '    ERROR: Failed to load FREYA kernel!', 13, 10
    db '    Check disk and try again.', 13, 10, 0

; Boot sector signature
times 510-($-$$) db 0
dw 0xAA55
