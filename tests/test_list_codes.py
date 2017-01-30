from tests import analysis_code_list


def test_numeric_list_assign():
    code = [
        'a = [1, 2, 3, 4]'
    ]

    assert analysis_code_list(code) == 'export a=(1 2 3 4)\n'

def test_mix_list_assign():
    code = [
        'a = ["1", "2", 1, 2]'
    ]

    assert analysis_code_list(code) == 'export a=("1" "2" 1 2)\n'

def test_list_parameter():
    code = [
        'def test(a, b):',
        '   echo(a)',
        '   echo(b)',
        'a = ["1", "2"]',
        'b = 10',
        'test(a, b)',
    ]

    assert analysis_code_list(code) == """function test() {
declare -a local a=("${!1}")
local b=$2
echo $a
echo $b
}
export a=("1" "2")
export b=10
test a[@] $b
"""
