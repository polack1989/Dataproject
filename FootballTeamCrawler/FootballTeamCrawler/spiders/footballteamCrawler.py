import scrapy, re, time


class FootballTeamSpider(scrapy.Spider):
    name = "transferSpider"



    def start_requests(self):

        year_2016_2017 = ['http://www.soccernews.com/soccer-transfers/english-premier-league-transfers/',
                          'http://www.soccernews.com/soccer-transfers/spanish-la-liga-transfers/',
                          'http://www.soccernews.com/soccer-transfers/italian-serie-a-transfers/',
                          'http://www.soccernews.com/soccer-transfers/german-bundesliga-transfers/',
                          'http://www.soccernews.com/soccer-transfers/rest-of-europe-transfers/'
                          ]

        year_2015_2016 = ['http://www.soccernews.com/soccer-transfers/english-premier-league-transfers-2015-2016/',
                          'http://www.soccernews.com/soccer-transfers/spanish-la-liga-transfers-2015-2016/',
                          'http://www.soccernews.com/soccer-transfers/italian-serie-a-transfers-2015-2016/',
                          'http://www.soccernews.com/soccer-transfers/german-bundesliga-transfers-2015-2016/',
                          'http://www.soccernews.com/soccer-transfers/rest-of-europe-transfers-2015-2016/'
                          ]

        year_2014_2015 = ['http://www.soccernews.com/soccer-transfers/english-premier-league-transfers-2014-2015/',
                          'http://www.soccernews.com/soccer-transfers/spanish-la-liga-transfers-2014-2015/',
                          'http://www.soccernews.com/soccer-transfers/italian-serie-a-transfers-2014-2015/',
                          'http://www.soccernews.com/soccer-transfers/german-bundesliga-transfers-2014-2015/',
                          'http://www.soccernews.com/soccer-transfers/rest-of-europe-transfers-2014-2015/'
                          ]

        year_2013_2014 = ['http://www.soccernews.com/soccer-transfers/english-premier-league-transfers-2013-2014/',
                          'http://www.soccernews.com/soccer-transfers/spanish-la-liga-transfers-2013-2014/',
                          'http://www.soccernews.com/soccer-transfers/italian-serie-a-transfers-2013-2014/',
                          'http://www.soccernews.com/soccer-transfers/german-bundesliga-transfers-2013-2014/',
                          'http://www.soccernews.com/soccer-transfers/rest-of-europe-transfers-2013-2014/'
                          ]

        year_2012_2013 = ['http://www.soccernews.com/soccer-transfers/english-premier-league-transfers-2012-2013/',
                          'http://www.soccernews.com/soccer-transfers/spanish-la-liga-transfers-2012-2013/',
                          'http://www.soccernews.com/soccer-transfers/italian-serie-a-transfers-2012-2013/',
                          'http://www.soccernews.com/soccer-transfers/german-bundesliga-transfers-2012-2013/',
                          'http://www.soccernews.com/soccer-transfers/rest-of-europe-transfers-2012-2013/'
                          ]

        year_2011_2012 = ['http://www.soccernews.com/soccer-transfers/english-premier-league-transfers-2011-2012/',
                          'http://www.soccernews.com/soccer-transfers/spanish-la-liga-transfers-2011-2012/',
                          'http://www.soccernews.com/soccer-transfers/italian-serie-a-transfers-2011-2012/',
                          'http://www.soccernews.com/soccer-transfers/german-bundesliga-transfers-2011-2012/',
                          'http://www.soccernews.com/soccer-transfers/rest-of-europe-transfers-2011-2012/'
                          ]

        year_2010_2011 = ['http://www.soccernews.com/soccer-transfers/english-premier-league-transfers-2010-2011/',
                          'http://www.soccernews.com/soccer-transfers/spanish-la-liga-transfers-2010-2011/',
                          'http://www.soccernews.com/soccer-transfers/italian-serie-a-transfers-2010-2011/',
                          'http://www.soccernews.com/soccer-transfers/german-bundesliga-transfers-2010-2011/',
                          'http://www.soccernews.com/soccer-transfers/rest-of-europe-transfers-2010-2011/',
                          ]

        year_2009_2010 = ['http://www.soccernews.com/soccer-transfers/english-premier-league-transfers-2009-2010/',
                          'http://www.soccernews.com/soccer-transfers/spanish-la-liga-transfers-2009-2010/',
                          'http://www.soccernews.com/soccer-transfers/italian-serie-a-transfers-2009-2010/',
                          'http://www.soccernews.com/soccer-transfers/german-bundesliga-transfers-2009-2010/',
                          'http://www.soccernews.com/soccer-transfers/rest-of-europe-transfers-2009-2010/'
                          ]

        year_2008_2009 = ['http://www.soccernews.com/soccer-transfers/english-premier-league-transfers-2008-2009/',
                          'http://www.soccernews.com/soccer-transfers/spanish-la-liga-transfers-2008-2009/',
                          'http://www.soccernews.com/soccer-transfers/italian-serie-a-transfers-2008-2009/',
                          'http://www.soccernews.com/soccer-transfers/german-bundesliga-transfers-2008-2009/',
                          'http://www.soccernews.com/soccer-transfers/rest-of-europe-transfers-2008-2009/'
                          ]

        year_2007_2008 = ['http://www.soccernews.com/soccer-transfers/english-premier-league-transfers-2007-2008/',
                          'http://www.soccernews.com/soccer-transfers/spanish-la-liga-transfers-2007-2008/',
                          'http://www.soccernews.com/soccer-transfers/italian-serie-a-transfers-2007-2008/',
                          'http://www.soccernews.com/soccer-transfers/german-bundesliga-transfers-2007-2008/',
                          'http://www.soccernews.com/soccer-transfers/rest-of-europe-transfers-2007-2008/'
                          ]

        urls = [year_2016_2017, year_2015_2016, year_2014_2015, year_2013_2014, year_2012_2013, year_2011_2012,
                year_2010_2011, year_2009_2010, year_2008_2009, year_2007_2008]

        #for url in urls:
        for yearUrl in year_2016_2017:
            yield scrapy.Request(url=yearUrl, callback=self.transferParse)


    def transferParse(self, response):
        for player in response.css('.transfer-zone-tab table tbody tr'):
            date = player.css('.date').extract_first()
            isExpensive = bool(re.search('[0-9]{4}', date))
            if isExpensive is True:
                continue
            name = player.css('.player-deals h4::text').extract_first()
            if name is None:
                continue
            info = player.css('td::text').extract()
            from_team = info[2]
            to_team = info[3]
            priceStatus = info[4]
            yield {name: {'OrigTeam': from_team, 'DestTeam': to_team, 'priceStatus': priceStatus}}