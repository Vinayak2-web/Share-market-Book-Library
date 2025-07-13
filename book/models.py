from django.db import models # type: ignore

class Book(models.Model):
    title = models.CharField(max_length=200,null=True,blank=True)
    author = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField()
    book_cover=models.ImageField( upload_to='book/',null=True,blank=True)
    slug=models.CharField(max_length=2000,null=True,blank=True)
    url=models.URLField(max_length=2000,null=True,blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = '-'.join((self.title + ' ' + str(self.author)).split())
        super().save(*args, **kwargs)


# Create your models here.
