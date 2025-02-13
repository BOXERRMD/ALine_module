from ALine import analyse, Style

@analyse(in_call=True, print_infos=['line', 'default', 'variables', 'annotation', 'event', 'filename', 'function'], set_line=(-1, -1))
def test(coucou:str, u=None):

    print(coucou)
    if 1 == 1:
        u = i(1)
        print(u)


def i(u):
    return str(u)

test('hey')


