class Link:
    def __init__(self, id, url, message_id):
        self.url = url
        self.message_id = message_id
        self.id = id
    
    def to_tuple(self):
        return (self.url, self.message_id)