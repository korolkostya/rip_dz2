from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.template.defaultfilters import slugify
from unidecode import unidecode
from django.db.models.signals import post_save
from django.dispatch import receiver


class Flight(models.Model):
    flightnumb = models.CharField(max_length=25, verbose_name='№ рейса')
    flighymodel = models.CharField(max_length=50, verbose_name='Модель самолета')
    flightfrom = models.CharField(max_length=25, verbose_name='Откуда')
    flightto = models.CharField(max_length=25, verbose_name='Куда')
    slug = models.SlugField(max_length=200, verbose_name='Слаг', db_index=True)
    description = models.TextField(blank=True, verbose_name='Описание рейса')
    photo = models.ImageField(default='../static/images/not_found2.jpg',
                              upload_to='flights/%Y',
                              verbose_name='Картинка рейса')
    customer = models.ForeignKey(User,
                                 related_name='flight_created',
                                 on_delete=models.CASCADE,
                                 verbose_name='Перевозчик')
    bookings = models.ManyToManyField(User, related_name='flight_booking', blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='Цена перелета',
                                validators=[MinValueValidator(0.01)])
    active = models.BooleanField(default=True, blank=False, verbose_name='Рейс активен')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return "{}".format(self.flightnumb)

    def get_absolute_url(self):
        return reverse('flights:detail', args=[self.id, self.slug])

    class Meta:
        ordering = ('-updated',)
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'


def create_slug(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(unidecode(instance.flightnumb))

    qs = Flight.objects.filter(slug=slug).order_by('-id')

    if qs.exists():
        new_slug = '{}-{}'.format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)

    return slug


@receiver(post_save, sender=Flight)
def pre_save_service_reciever(sender, instance, *args, **kwargs):

    if not instance.slug:
        instance.slug = create_slug(instance)
        instance.save()

    n_slug = slugify(unidecode(instance.flightnumb))

    print(n_slug)
    print(instance.slug)

    if n_slug != instance.slug:
        instance.slug = n_slug
        instance.save()
