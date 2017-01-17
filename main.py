#!/usr/bin/python
# TODO: rename everything leomulator

# For the frontend
import sys
import pygame
import time
import traceback

# For the system
import debug as gb_debug
import video as gb_video
import sound as gb_sound
import bus as gb_bus
import cpu as gb_cpu

class ROM(gb_bus.BUS_OBJECT):
    def __init__(self, rom_bin):
        super(ROM, self).__init__()
        self.rom_bytes = []
        if type(rom_bin) is file:
            rom_bin.seek(0x00)
            try:
                while True:
                    self.rom_bytes.append(ord(rom_bin.read(1)))
            except:
                pass

    def bus_write(self, addr, value):
        # TODO: this function shouldn't exist - handle in an MBC class
        print "WARNING: Write to ROM address 0x%04lx" % (addr+self.bus_addr_lo)

    def bus_read(self, addr):
        return self.rom_bytes[addr]


class RAM(gb_bus.BUS_OBJECT):
    def __init__(self, size=2**16):
        super(RAM, self).__init__()
        self.ram_bytes = [0x00]*size

    def bus_read(self, addr):
        return self.ram_bytes[addr]

    def bus_write(self, addr, value):
        self.ram_bytes[addr] = value


class TIMER(gb_bus.BUS_OBJECT):
    def __init__(self):
        super(TIMER, self).__init__()
        self.tick = 0.0
        self.clock = 0

        self.div_tick = 0.0
        self.div_clock = 0
        
        self.enabled = 0
        self.speed_select = 0
        
        self.frequencies = [4096,262144,65536,16384]
        self.periods = [1.0/f for f in self.frequencies]

        self.load_value = 0

        # ok why is the div register in the *middle* of the selectable
        # frequency spectrum? time to break out the PLL textbook...
        self.div_T = self.periods[3]

        # TODO: it would be fun to implement this with everything deriving from
        # one reference clock and all the obscure glitch behavior described by
        # the pandocs wiki

        self.reset()

    def reset(self):
        self.clock = 0
        self.load_value = 0
        self.enabled = 0
        self.speed_select = 0

    def advance(self, delta):
        # Note that delta is **SIMULATED** time
        if self.enabled == 1:
            T = self.periods[self.speed_select]
            self.tick += delta
            if self.tick >= T:
                self.tick -= T
                self.clock += 1
                if self.clock > 255:
                    self.clock = self.load_value
                    # Trigger an interrupt
                    # TODO: pull these magic numbers out somewhere
                    IF_state = self.bus.read(0xFF0F)
                    IF_state |= 0x4
                    self.bus.write(0xFF0F, IF_state)

        self.div_tick += delta
        if self.div_tick >= self.div_T:
            self.div_tick -= self.div_T
            self.div_clock += 1
            self.div_clock &= 0xFF

    def bus_read(self, addr):
        if addr == 0: # DIV
            return self.div_clock
        elif addr == 1: # TIMA
            return self.clock
        elif addr == 2: # TMA
            return self.load_value
        elif addr == 3: # TAC
            val = self.enabled << 2
            val |= self.speed_select
        else:
            raise Exception("timer doesn't know WHAT the fuck to do")

    def bus_write(self, addr, value):
        if addr == 0: # DIV
            self.div_clock = 0
            self.clock = 0
        elif addr == 1: # TIMA
            self.clock = value & 0xFF
        elif addr == 2: # TMA
            self.load_value = value & 0xFF
        elif addr == 3: # TAC
            self.enabled = (value & 0x4) != 0
            self.speed_select = value & 0x3
        else:
            raise Exception("timer doesn't know WHAT the fuck to do")

class JOYPAD(gb_bus.BUS_OBJECT):
    def __init__(self):
        super(JOYPAD, self).__init__()
        self.direction_select = False
        self.button_select = False
        self.directions = 0x0F
        self.buttons = 0x0F

        self.direction_idx = {
            "right": 0,
            "left": 1,
            "up": 2,
            "down": 3,
        }
        self.button_idx = {
            "a": 0,
            "b": 1,
            "select": 2,
            "start": 3,
        }
  
    def update(self, keys):
        changed = False
        for key, idx in self.direction_idx.items():
            if key in keys:
                if keys[key]:
                    self.directions &= ~(1 << idx)
                else:
                    self.directions |= 1 << idx
                changed = True
        for key, idx in self.button_idx.items():
            if key in keys:
                if keys[key]:
                    self.buttons &= ~(1 << idx)
                else:
                    self.buttons |= 1 << idx
                changed = True

        if changed:
            # Trigger an interrupt
            # This is technically only supposed to happen on high-to-low
            # transitions but because the real hardware buttons aren't
            # debounced it effectively happens on both button press and
            # release
            # TODO: pull these magic numbers out somewhere
            IF_state = self.bus.read(0xFF0F)
            IF_state |= 0x10
            self.bus.write(0xFF0F, IF_state)

    def bus_read(self, addr):
        if addr == 0:
            val = 0
            val |= self.button_select << 5
            val |= self.direction_select << 4
            if not self.direction_select:
                val |= self.directions
            if not self.button_select:
                val |= self.buttons
            return val
        else:
            raise Exception("joypad doesn't know WHAT the fuck to do")

    def bus_write(self, addr, value):
        if addr == 0:
            self.button_select = (value & (1 << 5)) != 0
            self.direction_select = (value & (1 << 4)) != 0
        else:
            raise Exception("joypad doesn't know WHAT the fuck to do")


