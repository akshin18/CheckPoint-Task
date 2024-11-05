import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Specify that this is an abstract base class
        abstract = True


class Pattern(BaseModel):
    name = models.CharField(max_length=100)
    regex = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class FlaggedMessage(BaseModel):
    client_msg_id = models.CharField(max_length=255, unique=True, default=None)
    content = models.TextField()
    matched_pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.matched_pattern.name} match at {self.created_at}"
