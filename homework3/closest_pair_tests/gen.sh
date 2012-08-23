#!/usr/bin/zsh

for i in {1..1000}
{
    python closest_pair_tests/gen_random.py $i > closest_pair_tests/random_ints_$i
}

for i in {1..100000}
{
    time python closest_pair.py closest_pair_tests/random_ints_$i
}


