from codelib.analyzer import CodeAnalyzer


def test_simple_anlyzer():
    code = [
        'a = 2 + "Hello"',
    ]
    analyzer = CodeAnalyzer('\n'.join(code))
    analyzer.analysis()


def test_function_return_type_anlyzer():
    code = [
	    "def echo(msg):",
		"    return 1",
        'a = echo("Hi")'
    ]
    analyzer = CodeAnalyzer('\n'.join(code))
    analyzer.analysis()
