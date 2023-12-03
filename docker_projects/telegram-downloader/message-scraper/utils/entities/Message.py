class Message:
    def __init__(self, id, date):
        self.id = id
        self.date = date
    
    def to_tuple(self):
        return (self.id, self.date)