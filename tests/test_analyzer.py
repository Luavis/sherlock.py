from code.analyzer import CodeAnalyzer


def test_simple_anlyzer():
    code = [
	    "def echo(msg):",
		"    return 1",
		'a = 2 + "Hello"',
		'echo(a)',
    ]
    analyzer = CodeAnalyzer('\n'.join(code))
    analyzer.analysis()
