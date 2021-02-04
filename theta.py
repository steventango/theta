import matplotlib.pyplot as plt
import math
import numpy as np
from numpy.polynomial import Polynomial
import os
import subprocess
import time
from tqdm import tqdm
from typing import Callable, List, Tuple


class theta:
    def compile(self) -> None:
        if os.name == 'nt':
            self.executable = [self.path.replace('.cpp', '.exe')]
        else:
            self.executable = [self.path.replace('.cpp', '')]

        subprocess.check_output(['g++', '-o', self.executable[0], self.path])

    def time(self) -> List[float]:
        y = []
        for n in self.x:
            p = subprocess.Popen(
                self.executable,
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )

            cin = self.generator(n)

            start = time.time()
            p.communicate(input=bytes(cin, 'utf-8'))[0].decode('utf-8')
            end = time.time()
            delta = end - start
            delta *= 1000
            y.append(delta)
        return y

    def infer(self) -> Tuple[Polynomial, str]:
        best = None
        complexity = None
        best_resid = np.inf

        linear, (resid, *_) = Polynomial.fit(self.x, self.y, 1, full=True)
        if resid < best_resid:
            best = linear
            if linear.coef[1] > self.epsilon:
                complexity = 'n'
            else:
                complexity = '1'

        # m, b = np.polyfit(np.log2(self.x), self.y, 1)
        # yp = np.polyval([m, b], np.log2(self.x))
        # plt.plot(self.x, yp, label=f'O(nlogn) [{m:.2f}log(x) + {b:.2f}]')

        quadradic, (resid, *_) = Polynomial.fit(self.x, self.y, 2, full=True)
        if resid < best_resid and quadradic.coef[2] > self.epsilon:
            best = quadradic
            complexity = 'n²'

        return best, complexity

    def plot(self, line: Polynomial, complexity: str) -> None:
        fig, ax = plt.subplots()
        ax.ticklabel_format(useOffset=False, style='plain')
        ax.set_xlabel('n')
        ax.set_ylabel('time (ms)')

        plt.grid(True)

        plt.plot(*line.linspace(), label=f'θ({complexity}) [{line:unicode}]')

        plt.scatter(self.x, self.y)
        ax.set_ylim(0)
        plt.legend()
        plt.show()

    def run(self) -> None:
        if self.path.endswith('.cpp'):
            self.compile()
        elif self.path.endswith('.py'):
            self.executable = ['python', self.path]
        else:
            raise ValueError('path: file must be a .py or .cpp file.')

        for k in tqdm(range(1, self.samples + 1)):
            y_new = self.time()
            # update y average
            self.y = [y + (y_new[i] - y) / k for i, y in enumerate(self.y)]

        self.plot(*self.infer())

        if self.path.endswith('.cpp'):
            os.remove(self.executable[0])

    def __init__(
        self,
        filename: str,
        generator: Callable[[int], str],
        start: int,
        stop: int,
        n: int = 10,
        samples: int = 5
    ) -> None:
        self.path = filename
        self.generator = generator
        self.samples = samples
        self.executable = None
        if n < 5:
            Warning('n: n should be greater than 5 to allow inference.')
            n = 5
        self.x = [n for n in range(start, stop, math.ceil((stop - start) / n))]
        self.y = [0 for _ in range(n)]
        self.epsilon = 10
        pass
