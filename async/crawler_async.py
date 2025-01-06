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

    2.2. findall <href> tags in the html content, parse the url of each tag and fill the urls in a set. (an html content) --> (set of urls)

    2.3. save each url in the set in the file target_urls.txt. (set of urls) --> (a file)

skeleton code flow:

    with open('path/to/the/target/file', 'wt+') as f:
        initialize dumper
        extract src_url from 'path/to/the/source/file' and create an iterable of urls
        loop all the urls:
            initialize a scrawler for each iteration to scrawl the url
            dump the extracted urls
    

Instead of running the iteration, sequentially executing 2.1, 2.2, 2.3 on each source urls, we wrap each round of execution of the 3 
sub tasks into an asynchronous task, register all the tasks(depends on how many source URLs are given) to the event loop and start them.

Thanks to the async libraries' help, any IO bond operations such as network communication and file read/write yield the control to the
event loop while being processed, thus, the event loop is able to switch the processing among many awaitable subtasks.

To embrace the non-blocking benefits of async, we should do two changes to the code. The first is to identify whatever IO bond 
operations and mark them as awaitable, and find corresponding async libraries or craft the awaitable object by ourselves to fulfill the 
awaitable operations. The second is to identify the resources that is dedicated resources in each iteration but have to be a shared ones 
among the concurrently running subtasks. Most of the time, the two efforts lead us to the same target. 

In this case, the file object for writing the extracted URLs has to be shared among the fetching-extracting-dumping subtasks. The HTTP 
Session is better to be shared among the subtasks with respect to the best practice.

The async crawler needs to do crawl and dump instead of doing crawl only.
'''

import time
import pathlib
import typing
import asyncio, aiofiles, aiohttp
from aiohttp import ClientSession
import re
from urllib.parse import urlparse, urlunparse, urljoin



class AsyncCrawler():
    ''' The asynchronous version of URL crawler.
        The instance is initiated with a dedicated source URL, and the shared file handler for writing,
        the shared ClientSession object for fetching the html.
    '''
    def __init__(self, url: str, session: ClientSession, file: typing.IO) -> None:
        ''' 
        '''
        self.url = url
        self.session = session
        self.file = file

    async def crawl_and_dump(self,) -> None:
        ''' The only public method to start the crawler.
            It crawls the given source url and dumps the extracted urls to the file.
        '''
        self.html = await self._fetch_html()
        if self.html is None:
            return None
        urls = self._extract_urls(self.html)
        if urls:
            await self._dump(urls)

    def _is_validate_url(self, url:str) -> bool:
        parsed = urlparse(url)
        return all((parsed.scheme, parsed.netloc))
    
    async def _fetch_html(self,) -> str | None:
        ''' Return a string that represents the html content or None if exceptions occur.
        '''
        # validate the input URL
        if not self._is_validate_url(self.url):
            print('Invalid source url')
            return None
        
        # handle exceptions and return the html content
        try:
            async with self.session.get(self.url) as response:
                # Manually check for HTTP error statuses
                if response.status >= 400:
                    # Raise an appropriate exception for non-successful HTTP status codes
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=f"HTTP error {response.status}",
                        headers=response.headers
                    )
                # If status code is 200-399, proceed to read the content
                html = await response.text()
                return html
            
        except aiohttp.ClientResponseError as e:
            print(f"Response error (status: {e.status}): {e.message}")
        except aiohttp.ClientConnectionError as e:
            print(f"Connection error: {e}")
        except aiohttp.InvalidURL as e:
            print(f"Invalid URL: {e}")
        except aiohttp.ClientError as e:
            print(f"Client error: {e}")
        except asyncio.TimeoutError:
            print("Request timed out.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}") 


    def _extract_urls(self, html: str) -> set:
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

    async def _dump(self, urls: set) -> None:
        ''' 
        '''
        try:
            for url in urls:    
                await self.file.write(f'[{self.file.name}] : [{self.url}] : [{url}]\n')
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
    


async def crawl() -> None:
    ''' We need an event loop to register and run the crawling tasks in the crawl().

    '''

    source_urls_file = pathlib.Path(__file__).parent / 'urls.txt'
    source_filepath = validate_source_file(source_urls_file)

    if source_filepath is None:
        print(f'{source_urls_file} does not exist.')
        return
    
    src_urls = source_urls(source_filepath)
    dest_filepath = source_filepath.parent / 'hrefs-async.txt'

    # open the writing file
    async with aiofiles.open(dest_filepath, 'tw+')  as f:
        
        # create the ClientSession for fetching
        async with ClientSession() as session:

            # create crawling tasks
            crawlers = []
            for url in src_urls:
                crawlers.append(AsyncCrawler(url, session, f).crawl_and_dump())
            await asyncio.gather(*crawlers)

start = time.time()
asyncio.run(crawl())
end = time.time()

print(f'async crawl uses {(end-start):.4f} seconds.')