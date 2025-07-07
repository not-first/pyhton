from typing import Dict, Any, List, Optional, Callable
from src.parser import (
    ASTNode,
    Program,
    FunctionDef,
    Assignment,
    Return,
    PrintStatement,
    BinaryOp,
    FunctionCall,
    Identifier,
    NumberLiteral,
)


class PyhtonFunction:
    def __init__(self, name: str, params: List[str], body: List[ASTNode]):
        self.name = name
        self.params = params
        self.body = body


class ReturnException(Exception):
    def __init__(self, value: Any):
        self.value = value


class Interpreter:
    def __init__(self, value: Any):
        self.value = value

    def interpret(self, program: Program):
        for statement in program.statements:
            self._execute(statement)

    def _execute(self, node: ASTNode) -> Any:
        if isinstance(node, NumberLiteral):
            return node.value

        elif isinstance(node, Identifier):
            return self._get_variable(node.name)

        elif isinstance(node, BinaryOp):
            return self._execute_binary_op(node)

        elif isinstance(node, Assignment):
            value = self._execute(node.value)
            self._set_variable(node.name, value)
            return value

        elif isinstance(node, FunctionDef):
            self.functions[node.name] = PyhtonFunction(node.name, node.params, node.body)

        elif isinstance(node, FunctionCall):
            return self._execute_function_call(node)

        elif isinstance(node, PrintStatement):
            value = self._execute(node.value)
            print(value)

        elif isinstance(node, Return):
            value = None
            if node.value:
                value = self._execute(node.value)

            raise ReturnException(value)

        else:
            raise Exception(f"Unknown AST node type: {type(node)}")

    def _execute_binary_op(self, node: BinaryOp) -> Any:
        left = self._execute(node.left)
        right = self._execute(node.right)

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

    def _execute_function_call(self, node: FunctionCall) -> Any:
        if node.name not in self.functions:
            raise Exception(f"Unknown function: {node.name}")

        function = self.functions[node.name]

        # evaluate arguments
        args = [self._execute(arg) for arg in node.args]

        # check parameter count
        if len(args) != len(function.params):
            raise Exception(f"Function {node.name} expects {len(function.params)} arguments, got {len(args)}")

        local_vars = {}
        for param, arg in zip(function.params, args):
            local_vars[param] = arg

        self.locals_stack.append(local_vars)

        try:
            for statement in function.body:
                self._execute(statement)
            return None
        except ReturnException as ret:
            return ret.value
        finally:
            self.locals_stack.pop()

    def _get_variable(self, name: str) -> Any:
        if self.locals_stack:
            local_vars = self.locals_stack[-1]
            if name in local_vars:
                return local_vars[name]

        if name in self.globals:
            return self.globals[name]

        raise Exception(f"Unknown variable: {name}")

    def _set_variable(self, name: str, value, Any):
        # set in local scope if in function, otherwise use global scope
        if self.locals_stack:
            self.locals_stack[-1][name] = value
        else:
            self.globals[name] = value
