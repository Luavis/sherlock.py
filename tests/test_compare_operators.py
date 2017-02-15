from tests import analysis_code_list


def test_number_equal_op():
    code = [
        'a = 10',
        'a == 10',
    ]

    assert analysis_code_list(code) == """export a=10
$a -eq 10
"""

def test_number_gt_op():
    code = [
        'a = 10',
        'a > 10',
    ]

    assert analysis_code_list(code) == """export a=10
$a -gt 10
"""

def test_number_ge_op():
    code = [
        'a = 10',
        'a >= 10',
    ]

    assert analysis_code_list(code) == """export a=10
$a -ge 10
"""

def test_number_lt_op():
    code = [
        'a = 10',
        'a < 10',
    ]

    assert analysis_code_list(code) == """export a=10
$a -lt 10
"""

def test_number_le_op():
    code = [
        'a = 10',
        'a <= 10',
    ]

    assert analysis_code_list(code) == """export a=10
$a -le 10
"""

def test_number_le_op():
    code = [
        'a = 10',
        'a != 10',
    ]

    assert analysis_code_list(code) == """export a=10
$a -ne 10
"""

def test_string_equal_op():
    code = [
        'a = "10"',
        'if a == "10":',
        '   pass'
    ]

    assert analysis_code_list(code) == """export a="10"
if [ $a = "10" ]; then

fi
"""

def test_string_not_equal_op():
    code = [
        'a = "10"',
        'if a != "10":',
        '   pass'
    ]

    assert analysis_code_list(code) == """export a="10"
if [ $a ! "10" ]; then

fi
"""

def test_string_is_op():
    code = [
        'a = "10"',
        'if a is "10":',
        '   pass'
    ]

    assert analysis_code_list(code) == """export a="10"
if [ $a = "10" ]; then

fi
"""

def test_string_not_equal_op():
    code = [
        'a = "10"',
        'if a != "10":',
        '   pass'
    ]

    assert analysis_code_list(code) == """export a="10"
if [ $a ! "10" ]; then

fi
"""

def test_string_not_equal_op():
    code = [
        'a = "10"',
        'if a is not "10":',
        '   pass'
    ]

    assert analysis_code_list(code) == """export a="10"
if [ $a ! "10" ]; then

fi
"""
