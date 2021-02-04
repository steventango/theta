from theta import theta


def generate(n: int) -> str:
  stdin = f'{n} 2000000000\n'
  stdin += ' '.join([str(x) for x in range(1000000000,
                                           2000000000, 2000000000 // n)])
  return stdin


test = theta(
    r'C:\Users\Steven\Google Drive\School\University of Alberta\Y1\CMPUT 275 Introduction to Tangible Computing II\Weekly Exercises\Interview Questions\3 Pair Hunt\pair_hunt.cpp',
    generate,
    2,
    250000,
    5,
    5
)

test.run()
