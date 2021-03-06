class INSTR(object):
    def __init__(self, opcode, name, func):
        self.opcode = opcode
        self.name = name
        self.func = fun

def ld_imm(cpu, dst):
    cpu.regs[dst].set(cpu.read(cpu.regs["PC"].get()+1))
    cpu.regs["PC"].set(cpu.regs["PC"].get() + 2)
    return 8

def ld_reg(cpu, dst, src):
    cpu.regs[dst].set(cpu.regs[src].get())
    cpu.regs["PC"].set(cpu.regs["PC"].get() + 2)
    return 4 if src.size == 8 and dst.size == 8 else 8

ops = [
    INSTR(0x00, "", lambda dst, src: None),
    INSTR(0x01, "", lambda dst, src: None),
    INSTR(0x02, "", lambda dst, src: None),
    INSTR(0x03, "", lambda dst, src: None),
    INSTR(0x04, "", lambda dst, src: None),
    INSTR(0x05, "", lambda dst, src: None),
    INSTR(0x06, "LD B, imm", lambda cpu: ld_imm(cpu, "B")),
    INSTR(0x07, "", lambda dst, src: None),
    INSTR(0x08, "", lambda dst, src: None),
    INSTR(0x09, "", lambda dst, src: None),
    INSTR(0x0a, "LD A, BC", lambda cpu: ld_reg(cpu, "A", "BC")),
    INSTR(0x0b, "", lambda dst, src: None),
    INSTR(0x0c, "", lambda dst, src: None),
    INSTR(0x0d, "", lambda dst, src: None),
    INSTR(0x0e, "LD C, imm", lambda cpu: ld_imm(cpu, "C")),
    INSTR(0x0f, "", lambda dst, src: None),
    INSTR(0x10, "", lambda dst, src: None),
    INSTR(0x11, "", lambda dst, src: None),
    INSTR(0x12, "", lambda dst, src: None),
    INSTR(0x13, "", lambda dst, src: None),
    INSTR(0x14, "", lambda dst, src: None),
    INSTR(0x15, "", lambda dst, src: None),
    INSTR(0x16, "LD D, imm", lambda cpu: ld_imm(cpu, "D")),
    INSTR(0x17, "", lambda dst, src: None),
    INSTR(0x18, "", lambda dst, src: None),
    INSTR(0x19, "", lambda dst, src: None),
    INSTR(0x1a, "LD A, DE", lambda cpu: ld_reg(cpu, "A", "DE")),
    INSTR(0x1b, "", lambda dst, src: None),
    INSTR(0x1c, "", lambda dst, src: None),
    INSTR(0x1d, "", lambda dst, src: None),
    INSTR(0x1e, "LD E, imm", lambda cpu: ld_imm(cpu, "E")),
    INSTR(0x1f, "", lambda dst, src: None),
    INSTR(0x20, "", lambda dst, src: None),
    INSTR(0x21, "", lambda dst, src: None),
    INSTR(0x22, "", lambda dst, src: None),
    INSTR(0x23, "", lambda dst, src: None),
    INSTR(0x24, "", lambda dst, src: None),
    INSTR(0x25, "", lambda dst, src: None),
    INSTR(0x26, "LD H, imm", lambda cpu: ld_imm(cpu, "H")),
    INSTR(0x27, "", lambda dst, src: None),
    INSTR(0x28, "", lambda dst, src: None),
    INSTR(0x29, "", lambda dst, src: None),
    INSTR(0x2a, "", lambda dst, src: None),
    INSTR(0x2b, "", lambda dst, src: None),
    INSTR(0x2c, "", lambda dst, src: None),
    INSTR(0x2d, "", lambda dst, src: None),
    INSTR(0x2e, "LD L, imm", lambda cpu: ld_imm(cpu, "L")),
    INSTR(0x2f, "", lambda dst, src: None),
    INSTR(0x30, "", lambda dst, src: None),
    INSTR(0x31, "", lambda dst, src: None),
    INSTR(0x32, "", lambda dst, src: None),
    INSTR(0x33, "", lambda dst, src: None),
    INSTR(0x34, "", lambda dst, src: None),
    INSTR(0x35, "", lambda dst, src: None),
    INSTR(0x36, "", lambda dst, src: None),
    INSTR(0x37, "", lambda dst, src: None),
    INSTR(0x38, "", lambda dst, src: None),
    INSTR(0x39, "", lambda dst, src: None),
    INSTR(0x3a, "", lambda dst, src: None),
    INSTR(0x3b, "", lambda dst, src: None),
    INSTR(0x3c, "", lambda dst, src: None),
    INSTR(0x3d, "", lambda dst, src: None),
    INSTR(0x3e, "", lambda dst, src: None),
    INSTR(0x3f, "", lambda dst, src: None),
    INSTR(0x40, "LD B, B", lambda cpu: ld_reg(cpu, "B", "B")),
    INSTR(0x41, "LD B, C", lambda cpu: ld_reg(cpu, "B", "C")),
    INSTR(0x42, "LD B, D", lambda cpu: ld_reg(cpu, "B", "D")),
    INSTR(0x43, "LD B, E", lambda cpu: ld_reg(cpu, "B", "E")),
    INSTR(0x44, "LD B, H", lambda cpu: ld_reg(cpu, "B", "H")),
    INSTR(0x45, "LD B, L", lambda cpu: ld_reg(cpu, "B", "L")),
    INSTR(0x46, "LD B, HL", lambda cpu: ld_reg(cpu, "B", "HL")),
    INSTR(0x47, "LD B, A", lambda cpu: ld_reg(cpu, "B", "A")),
    INSTR(0x48, "LD C, B", lambda cpu: ld_reg(cpu, "C", "B")),
    INSTR(0x49, "LD C, C", lambda cpu: ld_reg(cpu, "C", "C")),
    INSTR(0x4a, "LD C, D", lambda cpu: ld_reg(cpu, "C", "D")),
    INSTR(0x4b, "LD C, E", lambda cpu: ld_reg(cpu, "C", "E")),
    INSTR(0x4c, "LD C, H", lambda cpu: ld_reg(cpu, "C", "H")),
    INSTR(0x4d, "LD C, L", lambda cpu: ld_reg(cpu, "C", "L")),
    INSTR(0x4e, "LD C, HL", lambda cpu: ld_reg(cpu, "C", "HL")),
    INSTR(0x4f, "LD C, A", lambda cpu: ld_reg(cpu, "C", "A")),
    INSTR(0x50, "LD D, B", lambda cpu: ld_reg(cpu, "D", "B")),
    INSTR(0x51, "LD D, C", lambda cpu: ld_reg(cpu, "D", "C")),
    INSTR(0x52, "LD D, D", lambda cpu: ld_reg(cpu, "D", "D")),
    INSTR(0x53, "LD D, E", lambda cpu: ld_reg(cpu, "D", "E")),
    INSTR(0x54, "LD D, H", lambda cpu: ld_reg(cpu, "D", "H")),
    INSTR(0x55, "LD D, L", lambda cpu: ld_reg(cpu, "D", "L")),
    INSTR(0x56, "LD D, HL", lambda cpu: ld_reg(cpu, "D", "HL")),
    INSTR(0x57, "LD D, A", lambda cpu: ld_reg(cpu, "D", "A")),
    INSTR(0x58, "LD E, B", lambda cpu: ld_reg(cpu, "E", "B")),
    INSTR(0x59, "LD E, C", lambda cpu: ld_reg(cpu, "E", "C")),
    INSTR(0x5a, "LD E, D", lambda cpu: ld_reg(cpu, "E", "D")),
    INSTR(0x5b, "LD E, E", lambda cpu: ld_reg(cpu, "E", "E")),
    INSTR(0x5c, "LD E, H", lambda cpu: ld_reg(cpu, "E", "H")),
    INSTR(0x5d, "LD E, L", lambda cpu: ld_reg(cpu, "E", "L")),
    INSTR(0x5e, "LD E, HL", lambda cpu: ld_reg(cpu, "E", "HL")),
    INSTR(0x5f, "LD E, A", lambda cpu: ld_reg(cpu, "E", "A")),
    INSTR(0x60, "LD H, B", lambda cpu: ld_reg(cpu, "H", "B")),
    INSTR(0x61, "LD H, C", lambda cpu: ld_reg(cpu, "H", "C")),
    INSTR(0x62, "LD H, D", lambda cpu: ld_reg(cpu, "H", "D")),
    INSTR(0x63, "LD H, E", lambda cpu: ld_reg(cpu, "H", "E")),
    INSTR(0x64, "LD H, H", lambda cpu: ld_reg(cpu, "H", "H")),
    INSTR(0x65, "LD H, L", lambda cpu: ld_reg(cpu, "H", "L")),
    INSTR(0x66, "LD H, HL", lambda cpu: ld_reg(cpu, "H", "HL")),
    INSTR(0x67, "LD H, A", lambda cpu: ld_reg(cpu, "H", "A")),
    INSTR(0x68, "LD L, B", lambda cpu: ld_reg(cpu, "L", "B")),
    INSTR(0x69, "LD L, C", lambda cpu: ld_reg(cpu, "L", "C")),
    INSTR(0x6a, "LD L, D", lambda cpu: ld_reg(cpu, "L", "D")),
    INSTR(0x6b, "LD L, E", lambda cpu: ld_reg(cpu, "L", "E")),
    INSTR(0x6c, "LD L, H", lambda cpu: ld_reg(cpu, "L", "H")),
    INSTR(0x6d, "LD L, L", lambda cpu: ld_reg(cpu, "L", "L")),
    INSTR(0x6e, "LD L, HL", lambda cpu: ld_reg(cpu, "L", "HL")),
    INSTR(0x6f, "LD L, A", lambda cpu: ld_reg(cpu, "L", "A")),
    INSTR(0x70, "LD HL, B", lambda cpu: ld_reg(cpu, "HL", "B")),
    INSTR(0x71, "LD HL, B", lambda cpu: ld_reg(cpu, "HL", "C")),
    INSTR(0x72, "LD HL, B", lambda cpu: ld_reg(cpu, "HL", "D")),
    INSTR(0x73, "LD HL, B", lambda cpu: ld_reg(cpu, "HL", "E")),
    INSTR(0x74, "LD HL, B", lambda cpu: ld_reg(cpu, "HL", "H")),
    INSTR(0x75, "LD HL, B", lambda cpu: ld_reg(cpu, "HL", "L")),
    INSTR(0x76,), # TODO : HALT
    INSTR(0x77, "LD HL, A", lambda cpu: ld_reg(cpu, "HL", "A")),
    INSTR(0x78, "LD A, B", lambda cpu: ld_reg(cpu, "A", "B")),
    INSTR(0x79, "LD A, C", lambda cpu: ld_reg(cpu, "A", "C")),
    INSTR(0x7a, "LD A, D", lambda cpu: ld_reg(cpu, "A", "D")),
    INSTR(0x7b, "LD A, E", lambda cpu: ld_reg(cpu, "A", "E")),
    INSTR(0x7c, "LD A, H", lambda cpu: ld_reg(cpu, "A", "H")),
    INSTR(0x7d, "LD A, L", lambda cpu: ld_reg(cpu, "A", "L")),
    INSTR(0x7e, "LD A, HL", lambda cpu: ld_reg(cpu, "A", "HL")),
    INSTR(0x7f, "LD A, A", lambda cpu: ld_reg(cpu, "A", "A")),
    INSTR(0x80, "", lambda dst, src: None),
    INSTR(0x81, "", lambda dst, src: None),
    INSTR(0x82, "", lambda dst, src: None),
    INSTR(0x83, "", lambda dst, src: None),
    INSTR(0x84, "", lambda dst, src: None),
    INSTR(0x85, "", lambda dst, src: None),
    INSTR(0x86, "", lambda dst, src: None),
    INSTR(0x87, "", lambda dst, src: None),
    INSTR(0x88, "", lambda dst, src: None),
    INSTR(0x89, "", lambda dst, src: None),
    INSTR(0x8a, "", lambda dst, src: None),
    INSTR(0x8b, "", lambda dst, src: None),
    INSTR(0x8c, "", lambda dst, src: None),
    INSTR(0x8d, "", lambda dst, src: None),
    INSTR(0x8e, "", lambda dst, src: None),
    INSTR(0x8f, "", lambda dst, src: None),
    INSTR(0x90, "", lambda dst, src: None),
    INSTR(0x91, "", lambda dst, src: None),
    INSTR(0x92, "", lambda dst, src: None),
    INSTR(0x93, "", lambda dst, src: None),
    INSTR(0x94, "", lambda dst, src: None),
    INSTR(0x95, "", lambda dst, src: None),
    INSTR(0x96, "", lambda dst, src: None),
    INSTR(0x97, "", lambda dst, src: None),
    INSTR(0x98, "", lambda dst, src: None),
    INSTR(0x99, "", lambda dst, src: None),
    INSTR(0x9a, "", lambda dst, src: None),
    INSTR(0x9b, "", lambda dst, src: None),
    INSTR(0x9c, "", lambda dst, src: None),
    INSTR(0x9d, "", lambda dst, src: None),
    INSTR(0x9e, "", lambda dst, src: None),
    INSTR(0x9f, "", lambda dst, src: None),
    INSTR(0xa0, "", lambda dst, src: None),
    INSTR(0xa1, "", lambda dst, src: None),
    INSTR(0xa2, "", lambda dst, src: None),
    INSTR(0xa3, "", lambda dst, src: None),
    INSTR(0xa4, "", lambda dst, src: None),
    INSTR(0xa5, "", lambda dst, src: None),
    INSTR(0xa6, "", lambda dst, src: None),
    INSTR(0xa7, "", lambda dst, src: None),
    INSTR(0xa8, "", lambda dst, src: None),
    INSTR(0xa9, "", lambda dst, src: None),
    INSTR(0xaa, "", lambda dst, src: None),
    INSTR(0xab, "", lambda dst, src: None),
    INSTR(0xac, "", lambda dst, src: None),
    INSTR(0xad, "", lambda dst, src: None),
    INSTR(0xae, "", lambda dst, src: None),
    INSTR(0xaf, "", lambda dst, src: None),
    INSTR(0xb0, "", lambda dst, src: None),
    INSTR(0xb1, "", lambda dst, src: None),
    INSTR(0xb2, "", lambda dst, src: None),
    INSTR(0xb3, "", lambda dst, src: None),
    INSTR(0xb4, "", lambda dst, src: None),
    INSTR(0xb5, "", lambda dst, src: None),
    INSTR(0xb6, "", lambda dst, src: None),
    INSTR(0xb7, "", lambda dst, src: None),
    INSTR(0xb8, "", lambda dst, src: None),
    INSTR(0xb9, "", lambda dst, src: None),
    INSTR(0xba, "", lambda dst, src: None),
    INSTR(0xbb, "", lambda dst, src: None),
    INSTR(0xbc, "", lambda dst, src: None),
    INSTR(0xbd, "", lambda dst, src: None),
    INSTR(0xbe, "", lambda dst, src: None),
    INSTR(0xbf, "", lambda dst, src: None),
    INSTR(0xc0, "", lambda dst, src: None),
    INSTR(0xc1, "", lambda dst, src: None),
    INSTR(0xc2, "", lambda dst, src: None),
    INSTR(0xc3, "", lambda dst, src: None),
    INSTR(0xc4, "", lambda dst, src: None),
    INSTR(0xc5, "", lambda dst, src: None),
    INSTR(0xc6, "", lambda dst, src: None),
    INSTR(0xc7, "", lambda dst, src: None),
    INSTR(0xc8, "", lambda dst, src: None),
    INSTR(0xc9, "", lambda dst, src: None),
    INSTR(0xca, "", lambda dst, src: None),
    INSTR(0xcb, "", lambda dst, src: None),
    INSTR(0xcc, "", lambda dst, src: None),
    INSTR(0xcd, "", lambda dst, src: None),
    INSTR(0xce, "", lambda dst, src: None),
    INSTR(0xcf, "", lambda dst, src: None),
    INSTR(0xd0, "", lambda dst, src: None),
    INSTR(0xd1, "", lambda dst, src: None),
    INSTR(0xd2, "", lambda dst, src: None),
    INSTR(0xd3, "", lambda dst, src: None),
    INSTR(0xd4, "", lambda dst, src: None),
    INSTR(0xd5, "", lambda dst, src: None),
    INSTR(0xd6, "", lambda dst, src: None),
    INSTR(0xd7, "", lambda dst, src: None),
    INSTR(0xd8, "", lambda dst, src: None),
    INSTR(0xd9, "", lambda dst, src: None),
    INSTR(0xda, "", lambda dst, src: None),
    INSTR(0xdb, "", lambda dst, src: None),
    INSTR(0xdc, "", lambda dst, src: None),
    INSTR(0xdd, "", lambda dst, src: None),
    INSTR(0xde, "", lambda dst, src: None),
    INSTR(0xdf, "", lambda dst, src: None),
    INSTR(0xe0, "", lambda dst, src: None),
    INSTR(0xe1, "", lambda dst, src: None),
    INSTR(0xe2, "", lambda dst, src: None),
    INSTR(0xe3, "", lambda dst, src: None),
    INSTR(0xe4, "", lambda dst, src: None),
    INSTR(0xe5, "", lambda dst, src: None),
    INSTR(0xe6, "", lambda dst, src: None),
    INSTR(0xe7, "", lambda dst, src: None),
    INSTR(0xe8, "", lambda dst, src: None),
    INSTR(0xe9, "", lambda dst, src: None),
    INSTR(0xea, "", lambda dst, src: None),
    INSTR(0xeb, "", lambda dst, src: None),
    INSTR(0xec, "", lambda dst, src: None),
    INSTR(0xed, "", lambda dst, src: None),
    INSTR(0xee, "", lambda dst, src: None),
    INSTR(0xef, "", lambda dst, src: None),
    INSTR(0xf0, "", lambda dst, src: None),
    INSTR(0xf1, "", lambda dst, src: None),
    INSTR(0xf2, "", lambda dst, src: None),
    INSTR(0xf3, "", lambda dst, src: None),
    INSTR(0xf4, "", lambda dst, src: None),
    INSTR(0xf5, "", lambda dst, src: None),
    INSTR(0xf6, "", lambda dst, src: None),
    INSTR(0xf7, "", lambda dst, src: None),
    INSTR(0xf8, "", lambda dst, src: None),
    INSTR(0xf9, "", lambda dst, src: None),
    INSTR(0xfa, "", lambda dst, src: None),
    INSTR(0xfb, "", lambda dst, src: None),
    INSTR(0xfc, "", lambda dst, src: None),
    INSTR(0xfd, "", lambda dst, src: None),
    INSTR(0xfe, "", lambda dst, src: None),
    INSTR(0xff, "", lambda dst, src: None),
]
