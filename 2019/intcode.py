# Position  mode = 0
# Immediate mode = 1
# Relative mode  = 2

import queue, threading
from collections import defaultdict

DEBUG = False

class Intcode(threading.Thread):

    def __init__(self, program):
        threading.Thread.__init__(self)
        self.memory = defaultdict(int)
        self.memory.update(program)
        self.addr = 0
        self.input_queue  = queue.Queue()
        self.output_queue = queue.Queue()
        self.relative_base = 0

    def get(self, block=True, timeout=5):
        a = None
        try:
            a = self.output_queue.get(block, timeout)
        except queue.Empty:
            a = None
        return a

    def put(self, value):
        self.input_queue.put(value)

    def run(self):
        while True:
            instruction = self.memory[self.addr+0]
            opcode      = instruction % 100

            # Extract the parameter modes from the instruction
            param1_mode = (instruction // 100) % 10
            param2_mode = (instruction // 1000) % 10
            param3_mode = (instruction // 10000) % 10

            # Get the values of param1 and param2 for the specified opcodes and parameter modes from the instruction
            if opcode in [1, 2, 4, 5, 6, 7, 8, 9]:
                # Adjust parameters for different parameter modes
                if   param1_mode == 0: src1 = self.memory[self.addr+1]
                elif param1_mode == 1: src1 = self.addr+1
                else:                  src1 = self.memory[self.addr+1]+self.relative_base
                param1 = self.memory[src1]

                if   param2_mode == 0: src2 = self.memory[self.addr+2]
                elif param2_mode == 1: src2 = self.addr+2
                else:                  src2 = self.memory[self.addr+2]+self.relative_base
                param2 = self.memory[src2]

            if opcode in [1, 2, 7, 8]:
                if   param3_mode == 0: dst = self.memory[self.addr+3]
                elif param3_mode == 1: raise # Destinations are never immediate
                else:                  dst = self.memory[self.addr+3]+self.relative_base

            if opcode in [3]:
                if   param1_mode == 0: dst = self.memory[self.addr+1]
                elif param1_mode == 1: raise # Destinations are never immediate
                else:                  dst = self.memory[self.addr+1]+self.relative_base

            if opcode == 1: # Add
                result = int(param1 + param2)
                self.memory[dst] = result
                if DEBUG: print(f"[{self.addr:>3}] ADD [{src1:>3}:{param1:>3}] [{src2:>3}:{param2:>3}] -> [{dst:>3}:{result:>3}]")
                self.addr += 4
            elif opcode == 2: # Multiply
                result = int(param1 * param2)
                self.memory[dst] = result
                if DEBUG: print(f"[{self.addr:>3}] MUL [{src1:>3}:{param1:>3}] [{src2:>3}:{param2:>3}] -> [{dst:>3}:{result:>3}]")
                self.addr += 4
            elif opcode == 3: # Input - always uses immediate parameter as the self.address
                try:
                    _input = self.input_queue.get(block=True, timeout=5)
                except queue.Empty:
                    return
                result = int(_input)
                self.memory[dst] = result
                if DEBUG: print(f"[{self.addr:>3}] IN  [{dst:>3}:{result:>3}]")
                self.addr += 2
            elif opcode == 4: # Output
                result = int(param1)
                self.output_queue.put(result)
                if DEBUG: print(f"[{self.addr:>3}] OUT [{result:>3}]")
                self.addr += 2
            elif opcode == 5: # Jump if true
                if int(param1) != 0:
                    if DEBUG: print(f"[{self.addr:>3}] JiT [{src1:>3}:{param1:>3}]           -> [{param2:>3}]")
                    self.addr = int(param2)
                else: # Do nothing - just move on
                    self.addr += 3
            elif opcode == 6: # Jump if false
                if int(param1) == 0:
                    if DEBUG: print(f"[{self.addr:>3}] JiF [{src1:>3}:{param1:>3}]           -> [{param2:>3}]")
                    self.addr = int(param2)
                else: # Do nothing - just move on
                    self.addr += 3
            elif opcode == 7: # Less than
                result = int(param1 < param2)
                self.memory[dst] = result
                if DEBUG: print(f"[{self.addr:>3}] LT  [{src1:>3}:{param1:>3}] [{src2:>3}:{param2:>3}] -> [{dst:>3}:{result:>3}]")
                self.addr += 4
            elif opcode == 8: # Equals
                result = int(param1 == param2)
                self.memory[dst] = result
                if DEBUG: print(f"[{self.addr:>3}] EQ  [{src1:>3}:{param1:>3}] [{src2:>3}:{param2:>3}] -> [{dst:>3}:{result:>3}]")
                self.addr += 4
            elif opcode == 9: # Relative base offset adjust
                if DEBUG: print(f"[{self.addr:>3}] RBO -> {self.relative_base} + {param1}")
                self.relative_base = self.relative_base + int(param1)
                self.addr += 2
            elif opcode == 99: # Exit()
                if DEBUG: print(f"[{self.addr:>3}] EXT")
                return self.memory[0]
            else:
                print("Unknown opcode at addr", self.addr)
                return
