# Group 1
# Joseph de Joya, Martin Cardona
# Project 3 ISA Simulator

def Initialize_Registers():
    # Initializes the 4 general purpose registers, the stash/recover registers,
    # the branch register, and PC
    # All registers are 16-bits and initialized to 0 (except for the 8-bit PC and 1-bit branch).
    # The register file created will be in the format below.
    # 16-bit R0
    # 16-bit R1
    # 16-bit R2
    # 16-bit R3
    # 16-bit SR0
    # 16-bit SR1
    # 16-bit SR2
    # 16-bit SR3
    # 1-bit branch
    # 16-bit PC

    reg_file = open("reg_file.txt", "w")

    # Initialize R0-R3 and SR0-SR3
    for i in range(0, 8):
        reg_file.write("0000000000000000\n")
    # Initialize branch
    reg_file.write("0\n")
    # Initialize PC
    reg_file.write("00000000\n")
    # Close reg_file
    reg_file.close()

    # Create an array that stores the initialized register values.
    reg_file = open("reg_file.txt", "r");
    register = reg_file.readlines()
    reg_file.close()
    for i in range(0, len(register)):
        register[i] = register[i][0:len(register[i]) - 1]

    return register;

def Update_Reg_File(register):
    reg_file = open("reg_file.txt", "w")
    for i in range(0, len(register)):
        reg_file.write(register[i] + "\n")
    reg_file.close()
    return


def Update_Data_Mem_File(data, filename):
    d_mem = open(filename, "w")
    for i in range(0, len(data)):
        d_mem.write(data[i] + "\n")
    d_mem.close()
    return

def Instruction_Execute( instr, register, data ):

    # boolean return, return true if instruction END is reached
    end_of_program = False

    # Decode and Execute the Instruction
    if (instr[1:4] == '000'):
        Rd = int(instr[4:6], base=2)
        Rs = int(instr[6:8], base=2)
        print('ADD $R{}, $R{}'.format(Rd, Rs))
        Instr_ADD(Rd, Rs, register)

    elif (instr[1:4] == '001'):
        Rd = int(instr[4:6], base=2)
        imm = int(instr[6:8], base=2)
        imm = imm - ((imm << 1) & (2**2))
        print('ADDI $R{}, {}'.format(Rd, imm))
        Instr_ADDI(Rd, imm, register)

    elif (instr[1:4] == '010'):
        Rd = int(instr[4:6], base=2)
        Rs = int(instr[6:8], base=2)
        print('SLT $R{}, $R{}'.format(Rd, Rs))
        Instr_SLT(Rd, Rs, register)
    
    elif (instr[1:4] == '100'):
        imm = int(instr[4:8], base=2)
        imm = imm - ((imm << 1) & (2**4))
        print('B {}'.format(imm))
        Instr_B(imm, register)
        #register[9] = "{0:08b}".format(int(register[9], base=2) + 1)
    
    elif (instr[1:4] == '011'):
        imm = int(instr[4:8], base=2)
        imm = imm - ((imm << 1) & (2**4))
        print('J {}'.format(imm))
        Instr_J(imm, register)
        #register[9] = "{0:08b}".format(int(register[9], base=2) + 1)
    
    elif (instr[1:5] == '1010'):
        Rd = int(instr[5:7], base=2)
        Rs = int(instr[7], base=2)
        print('LOAD $R{}, $R{}'.format(Rd, Rs))
        Instr_LOAD(Rd, Rs, register, data)
    
    elif (instr[1:5] == '1011'):
        Rd = int(instr[5:7], base=2)
        Rs = int(instr[7], base=2)
        print('STR $R{}, $R{}'.format(Rd, Rs))
        Instr_STR(Rd, Rs, register, data)
    
    elif (instr[1:6] == '11000'):
        Rd = int(instr[6:8], base=2)
        print('LSL $R{}'.format(Rd))
        Instr_LSL(Rd, register)
    
    elif (instr[1:6] == '11001'):
        Rd = int(instr[6], base=2)
        Rs = int(instr[7], base=2)
        print('NXOR $R{}, $R{}'.format(Rd, Rs))
        print(register[Rd])
        print(register[Rs])
        Instr_NXOR(Rd, Rs, register)
        print(register[Rd])
    
    elif (instr[1:6] == '11010'):
        Rd = int(instr[6:8], base=2)
        print('EQZ $R{}'.format(Rd))
        Instr_EQZ(Rd, register)
    
    elif (instr[1:6] == '11011'):
        Rd = int(instr[6:8], base=2)
        print('COMP $R{}'.format(Rd))
        Instr_COMP(Rd, register)
    
    elif (instr[1:6] == '11101'):
        Rd = int(instr[6:8], base=2)
        print('RST $R{}'.format(Rd))
        Instr_RST(Rd, register)
    
    elif (instr[1:6] == '11100'):
        Rd = int(instr[6:8], base=2)
        print('RCVR $R{}'.format(Rd))
        Instr_RCVR(Rd, register)
    
    elif (instr[1:6] == '11110'):
        Rd = int(instr[6:8], base=2)
        print('STSH $R{}'.format(Rd))
        Instr_STSH(Rd, register)
    
    elif (instr[1:8] == '1111111'):
        end_of_program = True
        print('END')

    
    return end_of_program


