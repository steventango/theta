from theta import theta


def generate(n: int) -> str:
    return str(n)


test = theta(
    'quadratic.cpp',
    generate,
    2,
    1000,
    10,
    1
)

test.run()
