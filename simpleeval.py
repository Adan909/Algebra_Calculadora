import ast
import operator


class SimpleEval:
    """Evaluador matemático seguro con la interfaz mínima que usa este proyecto."""

    _default_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
    }

    def __init__(self, names=None, functions=None, operators=None):
        self.names = {} if names is None else dict(names)
        self.functions = {} if functions is None else dict(functions)
        self.operators = self._default_operators.copy()
        if operators:
            self.operators.update(operators)

    def parse(self, expression):
        return ast.parse(expression, mode="eval").body

    def eval(self, expression, previously_parsed=None):
        node = previously_parsed if previously_parsed is not None else ast.parse(expression, mode="eval").body
        return self._eval_node(node)

    def _eval_node(self, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool):
                return node.value
            if isinstance(node.value, (int, float)):
                return float(node.value) if isinstance(node.value, float) else float(node.value)
            raise ValueError(f"Constante no válida: {node.value!r}")

        if isinstance(node, ast.Name):
            if node.id in self.names:
                return self.names[node.id]
            raise ValueError(f"Nombre no permitido: {node.id}")

        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)
            if op_type not in self.operators:
                raise ValueError(f"Operador no permitido: {type(node.op).__name__}")
            return self.operators[op_type](left, right)

        if isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op_type = type(node.op)
            if op_type not in self.operators:
                raise ValueError(f"Operador unario no permitido: {type(node.op).__name__}")
            return self.operators[op_type](operand)

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Solo se permiten llamadas a funciones con nombre.")
            name = node.func.id
            if name in self.functions:
                func = self.functions[name]
            elif name in self.names and callable(self.names[name]):
                func = self.names[name]
            else:
                raise ValueError(f"Función no permitida: {name}")
            if node.keywords:
                raise ValueError("No se admiten argumentos con nombre.")
            args = [self._eval_node(arg) for arg in node.args]
            return func(*args)

        if isinstance(node, ast.Compare):
            left = self._eval_node(node.left)
            for op, comparator in zip(node.ops, node.comparators):
                right = self._eval_node(comparator)
                op_type = type(op)
                if op_type not in self.operators:
                    raise ValueError(f"Comparación no permitida: {type(op).__name__}")
                if not self.operators[op_type](left, right):
                    return False
                left = right
            return True

        if isinstance(node, ast.Tuple):
            return tuple(self._eval_node(item) for item in node.elts)

        if isinstance(node, ast.List):
            return [self._eval_node(item) for item in node.elts]

        raise ValueError(f"Expresión no soportada: {type(node).__name__}")
