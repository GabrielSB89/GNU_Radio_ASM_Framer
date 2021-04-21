"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import math
from gnuradio import gr, blocks


class asm_framer(gr.basic_block):
    #runs only once when the instance of the block is crated
    def __init__(self, golay=False):
        gr.basic_block.__init__(self, name='asm_framer',
        in_sig=[(np.int8)],
        out_sig=[(np.int8)])
        self._golay=golay
        self._asm_header = [(0xC9D08A7B >> bit) & 1 for bit in range(32 - 1, -1, -1)]

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        data_length=math.ceil(len(in0)/8)
        length_field = [(data_length >> bit) & 1 for bit in range(12 - 1, -1, -1)]

        output_array=np.int8(np.append(np.append(np.array(self._asm_header),np.array(length_field)),in0))
        output_items[0]=output_array
        self.consume(0, len(in0))
        return len(output_array)
