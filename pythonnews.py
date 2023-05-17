from gnewsclient import gnewsclient
import time

# Select only the top 8 countries with highest GDPs 
# English as a language 
# Maximum 10 results

temp_location = ['United States','China','Japan','Germany','United Kingdom','India','France','Italy']
temp_language='english' 
temp_max_results=10
temp_title = []
temp_link = []

text_file = open("News.txt", "w+")

for loc in temp_location: 
    text_file.writelines(str('\n'+time.ctime()+'\n'))
    text_file.writelines(str("Country : "+loc+'\n'))

    client = gnewsclient.NewsClient(location=loc,language=temp_language,max_results=temp_max_results)
    news_list = client.get_news()
    for news in news_list:
        if news in temp_title:
            continue
        else:
            temp_title.append(news['title'])
            temp_link.append(news['link'])
            text_file.writelines(str(news['title'] + '\n' + 'Source: ' + news['link']+'\n\n'))

# write the results in to txt file    
text_file.close()