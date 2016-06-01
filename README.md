# qche

qche is a tiny filesystem-persisted cache package for python2. It's useful for caching intermediate results of expensive computations that may fail catastrophically, causing you to otherwise lose the already calculated/received values.

## Installation
```sh
$ pip install qche
```

## Example

```python
results = []
with qche.PickleCache("/tmp/my_cache.pickle") as cache:
    for i in xrange(100):
        if i not in cache:
            cache[i] = long_computation(i)
        results.append(cache[i])

print "Got results: ", results
```

Here, `long_computation` might be, for instance:
-  a CPU-heavy computation, such as some optimization algorithm
-  a Network operation

If `long_computation` raises an exception in any one of the 100 calls, you can just re-execute the script and it will pick it right back where you left, because the previous results were persisted to disk.

## Available Serializers

- `qche.PickleCache`: reads/writes data from/to disk using the `pickle` protocol;
- `qche.JsonCache`: reads/writes data from/to disk using the `json` serializer;
