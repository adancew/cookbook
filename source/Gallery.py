
class Photo:
    def __init__(self, file: str):
        self.filename = file
        
    def __str__(self):
        return self.filename

class Gallery:
    def __init__(self):
        self.photos = []
        self.main_photo = None
    
    def addPhoto(self, filename: str):
        photo = Photo(filename)
        self.photos.append(photo)
        if self.main_photo == None:
            self.main_photo = photo

    def removePhoto(self, filename: str):
        photo = Photo(filename)
        self.photos.remove(photo)

    def __str__(self):
        return ' '.join([str(p) for p in self.photos])
