class Subtitle:
    def __init__(self,videoId, num, start, end, text, lang):
        self.videoId= videoId
        self.num=num
        self.start=start
        self.end=end
        self.text=text
        self.lang=lang

class Video:
    def __init__(self, id, categoryId, channelId, title, level):
        self.id = id
        self.categoryId=categoryId
        self.channelId = channelId
        self.title= title
        self.level= level














