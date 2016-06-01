import qche
import random
import time


# This is a long computation that will fail once in a while
def long_computation(i):
    time.sleep(.1)

    if random.random() < .05:
        raise Exception("Oops.")

    return i**2 + divmod(i, 7)[1]


results = 0
with qche.PickleCache("/tmp/pickle.pickle") as cache:
    for i in xrange(100):
        if i not in cache:
            cache[i] = long_computation(i)

        print "Got {} -> {}".format(i, cache[i])
        results += cache[i]

print "Got results: ", results
