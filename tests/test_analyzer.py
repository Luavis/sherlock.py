from errors import ParamTypeMismatchError
from codelib.analyzer import CodeAnalyzer


def test_simple_anlyzer():
    code = [
        'a = 2 + "Hello"',
    ]
    analyzer = CodeAnalyzer('\n'.join(code))
    print(analyzer.analysis().generate())

def test_variable_operation():
    code = [
        'b = "Hello"',
        'a = 2 + b',
    ]
    analyzer = CodeAnalyzer('\n'.join(code))
    print(analyzer.analysis().generate())

def test_function_return_type_anlyzer():
    code = [
        "def echo(msg):",
        "    return 1",
        'a = echo("Hi")'
    ]
    analyzer = CodeAnalyzer('\n'.join(code))
    analyzer.analysis().generate()


def test_function_parameter_type_mismatch():
    try:
        code = [
            "def echo(msg):",
            "    return 1",
            'echo(1)',
            'a = echo("Hi")'
        ]
        analyzer = CodeAnalyzer('\n'.join(code))
        analyzer.analysis().generate()
    except ParamTypeMismatchError:
        assert(1)
    else:
        assert(0)
