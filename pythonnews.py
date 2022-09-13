# Obtain news for US
from gnewsclient import gnewsclient
 
client = gnewsclient.NewsClient(language='english',
                                location='US',
                                topic='sports',
                                max_results=15)
 
news_list = client.get_news()
 
for item in news_list:
    print(item['title'])