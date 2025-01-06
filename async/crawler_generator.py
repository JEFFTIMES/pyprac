'''
Suppose there is a file saves a few links of websites.

$ cat src_urls.txt
https://regex101.com/
https://docs.python.org/3/this-url-will-404.html
https://www.nytimes.com/guides/
https://www.mediamatters.org/
https://1.1.1.1/
https://www.politico.com/tipsheets/morning-money
https://www.bloomberg.com/markets/economics
https://www.ietf.org/rfc/rfc2616.txt


Get all the links that embedded in the <href> tags of each page and save them in a file.


1. generator src_urls to yield a src_url one at a time, from the stream(generator) of a file 
2. generator htmls to yield an html once at a time, from each src_url of the generator src_urls
3. generator urls to yield a url once at a time, from generator htmls
4. dump each url from generator urls to the target  

            
'''

import pathlib
import typing
import io 
import requests
import re
from urllib.parse import urlparse, urlunparse, urljoin
import time


def dump(urls: typing.Generator[dict, None, None], file: io.TextIOWrapper) -> None:
    ''' dump the map {'src': url, 'href': url} to a file.
    '''
    
    for url_map in urls:  
        try:  
            file.write(f'[{file.name}] : [{url_map['src']}] : [{url_map['href']}]\n')
        except:
            print(f'dumping URL {url_map} failed.')

def extract_urls(html_maps: typing.Generator[dict, None, None]) -> typing.Generator[dict, None, None]:
    ''' Extract URLs from the href tags in the html content.
    '''

    HREF = re.compile(r'href=["\'].*?["\']')
    urls = set()
    for html_map in html_maps:
        hrefs = HREF.findall(html_map['html']) 
        if hrefs:
            for href in hrefs:
                link = href[6:-1].strip()
                urls.add((html_map['src'], urljoin(html_map['src'], link)))
    return ({'src':url[0],'href': url[1]} for url in urls)
    

def fetch_htmls(urls: typing.Generator[str,None, None]) -> typing.Generator[dict, None, None]:
    ''' iterate urls and generate html for each url.
        yield {'html':html, 'src':url}
    '''
        
    # handle exceptions and return the html content
    with requests.Session() as session:
        for url in urls:
            try:
                res = session.get(url)
                res.raise_for_status()
            except requests.exceptions.RequestException as err:
                print(f"An error occurred: {err}")
            else:
                yield {'src':url, 'html':res.text}

def validated_urls(urls:typing.Generator[str, None, None]) -> typing.Generator[str, None, None]:
    parsed = (urlparse(url) for url in urls)
    validated = (urlunparse(parsed_url) for parsed_url in parsed if all((parsed_url.scheme, parsed_url.netloc)))
    return validated

def source_urls(filepath: pathlib.Path) -> typing.Generator[str, None, None]:
    ''' Extract source URLs from a given filepath.
        Return a Generator object.ß
    '''
    raw_urls = (line for line in filepath.open('rt'))
    parsed_urls = (urlparse(str.strip(url)) for url in raw_urls)
    return (urlunparse(parsed_url) for parsed_url in parsed_urls if all((parsed_url.scheme, parsed_url.netloc)))


def validate_source_file(filename: str) -> pathlib.Path | None:
    ''' Convert a filename to a Path object representing the file. 
        If the received filename is a relative path, joint it to the path of __file__ of the script. 
    '''
    fp = pathlib.Path(filename)
    if fp.is_absolute():
        # check the existence and return accordingly. 
        return fp if fp.exists() else None        
    else:
        # join it to the script's filepath, check and return.
        abs_fp = pathlib.Path(__file__).cwd() / fp
        return abs_fp if abs_fp.exists() else None
    

def crawl_and_dump():
    ''' Lookup the source file and extract the source urls to be crawled.
        Create the target file for writing. 
        Kick off the crawling.
    '''

    source_urls_file = pathlib.Path(__file__).parent / 'urls.txt'
    source_filepath = validate_source_file(source_urls_file)

    if source_filepath is None:
        print(f'{source_urls_file} does not exist.')
        return
    
    dest_filepath = source_filepath.parent / 'hrefs-gen.txt'
    
    src_urls = source_urls(source_filepath)
    validated_src_urls = validated_urls(src_urls)
    htmls = fetch_htmls(validated_src_urls)    
    urls = extract_urls(htmls)


    with dest_filepath.open('tw') as dest_file:
        dump(urls, dest_file)


start = time.time()
crawl_and_dump()
end = time.time()
print(f'running time: {(end - start):.4f}')