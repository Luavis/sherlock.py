from tests import analysis_code_list


def test_if_statement():
    code = [
        'if a == 10:',
        '   pass',
    ]

    print(analysis_code_list(code))
