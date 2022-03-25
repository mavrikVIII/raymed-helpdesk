from django.db import models
from django.contrib.auth.models import User
from raymedasset.models import Device, Person, Subdevice

class Error(models.Model):
    STATUS_CHOICE = (
("wait","Ожидание"),
("in_work", "В работе"),
("ready", "Готово"))

    person = models.ForeignKey(User, blank = True, on_delete = models.CASCADE)
    device = models.ForeignKey(Device, blank = True, null = True, on_delete = models.CASCADE)
    message_error = models.TextField('Неисправность', null = True, blank = True)
    status = models.CharField("Статус обращения",max_length = 30, default = STATUS_CHOICE[0][0], choices = STATUS_CHOICE )
    time_post_message = models.DateTimeField('Время обращения')
    solutions = models.TextField('Решение проблемы', null = True, blank = True)
    image_error = models.ImageField('Скриншот ошибки', upload_to = 'images/error/',  blank=True)

    def __str__(self):
        if self.device:
            return  str(self.device)
        else:
            return str(self.person)

    class Meta:
        verbose_name = 'Проблема'
        verbose_name_plural = 'Проблемы'
