import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import subprocess
import time
from tqdm import tqdm


class theta:
    def compile(self) -> None:
        if os.name == 'nt':
            self.executable = self.filename.replace('.cpp', '.exe')
        else:
            self.executable = self.filename.replace('.cpp')
        subprocess.check_output(['g++', '-o', self.executable, self.filename])

    def time(self) -> None:
        for i in tqdm(range(2, 200001, 10000)):
            p = subprocess.Popen(
                [self.executable],
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT)

            cin = f'{i} 2000000000\n'
            cin += ' '.join([str(x) for x in range(1000000000,
                                                   2000000000, 2000000000 // i)])

            start = time.time()
            p.communicate(input=bytes(cin, 'utf-8'))[0].decode('utf-8')
            end = time.time()
            delta = end - start
            delta *= 1000000
            self.x.append(i)
            self.y.append(delta)

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
        if self.filename.endswith('.cpp'):
            self.compile()

        self.time()
        self.plot()

        if self.filename.endswith('.cpp'):
            os.remove(self.executable)

    def __init__(self, filename) -> None:
        self.filename = filename
        self.executable = None
        self.x = []
        self.y = []
        pass


def main():
    parser = argparse.ArgumentParser(
        description='Empirically estimate Big-θ time complexity.'
    )
    parser.add_argument('path', help='source code path')

    args = parser.parse_args()
    cpp = theta(args.path)
    cpp.run()


if __name__ == '__main__':
    main()
