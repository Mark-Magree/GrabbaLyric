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

def retrieve_data(search,opts):
    surl = "http://search.azlyrics.com/search.php?q=" +\
            '+'.join(search)
    if opts["verbose"]:
        print(surl)
    res = requests.get(surl)
    res.raise_for_status()
    if opts["verbose"]:
        print(res.text)
    return res

def parse_data(html,opts):
    #TODO use bs4 to return lyrics
    pass

def save_to_cache_file(text,srch,opts):
    #TODO save lyrics to a file somewhere 
    pass

def check_for_cached_lyrics(search,opts):
    #TODO check cache file for lyrics before downlodaing
    pass

def main(args):
    if not is_arguments(args):
        sys.exit()
    search,options = split_options(args)
    check_for_cached_lyrics(search,options)
    data = retrieve_data(search,options)
    text = parse_data(data,options)
    save_to_cache_file(text,search,options)
    print(text)

main(sys.argv)
