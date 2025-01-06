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


The main stream of a synchronous implementation looks like:

1. transfer lines in a file to a set of urls.  (a file) --> (an iterable of urls)

2. iterate on the iterable, repeatedly do:

    2.1. request to the website that the url points to and check the status, GET the html content if status is OK.  (an url) --> (an html content)

    2.2. findall <a href> tags in the html content, parse the url of each tag and fill the urls in a set. (an html content) --> (set of urls)

    2.3. save each url in the set in the file target_urls.txt. (set of urls) --> (a file)

skeleton code flow:

    with open('path/to/the/target/file', 'wt+') as f:
        initialize dumper
        extract src_url from 'path/to/the/source/file' and create an iterable of urls
        loop all urls:
            initialize a scrawler each iteration
            scrawl the url
            dump the extracted urls
    

'''

import pathlib
import typing
import io 
import requests
import re
from urllib.parse import urlparse, urlunparse, urljoin


class SyncCrawler():
    ''' The synchronous version of URL crawler.
        The instance of SyncCrawler is initiated with the homepage URL. 
        The method crawl() returns a set of URLs extracted from the homepage's <href> tags.
    '''
    def __init__(self, url: str) -> None:
        ''' 
        '''
        self.url = url
        self.session = requests.Session()
        self.html = None

    def crawl(self,) -> set | None:
        ''' The only public method to start the crawling.
            Return a set of urls.
        '''
        self.html = self._fetch_html()
        if self.html is None:
            return None
        return self._extract_urls(self.html)

    def _is_validate_url(self, url:str) -> bool:
        parsed = urlparse(url)
        return all((parsed.scheme, parsed.netloc))
    
    def _fetch_html(self,) -> str | None:
        ''' Return a raw string that represents the html content or None if exceptions occur.
        '''

        # validate the input URL
        if not self._is_validate_url(self.url):
            print('Invalid source url')
            return None
        
        # handle exceptions and return the html content
        with requests.Session() as session:
            try:
                res = session.get(self.url)
                res.raise_for_status()
            except requests.exceptions.RequestException as err:
                print(f"An error occurred: {err}")
                return None
            else:
                self.html = res.text
                return self.html
            

    def _extract_urls(self, html:str) -> set:
        ''' Extract URLs from the href tags in the html content.
        '''
        HREF = re.compile(r'href=["\'].*?["\']')
        hrefs = HREF.findall(html)
        urls = set()
        if hrefs:
            for href in hrefs:
                link = href[6:-1].strip()
                urls.add(urljoin(self.url, link))
        return urls

class Dumper():
    ''' The synchronous version of dumping a set of URLs to a file.
        Initialized with an opened file.
    '''

    def __init__(self, file: typing.IO) -> None:
        self.file = file 

    def dump(self, src: str, urls: typing.Iterable[str]) -> None:
        ''' The public interface to execute the dumping.
        '''
        try:
            for url in urls:    
                self.file.write(f'[{self.file.name}] : [{src}] : [{url}]\n')
        except:
            print(f'dumping URLs extracted from {src} failed.')
            


def source_urls(filepath: pathlib.Path) -> typing.Generator:
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
    

def crawl_and_dump(src_urls_path:str = None, dest_path:str = None) -> None:
    ''' Read urls from the file at src_urls_path if given, or try to open file 'urls.txt' at the script running folder.
        fetch the HTML content from the each url and extract the urls from any <a herf> tags.
        Create the target file and write the extracted urls to it. 
    '''

    
    source_filepath = pathlib.Path(src_urls_path) if src_urls_path else pathlib.Path(__file__).parent / 'urls.txt'
    dest_filepath = pathlib.Path(dest_filepath) if dest_path else source_filepath.parent / 'hrefs.txt'
    
    if not source_filepath.exists() or not dest_filepath.exists():
        print('Error: source file or dest file not exist.')
        return

    src_urls = source_urls(source_filepath)

    with dest_filepath.open('tw') as dest_file:
        dumper = Dumper(dest_file)
        for src_url in src_urls:
            crawler = SyncCrawler(src_url)
            urls = crawler.crawl()
            if urls is None:
                print(f'crawling {src_url} failed, continue to the next one.')
                continue
            dumper.dump(src_url, urls)

import time

start = time.time()
crawl_and_dump()
end = time.time()
print(f'running time: {(end - start):.4f}')