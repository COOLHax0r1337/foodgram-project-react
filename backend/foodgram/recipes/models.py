from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        'Ingredient name',
        max_length=200)
    measurement_unit = models.CharField(
        'Ingredient unit size',
        max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}.'


class Tag(models.Model):
    name = models.CharField(
        'Name',
        max_length=60,
        unique=True)
    color = models.CharField(
        'Color',
        max_length=7,
        unique=True)
    slug = models.SlugField(
        'Link',
        max_length=100,
        unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Author')
    name = models.CharField(
        'Recipe name',
        max_length=255)
    image = models.ImageField(
        'Recipe img',
        upload_to='static/recipe/',
        blank=True,
        null=True)
    text = models.TextField(
        'Recipe desc')
    cooking_time = models.BigIntegerField(
        'Cooking time')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient')
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Tags',
        related_name='recipes')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Cooking time minutes',
        validators=[validators.MinValueValidator(
            1, message='Min. cooking time is 1 minute'), ])
    pub_date = models.DateTimeField(
        'Pub date',
        auto_now_add=True)

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ('-pub_date', )

    def __str__(self):
        return f'{self.author.email}, {self.name}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe')
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        related_name='ingredient')
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=(
            validators.MinValueValidator(
                1, message='Min. ingredients amount is 1'),),
        verbose_name='Amount',)

    class Meta:
        verbose_name = 'Ingredient amount'
        verbose_name_plural = 'Ingredients amount'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique ingredient')]


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following')
    created = models.DateTimeField(
        'Sub date',
        auto_now_add=True)

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription')]

    def __str__(self):
        return f'User {self.user} -> author {self.author}'


class FavoriteRecipe(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='favorite_recipe',
        verbose_name='User')
    recipe = models.ManyToManyField(
        Recipe,
        related_name='favorite_recipe')

    class Meta:
        verbose_name = 'Favorite recipe'
        verbose_name_plural = 'Favorite recipes'

    def __str__(self):
        list_ = [item['name'] for item in self.recipe.values('name')]
        return f'User {self.user} added {list_} to favorites.'

    @receiver(post_save, sender=User)
    def create_favorite_recipe(
            sender, instance, created, **kwargs):
        if created:
            return FavoriteRecipe.objects.create(user=instance)


class ShoppingCart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        null=True,
        verbose_name='User')
    recipe = models.ManyToManyField(
        Recipe,
        related_name='shopping_cart',
        verbose_name='Purchase')

    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'
        ordering = ['-id']

    def __str__(self):
        list_ = [item['name'] for item in self.recipe.values('name')]
        return f'User {self.user} added {list_} in cart.'

    @receiver(post_save, sender=User)
    def create_shopping_cart(
            sender, instance, created, **kwargs):
        if created:
            return ShoppingCart.objects.create(user=instance)
