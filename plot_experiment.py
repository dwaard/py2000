# library
import numpy as np
import matplotlib.pyplot as plt

classes = ["Tens", "Zeros", "Ninities", "Eighties", "Seventies", "Sixties", "Older"]

def classify(year):
    class_year = 2010
    for class_name in classes[0:-1]:
        if year >= class_year:
            return class_name
        class_year -= 10
    return classes[len(classes) - 1]

for n in range(1956, 2020):
    s = classify(n)
    print "%s: %s" % (n, s)


# Your x and y axis
x=range(1,6)
y=[ [1,4,6,8,9], [2,2,7,10,12], [2,8,5,10,6] ]

# Basic stacked area chart.
plt.stackplot(x,y, labels=['A','B','C'])
plt.legend(loc='upper left')
#plt.show()

# --- FORMAT 2</pre>
x=range(1,6)
y1=[1,4,6,8,9]
y2=[2,2,7,10,12]
y3=[2,8,5,10,6]

# Basic stacked area chart.
plt.stackplot(x,y1, y2, y3, labels=['A','B','C'])
plt.legend(loc='upper left')
plt.show()