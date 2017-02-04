from tests import analysis_code_list


def test_simple_if_statement():
    code = [
        'a = 10',
        'if a == 10:',
        '   echo("Hi")',
    ]

    assert analysis_code_list(code) == """export a=10
if [ $a -eq 10 ]; then
echo "Hi"
fi
"""

def test_simple_for_statement():
    code = [
        'for i in range(1, 5):',
        '   pass'
    ]
    print(analysis_code_list(code))
