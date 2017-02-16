|wip| |pypi| |pypi-version| |travis-ci| |Code Climate| |Test Coverage| |Open Source Love|

.. image:: http://i.imgur.com/n8xH4Wd.png?1
   :target: https://github.com/Luavis/sherlock
   :align: center
   :alt: sherlock.py

**Sherlock.py**  Python으로 작성한 코드를 shell script언어로 바꿔주는 transpiler입니다.

`English <https://github.com/Luavis/sherlock/tree/master/README.rst>`_

.. contents::

Motivation
----------

.. figure:: http://i.imgur.com/7blJGwc.jpg
    :alt: map to buried treasure
    :width: 100%
    :align: center

    < Shell script를 작성하는 명탐정의 모습 >

Shell script는 많은 Unix-like 운영체제에서 보편적으로 사용되는 script language입니다. 이 언어는 Unix-like 운영체제에서 동작이 보장되어 많은 사람들이 Install script나 configure 스크립트에 사용됩니다. 하지만 개발된지 오래되어 다양한 `문제가 <http://teaching.idallen.com/cst8207/16w/notes/740_script_problems.html>`_ 있고 유지보수가 어렵습니다.

Install
-------

.. code:: sh

    $ pip install sherlock.py

Sherlock.py는 python버전 2.6 이상, 3.3 이상에서 동작을 보장하고 Linux 계열
운영체제와 macOS에서 동작을 보장합니다. 해당 버전과 운영체제에 대해서 문제가 있으면 issue를 남겨주세요.

Usage
-----

::

    usage: sherlock [-h] [-o output] [-c] [-v] [--version] [file | command]

    Python to bash trans-compiler.

    positional arguments:
      [file | command]  program read from script file

    optional arguments:
      -h, --help        show this help message and exit
      -o output         output file path
      -c, --command     program passed in as string
      -v, --verbose     program run in verbose mode
      --version         show program's version number and exit

다음은 기본적인 사용 예제입니다.

.. code:: sh

    $ sherlock target.py

위 커맨드를 사용하면 target.py를 shell script로 컴파일하고 이를 ``sh``
명령어를 이용하여 실행합니다. 실행 결과를 통해서 내가 작성하고 있는
코드가 shell script로 잘 컴파일 되는지 확인하고 디버깅할 수 있습니다.

.. code:: sh

    $ sherlock target.py -o output.sh

``-o``\ 플래그를 통해 sherlock의 결과물을 파일로 저장할 수 있습니다. 이 경우 유저가 작성한 스크립트가 실행되지 않습니다.

.. code:: sh

    $ sherlock -c "echo 'Hello World.'"

``-c``\ 플래그를 사용하면 입력한 커맨드가 즉시 ``sh``로 컴파일 되고 이를 실행합니다.

자세한 사용예는 `samples <https://github.com/Luavis/sherlock.py/tree/master/samples>`__ 에서 확인해주세요

Library
-------

**sherlock.cmd package**

일반적인 쉘 명령어를 ``sherlock.cmd``를 import하여 쓸 수 있습니다. 이 패키지를 import하게 되면, Sherlock.py로 만들어진 쉘 스크립트 코드를 실행하는 유저의 환경에 해당 명령어가 설치되어 있는지 미리 확인합니다.

.. code:: python

    from sherlock.cmd import ls

    ls('-al')

**pipe function**

쉘 스크립트에서는 ``|``를 통해서 명령어를 연결할 수 있습니다. 이를 Python code로 구현하기 위해서, Sherlock.py에서는 pipe 함수를 지원합니다.

.. code:: python

    from sherlock.cmd import wc
    pipe(print('./test'), wc('-c'))

Todo
----

* import 구문
* ``command`` 패키지 구현
* 문서화
* Windows BATCH/Powershell 스크립트 지원
* 더 많은 테스트

License
-------

- MIT © 2017 `Luavis <https://github.com/Luavis>`__
- Icon designed by `cyoh <https://github.com/cyoh>`_, Sherlock Holmes graphic by Matthew Davis from the Noun Project

.. |wip| image:: https://img.shields.io/badge/status-WIP-red.svg
.. |pypi| image:: https://img.shields.io/pypi/v/sherlock.py.svg
   :target: https://pypi.python.org/pypi/sherlock.py
.. |pypi-version| image:: https://img.shields.io/pypi/pyversions/sherlock.py.svg
   :target: https://pypi.python.org/pypi/sherlock.py
.. |travis-ci| image:: https://travis-ci.org/Luavis/sherlock.py.svg?branch=master
   :target: https://travis-ci.org/Luavis/sherlock.py
.. |Code Climate| image:: https://codeclimate.com/github/Luavis/sherlock/badges/gpa.svg
   :target: https://codeclimate.com/github/Luavis/sherlock
.. |Test Coverage| image:: https://codeclimate.com/github/Luavis/sherlock/badges/coverage.svg
   :target: https://codeclimate.com/github/Luavis/sherlock/coverage
.. |Open Source Love| image:: https://badges.frapsoft.com/os/mit/mit.svg?v=102
   :target: https://github.com/luavis/sherlock/
