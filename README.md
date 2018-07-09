Python Scrapy를 사용한 Crawling
=================================
Web Crawling, 또는 Web Scraping이나 Web Spidering이라고도 불리는 작업은, 여러 Web Page에 프로그램으로 접근해서 Data를 가지고 오는 작업을 얘기한다. 우리는 이 예제에서 BrickSet이라는 LEGO제품에 대한 정보들이 있는 사이트에서 Data를 받아와서 출력하는 것을 해볼것이다.  
  
일단 Windows사용자는 Anaconda로 Python3과 Scraper를 설치한다. 설치하는 것은 아래의 사이트에서 하면 된다.  
https://www.anaconda.com/download/   
https://doc.scrapy.org/en/1.1/intro/install.html   
  

## 1. 기본적인 Scraper만들기
먼저 이 예제를 저장할 Directory를 만들고 거기에 들어간다.  
~~~
$ mkdir brickset-scraper
$ cd brickset-scraper
~~~
  
그런뒤 사용하고 싶은 Text Editor를 사용해서 `scraper.py`를 아래와 같이 만든다.   
~~~
import scrapy


class BrickSetSpider(scrapy.Spider):
	name = "brickset_spider"
	start_urls = ['http://brickset.com/sets/year-2016']
~~~
위의 예제는 Scrapy가 제공하는 기본적인 Spider class인 `scrapy.Spider`를 사용해서 Class `BrickSetSpider`를 만드는 것이다. 이 안에는 두가지 Attribute가 들어가는데, `name`은 만들 spider의 이름이고, `start_urls`는 Crawling을 시작할 URL의 **리스트**이다. 하나씩 봐보자.   
  
먼저 `scrapy`를 import해서 이 package가 제공하는 class들을 사용할 수 있게 한다.   
그런 다음 Scrapy가 제공하는 `Spider` class를 사용해서 `BrickSetSpider`라는 **subclass**를 만든다. Subclass란 그것의 parent class보다 조금더 특화 되어있는 Class라고 생각하면 된다. `Spider` class자체는 URL로 어떻게 접근하거나 거기서 어떻게 데이터를 받아오는 지는 정해져있지만, 어느 URL의 어는 부분의 데이터를 받아와야 되는지를 모른다. 이것을 Subclassing함으로서 부족한 정보를 줄 수 있다.   
  
그래서 부족한 정보인 어느 spider를 쓰는지와 어느 URL에 접속하는 지를 안에서 설정해줬다. 이 예제의 경우 `name`으로 `brickset_spider`를 만들 것이라고 지정했고, `start_urls` 리스트에 `http://brickset.com/sets/year-2016`을 추가함으로서 이 URL로 Crawling을 시작하게 되었다.   
  
이것을 사용하는 방법은 Commad Line에서 아래와 같은 명령어를 주면 된다.   

~~~
$ scrapy runspider scraper.py
~~~
그러면 아래와 같은 결과를 확인할 수 있다. 

~~~
2016-09-22 23:37:45 [scrapy] INFO: Scrapy 1.1.2 started (bot: scrapybot)
2016-09-22 23:37:45 [scrapy] INFO: Overridden settings: {}
2016-09-22 23:37:45 [scrapy] INFO: Enabled extensions:
['scrapy.extensions.logstats.LogStats',
 'scrapy.extensions.telnet.TelnetConsole',
 'scrapy.extensions.corestats.CoreStats']
2016-09-22 23:37:45 [scrapy] INFO: Enabled downloader middlewares:
['scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
 ...
 'scrapy.downloadermiddlewares.stats.DownloaderStats']
2016-09-22 23:37:45 [scrapy] INFO: Enabled spider middlewares:
['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
 ...
 'scrapy.spidermiddlewares.depth.DepthMiddleware']
