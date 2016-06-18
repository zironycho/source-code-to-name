# -*- coding: utf-8 -*-
import ast
import subprocess


def extract_feature(path):
	code_tree = _parse_code(path)
	if not code_tree:
		code_tree = _parse_code(path, py2topy3=True)
		if not code_tree:
			return []

	func_listener = FuncListener()
	func_listener.visit(node=code_tree)
	return func_listener.get_func_features()


def _parse_code(path, py2topy3=False):
	if py2topy3:
		popen = subprocess.Popen(['2to3', '-w', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		popen.communicate()
	try:
		with open(path, 'rt') as f:
			return ast.parse(f.read())
	except SyntaxError:
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