def Instr_ADD(Rd, Rs, register):
    # Execute ADD instruction
    base10 = int(register[Rd], base=2) + int(register[Rs], base=2)
    register[Rd] = "{0:016b}".format(base10)
    register[9] = "{0:08b}".format(int(register[9], base=2) + 1)
    return


def Instr_ADDI(Rd, imm, register):
    # Execute ADDI instruction
    base10 = int(register[Rd], base=2) + imm
    register[Rd] = "{0:016b}".format(base10)
    register[9] = "{0:08b}".format(int(register[9], base=2) + 1)
    return


def Instr_SLT(Rd, Rs, register):
    # Execute SLT instruction
    op1 = int(register[Rd], base=2)
    op1 = op1 - ((op1 << 1) & (2**16))
    op2 = int(register[Rs], base=2)
    op2 = op2 - ((op2 << 1) & (2**16))
    
    if (op1 < op2):
        register[8] = "1"
    else:
        register[8] = "0"
    register[9] = "{0:08b}".format(int(register[9], base=2) + 1)
    return


def Instr_B(imm, register):
    # Execute B (Branch) instruction
    if (register[8] == "1"):
        register[9] = "{0:08b}".format(int(register[9], base=2) + imm)
    else:
        register[9] = "{0:08b}".format(int(register[9], base=2) + 1)
    return

def Instr_J(imm, register):
    # Execute J (Jump) instruction
    register[9] = "{0:08b}".format(int(register[9], base=2) + imm)
    return


def Instr_LOAD(Rd, Rs, register, data):
    # Execute LOAD instruction
    register[Rd] = data[int(register[Rs], base=2)]
    register[9] = "{0:08b}".format(int(register[9], base=2) + 1)
    return


def Instr_STR(Rd, Rs, register, data):
    # Execute STR instruction
    data[int(register[Rs], base=2)] = register[Rd]
    register[9] = "{0:08b}".format(int(register[9], base=2) + 1)
    return


def Instr_LSL(Rd, register):
    # Execute LSL instruction
    bitstring = register[Rd] + "0"
    register[Rd] = bitstring[1:len(bitstring)]
    register[9] = "{0:08b}".format(int(register[9], base=2) + 1)
    return


def Instr_NXOR(Rd, Rs, register):
    # Execute NXOR instruction
    op1 = list(register[Rd])
    op2 = list(register[Rs])
    for i in range(0, len(op1)):
        if (op1[i] == op2[i]):
            op1[i] = "1"
        else:
            op1[i] = "0"
    register[Rd] = "".join(op1)
    register[9] = "{0:08b}".format(int(register[9], base=2) + 1)
    return


def Instr_EQZ(Rd, register):
    # Execute LSL instruction
    if (int(register[Rd], base=2) == 0):
        register[8] = "1"
    else:
        register[8] = "0"
    register[9] = "{0:08b}".format(int(register[9], base=2) + 1)
    return


def Instr_COMP(Rd, register):
    # Execute COMP instruction
    base10 = int(register[Rd], base=2) * (-1)
    register[Rd] = "{0:016b}".format(base10)
    register[9] = "{0:08b}".format(int(register[9], base=2) + 1)
    return


def Instr_RCVR(Rd, register):
    # Execute RCVR instruction
    register[Rd] = register[Rd + 4]
    register[9] = "{0:08b}".format(int(register[9], base=2) + 1)
    return


