from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')


    def __str__(self):
        return f'{self.user.username} Profile'
    

    def save(self, *args, **kwargs):
        try:
            old_image = Profile.objects.get(pk=self.pk).image
        except Profile.DoesNotExist:
            old_image = None

        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

        if old_image and old_image != 'default.jpg' and old_image != self.image:
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)

    