
import numpy as np

class obj(object):

    def __init__(self, val):
        self.val = val

    def get_vals(self):
        return np.asarray([self.val, self.val+1, 1, 0])

    def __repr__(self):
        return str(self.get_vals())

arr = np.asarray([obj(1), obj(2), obj(3), obj(4), obj(5)])

m = np.asarray([2, 3])
v = np.vectorize(lambda x: np.array_equal(x.get_vals()[:m.size], m))
print(arr[v(arr)])

print(np.empty(0))