#!/usr/bin/zsh

for i in 210000 220000 230000 240000 250000 260000 270000 280000 290000 300000
{
    python closest_pair_tests/gen_random.py $i > closest_pair_tests/random_ints_$i
}

for i in 210000 220000 230000 240000 250000 260000 270000 280000 290000 300000
{
    time python closest_pair.py closest_pair_tests/random_ints_$i
}