2016-09-22 23:37:45 [scrapy] INFO: Enabled item pipelines:
[]
2016-09-22 23:37:45 [scrapy] INFO: Spider opened
2016-09-22 23:37:45 [scrapy] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2016-09-22 23:37:45 [scrapy] DEBUG: Telnet console listening on 127.0.0.1:6023
2016-09-22 23:37:47 [scrapy] DEBUG: Crawled (200) <GET http://brickset.com/sets/year-2016> (referer: None)
2016-09-22 23:37:47 [scrapy] INFO: Closing spider (finished)
2016-09-22 23:37:47 [scrapy] INFO: Dumping Scrapy stats:
{'downloader/request_bytes': 224,
 'downloader/request_count': 1,
 ...
 'scheduler/enqueued/memory': 1,
 'start_time': datetime.datetime(2016, 9, 23, 6, 37, 45, 995167)}
2016-09-22 23:37:47 [scrapy] INFO: Spider closed (finished)
~~~
매우 길지만, 조금만 뭔지 봐보자.   
먼저 scraper가 URL로부터 데이터를 읽어내기 위해서 필요한 추가적인 요소들을 불러들이고 초기화 시켰다.   
그런 다음 `start_urls`에 있는 URL을 사용해서 HTML을 받았다.  
마지막으로 그 받은 HTML을 `parse` method에보내서 parsing을 하는데, 우리는 아무 `parse` method도 지정하지 않았기 때문에 spider는 parsing을 하지 않은 채 끝난다.   


## 2. Page에서 데이터 끌어오기
위에서 HTML을 받아오는 기본적인 프로그램은 만들어 봤지만, 아직 Scraping이나 Spidering은 하지 않았다. 먼저 우리가 Scrapping을 하고자 하는 페이지를 봐보면, 아래와 같은 특징이 있음을 알 수 있다.   
* 각 페이지마다 Header가 있다.
* 검색에 관한 데이터, 몇개를 찾았는지, 뭐를 찾았는지 등에 대한 정보가 있다. 
* Table이나 Ordered List같이 나열되어 있는 LEGO Brick Set에 대한 정보가 있다.  
  
Scraper를 만들 때엔 HTML Source file를 보는 것이 가장 좋다. 아래는 보기 쉽게 하기 위해 조금 작업을 한 `brickset.com/sets/year-2016`의 HTML File이다.    

~~~
// brickset.com/sets/year-2016
<body>
  <section class="setlist">
    <article class='set'>
      <a href="https://images.brickset.com/sets/large/10251-1.jpg?201510121127" class="highslide plain mainimg" onclick="return hs.expand(this)">
        <img src="https://images.brickset.com/sets/small/10251-1.jpg?201510121127" title="10251-1: Brick Bank" onError="this.src='/assets/images/spacer.png'" />
      </a>
      <div class="highslide-caption">
        <h1>Brick Bank</h1>
        <div class='tags floatleft'>
        <a href='/sets/10251-1/Brick-Bank'>10251-1</a> 
        <a href='/sets/theme-Advanced-Models'>Advanced Models</a> 
        <a class='subtheme' href='/sets/theme-Advanced-Models/subtheme-Modular-Buildings'>Modular Buildings</a> 
        <a class='year' href='/sets/theme-Advanced-Models/year-2016'>2016</a> 
      </div>
      <div class='floatright'>&copy;2016 LEGO Group</div>
    ...
    </article>
    <article class='set'>

      ...

    </article>
  </section>
</body>
~~~
여기에서 Scraping을 하는 작업은 크게 두 단계로 나뉘어진다. 먼저 각 LEGO set에 대한 정보가 있는 파트를 끌어내고, 거기에서 우리가 원하는 정보만 얻어내기 위해서 HTML tag를 없앤다.   
  
Scrapy는 사용자가 지정하는 **selector**에 따라서 정보를 끌어온다. Selector란 우리가 원하는 Element를 끌어오기 위한 pattern을 정하는 것으로, 주로 CSS selector 또는 XPath Selector가 사용된다.  
  
우리는 CSS selector를 사용해서 원하는 class의 이름을 줘서 그 class를 갖고 있는 Element만 받아오게 할 것이다. 위의 HTML file을 봐보면 하나의 Brick Set마다 `set`이라는 `class`를 사용하고 있는 것을 알 수 있다. 따라서 우리는 `.set`을 우리의 CSS selector로 사용할 것이다. 하는 방법은 아래와 같이 `response` object에 원하는 selector를 넣으면 된다.   
  
