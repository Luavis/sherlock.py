from sherlock.errors import ParamTypeMismatchError
from tests import analysis_code_list


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
export a=$__return_echo
"""

def test_simple_numeric_operation_with_function_call():
    code = [
        'def a():',
        '    return 1',
        'b = a() + 3',
    ]
    assert analysis_code_list(code) == """function a() {

export __return_a=1
}
a
__temp_var_1=$__return_a
export b=$(( $__temp_var_1 + 3 ))
"""

def test_complex_numeric_operation_with_function_call():
    code = [
        'def a():',
        '    return 1',
        'c = 3 - a()',
    ]
    assert analysis_code_list(code) == """function a() {

export __return_a=1
}
a
__temp_var_1=$__return_a
export c=$(( 3 - $__temp_var_1 ))
"""

def test_complex_numeric_operation_with_function_call():
    code = [
        'def a():',
        '    return 1',
        'def b():',
        '   return 2',
        'c = b() + (3 - a()) * 6 / 2',
    ]
    assert analysis_code_list(code) == """function a() {

export __return_a=1
}
function b() {

export __return_b=2
}
b
__temp_var_1=$__return_b
a
__temp_var_2=$__return_a
export c=$(( $__temp_var_1 + $(( $(( $(( 3 - $__temp_var_2 )) * 6 )) / 2 )) ))
"""

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

def test_function_call_in_parameter():
    code = [
        "test1(echo('Hi'))",
        "test2(echo('Hi'))",
        "test3(echo('Hi'))",
    ]
    assert analysis_code_list(code) == """echo "Hi"
__temp_var_1=$__return_echo
test1 __temp_var_1
echo "Hi"
__temp_var_2=$__return_echo
test2 __temp_var_2
echo "Hi"
__temp_var_3=$__return_echo
test3 __temp_var_3
"""
