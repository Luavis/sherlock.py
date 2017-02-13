Sherlock.py
========

|wip| |pypi| |pypi-version| |travis-ci| |Code Climate| |Test Coverage| |Open Source Love|

.. image:: http://i.imgur.com/n8xH4Wd.png?1
   :target: https://github.com/Luavis/sherlock
   :align: center
   :alt: sherlock.py

Sherlock.py is transpiler that translate python to shell script language.

`한국어로 보기 <https://github.com/Luavis/sherlock/tree/master/README.ko.rst>`_

.. contents::

Motivation
----------

.. figure:: http://i.imgur.com/7blJGwc.jpg
    :alt: map to buried treasure
    :width: 100%
    :align: center

    < Ditective who program with Shell script >

Shell script is well known script language which is used in most of unix-like OS. Shell script lanuage garuntee to run in most unix-like OS. So many software developers are using this language when they program install script or configuration script. Because this language is really old, There are several `problems <http://teaching.idallen.com/cst8207/16w/notes/740_script_problems.html>`_. and it is hard to maintain program which is writted by Shell script language.

Install
-------

.. code:: sh

    $ pip install sherlock.py

Sherlock.py support python version over 2.6 or 3.3. and support linux and macOS. If there is error in install please write issue.

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

Following is basic usage.

.. code:: sh

    $ sherlock target.py

Using this command, target.py file is translated into shell sciprt. after, it is automatically run with ``sh``. We can find out bug from the running result.

.. code:: sh

    $ sherlock target.py -o output.sh

Using ``-o`` flag, you can save sherlock result in file. In this case script isn't run automatically.

.. code:: sh

    $ sherlock -c "echo 'Hello World.'"

Using ``-c`` flag, input command is immediately translated to shell script language and executed.

If you want to details. Please check `sample codes <https://github.com/Luavis/sherlock.py/tree/master/samples>`__

Todo
----

* import syntax
* ``command`` package
* documentation
* support windows batch and powershell script
* more test...

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
