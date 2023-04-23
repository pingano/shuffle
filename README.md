# Script to shuffle a fasta file of sequences

usage

```
python shuffle.py -f <fasta_file> -n <no_of_shuffles>
```

For example

```
python shuffle.py -f mature_two_test.fa -n 10
```

will shuffle each of the 7 sequences in `mature_two_test.fa` 10 times and write the output to a file named `mature_two_test__shuffled.fa`

