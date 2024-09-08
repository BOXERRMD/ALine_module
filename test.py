from ALine import ALine, analyse

@analyse(in_call=True)
def test(coucou):

    print(coucou)
    if True:
        u = i(1)
        print(u)

def i(u):
    return str(u)

test('hey')