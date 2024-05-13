#!/usr/bin/env python3
# coding: utf-8


import re
import os
import sys
import pyspark
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf

#Starting Spark Session
spark = SparkSession.builder.master('local[*]').appName("BetterInvertedIndex").getOrCreate()
sc = spark.sparkContext
#stdin = open(sys.stdin.fileno(), encoding='iso-8859-1', mode='r')



#Used functions
def find_words(x):
    return (re.findall(r'\b[A-Za-z]+\b', x.strip()))

def getFileName(x):
    return (x[1],os.path.basename(x[0]))

def update_output(x):
    x = ', '.join(f' {item} {c}'for item, c in x)
    return (x)


#Extracting words from files and getting the file names from path
textFiles = sc.wholeTextFiles(sys.argv[1])
map_words = textFiles.flatMapValues(find_words)
map_words = map_words.map(getFileName)

# mapping words, counting words, reducing, groupby and sorting words
word_c = map_words.map(lambda x: (x, 1)).reduceByKey(lambda a, b: a + b).sortByKey(True)
word_c_grp = word_c.map(lambda x: (x[0][0], (x[1],(x[0][1])))).groupByKey().sortByKey(True)
sorted_word_c = word_c_grp.map(lambda x: (x[0], sorted(x[1], key=lambda y: y[0], reverse=True)))

# updating result to get expected style of output and save to file
output = sorted_word_c.mapValues(update_output)
output2 = output.map(lambda x:"{}\t{}".format(x[0],x[1]))
output2.saveAsTextFile(sys.argv[2])

# if want to print to console
result = output.collect()
for value in result:
    print(value[0],'\t', value[1])

spark.stop()





