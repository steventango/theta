import matplotlib.pyplot as plt
import math
import numpy as np
import os
import subprocess
import time
from tqdm import tqdm
from typing import Callable, List


class theta:
    def compile(self) -> None:
        if os.name == 'nt':
            self.executable = self.path.replace('.cpp', '.exe')
        else:
            self.executable = self.path.replace('.cpp', '')

        subprocess.check_output(['g++', '-o', self.executable, self.path])

    def time(self) -> List[float]:
        y = []
        for n in self.x:

            p = subprocess.Popen(
                [self.executable],
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )

            cin = self.generator(n)

            start = time.time()
            p.communicate(input=bytes(cin, 'utf-8'))[0].decode('utf-8')
            end = time.time()
            delta = end - start
            delta *= 1000000
            y.append(delta)
        return y

    def plot(self) -> None:
        fig, ax = plt.subplots()
        ax.ticklabel_format(useOffset=False, style='plain')
        ax.set_xlabel('n')
        ax.set_ylabel('time (μs)')

        plt.grid(True)

        m, b = np.polyfit(self.x, self.y, 1)
        yp = np.polyval([m, b], self.x)
        plt.plot(self.x, yp, label=f'O(n) [{m:.2f}x + {b:.2f}]')

        m, b = np.polyfit(np.log2(self.x), self.y, 1)
        yp = np.polyval([m, b], np.log2(self.x))
        plt.plot(self.x, yp, label=f'O(nlogn) [{m:.2f}log(x) + {b:.2f}]')

        a, b, c = np.polyfit(self.x, self.y, 2)
        yp = np.polyval([a, b, c], self.x)
        plt.plot(self.x, yp, label=f'O(n²) [{a:.2f}x² + {b:.2f}x + {c:.2f}]')

        plt.axvline(x=200000)
        plt.scatter(self.x, self.y)
        ax.set_ylim(0)
        plt.legend()
        plt.show()

    def run(self) -> None:
        if self.path.endswith('.cpp'):
            self.compile()
        elif self.path.endswith('.py'):
            self.executable = 'python ' + self.path
        else:
            raise ValueError('path: file must be a .py or .cpp file.')

        for k in tqdm(range(1, self.samples + 1)):
            y_new = self.time()
            # update y average
            self.y = [y + (y_new[i] - y) / k for i, y in enumerate(self.y)]

        print(self.x, self.y)
        self.plot()

        if self.path.endswith('.cpp'):
            os.remove(self.executable)

    def __init__(self,
                 filename: str,
                 generator: Callable[[int], str],
                 start: int, stop: int, n: int = 10, samples: int = 5) -> None:
        self.path = filename
        self.generator = generator
        self.samples = samples
        self.executable = None
        if n < 5:
            Warning('n: n should be greater than 5 to allow inference.')
            n = 5
        self.x = [n for n in range(start, stop, math.ceil((stop - start) / n))]
        self.y = [0 for _ in range(n)]
        pass
