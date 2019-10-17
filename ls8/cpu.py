"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        # store program counter
        self.PC = self.reg[0]
        # store flag
        self.FL = self.reg[4]
        # store stack pointer
        self.SP = self.reg[7]
        self.SP = 244

        # store operation handling
        self.commands = {
            0b00000001: self.hlt,
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b10100010: self.mul,
            0b01000110: self.pop,
            0b01000101: self.push
        }

    def __repr__(self):
        return f"RAM: {self.ram} \n Register: {self.ram}"

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def hlt(self, operand_a, operand_b):
        return (0, False)

    def ldi(self, operand_a, operand_b):
        # sets register to value
        self.reg[operand_a] = operand_b
        return (3, True)

    def prn(self, operand_a, operand_b):
        # print value at register
        print(self.reg[operand_a])
        return (2, True)

    def mul(self, operand_a, operand_b):
        # multiply two values to store in register
        self.alu("MUL", operand_a, operand_b)
        return (3, True)

    def pop(self, operand_a, operand_b):
        # gets value from memory at stack pointer
        value = self.ram_read(self.SP)
        # write that value to indicated spot in register
        self.reg[operand_a] = value
        # increment stack pointer to next filled spot in stack memory
        self.SP += 1

        return (2, True)

    def push(self, operand_a, operand_b):
        # decrements SP tp next open spot in stack memory
        self.SP -= 1
        # grabs value from indicated register spot
        value = self.reg[operand_a]
        # writes value to RAM at stack pointer address
        self.ram_write(value, self.SP)

        return (2, True)

    def load(self, program):
        """Load a program into memory."""
        try:
            address = 0

            with open(program) as f:
                for line in f:
                    comment_split = line.split('#')

                    number = comment_split[0].strip()

                    if number == "":
                        continue

                    value = int(number, 2)

                    self.ram_write(value, address)

                    address += 1

        except FileNotFoundError:
            print(f"{program} not found")
            sys.exit(2)

        if len(sys.argv) != 2:
            print(
                f"Please format the command: \n python3 ls8.py <filename>", file=sys.stderr)
            sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] = (self.reg[reg_a]) * (self.reg[reg_b])
            return 2

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        running = True

        while running:
            IR = self.ram[self.PC]

            operand_a = self.ram[self.PC + 1]
            operand_b = self.ram[self.PC + 2]

            try:
                operation_output = self.commands[IR](operand_a, operand_b)

                running = operation_output[1]
                self.PC += operation_output[0]

            except:
                print(f"Unknown command: {IR}")
                sys.exit(1)