~~~
class BrickSetSpider(scrapy.Spider):
	name = "brickset_spider"
	start_urls = ['http://brickset.com/sets/year-2016']

	def parse(self, response):
		SET_SELECTOR = '.set'
		for brickset in response.css(SET_SELECTOR):
			pass
~~~
이 코드는 이 페이지의 모든 `set`를 끌어와서 반복하면서 데이터를 끌어낸다. 그렇다면 실제로 끌어낸 데이터를 출력하기 위해서 데이터를 끌어내보자. 위의 HTML code를 다시 한번 봐보면 Brick Set의 이름은 `h1` tag 안에 있는 것을 확인할 수 있다.  
  
우리가 사용하는 `brickset` object는 자신만의 `css` method가 있어서 이것을 사용해서 데이터를 끌어낼 child element를 지정할 수 있다.  

~~~
class BrickSetSpider(scrapy.Spider):
	name = "brickset_spider"
	start_urls= ['http://brickset.com/sets/year-2016']

	def parse(self, response):
		SET_SELECTOR= '.set'
		for bricksetin response.css(SET_SELECTOR):
			
			NAME_SELECTOR = 'h1 ::text'
			yield {
				'name': brickset.css(NAME_SELECTOR).extract_first(),
			}
~~~
여기서 주의할 점은 `extract_first()` 다음에 넣은 `,`는 실수가 아니라는 것이다. 다음에도 더 많은 것들을 넣을 것이기 때문에 먼저 넣어놓은 것이다.   
  
먼저 위 코드를 보고 `NAME_SELECTOR`안에 `hi a ::text`가 들어가있는데, 여기서 `::text`는 CSS의 pseudo-selector를 그대로 사용한 것으로, `a` tag 자체를 지정하기 보단 `a` tag안에 있는 Text를 지정하기 위한 작업이다. 다음으로 `extract_first()`를 마지막에 사용한 이유는, `brickset.css(NAME_SELECTOR)`는 element들의 리스트를 반환하기 때문에, 거기의 첫번째 String만 사용하기 위해서이다.   
   
그러면 이제 저장을 하고 실행해보자. 

~~~
$ scrapy runspider scraper.py
~~~
이번엔 이름들이 출력되는 것을 확인할 수 있다. 

~~~
...
[scrapy] DEBUG: Scraped from <200 http://brickset.com/sets/year-2016>
{'name': 'Brick Bank'}
[scrapy] DEBUG: Scraped from <200 http://brickset.com/sets/year-2016>
{'name': 'Volkswagen Beetle'}
[scrapy] DEBUG: Scraped from <200 http://brickset.com/sets/year-2016>
{'name': 'Big Ben'}
[scrapy] DEBUG: Scraped from <200 http://brickset.com/sets/year-2016>
{'name': 'Winter Holiday Train'}
...
~~~
이젠 이름 뿐만이 아니라 images, pieces, 그리고 minifigs(miniature figures)도 받아와 보자. 아래의 HTML 코드를 다시 한번 확인해보자.  
  
~~~
<article class='set'>
  <a href="https://images.brickset.com/sets/large/10251-1.jpg?201510121127" class="highslide plain mainimg" onclick="return hs.expand(this)">
    <img src="https://images.brickset.com/sets/small/10251-1.jpg?201510121127" title="10251-1: Brick Bank" onError="this.src='/assets/images/spacer.png'" />
  </a>
  <div class="highslide-caption">
    <h1>Brick Bank</h1>

    ...

  </div>
  <div class='meta'>
    <div class='col'>
      <dl>
        <dt>Pieces</dt>
        <dd>
          <a class='plain' href='/inventories/10251-1'>2380</a>
        </dd>
        <dt>Minifigs</dt>
        <dd>
          <a class='plain' href='/minifigs/inset-10251-1'>5</a>
        </dd>

	...

      </dl>
    </div>

    ...

  </div>
