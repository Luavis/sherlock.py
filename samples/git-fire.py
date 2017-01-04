def main():
    git('add', '-A')
    git('commit', '-m', 'Git commit: fire')
    git('push', 'origin', 'master')

main()
