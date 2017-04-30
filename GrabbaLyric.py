#!/usr/bin/env python
#GrabbaLyric.py - download lyrics from azlyrics.com
#Usage: GrabbaLyric.py [-v] query search terms
#Output: Text 

import requests, sys
import bs4

def is_arguments(args):
    #TODO list comprehension to shorten?
    if len(sys.argv) > 1:
        return True
    else: 
        print("Error: Argument[s] required")
        print("Usage: GrabbaLyric.py [-v] query")
        return False

def split_options(args):
    options = {"verbose":False}
    if args[1].startswith("-"):
        if 'v' in args[1]:
            options["verbose"] = True
        return args[2:], options
    else:
        return args[1:], options

#TODO '+'.join(search) isn't putting the '+' in there
def retrieve_data(search,opts):
    surl = "search.azlyrics.com/search.php?q=" + '+'.join(search)
    if opts["verbose"]:
        print(surl)


def main(args):
    if not is_arguments(args):
        sys.exit()
    search,options = split_options(args)
    retrieve_data(search,options)

main(sys.argv)
