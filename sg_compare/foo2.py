

from math import exp
from math import expm1
import numpy
import matplotlib.pyplot as plt


def b1(x):
    return 1./(1.0 + 0.5 * x + x*x/6. + x*x*x/24.)

def b2(x):
    return 1./(1.0 + 0.5 * x)

def b3(x):
    y = expm1(x)
    if y != x:
        return x/y
    return 1.0


x = numpy.linspace(0., 1e-3, 1001)

y = []
#plt.title("comparison of 3 different Bernouilli Function implementations")
fig, ax = plt.subplots(1,2)
for i in b1, b2, b3:
    y.append(numpy.array(list(map(i, x))))
    ax[0].plot(x, y[-1])
ax[0].legend([r'$B4=\frac{1}{1+0.5*x + x*x/6. + x*x*x/24.}$', r'$B2=\frac{1}{1+0.5*x}$', r'$B3=\frac{x}{\text{expm1}(x)}$' "\n" r'      $x \ne \text{expm1}(x), \text{else} 1$'], loc="lower left",
fancybox=True, framealpha=0.5)
pdiffs = []
for i in range(0,2):
    pdiffs.append(abs(y[i]-y[2])/y[2])
    ax[1].semilogy(x,pdiffs[-1])
ax[1].legend(['$|B3-B4|/B3$', '$|B3-B2|/B3$'])
plt.show()
plt.savefig('foo2.pdf')
