from sherlock.errors import ParamTypeMismatchError
from sherlock.codelib.analyzer import CodeAnalyzer


def analysis_code_list(code_list):
    analyzer = CodeAnalyzer('\n'.join(code_list))
    return analyzer.analysis().generate()

def test_simple_add_string_and_number_anlyzer():
    code = [
        'a = 2 + "Hello"',
    ]
    assert analysis_code_list(code) == 'export a=2"Hello"'

def test_simple_add_numbers_anlyzer():
    code = [
        'a = 2 + 3',
    ]
    analyzer = CodeAnalyzer('\n'.join(code))
    code = analyzer.analysis().generate()
    assert code == 'export a=$(( 2 + 3 ))'

def test_add_string_variable_and_number():
    code = [
        'b = "Hello"',
        'a = 2 + b',
    ]
    assert analysis_code_list(code) == """export b="Hello"
export a=2$b"""

def test_complex_add():
    code = [
        'a = 2 + (3 + 4) + 6',
    ]
    assert analysis_code_list(code) == 'export a=$(( $(( 2 + $(( 3 + 4 )) )) + 6 ))'

def test_complex_numeric_operation():
    code = [
        'a = 2 + (3 - 4) * 6 / 2',
    ]
    assert analysis_code_list(code) == 'export a=$(( 2 + $(( $(( $(( 3 - 4 )) * 6 )) / 2 )) ))'

def test_run_command_line_command():
    code = [
        'git("commit", "-m", "Hello")',
    ]
    assert analysis_code_list(code) == 'git "commit" "-m" "Hello"'

def test_function_return_type_anlyzer():
    code = [
        'def echo(msg):',
        '    return 1',
        'a = echo("Hi")'
    ]
    assert analysis_code_list(code) == """function echo() {
local msg=$1
export __return_echo=1
}
echo "Hi"
export a=$__return_echo"""

def test_simple_numeric_operation_with_function_call():
    code = [
        'def a():',
        '    return 1',
        'b = a() + 3',
    ]
    assert analysis_code_list(code) == 'export a=$(( 2 + $(( $(( $(( 3 - 4 )) * 6 )) / 2 )) ))'

# def test_complex_numeric_operation_with_function_call():
#     code = [
#         'def a():',
#         '    return 1',
#         'def b():',
#         '   return 2',
#         'c = b() + (3 - a()) * 6 / 2',
#     ]
#     assert analysis_code_list(code) == 'export a=$(( 2 + $(( $(( $(( 3 - 4 )) * 6 )) / 2 )) ))'

def test_function_parameter_type_mismatch():
    try:
        code = [
            "def echo(msg):",
            "    return 1",
            'echo(1)',
            'a = echo("Hi")'
        ]
        analysis_code_list(code)
    except ParamTypeMismatchError:
        assert True
    else:
        assert False
