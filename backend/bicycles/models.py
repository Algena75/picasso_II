from django.db import models

from users.models import User


class Bicycle(models.Model):
    number = models.IntegerField(unique=True, verbose_name='Номер велосипеда')
    is_rented = models.BooleanField(
        default=False,
        verbose_name='Статус велосипеда'
    )

    def __str__(self) -> str:
        return f'{self.number}'


class Rent(models.Model):
    bicycle = models.ForeignKey(
        Bicycle,
        on_delete=models.CASCADE,
        related_name='rents',
        verbose_name='Велосипед'
    )
    renter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rents',
        verbose_name='Арендатор'
    )
    start_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Начало аренды'
    )
    finish_time = models.DateTimeField(
        verbose_name='Конец аренды',
        default=None,
        null=True,
        blank=True
    )
    value = models.IntegerField(
        verbose_name='Стоимость аренды',
        default=None,
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return f'{self.renter} >>> {self.bicycle}'
