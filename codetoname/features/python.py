# -*- coding: utf-8 -*-
import os
import ast
import subprocess
import tempfile

from codetoname.features.language import language_to_extension


def extract_feature(path):
    code_tree = _parse_code(path)
    if not code_tree:
        code_tree = _parse_code(path, py2topy3=True)
        if not code_tree:
            return []

    func_listener = FuncListener()
    func_listener.visit(node=code_tree)
    return func_listener.get_func_features()


def extract_feature_from_code(code):
    ext = language_to_extension('python')
    temp = tempfile.mktemp(prefix=__name__, suffix=ext)

    with open(temp, 'wt') as f:
        f.write(code)
        f.close()

    feature = extract_feature(temp)
    os.remove(temp)
    return feature


def _parse_code(path, py2topy3=False):
    if py2topy3:
        popen = subprocess.Popen(['2to3', '-w', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        popen.communicate()
    try:
        with open(path, 'rt') as f:
            return ast.parse(f.read())
    except SyntaxError as e:
        print(e)
        return False
    except UnicodeDecodeError as e:
        print(path)
        print(e)
    except FileNotFoundError as e:
        print(path)
        print(e)
        return False


class FuncListener(ast.NodeVisitor):
    def __init__(self):
        self.funcs = []

    def visit_FunctionDef(self, node):
        self.funcs.append({
            'name': node.name,
            'body': [line.__class__.__name__ for line in node.body],
        })
        self.generic_visit(node)

    def get_func_features(self):
        return self.funcs
