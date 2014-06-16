import ast


ERR_NO_PARAM_TEMPLATE = "Function %s is missing sphinx doc for argument %s (%s:%i)"


class FindDocstrings(ast.NodeVisitor):
    """
    AST visitor to find functions with incomplete docstrings.

    Currently checks to see that all parameters are mentioned in docstring.
    """

    def __init__(self, src_filename):
        """
        Initialize doc checker

        :param src_filename: filename of source to check
        """

        self.src_filename = src_filename
        self.error_list = []

    def generic_visit(self, node):
        """
        visits any non-function AST node

        :param node: AST node to visit
        """

        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        """
        visits FunctionDef AST nodes and does docstring checks

        :param node: AST node to visit
        """

        docstring = ast.get_docstring(node)
        if node.args:
            arglist = node.args.args
            for param in arglist:
                if param.id == 'self' or param.id == 'cls':
                    continue
                # if there is no docstring, just keep going. It will get caught
                # by pep257 checks
                if docstring and param.id not in docstring and 'See super' not in docstring:
                    self.error_list.append(ERR_NO_PARAM_TEMPLATE %
                                           (node.name, param.id, self.src_filename, param.lineno))

        ast.NodeVisitor.generic_visit(self, node)


class RunDocstringCheck():
    """
    Wrapper for FindDocstrings.
    """

    def check(self, src_filename):
        """
        checks docstrings for a file

        :param src_filename: source filename to check
        """
        self.finder = FindDocstrings(src_filename)
        with open(src_filename) as src_fd:
            src_str = file.read(src_fd)
            root_node = ast.parse(src_str, filename=src_filename)
            self.finder.visit(root_node)

    def get_errors(self):
        """
        return found errors
        """
        return self.finder.error_list
