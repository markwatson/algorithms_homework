import random
import sys

if len(sys.argv) != 2:
    print "USAGE: python gen_random.py NUM_TO_GENERATE"

to_gen = int(sys.argv[1])
all_n = set()
for i in xrange(to_gen):
    rand = lambda: random.randrange(0, to_gen, 1)

    n = rand()
    while n in all_n:
        n = rand()
    all_n.add(n)

    print n
