import matplotlib.pyplot as plt
import numpy as np
import os
import subprocess
import time
from tqdm import tqdm

def main():
  executable = 'pair_hunt.exe'

  subprocess.check_output(
      ['g++', '-o', executable, executable.replace('.exe', '.cpp')])

  x = []
  y = []

  for i in tqdm(range(2, 200001, 10000)):
    p = subprocess.Popen(
        [executable],
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT)

    cin = f'{i} 2000000000\n'
    cin += ' '.join([str(x)
                    for x in range(1000000000, 2000000000, 2000000000 // i)])

    start = time.time()
    cout = p.communicate(input=bytes(cin, 'utf-8'))[0].decode('utf-8')
    end = time.time()
    delta = end - start
    delta *= 1000000
    x.append(i)
    y.append(delta)

  fig, ax = plt.subplots()
  ax.ticklabel_format(useOffset=False, style='plain')
  ax.set_xlabel('n')
  ax.set_ylabel('time (μs)')

  plt.grid(True)

  m, b = np.polyfit(x, y, 1)
  yp = np.polyval([m, b], x)
  plt.plot(x, yp, label=f'O(n) [{m:.2f}x + {b:.2f}]')

  m, b = np.polyfit(np.log2(x), y, 1)
  yp = np.polyval([m, b], np.log2(x))
  plt.plot(x, yp, label=f'O(nlogn) [{m:.2f}log(x) + {b:.2f}]')

  a, b, c = np.polyfit(x, y, 2)
  yp = np.polyval([a, b, c], x)
  plt.plot(x, yp, label=f'O(n²) [{a:.2f}x² + {b:.2f}x + {c:.2f}]')

  plt.axvline(x=200000)
  plt.scatter(x, y)
  ax.set_ylim(0)
  plt.legend()
  plt.show()

  os.remove(executable)

if __name__ == '__main__':
  main()
