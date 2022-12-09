from django.db import models
from datetime import datetime

class Trait(models.Model):
    name = models.CharField(max_length=20, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    pets = models.ManyToManyField(
        "pets.Pet",
        related_name="traits"
    )

    def __repr__(self):
        return f"<Trait {self.id} - {self.name}>"
