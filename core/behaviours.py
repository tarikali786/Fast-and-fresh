import uuid
from django.db import models


class StatusMixin(models.Model):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    isActive = models.BooleanField(default=True, blank=True)
    created_at= models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    class Meta:
        abstract = True



class UUIDMixin(models.Model):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_at= models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True
