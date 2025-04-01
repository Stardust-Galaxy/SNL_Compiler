"""
@author: Stardust-Galaxy
@software: PyCharm
@file: codegenerator.py
@time: 2024/10/14
"""

from Parser.AST import *
from Analyzer.semantic import Analyzer
from Analyzer.symbol import *


class CodeGenerator:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.root = analyzer.root
        self.current = self.root
        self.data_section = []    # MIPS .data section
        self.text_section = []    # MIPS .text section
        self.label_counter = 0
        self.scope = analyzer.scope
        self.current_proc = None
        self.var_offsets = {}     # Maps variables to stack offsets
        self.stack_offset = 0     # Current stack offset
        self.reg_map = {}         # Maps temporary variables to registers
        self.next_temp_reg = 0    # Next available temporary register

    def generate_label(self):
        """Generate a unique label for jumps."""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label

    def get_temp_reg(self):
        """Get next available temporary register."""
        reg = f"$t{self.next_temp_reg}"
        self.next_temp_reg = (self.next_temp_reg + 1) % 10  # t0-t9
        return reg

    def emit_data(self, instruction):
        """Add an instruction to the data section."""
        self.data_section.append(instruction)

    def emit_text(self, instruction):
        """Add an instruction to the text section."""
        self.text_section.append(instruction)

    def generate_code(self):
        """Start code generation from the root of AST."""
        # Setup data section
        self.emit_data(".data")
        self.emit_data("newline: .asciiz \"\\n\"")

        # Setup text section
        self.emit_text(".text")
        self.emit_text(".globl main")
        self.emit_text("# Entry point")
        self.emit_text("j main")  # Add this jump to main

        # Process program
        self.current = self.root.firstChild()
        self.program_head()
        self.declare_part()

        # Add main label for program body
        self.emit_text("main:")
        self.emit_text("    # Setup stack frame")
        self.emit_text("    subu $sp, $sp, 4")
        self.emit_text("    sw $ra, 0($sp)  # Save return address")

        self.program_body()

        # Program exit
        self.emit_text("    # Program exit")
        self.emit_text("    lw $ra, 0($sp)  # Restore return address")
        self.emit_text("    addu $sp, $sp, 4")
        self.emit_text("    li $v0, 10")
        self.emit_text("    syscall")

        # Combine data and text sections
        return self.data_section + ["\n"] + self.text_section

    def program_head(self):
        """Process program header."""
        self.stepInto("ProgramName")
        self.stepInto("ID")
        prog_name = self.current.getTokenVal()
        self.emit_text(f"# Program: {prog_name}")

    def declare_part(self):
        """Process declarations."""
        self.stepInto("DeclarePart")
        self.type_dec()
        self.var_dec()
        self.proc_dec()

    def type_dec(self):
        """Process type declarations."""
        self.stepInto("TypeDec")
        self.step()
        if self.current.isTokenType("ε"):
            return
        self.stepInto("TypeDecList")
        while True:
            if self.current.isTokenType("TypeDecMore") and self.current.firstChild().isTokenType("ε"):
                break
            self.stepInto("TypeId")
            self.stepInto("ID")
            type_name = self.current.getTokenVal()
            self.emit_text(f"# Type {type_name} declaration")
            self.stepInto("TypeDecMore")

    def var_dec(self):
        """Process variable declarations."""
        self.stepInto("VarDec")
        self.step()
        if self.current.isTokenType("ε"):
            return
        self.stepInto("VarDecList")
        while True:
            if self.current.isTokenType("VarDecMore") and self.current.firstChild().isTokenType("ε"):
                break
            # Get type information
            type_name = self.type_name()
            self.stepInto("VarIdList")
            while True:
                if self.current.isTokenType("VarIdMore") and self.current.firstChild().isTokenType("ε"):
                    break
                self.stepInto("ID")
                var_name = self.current.getTokenVal()

                # Only add to data section if this is a global variable
                if self.current_proc is None:
                    self.emit_data(f"{var_name}: .word 0")

                self.stepInto("VarIdMore")
            self.stepInto("VarDecMore")

    def proc_dec(self):
        """Process procedure declarations."""
        self.stepInto("ProcDec")
        self.step()
        if self.current.isTokenType("ε"):
            return

        while True:
            if self.current.isTokenType("ProcDecMore") and self.current.firstChild().isTokenType("ε"):
                break

            self.stepInto("ProcName")
            self.step()
            proc_name = self.current.getTokenVal()
            self.current_proc = proc_name

            # Generate procedure entry
            self.emit_text(f"{proc_name}:")
            self.emit_text("    # Setup stack frame")
            self.emit_text("    subu $sp, $sp, 8")
            self.emit_text("    sw $ra, 0($sp)  # Save return address")
            self.emit_text("    sw $fp, 4($sp)  # Save frame pointer")
            self.emit_text("    move $fp, $sp   # Setup new frame pointer")

            # Find the procedure's scope
            new_sym_tab = None
            for scope in self.scope:
                for sym in scope:
                    if sym.name == proc_name and sym.decKind == "procDec":
                        proc_idx = self.scope.index(scope)
                        if proc_idx + 1 < len(self.scope):
                            new_sym_tab = self.scope[proc_idx + 1]
                        break
                if new_sym_tab:
                    break

            # Save current symbol table and collect local variables
            old_sym_tab = self.analyzer.symTable
            local_vars = []

            # Set symbol table to procedure's scope if found
            if new_sym_tab:
                self.analyzer.symTable = new_sym_tab

                # Process local variables
                for sym in self.analyzer.symTable:
                    if sym.decKind == "varDec":
                        local_vars.append(sym.name)
                        var_key = f"{proc_name}.{sym.name}"
                        self.var_offsets[var_key] = -4 * (len(local_vars))

            # Process procedure declarations
            self.stepInto("ProcDecPart")
            self.declare_part()

            # Allocate stack space for local variables right after frame setup
            if local_vars:
                local_vars_size = len(local_vars) * 4
                self.emit_text(f"    # Allocate space for {len(local_vars)} local variables")
                self.emit_text(f"    subu $sp, $sp, {local_vars_size}")
                # Initialize local variables to zero if needed
                for var_name in local_vars:
                    offset = self.var_offsets[f"{proc_name}.{var_name}"]
                    self.emit_text(f"    # Initialize local var {var_name}")
                    self.emit_text(f"    li $t0, 0")
                    self.emit_text(f"    sw $t0, {offset}($fp)")

            # Process procedure body
            self.stepInto("ProcBody")
            self.program_body()

            # Generate procedure exit
            self.emit_text("    # Procedure exit")
            self.emit_text("    move $sp, $fp   # Restore stack pointer")
            self.emit_text("    lw $fp, 4($sp)  # Restore frame pointer")
            self.emit_text("    lw $ra, 0($sp)  # Restore return address")
            self.emit_text("    addu $sp, $sp, 8")
            self.emit_text("    jr $ra          # Return to caller")

            # Reset current procedure and symbol table
            self.current_proc = None
            self.analyzer.symTable = old_sym_tab
            self.stepInto("ProcDecMore")

    def program_body(self):
        """Process program body."""
        self.stepInto("BEGIN")
        self.stm_list()
        self.stepInto("END")

    def stm_list(self):
        """Process statement list."""
        self.stepInto("StmList")

        while True:
            self.stepInto("Stm")
            cur_stm = self.current.firstChild().getTokenType()

            if cur_stm == "ConditionalStm":
                self.process_conditional_stmt()
            elif cur_stm == "LoopStm":
                self.process_loop_stmt()
            elif cur_stm == "InputStm":
                self.process_input_stmt()
            elif cur_stm == "OutputStm":
                self.process_output_stmt()
            elif cur_stm == "ReturnStm":
                self.process_return_stmt()
            elif cur_stm == "ID":
                self.process_id_stmt()

            self.stepInto("StmMore")
            if self.current.firstChild().isTokenType("ε"):
                break

    def process_conditional_stmt(self):
        """Process if-then-else statement."""
        self.stepInto("ConditionalStm")
        self.stepInto("IF")

        # Generate labels for jumps
        else_label = self.generate_label()
        end_label = self.generate_label()

        # Process condition (result will be in $t0)
        self.rel_exp()

        # Branch if condition is false
        self.emit_text(f"    beqz $t0, {else_label}")

        # Process then part
        self.stepInto("THEN")
        self.stm_list()
        self.emit_text(f"    j {end_label}")

        # Process else part
        self.emit_text(f"{else_label}:")
        self.stepInto("ELSE")
        self.stm_list()

        # End of if statement
        self.emit_text(f"{end_label}:")
        self.stepInto("FI")

    def process_loop_stmt(self):
        """Process while-do statement."""
        self.stepInto("LoopStm")
        self.stepInto("WHILE")

        # Generate labels
        start_label = self.generate_label()
        end_label = self.generate_label()

        # Start of loop
        self.emit_text(f"{start_label}:")

        # Process condition (result will be in $t0)
        self.rel_exp()

        # Branch if condition is false
        self.emit_text(f"    beqz $t0, {end_label}")

        # Process loop body
        self.stepInto("DO")
        self.stm_list()

        # Jump back to condition check
        self.emit_text(f"    j {start_label}")

        # End of loop
        self.emit_text(f"{end_label}:")
        self.stepInto("ENDWH")

    def process_input_stmt(self):
        """Process read statement."""
        self.stepInto("InputStm")
        self.stepInto("READ")
        self.stepInto("Invar")
        self.stepInto("ID")
        var_name = self.current.getTokenVal()

        # Read integer from console
        self.emit_text("    # Read integer input")
        self.emit_text("    li $v0, 5")
        self.emit_text("    syscall")

        # Store result in variable
        self.emit_text(f"    sw $v0, {var_name}")

    def process_output_stmt(self):
        """Process write statement."""
        self.stepInto("OutputStm")
        self.stepInto("WRITE")

        # Evaluate expression (result in $t0)
        self.expression()

        # Write integer to console
        self.emit_text("    # Write integer output")
        self.emit_text("    move $a0, $t0")
        self.emit_text("    li $v0, 1")
        self.emit_text("    syscall")

        # Print newline
        self.emit_text("    la $a0, newline")
        self.emit_text("    li $v0, 4")
        self.emit_text("    syscall")

    def process_return_stmt(self):
        """Process return statement."""
        self.stepInto("ReturnStm")
        self.stepInto("RETURN")

        # Evaluate expression (result in $t0)
        self.expression()

        # Move result to return value register
        self.emit_text("    move $v0, $t0")

        # Return will be handled by procedure epilogue

    def process_id_stmt(self):
        """Process ID statement (assignment or call)."""
        self.stepInto("ID")
        id_name = self.current.getTokenVal()
        self.stepInto("AssCall")
        self.step()
        decision = self.current.getTokenType()

        if decision == "AssignmentRest":
            # Assignment statement
            target = self.process_variable(id_name)
            self.stepInto(":=")

            # Evaluate expression (result in $t0)
            self.expression()

            # In process_id_stmt method, modify the storage logic:
            # Store result in variable
            if "[" in target or "." in target:
                # Complex variable access (array or record element)
                self.emit_text(f"    # Assignment to {target}")
                self.emit_text(f"    sw $t0, {target}")
            else:
                # Simple variable - could be local or global
                if self.current_proc and f"{self.current_proc}.{id_name}" in self.var_offsets:
                    offset = self.var_offsets[f"{self.current_proc}.{id_name}"]
                    self.emit_text(f"    # Store to local var {id_name}")
                    self.emit_text(f"    sw $t0, {offset}($fp)")
                else:
                    self.emit_text(f"    sw $t0, {id_name}")

        elif decision == "CallStmRest":
            # Procedure call
            self.emit_text(f"    # Call to procedure {id_name}")

            # Save temporary registers if needed
            self.emit_text("    # Save temporary registers")
            self.emit_text("    subu $sp, $sp, 40")  # Space for t0-t9
            for i in range(10):
                self.emit_text(f"    sw $t{i}, {i*4}($sp)")

            # Prepare parameters
            param_index = 0
            self.stepInto("CallStmRest")
            self.stepInto("ActParamList")
            self.step()

            if not self.current.isTokenType("ε"):
                while True:
                    if (self.current.isTokenType("ActParamMore") and
                            self.current.firstChild().isTokenType("ε")):
                        break

                    # Evaluate parameter expression (result in $t0)
                    self.expression()

                    # Move to argument register
                    if param_index < 4:
                        self.emit_text(f"    move $a{param_index}, $t0")
                    else:
                        # Parameters beyond 4 go on stack
                        self.emit_text(f"    subu $sp, $sp, 4")
                        self.emit_text(f"    sw $t0, 0($sp)")

                    param_index += 1
                    self.stepInto("ActParamMore")

            # Call procedure
            self.emit_text(f"    jal {id_name}")

            # Clean up stack if needed
            if param_index > 4:
                excess_params = param_index - 4
                self.emit_text(f"    addu $sp, $sp, {excess_params * 4}")

            # Restore temporary registers
            self.emit_text("    # Restore temporary registers")
            for i in range(10):
                self.emit_text(f"    lw $t{i}, {i*4}($sp)")
            self.emit_text("    addu $sp, $sp, 40")

    def process_variable(self, var_name=None):
        """Process variable access."""
        if var_name is None:
            self.stepInto("Variable")
            self.stepInto("ID")
            var_name = self.current.getTokenVal()

        # Check if it's a local variable in current procedure
        local_var_key = f"{self.current_proc}.{var_name}" if self.current_proc else None
        is_local = self.current_proc and local_var_key in self.var_offsets

        self.stepInto("VariMore")
        self.step()
        choice = self.current.getTokenType()

        if choice == "ε":
            # Simple variable access
            if is_local:
                # Local variable - use stack offset
                offset = self.var_offsets[local_var_key]
                self.emit_text(f"    # Access local var {var_name}")
                self.emit_text(f"    lw $t0, {offset}($fp)")
                return f"{offset}($fp)"
            else:
                # Global variable
                self.emit_text(f"    lw $t0, {var_name}")
                return var_name
        elif choice == "[":
            # Array access
            base_reg = "$t1"
            if is_local:
                offset = self.var_offsets[local_var_key]
                self.emit_text(f"    # Local array access {var_name}[...]")
                self.emit_text(f"    addi {base_reg}, $fp, {offset}")
            else:
                self.emit_text(f"    # Global array access {var_name}[...]")
                self.emit_text(f"    la {base_reg}, {var_name}")

            # Process index - must handle local vars in index expression too
            self.stepInto("Exp")
            self.expression()  # Result in $t0

            # Calculate element address
            self.emit_text("    sll $t0, $t0, 2")  # Multiply by 4
            self.emit_text(f"    add {base_reg}, {base_reg}, $t0")
            self.emit_text(f"    lw $t0, 0({base_reg})")

            return f"0({base_reg})"
        elif choice == ".":
            # Record field access - simplified implementation
            self.stepInto("FieldVar")
            self.stepInto("ID")
            field_name = self.current.getTokenVal()

            if self.current_proc and local_var_key in self.var_offsets:
                offset = self.var_offsets[local_var_key]
                self.emit_text(f"    # Local record access {var_name}.{field_name}")
                self.emit_text(f"    addi $t1, $fp, {offset}")
            else:
                self.emit_text(f"    # Global record access {var_name}.{field_name}")
                self.emit_text(f"    la $t1, {var_name}")

            # This is simplified - would need field offset calculation
            self.emit_text("    lw $t0, 0($t1)")

            return f"{var_name}.{field_name}"

    def rel_exp(self):
        """Process relational expression."""
        self.stepInto("RelExp")

        # Evaluate left expression (result in $t0)
        self.expression()

        # Save left result
        self.emit_text("    move $t2, $t0")

        # Get comparison operator
        self.stepInto("CmpOp")
        self.step()
        op = self.current.getTokenVal()

        # Evaluate right expression (result in $t0)
        self.expression()

        # Perform comparison based on operator
        if op == "<":
            self.emit_text("    slt $t0, $t2, $t0")
        elif op == "=":
            self.emit_text("    seq $t0, $t2, $t0")
        elif op == ">":
            self.emit_text("    sgt $t0, $t2, $t0")
        else:
            self.emit_text(f"    # Unsupported operator: {op}")
            self.emit_text("    li $t0, 0")

    def expression(self):
        """Process expression."""
        self.stepInto("Exp")

        # Evaluate first term (result in $t0)
        self.term()

        self.stepInto("OtherTerm")
        while True:
            if self.current.isTokenType("OtherTerm") and self.current.firstChild().isTokenType("ε"):
                break

            # Save first term result
            self.emit_text("    move $t2, $t0")

            # Get operator
            self.stepInto("AddOp")
            self.step()
            op = self.current.getTokenVal()

            # Evaluate second term (result in $t0)
            self.stepInto("Exp")
            self.term()

            # Perform operation
            if op == "+":
                self.emit_text("    add $t0, $t2, $t0")
            elif op == "-":
                self.emit_text("    sub $t0, $t2, $t0")
            else:
                self.emit_text(f"    # Unsupported operator: {op}")

            self.stepInto("OtherTerm")

    def term(self):
        """Process term."""
        self.stepInto("Term")

        # Evaluate first factor (result in $t0)
        self.factor()

        self.stepInto("OtherFactor")
        while True:
            if self.current.isTokenType("OtherFactor") and self.current.firstChild().isTokenType("ε"):
                break

            # Save first factor result
            self.emit_text("    move $t2, $t0")

            # Get operator
            self.stepInto("MultOp")
            self.step()
            op = self.current.getTokenVal()

            # Evaluate second factor (result in $t0)
            self.stepInto("Term")
            self.factor()

            # Perform operation
            if op == "*":
                self.emit_text("    mul $t0, $t2, $t0")
            elif op == "/":
                self.emit_text("    div $t2, $t0")
                self.emit_text("    mflo $t0")
            else:
                self.emit_text(f"    # Unsupported operator: {op}")

            self.stepInto("OtherFactor")

    def factor(self):
        """Process factor."""
        self.stepInto("Factor")
        self.step()
        choice = self.current.getTokenType()

        if choice == "(":
            # Parenthesized expression
            self.expression()
            self.stepInto(")")
        elif choice == "INTC":
            # Integer constant
            value = self.current.getTokenVal()
            self.emit_text(f"    li $t0, {value}")
        elif choice == "Variable":
            # Variable access - will handle local/global distinction
            self.process_variable()

    def type_name(self):
        """Process type name."""
        self.stepInto("TypeName")
        choice = self.current.firstChild().getTokenType()
        self.stepInto(choice)

        if choice == "ID":
            return self.current.getTokenVal()
        elif choice == "BaseType":
            return self.base_type()
        elif choice == "StructureType":
            struct_type = self.current.firstChild().getTokenType()
            self.stepInto(struct_type)

            if struct_type == "ArrayType":
                return self.array_type()
            elif struct_type == "RecType":
                return "record"

        return None

    def base_type(self):
        """Process base type."""
        self.stepInto("BaseType")
        self.step()
        return self.current.getTokenType()

    def array_type(self):
        """Process array type."""
        self.stepInto("Low")
        self.stepInto("INTC")
        low = self.current.getTokenVal()
        self.stepInto("Top")
        self.stepInto("INTC")
        top = self.current.getTokenVal()
        self.stepInto("BaseType")
        self.step()
        element_type = self.current.getTokenType()

        array_size = top - low + 1
        return f"array[{array_size}]"

    def step(self):
        """Move to next node in AST."""
        if self.current.isEmpty():
            self.current = self.current.step()
        else:
            self.current = self.current.firstChild()

    def stepInto(self, token_type):
        """Step into a specific token type."""
        while not self.current.isTokenType(token_type):
            self.step()


def main():
    """Main function to compile SNL to MIPS assembly."""
    from Parser.LL1 import generateAST
    from Lexer.scanner import Scan
    import sys

    if len(sys.argv) < 2:
        print("Usage: python codegenerator.py input_file [output_file]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.asm"

    try:
        # Lexical analysis
        with open(input_file, "r") as f:
            scanner = list(f.read())
        tokens = Scan(scanner)

        # Save tokens to lexer output
        lexer_output = input_file + "-Lexer.txt"
        with open(lexer_output, "w") as out:
            for token in tokens:
                out.write(str(token) + "\n")

        # Parse to generate AST
        token_strings = [str(token) for token in tokens]
        root = generateAST(token_strings)

        # Semantic analysis
        analyzer = Analyzer(tokens, root)
        analyzer.analyze()

        if analyzer.error:
            print("Semantic errors found. Code generation aborted.")
            sys.exit(1)

        # Code generation
        generator = CodeGenerator(analyzer)
        code = generator.generate_code()

        # Write generated code to file
        with open(output_file, "w") as f:
            for line in code:
                f.write(line + "\n")

        print(f"MIPS code generation complete. Output written to {output_file}")

    except Exception as e:
        print(f"Error during compilation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()