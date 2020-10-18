from django.db import models
from django.urls import reverse

# Create your models here.

## Vessel Model
class Vessel(models.Model):
    '''Model representing a Vessel.'''
    code = models.CharField(
        max_length=6,
        unique=True,
        null=False,
        blank=False,
    )

    def __str__(self):
        '''String representing the vessel object.'''
        return self.code


class Equipment(models.Model):
    '''Model representing an equipment.'''
    name = models.CharField(
        max_length=20,
        null=False,
        blank=False,
    )

    code = models.CharField(
        max_length=8,
        unique=True,
        null=True,
        blank=False,
    )

    location = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        help_text=' Location of the Equipment'
    )

    vessel = models.ForeignKey(
        Vessel,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        default=1,
    )

    status = models.BooleanField(
        blank=False,
        null=False,
        default=True,
        help_text='Equipment status'
    )


    class Meta:
        ordering = [
            'vessel',
            'name',
            'code',
            'location',
            'status',
        ]


    def __str__(self):
        '''String representing the model equipment.'''
        return self.name
