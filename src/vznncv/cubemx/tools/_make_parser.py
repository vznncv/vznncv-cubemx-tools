import re


class MakeParser:
    """
    Limited Makefile parser to extract declared variables from makefile.
    """
    # directives dictionary
    # key - opening directive
    # value - closing directive (None if it's one line directive)
    _MAKE_DIRECTIVES = {
        'include': None,
        '-include': None,
        'define': 'endef',
        'ifeq': 'endif',
        'ifneq': 'endif',
        'ifdef': 'endif',
        'ifndef': 'endif',
        'vpath': None
    }

    def _extract_lines(self, makefile):
        if isinstance(makefile, str):
            with open(makefile, encoding='utf-8') as f:
                lines = f.readlines()
        else:
            # assume that makefile is file like object
            lines = makefile.readlines()
        lines = [line.rstrip('\n') for line in lines]
        return lines

    def _remove_comments_and_empty_lines(self, lines):
        res_lines = []
        for line in lines:
            m = re.search(r'(?<!\\)#', line)
            if m is not None:
                line = line[:m.pos]
            if not (line.isspace() or not line):
                res_lines.append(line)

        return res_lines

    def _remove_directives(self, lines):
        """
        Remove directives from makefile lines.

        Note: empty lines should be deleted before invocation of this method.
        """
        res_lines = []
        dir_stack = []
        for line in lines:
            line_start = line.split(maxsplit=1)[0]
            if line_start in self._MAKE_DIRECTIVES:
                dir_end = self._MAKE_DIRECTIVES[line_start]
                if dir_end is not None:
                    dir_stack.append(dir_end)
            elif dir_stack and dir_stack[-1] == line_start:
                dir_stack.pop()
            elif not dir_stack:
                res_lines.append(line)

        return res_lines

    def _unite_lines(self, lines):
        """
        Unite lines that are split with '\' symbol
        """
        res_lines = []
        merge_with_previous = False
        for line in lines:
            line = line.rstrip()
            processed_line = line.rstrip('\\').rstrip()
            if merge_with_previous:
                res_lines[-1].append(processed_line)
            else:
                res_lines.append([processed_line])

            merge_with_previous = line.endswith('\\')

        return [' '.join(line) for line in res_lines]

    def parse_variables(self, makefile):
        """
        Get dictionary with make variables, that are declared in the ``makefile``

        :param makefile: path or file-like object
        :return: dictionary with variables
        """
        lines = self._extract_lines(makefile)

        # preprocess make lines for variable searching and parsing
        lines = self._remove_comments_and_empty_lines(lines)
        lines = self._remove_directives(lines)
        lines = self._unite_lines(lines)

        make_vars = {}
        for line in lines:
            m = re.match(r'^(?P<var_name>[a-zA-Z_-][a-zA-Z_-]*)\s*(?P<var_op>=|\+=)\s*(?P<var_value>.*)$', line)
            if m is None:
                continue
            var_value = m.group('var_value')
            var_value = re.sub(
                r'\$[{(](?P<var_name>[^})]+)[})]',
                lambda m: make_vars.get(m.group('var_name'), ''),
                var_value
            )
            var_name = m.group('var_name')
            var_op = m.group('var_op')
            if var_op == '=':
                make_vars[var_name] = var_value
            elif var_op == '+=':
                if var_name not in make_vars:
                    raise ValueError('"{} +=" usage before variable definition'.format(var_name))
                make_vars[var_name] = "{} {}".format(make_vars[var_name], var_value)
            else:
                raise ValueError("Unknown operation: {}".format(var_op))

        return make_vars


def parse_variables(makefile):
    """
    Parse makefile and extract declared variables.

    .. note:: the parsed ignores any make declaration and has limited support of the variable expansion

    :param makefile: makefile path or file-like object
    :return: dictionary with extracted variables
    """
    return MakeParser().parse_variables(makefile)
