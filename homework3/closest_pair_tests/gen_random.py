import random
import sys

if len(sys.argv) != 2:
    print "USAGE: python gen_random.py NUM_TO_GENERATE"

to_gen = int(sys.argv[1])
all_y = set()
all_x = set()
for i in xrange(to_gen):
    rand = lambda: random.randrange(0, to_gen, 1)

    x = rand()
    while x in all_x:
        x = rand()
    all_x.add(x)

    y = rand()
    while y in all_y:
        y = rand()
    all_y.add(y)

    print "%d,%d" % (x,y)
