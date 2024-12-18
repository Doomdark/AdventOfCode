# Position  mode = 0
# Immediate mode = 1
# Relative mode  = 2

import copy, queue, threading

class Intcode(threading.Thread):

    def __init__(self, program):
        threading.Thread.__init__(self)
        self.memory = copy.deepcopy(program)
        self.addr = 0
        self.input_queue  = queue.Queue()
        self.output_queue = queue.Queue()
        self._exit = False
        self.running = False
        self.last_output = 0
        self.relative_base_offset = 0
        self.input_value = None
        self.input_count = 0
        self.output_count = 0
        self.kill = False

    def get(self, block=True, timeout=1):
        a = None
        try:
            a = self.output_queue.get(block, timeout)
        except queue.Empty:
            a = None
        return a

    def put(self, value):
        self.input_queue.put(value)

    def run(self):
        while 1:
            self.running = True
            instruction = self.memory[self.addr+0]
            opcode      = instruction % 100

            # Extract the parameter modes from the instruction
            param1_mode = (instruction // 100) % 10
            param2_mode = (instruction // 1000) % 10
            param3_mode = (instruction // 10000) % 10

            # Get the values of param1 and param2 for the specified opcodes and parameter modes from the instruction
            if opcode in [1, 2, 4, 5, 6, 7, 8, 9]:
                # Adjust parameters for different parameter modes
                if   param1_mode == 0: param1 = self.memory[self.memory[self.addr+1]]
                elif param1_mode == 1: param1 = self.memory[self.addr+1]
                else:                  param1 = self.memory[self.memory[self.addr+1]+self.relative_base_offset]

                if   param2_mode == 0: param2 = self.memory[self.memory[self.addr+2]]
                elif param2_mode == 1: param2 = self.memory[self.addr+2]
                else:                  param2 = self.memory[self.memory[self.addr+2]+self.relative_base_offset]

            if opcode == 1: # Add
                result = param1 + param2
                if   param3_mode == 0: self.memory[self.memory[self.addr+3]] = result
                elif param3_mode == 1: self.memory[self.addr+3] = result
                else:                  self.memory[self.memory[self.addr+3]+self.relative_base_offset] = result
                self.addr += 4
            elif opcode == 2: # Multiply
                result = param1 * param2
                if   param3_mode == 0: self.memory[self.memory[self.addr+3]] = result
                elif param3_mode == 1: self.memory[self.addr+3] = result
                else:                  self.memory[self.memory[self.addr+3]+self.relative_base_offset] = result
                self.addr += 4
            elif opcode == 3: # Input - always uses immediate parameter as the self.address
                self.running = False
                #print "({}) Input...".format(self.input_count)
                #self.input_count += 1
                if self.input_value is not None:
                    _input = self.input_value
                else:
                    try:
                        _input = self.input_queue.get(block=True, timeout=1)
                        print("({}) Input...".format(_input))
                    except queue.Empty:
                        return
                    self.running = True
                if   param1_mode == 0: self.memory[self.memory[self.addr+1]] = int(_input)
                elif param1_mode == 1: self.memory[self.addr+1] = int(_input)
                else:                  self.memory[self.memory[self.addr+1]+self.relative_base_offset] = int(_input)
                self.addr += 2
            elif opcode == 4: # Output
                _output = param1
                self.last_output = _output
                self.output_queue.put(_output)
                self.addr += 2
                #print "({}) Output...".format(self.output_count)
                #self.output_count += 1
            elif opcode == 5: # Jump if true
                if param1 != 0:
                    self.addr = param2
                else: # Do nothing - just move on
                    self.addr += 3
            elif opcode == 6: # Jump if false
                if param1 == 0:
                    self.addr = param2
                else: # Do nothing - just move on
                    self.addr += 3
            elif opcode == 7: # Less than
                result = int(param1 < param2)
                if   param3_mode == 0: self.memory[self.memory[self.addr+3]] = result
                elif param3_mode == 1: self.memory[self.addr+3] = result
                else:                  self.memory[self.memory[self.addr+3]+self.relative_base_offset] = result
                self.addr += 4
            elif opcode == 8: # Equals
                result = int(param1 == param2)
                if   param3_mode == 0: self.memory[self.memory[self.addr+3]] = result
                elif param3_mode == 1: self.memory[self.addr+3] = result
                else:                  self.memory[self.memory[self.addr+3]+self.relative_base_offset] = result
                self.addr += 4
            elif opcode == 9: # Relative base offset adjust
                self.relative_base_offset += param1
                #print "RBO:", self.relative_base_offset
                self.addr += 2
            elif opcode == 99: # Exit()
                print("Intcode exit")
                #self._exit = True
                #import sys
                #sys.exit(1)
                self.running = False
                return self.memory[0]
            else:
                print("Unknown opcode at addr", self.addr)
                return

            # Exit the thread if we're killed
            if self.kill:
                return
