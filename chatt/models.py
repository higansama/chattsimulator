from os import name
from django.db import models
# Create your models here.


class UserChatt(models.Model):
    username = models.CharField(max_length=32, blank=False, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pk) + " " + self.username

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.judul)
    #     super(Books, self).save(*args, **kwargs)


class Rooms(models.Model):
    name = models.CharField(max_length=32, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk) + " " + self.name

    

class Participants(models.Model):
    rooms_id = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    participant = models.ForeignKey(UserChatt, on_delete=models.CASCADE)

    def __str__(self):
        return str(
            self.pk
        ) + " " + self.rooms_id.name + " " + self.participant.username

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.judul)
    #     super(Books, self).save(*args, **kwargs)


class Chatt(models.Model):
    message = models.TextField()
    rooms = models.ForeignKey(Rooms, on_delete=models.CASCADE, blank=True)
    participant = models.ForeignKey(Participants, on_delete=models.CASCADE)
    read_by = models.CharField(max_length=92)

    def __str__(self):
        return str(self.pk) + " " + str(
            self.participant.rooms_id) + " " + self.participant.username

    def ReadThisMessage(self, reader):
        pass