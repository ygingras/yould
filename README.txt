
This is Yould, a generator for pronounceable random words.

The engine uses Markov chains with two letter transitions.  This
distribution includes trained engines for 
 
 * English (en, kjb)
 * Dutch (nl)
 * Finnish (fi)
 * Italian (it)
 * French (fr)
 * German (de)


Installation
------------

Quick and simple:

  easy_install yould

Just a litle harder:

  tar -xvf yould-0.3.3.tar.gz  
  cd yould-0.3.3
  python setup.py install


Usage
-----
  # generate a random word
  yould
or
  # generate 30 random words
  yould -n 30
or 
  # generate a random word with the French engine
  yould -t fr

try
  yould --help
for more options


Training
--------

 1) Get a bunch of text files.  Project Gutenberg is a good place to
    start.

 2) Train a new engine:

      yould-train new-engine.yould file1.txt file2.txt ...

 3) Use your new engine:

      yould -t new-elvish-engine.yould


 4) (optional)
    Training is incremental.  You can tune an engine that it almost
    right by feeding it new texts.
    
      yould-train viking.yould englishtext.txt germantext.txt
      yould-train viking.yould finnishtext.txt
     

Have fun and check for new releases on my website:

  http://ygingras.net/b/tab/yould



-- Yannick Gingras <ygingras@ygingras.net>
