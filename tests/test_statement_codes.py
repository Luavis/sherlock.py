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
    assert analysis_code_list(code) == """for i in 1 2 3 4 5 6
do

done
"""


def  test_simple_while_statement():
    code = [
        'i = 0',
        'while i < 5:',
        '   echo(i)',
        '   i += 1'
    ]

    assert analysis_code_list(code) == """export i=0
while [ $i -lt 5 ]; do
echo $i
__temp_var_1=1
export i=$(( $export i + $__temp_var_1 ))
done
"""
