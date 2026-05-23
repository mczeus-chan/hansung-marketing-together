import os
path = os.path.join('..', 'frontend', 'index.html')
c = open(path, 'r', encoding='utf-8').read()
c = c.replace('filter: brightness(0) invert(1);', 'filter: brightness(10);')
open(path, 'w', encoding='utf-8').write(c)
print('[OK] logo fixed')
