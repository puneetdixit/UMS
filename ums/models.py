import binascii
import os
import time

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


class CustomToken(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)

    """Uncomment below part if you want to use Predefined Token Model"""
    # user = models.OneToOneField(User,
    #     related_name='custom_auth_token',
    #     on_delete=models.CASCADE, verbose_name="user_id"
    # )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user_id")
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    expires_time = models.CharField(max_length=30, default=time.time() + 86400)
    is_revoked = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(CustomToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        CustomToken.objects.create(user=instance, expires_time=time.time() + 86400)


class Courses(models.Model):
    course_name = models.CharField(max_length=100, null=False, unique=True)
    duration = models.IntegerField(null=False)


class Streams(models.Model):
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    stream_name = models.CharField(max_length=50, null=False)


class Subjects(models.Model):
    stream_id = models.ForeignKey(Streams, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=50, null=False, unique=True)
    semester = models.IntegerField(null=False)

# def update_auto_increment(start, table_name):
#     """Update our increments"""
#     from django.db import connection, transaction
#     cursor = connection.cursor()
#     q = "ALTER table {} AUTO_INCREMENT={}".format(table_name, start)
#     c = cursor.execute(q)
#     print("Update auto increment", c)
#     transaction.commit()

# update_auto_increment(20210001, "ums_studentmodel")
