import logging

import matplotlib.pyplot as plt

from .Simulation import Simulation

plt.style.use('ggplot')
plt.rcParams["figure.dpi"] = 250
plt.rcParams["legend.fontsize"] = 5
plt.rcParams["lines.linewidth"] = 1

logging.basicConfig(format='[%(levelname)s:%(filename)s:%(funcName)s()] %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


def start_simulation():
    Simulation().start()


if __name__ == "__main__":
    start_simulation()
