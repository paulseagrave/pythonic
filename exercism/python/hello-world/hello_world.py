#
# Skeleton file for the Python "Hello World" exercise.
#


def hello(name=''):
    '''
    The ubiquitous hello world
    '''
    hello_string = 'Hello, World!'

    if name:
        hello_string = 'Hello, {name}!'.format(name=name)

    return hello_string
