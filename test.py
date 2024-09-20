from ALine import analyse, Style
@analyse(in_call=False, print_infos=['line', 'annotation', 'function', 'default'], set_line=(-1, -1))
def test(coucou, u=None):

    print(coucou)
    if 1 == 1:
        u = i(1)
        print(u)


def i(u):
    return str(u)

test('hey')


