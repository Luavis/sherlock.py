from tests import analysis_code_list


def test_simple_add_string_and_number_anlyzer():
    code = [
        'a = 2 + "Hello"',
    ]
    assert analysis_code_list(code) == 'export a=2"Hello"\n'

def test_simple_add_numbers_anlyzer():
    code = [
        'a = 2 + 3',
    ]
    assert analysis_code_list(code) == 'export a=$(( 2 + 3 ))\n'

def test_add_string_variable_and_number():
    code = [
        'b = "Hello"',
        'a = 2 + b',
    ]
    assert analysis_code_list(code) == """export b="Hello"
export a=2$b
"""

def test_complex_add():
    code = [
        'a = 2 + (3 + 4) + 6',
    ]
    assert analysis_code_list(code) == 'export a=$(( $(( 2 + $(( 3 + 4 )) )) + 6 ))\n'

def test_complex_numeric_operation():
    code = [
        'a = 2 + (3 - 4) * 6 / 2',
    ]
    assert analysis_code_list(code) == 'export a=$(( 2 + $(( $(( $(( 3 - 4 )) * 6 )) / 2 )) ))\n'

def test_run_command_line_command():
    code = [
        'git("commit", "-m", "Hello")',
    ]
    assert analysis_code_list(code) == 'git "commit" "-m" "Hello"\n'
