from django.db import models
from django.contrib.auth import get_user_model 
from django.db.models import Sum

class Fundraiser(models.Model):
    GENRE_TYPES_CHOICES = [
    ### Fiction
    ('drama', 'Drama'),
    ('romance', 'Romance'),
    ('crime', 'Crime'),
    ('thriller', 'Thriller'),
    ('fantasy', 'Fantasy'),
    ('scifi', 'Sci-Fi'),
    ('youngadult', 'Young Adult'),
    ('children', 'Children'),

    #### Non-fiction
    ('selfhelp', 'Self-Help'),
    ('biography', 'Biography'),
    ('history', 'History'),
    ('knowledge', 'Knowledge'),
    ('poem', 'Poem'),

    #### Poetry
    ('classic', 'Classic'),
    ('modern', 'Modern'),
    ('short', 'Short'),

    #### Kids
    ('picture', 'Picture'),
    ('middle', 'Middle'),

    #### Other
    ('misc', 'Misc'),

    ]
    title = models.CharField(max_length=200)
    genre_type=models.CharField(max_length=20, choices=GENRE_TYPES_CHOICES, default='drama')
    description = models.TextField()
    goal=models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    start_date =models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(get_user_model(),related_name='owned_fundraisers',on_delete=models.CASCADE )

    def progress(self):
        total_donations = sum(s.amount for s in self.pledges.all())
        if self.goal == 0:
            return 0
        progress_percentage = (total_donations / self.goal) * 100
        return (progress_percentage, 100)

class Pledge(models.Model):
    TIER_CHOICES = [
        (1, 'Tier 1:Baisc'),
        (2, 'Tier 2:Hard Copy'),
        (3, 'Tier 3:Signed Copy'),
    ]
    tier_level = models.IntegerField(choices=TIER_CHOICES, default=1)
    amount = models.IntegerField()
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    fundraiser = models.ForeignKey('Fundraiser', related_name='pledges',on_delete=models.CASCADE) # if fundraiser is deleted, it deletes the pledge as well.
    supporter = models.ForeignKey(get_user_model(),related_name='pledges',on_delete=models.CASCADE # if fundraiser is deleted, it deletes the pledge as well.  

    )
class Comment(models.Model):
    text = models.TextField()
    fundraiser = models.ForeignKey('Fundraiser', related_name='comments', on_delete=models.CASCADE) # if fundraiser is deleted, it deletes the comment as well.
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(),related_name='comments',on_delete=models.CASCADE) # if user is deleted, it deletes the comment as well.

class Like(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='likes', on_delete=models.CASCADE)
    fundraiser = models.ForeignKey('Fundraiser', related_name='likes', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'fundraiser')  # ensures a user can like a fundraiser only once