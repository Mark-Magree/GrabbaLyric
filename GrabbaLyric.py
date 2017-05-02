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
    options = {"verbose":False,"verboser":False}
    if args[1].startswith("-"):
        if 'v' in args[1]:
            options["verbose"] = True
        if 'vv' in args[1]:
            options["verboser"] = True
        return args[2:], options
    else:
        return args[1:], options

def get_first_result_url(search,opts):
    surl = "http://search.azlyrics.com/search.php?q=" +\
            '+'.join(search)
    if opts["verbose"]:
        print("Search URL: " + surl)
    res = requests.get(surl)
    res.raise_for_status()
    if opts["verboser"]:
        print(res.text)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    lyrics_elem = soup.select('td.text-left a')
    first_result = lyrics_elem[0].get('href')
    if opts["verbose"]:
        print("First Search Result: " + first_result)
    return first_result

def get_lyrics_from_search(html,opts):
    #TODO
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
    lyric_url = get_first_result_url(search,options)
    text = get_lyrics_from_search(lyric_url,options)
    save_to_cache_file(text,search,options)
    print(text)

main(sys.argv)