</article>
~~~
위의 코드에서 아래와 같은 특징들을 알아낼 수 있다. 
* 이미지에 대한 정보는 첫번째 `a` tag 안의 `img` tag의 `src` attribute 안에 있다. 
* Pieces에 대한 정보를 얻는건 조금 더 복잡하다. `Pieces`라는 Text를 갖는 `dt` tag 다음에 오는 `dd` tag 안의 `a` tag 안에 있다. 이걸 끌어내기 위해선 CSS selector가 아니라 XPath selector를 사용할 것이다. 
* Minigifs의 숫자도 Pieces와 비슷한 방법으로 찾을 수 있을 것 같다.   
  
이제 주어진 새로운 정보로 scraper를 바꿔보자. 

~~~
import scrapy


class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['http://brickset.com/sets/year-2016']

    def parse(self, response):
        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):

            NAME_SELECTOR = 'h1 ::text'
            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            IMAGE_SELECTOR = 'img ::attr(src)'
            yield {
                'name': brickset.css(NAME_SELECTOR).extract_first(),
                'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
                'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
                'image': brickset.css(IMAGE_SELECTOR).extract_first(),
            }
~~~
이렇게 만든 scraper를 위와 같은 방법으로 실행 시켜보면 아래와 같은 출력을 볼 수 있을 것이다.   
  
~~~
2018-07-09 15:07:32 [scrapy.core.scraper] DEBUG: Scraped from <200 https://brickset.com/sets/year-2016>
{'name': 'Brick Bank', 'pieces': '2380', 'minifigs': '5', 'image': 'https://images.brickset.com/sets/small/10251
-1.jpg?201510121127'}
2018-07-09 15:07:32 [scrapy.core.scraper] DEBUG: Scraped from <200 https://brickset.com/sets/year-2016>
{'name': 'Volkswagen Beetle', 'pieces': '1167', 'minifigs': None, 'image': 'https://images.brickset.com/sets/sma
ll/10252-1.jpg?201606140214'}
~~~
XPath에 대한 구체적인 설명은 다른 페이지에서 하겠다. 그럼 이제 이 Scraper를 Spider로 만들어서 여러 페이지를 다니면서 작업하게 하자.  
  
  

## 3. 여러 페이지를 Crawling하기
지금까지 만든 것은 한 페이지에 대해서 Crawling을 하는 Scraper이고, 이제부터 만들 것은 여러 페이지에 대해서 Crawling을 하는 Spider이다. 우리가 지금까지 사용한 페이지를 봐보면 제일 위/아래에 다음페이지로 넘어가는 버튼 (`>`)이 있는 것을 확인할 수 있다. 이것들의 HTML은 아래와 같다.   
   
~~~
<ul class="pagelength">

  ...

  <li class="next">
    <a href="http://brickset.com/sets/year-2017/page-2">&#8250;</a>
  </li>
  <li class="last">
    <a href="http://brickset.com/sets/year-2016/page-32">&#187;</a>
  </li>
</ul>
~~~
위의 코드에시 `next`를 `class`로 갖는 `li` element를 봐보면 안에 `a` tag가 있는데, 여기의 `href`가 다음페이지로 가는 URL이다. 우리는 이것을 긁어내서 다음페이지로 가게 할 것이다. 위에서 사용했던 scraper.py를 그대로 아래와 같이 바꾼다.  
  
~~~
import scrapy


class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['http://brickset.com/sets/year-2016']

    def parse(self, response):
        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):

            NAME_SELECTOR = 'h1 ::text'
            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            IMAGE_SELECTOR = 'img ::attr(src)'
            yield {
                'name': brickset.css(NAME_SELECTOR).extract_first(),
                'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
                'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
                'image': brickset.css(IMAGE_SELECTOR).extract_first(),
            }

        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
~~~
먼저, 새로운 Selector `NEXT_PAGE_SELECTOR`를 만드는데, 여기선 CSS Selector를 사용해서 링크를 얻어온다. 그리고 `next_page`안에 긁어 온 URL을 넣는다. 만약에 링크가 존재한다면 `scrapy.Request`로 그 링크를 Crawling하게 하고, `callback=self.parse`로 그 받은 HTML을 Parsing한 후 다음 페이지의 링크를 다시 찾아서 만약에 존재한다면 다시 다음페이지로 가서 Crawling을 하도록 한다. 












