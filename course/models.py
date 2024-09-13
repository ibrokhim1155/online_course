from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.title

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='teachers/', blank=True, null=True)
    telegram_url = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    instagram_url = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def clean(self):
        if not (self.telegram_url or self.instagram_url):
            raise ValidationError(_("At least one social media URL should be provided."))

    def __str__(self):
        return self.full_name

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, blank=True, null=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

class Video(models.Model):
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    duration = models.DurationField()
    file = models.FileField(upload_to='videos/')

    class Meta:
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")

    def __str__(self):
        return f'{self.name} - {self.course.name}'

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    phone_number = models.CharField(max_length=20, validators=[])
    courses = models.ManyToManyField(Course, related_name='customers')

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return self.user.username

    def clean(self):
        if not self.phone_number.isdigit():
            raise ValidationError(_("Phone number should only contain digits."))

class Blog(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")

    def __str__(self):
        return self.title

class Comment(models.Model):
    class RatingChoices(models.IntegerChoices):
        ONE = 1, _("One")
        TWO = 2, _("Two")
        THREE = 3, _("Three")
        FOUR = 4, _("Four")
        FIVE = 5, _("Five")

    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    rating = models.IntegerField(choices=RatingChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.title}'

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError(_("Rating must be between 1 and 5."))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
