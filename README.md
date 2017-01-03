# Sherlock
[![travis-ci](https://travis-ci.org/Luavis/sherlock.svg?branch=master)](https://travis-ci.org/Luavis/sherlock)
[![Code Climate](https://codeclimate.com/github/Luavis/sherlock/badges/gpa.svg)](https://codeclimate.com/github/Luavis/sherlock)
[![Test Coverage](https://codeclimate.com/github/Luavis/sherlock/badges/coverage.svg)](https://codeclimate.com/github/Luavis/sherlock/coverage)
[![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/luavis/sherlock/)

Sherlock은 Python을 shell script로 바꿔주는 컴파일러입니다. **[WIP]**

## Install
```sh
$ pip install sherlock.py
```
Sherlock은 python버전 2.6 이상, 3.3 이상에서 동작을 보장하고 Linux 계열 운영체제와 macOS에서 동작을 보장합니다. 그 이외의 운영체제 혹은 버전에 대해서 문제가 있으면 issue를 남겨주세요.

## Usage

```
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

```

다음은 기본적인 사용 예제입니다.

```sh
$ sherlock target.py
```
위 커맨드를 사용하면 target.py를 shell script로 컴파일하고 이를 ```sh``` 명령어를 이용하여 실행합니다. 실행 결과를 통해서 내가 작성하고 있는 코드가 shell script로 잘 컴파일 되는지 확인하고 디버깅할 수 있습니다.

```sh
$ sherlock target.py -o output.sh
```
```-o```플래그를 통해 sherlock의 결과물을 파일로 저장할 수 있습니다. 이 경우 유저가 작성한 스크립트가 실행되지 않습니다.

```sh
$ sherlock -c "echo 'Hello World.'"
```
```-c```플래그를 사용하면 입력한 커맨드가 즉시 bash로 컴파일 되고 이를 실행합니다.

## License

MIT © [Luavis Kang](https://github.com/Luavis)
