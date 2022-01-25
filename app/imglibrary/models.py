from django.db import models

class ImageFile(models.Model):
    image_file = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.image_file.name