class GAMEBOY(object):
    def __init__(self):
        self.debug_trigger = False

        self.bus = gb_bus.BUS()

        self.rom = ROM(f)
        # TODO: implement banks instead of fixing bank 2:
        # self.bus.attach(self.rom, 0x0000, 0x3FFF)
        self.bus.attach(self.rom, 0x0000, 0x7FFF)

        self.ram = [RAM(4096), RAM(4096)]
        self.bus.attach(self.ram[0], 0xC000, 0xCFFF)
        self.bus.attach(self.ram[1], 0xD000, 0xDFFF)

        self.hram = RAM(127)
        self.bus.attach(self.hram, 0xFF80, 0xFFFE)

        self.video_driver = gb_video.VIDEO(self.bus)
        self.sound_driver = gb_sound.SOUND(self.bus)

        self.joypad = JOYPAD()
        self.bus.attach(self.joypad, 0xFF00, 0xFF00)

        self.if_reg = gb_cpu.REG("IF", 8)
        self.bus.attach(self.if_reg, 0xFF0F, 0xFF0F)
        
        self.ie_reg = gb_cpu.REG("IE", 8)
        self.bus.attach(self.ie_reg, 0xFFFF, 0xFFFF)

        self.timer = TIMER()
        self.bus.attach(self.timer, 0xFF04, 0xFF07)

        # Serial dummy hardware
        self.serial_data = gb_cpu.REG("SB", 8)
        self.bus.attach(self.serial_data, 0xFF01, 0xFF01)
        self.serial_control = gb_cpu.REG("SC", 8)
        self.bus.attach(self.serial_control, 0xFF02, 0xFF02)

        self.cpu = gb_cpu.CPU(self.bus)

    def advance(self):
        # TODO: double-check signed arithmetic everywhere. does C/H work
        # as borrow flags when doing SUB/DEC/etc?
        # TODO: implement the STOP instruction correctly

        if not self.cpu._halted:
            opcode = self.bus.read(self.cpu.PC.read())
            op = self.cpu.decode(opcode)
            cycles = op()
        else:
            # NOP if halted
            cycles = 4

        # TODO: not sure where/when/how often to do this, putting it here
        # for now so we only have to call timer.advance() once:
        # TODO: also, should this be an add or a direct assign?
        cycles += self.cpu.service_interrupts()

        # TODO: this seems to help the DMA calculation? uhhhh????
        # cycles *= 4

        T_op = self.cpu.T_cyc * cycles
        # TODO: this is useful debug output:
        # print T_op, cycles
        self.timer.advance(T_op)

        # TODO: decompose this and allow for configurable keybindings
        keys = {}
        key_bindings = {
            pygame.K_LEFT: "left",
            pygame.K_RIGHT: "right",
            pygame.K_UP: "up",
            pygame.K_DOWN: "down",
            pygame.K_z: "a",
            pygame.K_x: "b",
            pygame.K_RETURN: "start",
            pygame.K_TAB: "select",
        }
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                self.cpu.op_stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAUSE:
                    self.debug_trigger = True
                elif event.key in key_bindings:
                    keys[key_bindings[event.key]] = True
            elif event.type == pygame.KEYUP:
                if event.key in key_bindings:
                    keys[key_bindings[event.key]] = False
        if len(keys) > 0:
            self.joypad.update(keys)

        self.video_driver.advance(T_op)

        # TODO: this DMA blockade seems to break tetris, investigate more
        # closely what's going on
        # seems like it's lasting a *little bit* too long
        #
        # TODO: make sure this DMA blockade covers MBCs once they're
        # implemented
        if self.video_driver.dma_active():
            self.rom.bus_enabled = False
            for ram_bank in self.ram:
                ram_bank.bus_enabled = False
        else:
            self.rom.bus_enabled = True
            for ram_bank in self.ram:
                ram_bank.bus_enabled = True


if __name__=="__main__":
    if len(sys.argv) < 2:
        print "Usage: %s [-v] [-d] [--paused] ROMFILE" % sys.argv[0]
        sys.exit(1)

    # TODO: use argparser
    debug = "-d" in sys.argv or "--debug" in sys.argv
    verbose = "-v" in sys.argv
    start_paused = "--paused" in sys.argv

    pygame.init()
    pygame.display.set_caption("pygb")
    pygame.key.set_repeat(10, 10)

    with open(sys.argv[1], "rb") as f:
        print "Building system"
        system = GAMEBOY()
        if debug:
            debugger = gb_debug.DEBUGGER(system, verbose=verbose)
            if start_paused:
                system.debug_trigger = True

        print "Starting execution"

        n_instr = 0
        n_cyc = 0
        T_start = time.time()
        running = True
        while running:
            try:
                system.advance()
                running = not system.cpu._stopped
                if debug:
                    debugger.scan()
            except gb_debug.DEBUGGER_TRIGGER:
                if debug:
                    debugger.start()
                else:
                    raise
            except Exception as e:
                traceback.print_exc()
                if debug:
                    debugger.start()
                else:
                    print "------------"
                    print "CORE DUMP"
                    print system.cpu.core_dump()
                    print "------------"
                running = False

            n_instr += 1
            n_cyc += 1
        T_end = time.time()
        print "Executed %i instructions in %f seconds (%f simulated)" % (n_instr, T_end-T_start, n_cyc*system.cpu.T_cyc)

