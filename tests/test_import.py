from tests import analysis_code_list


def test_simple_import():
    code = [
        'import os',
    ]

    try:
        analysis_code_list(code)
    except ImportError:
        assert True
    else:
        assert False

def test_simple_from_import():
    code = [
        'from os.path import join',
    ]

    try:
        analysis_code_list(code)
    except ImportError:
        assert True
    else:
        assert False

def test_command():
    code = [
        'from sherlock.cmd import ls',
        'ls("-al")'
    ]

    assert analysis_code_list(code) == """if ! type "ls" &> /dev/null ; then
echo "Error: Command 'ls' is not found\nplease install first"
exit 1
fi
function __sherlock_cmd_ls() {
    export __return__sherlock_cmd_ls="$(ls $@)"
}
__sherlock_cmd_ls "-al"
__return__sherlock_cmd_ls
"""
