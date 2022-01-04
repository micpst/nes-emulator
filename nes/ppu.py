import random
import pygame as pg
from enum import Enum
from typing import Optional, List, Tuple
from .cartridge import Cartridge


class PPU:
    """
    An emulation of the 2C02 picture processing unit.
    """

    __slots__ = ("controller_reg", "mask_reg", "status_reg",
                 "name_table", "pattern_table", "palette_table", "cart", "frame_complete", "screen", "patterns",
                 "_cycles", "_scanline", "_clock_count", "_colors")

    class CONTROLLER(Enum):
        """
        The controller register flags.
        """
        X = 1 << 0
        Y = 1 << 1
        IM = 1 << 2
        PB = 1 << 3
        PS = 1 << 4
        SS = 1 << 5
        SM = 1 << 6
        N = 1 << 7

    class MASK(Enum):
        """
        The mask register flags.
        """
        CGS = 1 << 0  # Grayscale
        RBL = 1 << 1  # Render background in leftmost
        RSL = 1 << 2  # Render sprites in leftmost
        RB  = 1 << 3  # Render background
        RS  = 1 << 4  # Render sprites
        CR  = 1 << 5  # Emphasise red
        CG  = 1 << 6  # Emphasise green
        CB  = 1 << 7  # Emphasise blue

    class STATUS(Enum):
        """
        The status register flags.
        """
        SO = 1 << 5
        SZH = 1 << 6
        VB = 1 << 7

    def __init__(self) -> None:
        # PPU internal registers:
        self.controller_reg: int = 0x00
        self.mask_reg: int = 0x00
        self.status_reg: int = 0x00

        # PPU bus:
        self.name_table: List[List[int]] = 2 * [1024 * [0x00]]
        self.pattern_table: List[List[int]] = 2 * [4096 * [0x00]]
        self.palette_table: List[int] = 32 * [0x00]
        self.cart: Optional[Cartridge] = None

        # For the purpose of emulation:
        self.frame_complete: bool = False
        self.screen: pg.Surface = pg.Surface((341, 261))
        self.patterns: List[pg.Surface] = [pg.Surface((128, 128)), pg.Surface((128, 128))]

        # Helper variables:
        self._cycles: int = 0
        self._scanline: int = 0
        self._clock_count: int = 0

        self._colors: List[Tuple[int, int, int]] = [
            ( 84,  84,  84), (  0,  30, 116), (  8,  16, 144), ( 48,   0, 136),
            ( 68,   0, 100), ( 92,   0,  48), ( 84,   4,   0), ( 60,  24,   0),
            ( 32,  42,   0), (  8,  58,   0), (  0,  64,   0), (  0,  60,   0),
            (  0,  50,  60), (  0,   0,   0), (  0,   0,   0), (  0,   0,   0),

            (152, 150, 152), (  8,  76, 196), ( 48,  50, 236), ( 92,  30, 228),
            (136,  20, 176), (160,  20, 100), (152,  34,  32), (120,  60,   0),
            ( 84,  90,   0), ( 40, 114,   0), (  8, 124,   0), (  0, 118,  40),
            (  0, 102, 120), (  0,   0,   0), (  0,   0,   0), (  0,   0,   0),

            (236, 238, 236), ( 76, 154, 236), (120, 124, 236), (176,  98, 236),
            (228,  84, 236), (236,  88, 180), (236, 106, 100), (212, 136,  32),
            (160, 170,   0), (116, 196,   0), ( 76, 208,  32), ( 56, 204, 108),
            ( 56, 180, 204), ( 60,  60,  60), (  0,   0,   0), (  0,   0,   0),

            (236, 238, 236), (168, 204, 236), (188, 188, 236), (212, 178, 236),
            (236, 174, 236), (236, 174, 212), (236, 180, 176), (228, 196, 144),
            (204, 210, 120), (180, 222, 120), (168, 226, 144), (152, 226, 180),
            (160, 214, 228), (160, 162, 160), (  0,   0,   0), (  0,   0,   0),
        ]

    def connect_cartridge(self, cart: Cartridge) -> None:
        self.cart = cart

    def clock(self) -> None:
        # Produce some noise:
        self.screen.set_at((self._cycles - 1, self._scanline), self._colors[random.choice((0x3F, 0x30))])

        self._clock_count += 1
        self._cycles += 1

        if self._cycles >= 341:
            self._cycles = 0
            self._scanline += 1

            if self._scanline >= 261:
                self._scanline = -1
                self.frame_complete = True

    def write(self, address: int, data: int) -> None:
        if address == 0x0000:
            pass

        elif address == 0x0001:
            pass

        elif address == 0x0002:
            pass

        elif address == 0x0003:
            pass

        elif address == 0x0004:
            pass

        elif address == 0x0005:
            pass

        elif address == 0x0006:
            pass

        elif address == 0x0007:
            pass

    def read(self, address: int, read_only: bool) -> int:
        if address == 0x0000:
            pass

        elif address == 0x0001:
            pass

        elif address == 0x0002:
            pass

        elif address == 0x0003:
            pass

        elif address == 0x0004:
            pass

        elif address == 0x0005:
            pass

        elif address == 0x0006:
            pass

        elif address == 0x0007:
            pass

        return 0x00

    def _write(self, address: int, data: int) -> None:
        address &= 0x3FFF

        if 0x0000 <= address <= 0x1FFF:
            self.pattern_table[(address & 0x1000) >> 12][address & 0x0FFF] = data

        elif 0x2000 <= address <= 0x3EFF:
            pass

        elif 0x3F00 <= address <= 0x3FFF:
            pass

        elif self.cart:
            self.cart.write(address & 0x3FFF, data)

    def _read(self, address: int, read_only: bool) -> int:
        address &= 0x3FFF

        if 0x0000 <= address <= 0x1FFF:
            return self.pattern_table[(address & 0x1000) >> 12][address & 0x0FFF]

        elif 0x2000 <= address <= 0x3EFF:
            pass

        elif 0x3F00 <= address <= 0x3FFF:
            address &= 0xF if (address & 0x1F) in (0x10, 0x14, 0x18, 0x1C) else 0x1F
            return self.palette_table[address]

        return self.cart.read(address & 0x3FFF) if self.cart else 0x00
