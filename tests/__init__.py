from sherlock.codelib.analyzer import CodeAnalyzer


def analysis_code_list(code_list):
    analyzer = CodeAnalyzer('\n'.join(code_list))
    return analyzer.analysis().generate()
