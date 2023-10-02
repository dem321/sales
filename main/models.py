from django.db import models

from django.core.mail import send_mail
from django.utils import timezone

# Create your models here.
class Employee(models.Model):
    first_name = models.CharField('Имя', max_length=30)
    second_name = models.CharField('Фамилия', max_length=30)
    middle_name = models.CharField('Отчество', max_length=30)
    
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.second_name + ' ' + self.first_name + ' ' + self.middle_name

class Dish(models.Model):
    name = models.CharField('Название', max_length=30)
    components = models.CharField('Состав', max_length=30)
    price = models.IntegerField('Цена')
    picture = models.ImageField('Изображение', upload_to='media/img')

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

class Order(models.Model):
    date = models.DateTimeField('Дата заказа')
    employee = models.ForeignKey(Employee, models.CASCADE, verbose_name='Сотрудник')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class DishOrder(models.Model):
    order = models.ForeignKey(Order, models.CASCADE, verbose_name='Заказ')
    dish = models.ForeignKey(Dish, models.CASCADE, verbose_name='Блюдо')
    count = models.PositiveIntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'БлюдоЗаказа'
        verbose_name_plural = 'БлюдоЗаказа'

