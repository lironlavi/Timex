# Code for tagging temporal expressions in text
# For details of the TIMEX format, see http://timex2.mitre.org/

import nltk
import re
import string
import os
import sys

text = r'C:\text.txt'
time_word_filename = r'C:\time_word_filename.txt'

# Requires eGenix.com mx Base Distribution
# http://www.egenix.com/products/python/mxBase/
try:
    from mx.DateTime import *
except ImportError:
    print """
Requires eGenix.com mx Base Distribution
http://www.egenix.com/products/python/mxBase/"""

# Predefined strings.
# Predefined strings.
numbers = "(^a(?=\s)|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand)"
day = r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
week_day = r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
month = r"(january|february|march|april|may|june|july|august|september|october|november|december)"
dmy = r"(year|day|week|month|decade|century|hour|minute|moment)"
rel_day = r"(today|yesterday|tomorrow|tonight|tonite|2day|2nite)"

repeat = r"(again$|renew[s])"
change = r"(chang[a-zA-Z]*|revolution[a-zA-Z]*|shift[a-zA-Z]*|everything stays the same|nothing change[a-zA-Z]*)"
chron = r"(chronology|chronological|continu[a-zA-Z]*|sequence)"
parts_day = r"(morning$|noon$|evening|night$)"
long_time = r"(era$|eternity|histor[a-zA-Z]*|lifetime)"
tenses = r"(present|future|past$|now$|progress$|certainty|uncertainty)"
on_time = r"(start$|end$|anytime|delay|late$|premature|someday|soon$|it's time|it is time|in an instant|immediatly|right away|begin[a-zA-Z]*)"

exp1 = "(before|after|earlier|later|ago|B4)"
exp2 = "(this|next|last|every)"
iso = "\d+[/-]\d+[/-]\d+ \d+:\d+:\d+\.\d+"
year = "((?<=\s)\d{4}|^\d{4})"
regxp1 = "((\d+|(" + numbers + "[-\s]?)+) " + dmy + "s? " + exp1 + ")"
regxp2 = "(" + exp2 + " (" + dmy + "|" + week_day + "|" + month + "|" + parts_day +"))"
regxp3 = "(" + day + " " + parts_day +")"




reg1 = re.compile(regxp1, re.IGNORECASE)
reg2 = re.compile(regxp2, re.IGNORECASE)
reg3 = re.compile(rel_day, re.IGNORECASE)
reg4 = re.compile(iso)
reg5 = re.compile(year)
reg6 = re.compile (regxp3, re.IGNORECASE)
reg7 = re.compile (day, re.IGNORECASE)
reg8 = re.compile (repeat, re.IGNORECASE)
reg9 = re.compile (change, re.IGNORECASE)
reg10 = re.compile (chron, re.IGNORECASE)
reg11 = re.compile (long_time, re.IGNORECASE)
reg12 = re.compile (tenses, re.IGNORECASE)
reg14 = re.compile (on_time, re.IGNORECASE)
reg15 = re.compile (month, re.IGNORECASE)



def tag(text,time_word_fout):

    # Initialization
    timex_found = []

    # re.findall() finds all the substring matches, keep only the full
    # matching string. Captures expressions such as 'number of days' ago, etc.
    found = reg1.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
        timex_found.append(timex)

    # Variations of this thursday, next year, etc
    found = reg2.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
        timex_found.append(timex)

    # today, tomorrow, etc
    found = reg3.findall(text)
    for timex in found:
        timex_found.append(timex)

    # ISO
    found = reg4.findall(text)
    for timex in found:
        timex_found.append(timex)

    # Year
    found = reg5.findall(text)
    for timex in found:
        timex_found.append(timex)

    # Tuesday morning, Sunday evening, etc.
    found = reg6.findall(text)
    for timex in found:
        timex_found.append(timex)

    # days - monday, tuesday...
    found = reg7.findall(text)
    for timex in found:
        timex_found.append(timex)

    # repetition expressions (again)
    found = reg8.findall(text)
    for timex in found:
        timex_found.append(timex)

    # change expressions
    found = reg9.findall(text)
    for timex in found:
        timex_found.append(timex)

    # chronological expressions
    found = reg10.findall(text)
    for timex in found:
        timex_found.append(timex)

    # long-time expressions
    found = reg11.findall(text)
    for timex in found:
        timex_found.append(timex)

    # past,present,future expressions
    found = reg12.findall(text)
    for timex in found:
        timex_found.append(timex)

    # on time/off time expressions
    found = reg14.findall(text)
    for timex in found:
        timex_found.append(timex)

    # months
    found = reg15.findall(text)
    for timex in found:
        timex_found.append(timex)

    # Tag only temporal expressions which haven't been tagged.
    #write all time words into 'time_word_fout', one expression per line
    ff = open(time_word_fout,"wb")

    for timex in timex_found:
        ff.write(timex + "\n")
        ff.close()
        text = re.sub(timex + '(?!</TIMEX2>)', '<TIMEX2>' + timex + '</TIMEX2>', text)
        ff = open(time_word_fout,"a+")

    return text



def main():

    f = open(text, 'r')
    text = f.read()
    tagged_text = tag(text,time_word_filename)

if __name__ == '__main__':
    main()








#def demo():
#    import nltk
 #   text = nltk.corpus.abc.raw('rural.txt')[:10000]
  #  print tag(text)

#if __name__ == '__main__':
 #   demo()