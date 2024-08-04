

from math import exp
from math import expm1
import numpy
import matplotlib.pyplot as plt



class Bernoulli:
    def __init__(self, maxorder):
        self.maxorder = maxorder
        self.denominators = [1.0,] * maxorder
        for i in range(1, maxorder):
            self.denominators[i] = (i+1) * self.denominators[i-1]
        self.factors = [1.0/x for x in self.denominators]

    def calcbernoulli(self, x):
        xv = 1.0
        y = 0.0
        for i, v in enumerate(self.factors):
            y += v * xv
            xv *= x
        return 1.0 / y


def bexpm(x):
    y = expm1(x)
    if y != x:
        return x/y
    return 1.0



def create_bernoulli(i):
    fx = Bernoulli(i)
    return lambda x : fx.calcbernoulli(x)

def b1(x):
    return x / (exp(x) - 1.0)

b2 = create_bernoulli(15)

b3 = bexpm


x = numpy.linspace(0., 1.0, 10001)


y = []
#plt.title("comparison of 3 different Bernouilli Function implementations")
fig, ax = plt.subplots(2,1)



funcs = [b2, b1]
for i in range(2, 20):
    funcs.append(create_bernoulli(i))

for f in funcs:
    y.append(numpy.array(list(map(f, x))))
    ax[0].plot(x, y[-1])
#ax[0].legend([r'$B1= \frac{x}{\exp(x)-1)}$', r'$B2=\frac{1}{1+0.5*x}$', r'$B3=\frac{x}{\text{expm1}(x)}$' "\n" r'      $x \ne \text{expm1}(x), \text{else} 1$'], loc="lower left",
#fancybox=True, framealpha=0.5)
pdiffs=[]
for i in range(1,len(y)):
    pdiffs.append(abs(y[i]-y[0])/y[0])
    ax[1].semilogy(x,pdiffs[-1])
#ax[1].legend(['$|B3-B1|/B3$', '$|B3-B2|/B3$'])
plt.show()

