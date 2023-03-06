from gnewsclient import gnewsclient

# Select only the top 8 countries with highest GDPs 
# English as a language 
# Maximum 10 results

temp_location = ['United States','China','Japan','Germany','United Kingdom','India','France','Italy']
temp_language='english' 
temp_max_results=10
temp_title = []

for loc in temp_location: 
    client = gnewsclient.NewsClient(location=loc,language=temp_language,max_results=temp_max_results)
    news_list = client.get_news()
    for news in news_list:
        if news in temp_title:
            continue
        else:
            temp_title.append(news['title'])
        
    result = ''
    result = '\n'.join(set(temp_title))

# write the results in to txt file 

with open("News.txt", "w") as text_file:
    text_file.write(result)

text_file.close()
