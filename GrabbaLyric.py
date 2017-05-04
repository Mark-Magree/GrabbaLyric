#!/usr/bin/env python
#GrabbaLyric.py - download lyrics for given song
#Usage: GrabbaLyric.py [-vv] query search terms
#Options:
#   -v  Verbose: print diagnostic text
#   -vv Verboser: print entire page ment to be scraped plus verbose
#Output: Text, several lines

import requests, os, sys, shelve
import bs4

home = os.path.expanduser('~')
CACHE_FILE = home + "/.cache/GrabbaLyric.cache"

def is_arguments(args):
    #TODO list comprehension to shorten?
    if len(sys.argv) > 1:
        return True
    else: 
        print("Error: Argument[s] required")
        print("Usage: GrabbaLyric.py [-v] query")
        return False

def split_options(args):
    options = {"verbose":False,"verboser":False,"list_only":False}
    if args[1].startswith("-"):
        if 'l' in args[1]:
            options["list_only"] = True
        if 'v' in args[1]:
            options["verbose"] = True
        if 'vv' in args[1]:
            options["verboser"] = True
        return args[2:], options
    else:
        return args[1:], options

def get_first_result_url(search,opts):
    base = "https://search.letssingit.com"
    strm1 = '+'.join(search) 
    surl = base + "/?a=search&artist_id=&l=archive&s=" + strm1
    if opts["verbose"]:
        print("Search URL: ")
        print(surl)
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64;\
            rv:24.0) Gecko/20100102 Firefox/34.0' }
    res = requests.get(surl, headers=headers)
    res.raise_for_status()
    if opts["verboser"]:
        print(res.text)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    song_link = soup.select('td a.high_profile')
    first_result = song_link[0].get('href')
    if opts["verbose"]:
        print("First Result:")
        print(first_result)
    return first_result

def get_lyrics_from_search(url,opts):
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64;\
            rv:24.0) Gecko/20100103 Firefox/44.0' }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    if opts["verboser"]:
        print(res.text)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    lyrics_text = soup.select('div#lyrics')
    return lyrics_text[0].text

def sanatize_cache_key(word_list):
    for i in range(len(word_list)):
        word_list[i] = word_list[i].title()
    word_list.sort()
    return ''.join(word_list)

def save_to_cache_file(text,srch,opts):
    key = sanatize_cache_key(srch)
    
    with shelve.open(CACHE_FILE) as shelf:
        shelf[key] = text
    if opts['verbose']:
        print("%s written to cache" % (key))

def list_cached_keys():
    with shelve.open(CACHE_FILE) as shelf:
        for key in shelf.keys:
            print(key)

def check_for_cached_lyrics(search,opts):
    #TODO check cache file for lyrics before downlodaing
    pass

def main(args):
    if not is_arguments(args):
        sys.exit()
    search,options = split_options(args) #search,options = list,dict
    if options['list_only']:
        list_cached_keys()
        sys.exit()
    check_for_cached_lyrics(search,options)
    lyric_url = get_first_result_url(search,options)
    text = get_lyrics_from_search(lyric_url,options)
    save_to_cache_file(text,search,options)
    print(text)

if __name__ == "__main__":
    main(sys.argv)
