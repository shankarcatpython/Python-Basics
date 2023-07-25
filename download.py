
from pytube import YouTube

# This captures the link(url) and locates it from YouTube.
'''
'https://www.youtube.com/watch?v=MUXPL4rZL_E',
            'https://www.youtube.com/watch?v=WcIcVapfqXw',
            'https://www.youtube.com/watch?v=HfMTwkVQohM',
            'https://www.youtube.com/watch?v=3VES2soIJXs',
            'https://www.youtube.com/watch?v=-E2mRSZvJlM',
            'https://www.youtube.com/watch?v=9nRvqemGydw&list=PLuen39320a7L10y0SMWbWwdZT9FmB13wn',
            'https://www.youtube.com/watch?v=NtyrdMgSRKY&list=PLuen39320a7L10y0SMWbWwdZT9FmB13wn',
            'https://www.youtube.com/watch?v=Yt4xOLzQgrE&list=PLuen39320a7L10y0SMWbWwdZT9FmB13wn',
            'https://www.youtube.com/watch?v=nNTDM_nxfZs&list=PL7jqd335f8HLpjujaLAYPeNZJcm3paGS9',
            'https://www.youtube.com/watch?v=xYwCwdIbUmg&list=PL7jqd335f8HLpjujaLAYPeNZJcm3paGS9',
            'https://www.youtube.com/watch?v=OaGUwAFRKAQ&list=PL7jqd335f8HLpjujaLAYPeNZJcm3paGS9',
            'https://www.youtube.com/watch?v=l3hCZY4AyCA&list=PL7jqd335f8HLpjujaLAYPeNZJcm3paGS9',
            'https://www.youtube.com/watch?v=ib8FunNzsg0&list=PL7jqd335f8HLpjujaLAYPeNZJcm3paGS9',
            'https://www.youtube.com/watch?v=HNUYaAkuoiY',
            'https://www.youtube.com/watch?v=MBdVXkSdhwU&list=PL7yBElkdbdidH7nRZ0CriGvatgI9BCWDw',
            'https://www.youtube.com/watch?v=YHV1ElWorVg&list=PL7jqd335f8HLpjujaLAYPeNZJcm3paGS9',
            'https://www.youtube.com/watch?v=OHlVhhPIcu4&list=PL7jqd335f8HLpjujaLAYPeNZJcm3paGS9',
            'https://www.youtube.com/watch?v=cqtHelZZZRY',
'''
list_url  =['https://www.youtube.com/watch?v=Rr6jwLeXN7I&list=PLg-FPsrrA2425lsGINyhnUHNBJEFx7kXI',
            'https://www.youtube.com/watch?v=m87B0ulgN64&list=PL7jqd335f8HLpjujaLAYPeNZJcm3paGS9',
            'https://www.youtube.com/watch?v=YudHcBIxlYw&list=PLNF8K9Ddz0kKfujG6blfAxngYh_C66C_q',
            'https://www.youtube.com/watch?v=gQlMMD8auMs&list=PLNF8K9Ddz0kKfujG6blfAxngYh_C66C_q',
            'https://www.youtube.com/watch?v=awkkyBH2zEo&list=PLNF8K9Ddz0kKfujG6blfAxngYh_C66C_q',
            'https://www.youtube.com/watch?v=CKZvWhCqx1s&list=PLNF8K9Ddz0kKfujG6blfAxngYh_C66C_q',
            'https://www.youtube.com/watch?v=dyRsYk0LyA8&list=PLNF8K9Ddz0kKfujG6blfAxngYh_C66C_q',
            'https://www.youtube.com/watch?v=vRXZj0DzXIA&list=PLNF8K9Ddz0kKfujG6blfAxngYh_C66C_q',
            'https://www.youtube.com/watch?v=ioNng23DkIM&list=PLNF8K9Ddz0kKfujG6blfAxngYh_C66C_q',
            'https://www.youtube.com/watch?v=2S24-y0Ij3Y&list=PLNF8K9Ddz0kKfujG6blfAxngYh_C66C_q',
            'https://www.youtube.com/watch?v=b73BI9eUkjM&list=PLNF8K9Ddz0kKfujG6blfAxngYh_C66C_q',
            'https://www.youtube.com/watch?v=W0DM5lcj6mw',
            'https://www.youtube.com/watch?v=jJvDnYdD8JQ',
            'https://www.youtube.com/watch?v=ZFTOFnVybFU',
            'https://www.youtube.com/watch?v=AR0E8p2kYHE',
            'https://www.youtube.com/watch?v=C11N204LR1k',
            'https://www.youtube.com/watch?v=rpC1PohpbaQ',
            'https://www.youtube.com/watch?v=klCGOOgbqE4',
            'https://www.youtube.com/watch?v=ZpP1B_PM51s',
            'https://www.youtube.com/watch?v=A1vfHU7T08A',
            'https://www.youtube.com/watch?v=jS6F5D60y_c',
            'https://www.youtube.com/watch?v=lf0GKn9rbs8',
            'https://www.youtube.com/watch?v=pRbxlpvXw2s',
            'https://www.youtube.com/watch?v=eMaDFNRbmDQ',
            'https://www.youtube.com/watch?v=mG7kGuIFAw8',
            'https://www.youtube.com/watch?v=e-ORhEE9VVg&list=PLmU8B4gZ41idkZQL1ggCHkH94tVH3jVCT',
            'https://www.youtube.com/watch?v=IdneKLhsWOQ&list=PLmU8B4gZ41idkZQL1ggCHkH94tVH3jVCT',
            'https://www.youtube.com/watch?v=uI_ug1H6u0k&list=RDQMPE3ku5FqDjk',
            'https://www.youtube.com/watch?v=PaTBeGcDfHg&list=RDQMPE3ku5FqDjk',
            'https://www.youtube.com/watch?v=OViH68fJUhM&list=RDQMPE3ku5FqDjk',
            'https://www.youtube.com/watch?v=0FsPYnmjkN4&list=RDQMPE3ku5FqDjk',
            'https://www.youtube.com/watch?v=MmvpbLdaIRs&list=RDQMPE3ku5FqDjk',
            'https://www.youtube.com/watch?v=A_z5g0_hJN8&list=RDQMPE3ku5FqDjk',
]

for value in list_url:

# iterate the list 
# This captures the streams available for downloaded for the video i.e. 360p, 720p, 1080p. etc.
# filter out audio only but the format will be MP4

    url = YouTube(str(value))
    video_dl = url.streams.filter(only_audio=True, file_extension='mp4').first()
    video_dl.download(r'C:\Users\email\OneDrive\Desktop\Download\Audio')



# Commit can be done