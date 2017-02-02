from tests import analysis_code_list


def test_simple_if_statement():
    code = [
        'a = 10',
        'if a == 10:',
        '   echo("Hi")',
    ]

    print(analysis_code_list(code))

