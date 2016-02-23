cluster-preprocessing
=====================

This README explains the pre-processing performed to create the cluster lexicons that are used as features in the IXA pipes tools [http://ixa2.si.ehu.es/ixa-pipes]. So far we use the following three methods: Brown, Clark and Word2vec.

## TABLE OF CONTENTS

1. [Overview](#overview)
2. [Brown clusters](#brown)
3. [Clark clusters](#clark)
4. [Word2vec clusters](#word2vec)

## OVERVIEW

We induce the following clustering types:

+ **Brown hierarchical word clustering algorithm**: [Brown, et al.: Class-Based n-gram Models of Natural Language.](http://acl.ldc.upenn.edu/J/J92/J92-4003.pdf)
  + Input: a sequence of words separated by whitespace with no punctuation. See [brown-input.txt](https://github.com/percyliang/brown-cluster/blob/master/input.txt) for an example.
  + Output: for each word type, its cluster. See [brown-output.txt](https://github.com/percyliang/brown-cluster/blob/master/output.txt) for an example.
  + In particular, each line is:
  ````shell
  <cluster represented as a bit string> <word> <number of times word occurs in input>
  ````
  + We use [Percy Liang's implementation](https://github.com/percyliang/brown-cluster) off-the-shelf. 
  + [Liang: Semi-supervised learning for natural language processing.](http://cs.stanford.edu/~pliang/papers/meng-thesis.pdf)

+ **Clark clustering**: [Alexander Clark (2003). Combining distributional and morphological information for part of speech induction](http://www.aclweb.org/anthology/E03-1009).
  + Input: one lowercased token per line, punctuation removed, sentences separated by two newlines. See [clark-input.txt](https://github.com/ragerri/cluster-preprocessing/examples/clark-input.txt)
  + Output: for each word type, its cluster and a weight. See [clark-output.txt](https://github.com/ragerri/cluster-preprocessing/examples/clark-output.txt)
  + Each line consists of
  ````shell
  <word> <cluster> <weight>
  ````
  + We use [Alexander Clark's implementation](https://github.com/ninjin/clark_pos_induction) off-the-shelf.

+ **Word2vec Skip-gram word embeddings clustered via K-Means**: [Mikolov et al. (2013). Efficient estimation of word representations in Vector Space.](http://arxiv.org/pdf/1301.3781.pdf)
  + Input: lowercased tokens separated by space, punctuation removed. See [word2vec-input.txt](https://github.com/ragerri/cluster-preprocessing/examples/word2vec-input.txt)
  + Output: for each word type, its cluster. See [word2vec-output.txt](https://github.com/ragerri/cluster-preprocessing/examples/word2vec-output.txt)
  + Each line consists of
  ````shell
  <word> <cluster>
  ````
  + We use [Word2vec implementation](https://code.google.com/archive/p/word2vec/) off-the-shelf. 

## Brown

Let us assume that the source data is in plain text format (e.g., without html or xml tags, etc.), and that every document is in a directory called *corpus-directory*. Then the following steps are performed:

### Preclean corpus

1. Remove all sentences or paragraphs consisting of less than 90\% lowercase characters, as suggested by [Liang: Semi-supervised learning for natural language processing.](http://cs.stanford.edu/~pliang/papers/meng-thesis.pdf).

This step is performed by using the following function in [ixa-pipe-convert](https://github.com/ragerri/ixa-pipe-convert):

````shell
java -jar ixa-pipe-convert-$version.jar --brownClean corpus-directory/
````

ixa-pipe-convert will create a *.clean* file for each file contained in the folder *corpus-directory*.

2. Move all *.clean* files into a new directory called, for example, *corpus-preclean*.

### Tokenize clean files to oneline format

1. Tokenize all the files in the folder to one line per sentence. This step is performed by using [ixa-pipe-tok](https://github.com/ixa-ehu/ixa-pipe-tok) in the following shell script:

````shell
./recursive-tok.sh $lang corpus-preclean
````
The tokenized version of each file in the directory *corpus-preclean* will be saved with a *.tok* suffix.

2. **cat to one large file**: all the tokenize files are concatenate it into a large huge file called *corpus-preclean.tok*.

````shell
cd corpus-preclean
cat *.tok > corpus-preclean.tok
````

### Format the corpus for Liang's implementation

1. Run the brown-clusters-preprocess.sh script like this to create the format required to induce Brown clusters using [Percy Liang's program](https://github.com/percyliang/brown-cluster).

````shell
./brown-clusters-preprocess.sh corpus-preclean.tok > corpus-preclean.tok.punct
````
2. Induce brown clusters:

````shell
brown-cluster/wcluster --text corpus-preclean.tok.punct --c 1000 --threads 8
````
This trains 1000 class Brown clusters using 8 threads in parallel.

## Clark

## Word2vec

## Contact information

````shell
Rodrigo Agerri
IXA NLP Group
University of the Basque Country (UPV/EHU)
E-20018 Donostia-San Sebastián
rodrigo.agerri@ehu.eus
````
