import sys, site, importlib.util, pprint

print('Executable:', sys.executable)
print('Version:', sys.version)
try:
    print('User site-packages:', site.getusersitepackages())
except Exception as e:
    print('User site-packages error:', e)
print('sys.path:')
pprint.pprint(sys.path)
spec = importlib.util.find_spec('flask')
print('Flask spec found:', bool(spec))
if spec:
    import flask
    print('Flask version:', getattr(flask, '__version__', 'unknown'))