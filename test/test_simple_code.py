from unittest import TestCase


class AssignmentOperatorTest(TestCase):
	def runTest(self):
		code = "a = 20"
		generator = CodeGenerator()
		generator.generate()
		self.assertEqual()
