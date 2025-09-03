import numpy as np
import pandas
from mnist import MNIST
import random
from matplotlib import pyplot as plt

mndata = MNIST('mnistSamples')
images, labels = mndata.load_training()
index = random.randrange(0, len(images))

#print(mndata.display(images[0]))

pixels = np.array(images[0]).reshape((28,28))
plt.imshow(pixels, cmap='gray')
plt.show()