def Instr_RST(Rd, register):
    # Execute RST instruction
    register[Rd] = "{0:016b}".format(0)
    register[9] = "{0:08b}".format(int(register[9], base=2) + 1)
    return


def Instr_STSH(Rd, register):
    # Execute STSH instruction
    register[Rd + 4] = register[Rd]
    register[9] = "{0:08b}".format(int(register[9], base=2) + 1)
    return


def main():
    print("Project 3 - ISA Simulator")

    # Choose Pattern (i.e. which data memory to use)
    print("Choose Pattern/Data Memory used for the simulation")
    print("(i.e. patternA.txt)")

    while (True):
        filename = input("Data Memory Filename: ")
        #filename = "patternA.txt"
        #filename = "patternB.txt"

        # Check if the file exist
        try:
            d_mem = open(filename, "r")
            data = d_mem.readlines()
            # remove newline character
            for i in range(0, len(data)):
                data[i] = data[i][0:len(data[i]) - 1]
            d_mem.close()
            print("\n")
            break
        except FileNotFoundError:
            print(filename + " does not exist")

    # The variable registers is an array containing the initial bit string values of the registers
    # registers[0] = 16-bit R0 register
    # registers[1] = 16-bit R1 register
    # registers[2] = 16-bit R2 register
    # registers[3] = 16-bit R3 register
    # registers[4] = 16-bit SR0 register
    # registers[5] = 16-bit SR1 register
    # registers[6] = 16-bit SR2 register
    # registers[7] = 16-bit SR3 register
    # registers[8] = 1-bit branch register
    # registers[9] = 16-bit PC
    register = Initialize_Registers()

    print("Program 1 - Modular Exponentiation")
    # Initialize to which instruction memory to read from.
    #instr_mem_filename = "p1_Machine_Code.asm"
    instr_mem = open("p3_group_1_p1_imem.txt", "r")
    instructions = instr_mem.readlines()
    instr_mem.close()

    # Run Program 1
    end_of_program = False
    instr_count_1 = 0;
    print("Start of Program 1 Execution")
    while (not end_of_program):
        # Fetch instruction and update PC
        PC = int(register[9], base=2)
        instr =  instructions[PC][0:len(instructions[PC]) - 1]
        end_of_program = Instruction_Execute(instr, register, data)
        instr_count_1 = instr_count_1 + 1
    print("End of Program 1 Execution")

    print("\n")
    register = Initialize_Registers()
    print("Program 2 - Best Match Count")
    # Initialize to which instruction memory to read from.
    #instr_mem_filename = "p1_Machine_Code.asm"
    instr_mem = open("p3_group_1_p2_imem.txt", "r")
    instructions = instr_mem.readlines()
    instr_mem.close()


    # Run Program 2
    end_of_program = False
    instr_count_2 = 0;
    #i = 1
    print("Start of Program 2 Execution")
    while (not end_of_program):
        # Fetch instruction and update PC
        PC = int(register[9], base=2)
        instr =  instructions[PC][0:len(instructions[PC]) - 1]
        end_of_program = Instruction_Execute(instr, register, data)
        instr_count_2 = instr_count_2 + 1
        #r0 = int(register[0], base=2)
        #r0 = r0 - ((r0 << 1) & (2**16))
        #print("r0 = {}".format(r0))
        #print("r0 = " + register[0])
        #print("r1 = {}".format(int(register[1], base=2)))
        #print("r2 = {}".format(int(register[2], base=2)))
        #print("r3 = {}".format(int(register[3], base=2)))
        #print("sr1 = {}".format(int(register[1+4], base=2)))
        #print("sr2 = {}".format(int(register[2+4], base=2)))
        #print("branch = {}".format(int(register[8], base=2)))
        #print("PC = {}".format(int(register[9], base=2)))
        #print("instr: " + instr)
        #print("instr: {}\n".format(i))
        #i = i + 1
    print("End of Program 2 Execution\n")

    # Update registers
    Update_Reg_File(register)
    # Update Data Memory File/Pattern
    Update_Data_Mem_File(data, filename)
    # Summary
    print("---Summary of Execution---------------------")
    print("Dynamic Instruction Count For Program 1: {} instructions".format(instr_count_1))
    print("Dynamic Instruction Count For Program 2: {} instructions".format(instr_count_2))
    print("---End of Summary---------------------------")

    return


if __name__ == '__main__':
    main()
