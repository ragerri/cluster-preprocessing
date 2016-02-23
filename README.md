cluster-preprocessing
=====================

This README explains the pre-processing performed to create the cluster lexicons to be used as features in IXA pipes tools [http://ixa2.si.ehu.es/ixa-pipes]. So far we use the clusters three methods: Brown, Clark and Word2vec.

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
  + (Liang: Semi-supervised learning for natural language processing)[http://cs.stanford.edu/~pliang/papers/meng-thesis.pdf]

+ **Clark clustering**: [Alexander Clark (2003). Combining distributional and morphological information for part of speech induction](http://www.aclweb.org/anthology/E03-1009).
  + Input: one lowercased token per line, punctuation removed, sentences separated by two newlines. See [clark-input.txt]((https://github.com/ragerri/cluster-preprocessing/examples/clark-input.txt)
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

The following steps are performed:

1. **server**: starts a TCP service loading the model and required resources.
2. **client**: sends a NAF document to a running TCP server.
3. **tag**: reads a NAF document containing *wf* elements and creates *term* elements with the morphological information.
2. **train**: trains new models for with several options
   available (read trainParams.properties file for details).
3. **eval**: evaluates a trained model with a given test set.
4. **cross**: perform cross-validation evaluation.

Each of these functionalities are accessible by adding (tag|train|eval|cross|server|client) as a
subcommand to ixa-pipe-pos-$version.jar. Please read below and check the -help
parameter ($version refers to the current ixa-pipe-pos version).

````shell
java -jar target/ixa-pipe-pos-1.5.0.jar (tag|train|eval|cross|server|client) -help
````

### Tagging

If you are in hurry, [Download](http://ixa2.si.ehu.es/ixa-pipes/models/guardian.txt) or create a plain text file and use it like this:

````shell
cat guardian.txt | java -jar ixa-pipe-tok-1.8.4.jar tok -l en | ixa-pipe-pos-1.5.0.jar tag -m en-pos-perceptron-autodict01-conll09.bin -lm en-lemma-perceptron-conll09.bin
````

If you want to know more, please follow reading.

ixa-pipe-pos reads NAF documents containing *wf* elements via standard input and outputs NAF
through standard output. The NAF format specification is here:

(http://wordpress.let.vupr.nl/naf/)

You can get the necessary input for ixa-pipe-pos by piping it with
[ixa-pipe-tok](https://github.com/ixa-ehu/ixa-pipe-tok).

There are several options to tag with ixa-pipe-pos:

+ **model**: it is **required** to provide the model to do the tagging.
+ **lemmatizerModel**: it is **required** to provide the lemmatizer model.
+ **lang**: choose between en and es. If no language is chosen, the one specified
  in the NAF header will be used.
+ **multiwords**: activates the multiword detection option.
+ **dictag**: post-process the Statistical POS tagger output via a monosemic
  postag dictionary.

**Tagging Example**:

[Download](http://ixa2.si.ehu.es/ixa-pipes/models/guardian.txt) or create a plain text file and use it like this:

````shell
cat guardian.txt | java -jar ixa-pipe-tok-1.8.4.jar tok -l en | java -jar ixa-pipe-pos-1.5.0.jar tag -m en-pos-perceptron-autodict01-conll09.bin -lm en-lemma-perceptron-conll09.bin
````
**Remember to download some models from the distributed packages!!**
+ Universal Dependencies Models: Basque, English and Italian.
  + [ud-morph-models-1.5.0](http://ixa2.si.ehu.es/ixa-pipes/models/ud-morph-models-1.5.0.tar.gz).
+ Language Specific Models: Dutch, English, French, Galician, German, Spanish.
  + [morph-models-1.5.0](http://ixa2.si.ehu.es/ixa-pipes/models/morph-models-1.5.0.tar.gz)

### Server

We can start the TCP server as follows:

````shell
java -jar target/ixa-pipe-pos-1.5.0.jar server -l en --port 2040 -m en-pos-perceptron-autodict01-conll09.bin -lm en-lemma-perceptron-conll09.bin
````
Once the server is running we can send NAF documents containing (at least) the text layer like this:

````shell
 cat guardian.txt | java -jar ixa-pipe-tok-1.8.4.jar tok -l en | java -jar target/ixa-pipe-pos-1.5.0.jar client -p 2040
````

### Training

To train a new model, you just need to pass a training parameters file as an
argument. Every training option is documented in the template trainParams.properties file.

**Example**:

````shell
java -jar target/ixa.pipe.pos-$version.jar train -p trainParams.properties
````

### Evaluation

To evaluate a trained model, the eval subcommand provides the following
options:

+ **component**: choose between POS or Lemma
+ **model**: input the name of the model to evaluate.
+ **testSet**: testset to evaluate the model.
+ **evalReport**: choose the detail in displaying the results:
  + **brief**: it just prints the word accuracy.
  + **detailed**: detailed report with confusion matrixes and so on.
  + **error**: print to stderr all the false positives.

**Example**:

````shell
java -jar target/ixa.pipe.pos-$version.jar eval -c pos -m test-pos.bin -l en -t test.data
````

## API

The easiest way to use ixa-pipe-pos programatically is via Apache Maven. Add
this dependency to your pom.xml:

````shell
<dependency>
    <groupId>eus.ixa</groupId>
    <artifactId>ixa-pipe-pos</artifactId>
    <version>1.5.0</version>
</dependency>
````

## JAVADOC

The javadoc of the module is located here:

````shell
ixa-pipe-pos/target/ixa-pipe-pos-$version-javadoc.jar
````
## Module contents

The contents of the module are the following:

    + formatter.xml           Apache OpenNLP code formatter for Eclipse SDK
    + pom.xml                 maven pom file which deals with everything related to compilation and execution of the module
    + src/                    java source code of the module and required resources
    + trainParams.properties      A template properties file containing documention
    + Furthermore, the installation process, as described in the README.md, will generate another directory:
    target/                 it contains binary executable and other directories


## INSTALLATION

Installing the ixa-pipe-pos requires the following steps:

If you already have installed in your machine the Java 1.7+ and MAVEN 3, please go to step 3
directly. Otherwise, follow these steps:

### 1. Install JDK 1.7 or JDK 1.8

If you do not install JDK 1.7+ in a default location, you will probably need to configure the PATH in .bashrc or .bash_profile:

````shell
export JAVA_HOME=$pwd/java8
export PATH=${JAVA_HOME}/bin:${PATH}
````
Replacing $pwd with the full path given by typing the **pwd** inside the java directory.

If you use tcsh you will need to specify it in your .login as follows:

````shell
setenv JAVA_HOME $pwd/java8
setenv PATH ${JAVA_HOME}/bin:${PATH}
````

If you re-login into your shell and run the command

````shell
java -version
````

You should now see that your JDK is 1.7+

### 2. Install MAVEN 3

Download MAVEN 3 from

````shell
wget http://apache.rediris.es/maven/maven-3/3.0.5/binaries/apache-maven-3.0.5-bin.tar.gz
````

Now you need to configure the PATH. For Bash Shell:

````shell
export MAVEN_HOME=$pwd/apache-maven-3.0.5
export PATH=${MAVEN_HOME}/bin:${PATH}
````
Replacing $pwd with the full path given by typing the **pwd** inside the apache maven directory.

For tcsh shell:

````shell
setenv MAVEN3_HOME $pwd/apache-maven-3.0.5
setenv PATH ${MAVEN3}/bin:{PATH}
````

If you re-login into your shell and run the command

````shell
mvn -version
````

You should see reference to the MAVEN version you have just installed plus the JDK 7 that is using.

### 3. Get module source code

If you must get the module source code from here do this:

````shell
git clone https://github.com/ixa-ehu/ixa-pipe-pos
````

### 4. Download the Resources and Models

Download the POS tagging and lemmatization models:

+ Universal Dependencies Models: Basque, English and Italian.
  + [ud-morph-models-1.5.0](http://ixa2.si.ehu.es/ixa-pipes/models/ud-morph-models-1.5.0.tar.gz).
+ Language Specific Models: Dutch, English, French, Galician, German, Spanish.
  + [morph-models-1.5.0](http://ixa2.si.ehu.es/ixa-pipes/models/morph-models-1.5.0.tar.gz)

Additionally, we distribute dictionaries to correct the output of the statistical lemmatization.
To use them, you will need to download the resources and copy them to ixa-pipe-pos/src/main/resources/
**before compilation** for the module to use:

Download the resources and untar the archive into the src/main/resources directory:

````shell
cd ixa-pipe-pos/src/main/resources
wget http://ixa2.si.ehu.es/ixa-pipes/models/lemmatizer-dicts.tar.gz
tar xvzf lemmatizer-dicts.tar.gz
````
The lemmatizer-dicts contains the required dictionaries to help the statistical lemmatization.

### 5. Compile

````shell
cd ixa-pipe-pos
mvn clean package
````

This step will create a directory called target/ which contains various directories and files.
Most importantly, there you will find the module executable:

ixa-pipe-pos-$version.jar

This executable contains every dependency the module needs, so it is completely portable as long
as you have a JVM 1.7 or newer installed.

To install the module in the local maven repository, usually located in ~/.m2/, execute:

````shell
mvn clean install
````

## Extend

To add your language to ixa-pipe-pos the following steps are required:

+ Create lemmatizer and (if required) multiword and monosemic dictionaries following the format of those distributed in **lemmatizer-dicts.tar.gz**.
  + **Create binary dictionaries (FSA):** Starting from the plain text tabulated dictionaries, do the following steps:
    + Get Morfologik standalone binary: http://sourceforge.net/projects/morfologik/files/morfologik-stemming/
    + java -jar morfologik-tools-1.6.0-standalone.jar tab2morph --annotation "*" -i
    ~/javacode/ixa-pipe-pos/pos-resources/lemmatizer-dicts/freeling/es-lemmatizer.dict -o spanish.morph
    + java -jar morfologik-tools-1.6.0-standalone.jar fsa_build -i spanish.morph -o spanish.dict
    + **Create a *.info file like spanish.info**
+ **Modify the classes** CLI, Resources and Annotate; if multiword is required also MultiWordMatcher; if monosemic dictionaries for post-processing also MorfologikMorphoTagger) adding for your language the same information that it is available for other languages.
+ Train a model. **It is crucial that the tagset of the dictionaries and corpus be the same**. Also it is recommended to train a model with an external dictionary (the external tag dictionary needs to be in opennlp tag format).
+ Add documentation to this README.md.
+ **Do a pull request** to merge the changes with your new language.
+ Send us the resources and models created if you want them to be distributed with ixa-pipe-pos (Apache License 2.0 is favoured).

## Contact information

````shell
Rodrigo Agerri
IXA NLP Group
University of the Basque Country (UPV/EHU)
E-20018 Donostia-San Sebastián
rodrigo.agerri@ehu.eus
````
