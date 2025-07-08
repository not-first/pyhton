from typing import Any, Dict, List
from blessed import Terminal

from .parser import (
    Assignment,
    ASTNode,
    BinaryOp,
    BooleanLiteral,
    ComparisonOp,
    ForLoop,
    FunctionCall,
    FunctionDef,
    Identifier,
    IfStatement,
    LogicalOp,
    NumberLiteral,
    StringLiteral,
    PrintStatement,
    Program,
    Return,
    UnaryOp,
    WhileLoop,
)

term = Terminal()


# class to represent a Python function in the interpreter
class PyhtonFunction:
    def __init__(self, name: str, params: List[str], body: List[ASTNode]):
        self.name = name
        self.params = params
        self.body = body


# class to represent a built-in function
class BuiltinFunction:
    def __init__(self, name: str, func):
        self.name = name
        self.func = func


# class to represent a return exception
class ReturnException(Exception):
    def __init__(self, value: Any):
        self.value = value


# the interpreter class that executes the AST
class Interpreter:
    def __init__(self):
        self.globals: Dict[str, Any] = {}
        self.functions: Dict[str, PyhtonFunction] = {}
        self.locals_stack: List[Dict[str, Any]] = []

        self._register_builtins()

    def _register_builtins(self):
        self.functions["range"] = BuiltinFunction("range", self._builtin_range)

    def _builtin_range(self, args):
        if len(args) == 0 or len(args) > 3:
            raise Exception(f"{term.bold_red}Error{term.normal}range() expects 1 to 3 arguments")

        # make sure all arguments are numbers
        if not all(isinstance(arg, (int, float)) for arg in args):
            raise Exception(f"{term.bold_red}Error{term.normal}range() expects numeric arguments")

        # convert all arguments to integers
        args = [int(arg) for arg in args]

        # handle different number of arguments
        if len(args) == 1:
            return range(0, args[0])  # range(n) -> 0 to n-1
        elif len(args) == 2:
            return range(args[0], args[1])
        else:
            return range(args[0], args[1], args[2])

    # main entry point to interpret a program by executing its statements
    def interpret(self, program: Program):
        for statement in program.statements:
            self._execute(statement)

    # private method to execute a single AST node
    def _execute(self, node: ASTNode) -> Any:
        # if the node is a number,  string or boolean simply return its value

        if isinstance(node, NumberLiteral):
            return node.value

        elif isinstance(node, StringLiteral):
            return node.value

        elif isinstance(node, BooleanLiteral):
            return node.value

        # if the node is a comparison operation, execute it
        elif isinstance(node, ComparisonOp):
            return self._execute_comparison_op(node)

        # if the node is a logical operation, execute it
        elif isinstance(node, LogicalOp):
            return self._execute_logical_op(node)

        # if the node is a unary operation, execute it
        elif isinstance(node, UnaryOp):
            return self._execute_unary_op(node)

        # if the node is a binary operation, execute it
        elif isinstance(node, BinaryOp):
            return self._execute_binary_op(node)

        # if the node is an if statement, execute it
        elif isinstance(node, IfStatement):
            return self._execute_if_statement(node)

        # if the node is a for loop, execute it
        elif isinstance(node, ForLoop):
            return self._execute_for_loop(node)

        # if the node is a while loop, execute it
        elif isinstance(node, WhileLoop):
            return self._execute_while_loop(node)

        # if the node is an identifier, retrieve its value
        elif isinstance(node, Identifier):
            return self._get_variable(node.name)

        # if the node is an assignment, set the variable to the evaluated value
        elif isinstance(node, Assignment):
            value = self._execute(node.value)
            self._set_variable(node.name, value)
            return value

        # if the node is a function definition, store it in the functions dictionary
        elif isinstance(node, FunctionDef):
            self.functions[node.name] = PyhtonFunction(node.name, node.params, node.body)

        # if the node is a function call, execute it
        elif isinstance(node, FunctionCall):
            return self._execute_function_call(node)

        # if the node is a print statement, evaluate the value and print it
        elif isinstance(node, PrintStatement):
            value = self._execute(node.value)
            print(value)

        # if the node is a return statement, raise a ReturnException
        elif isinstance(node, Return):
            value = None
            if node.value:
                value = self._execute(node.value)

            raise ReturnException(value)  # exit the current function and return the value

        else:
            raise Exception(f"Unknown AST node type: {type(node)}")  # raise an error if the node type is not recognized

    # private method to execute a binary operation
    def _execute_binary_op(self, node: BinaryOp) -> Any:
        left = self._execute(node.left)  # evaluate the left side of the operator
        right = self._execute(node.right)  # evaluate the right side of the operator

        # peform the operation based on the operator type
        if node.operator == "+":
            return left + right
        elif node.operator == "-":
            return left - right
        elif node.operator == "*":
            return left * right
        elif node.operator == "/":
            return left / right
        else:
            raise Exception(f"Unknown operator: {node.operator}")

    # private method to execute a comparison operation
    def _execute_comparison_op(self, node: ComparisonOp) -> bool:
        left = self._execute(node.left)
        right = self._execute(node.right)

        if node.operator == "==":
            return left == right
        elif node.operator == "!=":
            return left != right
        elif node.operator == "<":
            return left < right
        elif node.operator == "<=":
            return left <= right
        elif node.operator == ">":
            return left > right
        elif node.operator == ">=":
            return left >= right
        else:
            raise Exception(f"Unknown comparison operator: {node.operator}")

    # private method to execute a logical operation
    def _execute_logical_op(self, node: LogicalOp) -> bool:
        left = self._execute(node.left)

        if node.op_type == "or":
            if left:
                return True
            return bool(self._execute(node.right))
        else:  # node.op_type == "and"
            if not left:
                return False
            return bool(self._execute(node.right))

    # private method to execute an unary operation
    def _execute_unary_op(self, node: UnaryOp) -> Any:
        operand = self._execute(node.operand)

        return not operand

    # private method to execute an if statement
    def _execute_if_statement(self, node: IfStatement) -> Any:
        # evaluate the main condition
        condition = self._execute(node.condition)

        if condition:
            # execute the body
            for statement in node.then_body:
                self._execute(statement)
            return

        # check elif clauses
        for elif_condition, elif_body in node.elif_clauses:
            if self._execute(elif_condition):
                for statement in elif_body:
                    self._execute(statement)
                return

        # if no conditions matched, execute the else body if it exists
        if node.else_body:
            for statement in node.else_body:
                self._execute(statement)

    # private method to execute a for loop
    def _execute_for_loop(self, node: ForLoop) -> Any:
        # evaluate the iterable expression
        iterable = self._execute(node.iterable)

        # check if it's a string or range
        if not isinstance(iterable, (str, range)):
            raise Exception(f"For loop iterable must be a string or range, got {type(iterable).__name__}")

        # create a new local variable scope for the loop variable
        self.locals_stack.append({})

        try:
            for item in iterable:
                # set the loop variable to the current item
                self.locals_stack[-1][node.variable] = item

                # execute each statement in the loop body
                for statement in node.body:
                    self._execute(statement)
        finally:
            self.locals_stack.pop()  # pop the local variables off the stack after execution

    # private method to execute a while loop
    def _execute_while_loop(self, node: WhileLoop) -> Any:
        # create a new local variable scope for the loop
        self.locals_stack.append({})

        try:
            # continue looping while the condition is true
            while self._execute(node.condition):
                # execute each statement in the loop body
                for statement in node.body:
                    self._execute(statement)
        finally:
            self.locals_stack.pop()  # pop the local variables off the stack after execution

    # private method to execute a function call
    def _execute_function_call(self, node: FunctionCall) -> Any:
        # throw an error if the function is not defined
        if node.name not in self.functions:
            raise Exception(f"Unknown function: {node.name}")

        function = self.functions[node.name]  # retrieve the function definition from the functions dictionary

        # evaluate all its arguments
        args = [self._execute(arg) for arg in node.args]

        # handle built-in functions
        if isinstance(function, BuiltinFunction):
            return function.func(args)

        # check parameter count is corerct
        if len(args) != len(function.params):
            raise Exception(f"Function {node.name} expects {len(function.params)} arguments, got {len(args)}")

        # create a new local variable scope for the function call
        local_vars = {}
        for param, arg in zip(function.params, args):
            local_vars[param] = arg

        self.locals_stack.append(local_vars)  # push the local variables onto the stack

        try:
            # execute each statement in the function body
            for statement in function.body:
                self._execute(statement)
            return None

        # if a return statement is encountered, catch the ReturnException and return its value
        except ReturnException as ret:
            return ret.value

        finally:
            self.locals_stack.pop()  # pop the local variables off the stack after execution

    # private method to get a variable's value from the local or global scope
    def _get_variable(self, name: str) -> Any:
        # if the variable is in the local scope, return it
        if self.locals_stack:
            local_vars = self.locals_stack[-1]
            if name in local_vars:
                return local_vars[name]

        # if the variable is not in the local scope, check the global scope
        if name in self.globals:
            return self.globals[name]

        raise Exception(f"Unknown variable: {name}")  # raise an error if the variable is not found in either scope

    # private method to set a variable's value in the local or global scope
    def _set_variable(self, name: str, value: Any):
        # set in local scope if in function, otherwise use global scope
        if self.locals_stack:
            self.locals_stack[-1][name] = value
        else:
            self.globals[name] = value
