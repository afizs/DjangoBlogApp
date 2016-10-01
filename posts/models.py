from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse


# Create your models here.
def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    content = models.TextField(max_length=5000)
    image = models.ImageField(null=True, blank=True, upload_to=upload_location,
                              height_field="height_field", width_field="width_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    draft = models.BooleanField(default=False)
    publish = models.DateTimeField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={"post_id": self.id})
        # return "/posts/%s/" % self.id

    # this help to retrieve objects in the reverse order - represents reverse
    class Meta:
        ordering = ["-timestamp", "-updated"]





