from django.db import models

# Create your models here.
YEAR = (
    ('Second', 'Second'),
    ('Third', 'Third'),
    ('Fourth', 'Fourth'),
)

MODE = (
    ('Online', 'Online'),
    ('Offline', 'Offline'),
)

STATUS = (
    ('Upcoming', 'Upcoming'),
    ('Past', 'Past'),
    ('Live', 'Live'),
)
class Members(models.Model):
    username = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    bio = models.TextField(default='', null=True, blank=True)
    year = models.CharField(max_length=10, choices=YEAR, default='Second')
    post = models.CharField(max_length=100, null=True, blank=True, default='Senior Member')
    sno = models.IntegerField(blank=True, null =True)
    dp = models.ImageField(upload_to='memberDPs/', blank=True, null=True)
    facebook_url = models.URLField(max_length=300, null=True, blank=True)
    instagram_url = models.URLField(max_length=300, null=True, blank=True)
    linkedin_url = models.URLField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.firstname


class blog(models.Model):
    title = models.CharField(max_length=255)
    blog_text = models.TextField(max_length=50000)
    image_url = models.URLField(max_length=300, null=True, blank=True)
    created_on = models.DateTimeField('Date created on.', auto_now_add=True)
    active = models.BooleanField(default=True)
    author = models.CharField(max_length=255)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comments(models.Model):
    post = models.ForeignKey(
        blog, on_delete=models.CASCADE, related_name='comments')
    comment_by = models.CharField(max_length=255, null=True)
    comment = models.TextField(max_length=5000)
    commented_on = models.DateTimeField(
        'Date commented on :', auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-commented_on']

    def __str__(self):
        return self.comment_by


class event(models.Model):
    event_name = models.CharField(max_length=255)
    event_description = models.TextField(max_length=50000)
    poster = models.ImageField(
        upload_to='eventPosters/', blank=True, null=True)
    event_datetime = models.DateTimeField(
        'Date of event : ', auto_now_add=False)
    event_mode = models.CharField(
        max_length=15, choices=MODE, default='Online')
    event_status = models.CharField(
        max_length=20, choices=STATUS, default='Past')
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-event_datetime']

    def __str__(self):
        return self.event_name

class Candidates(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=20)
    status = models.BooleanField(default=1)


    class Meta:
        ordering = ['-status', 'name']

    def __str__(self):
        return "{} : status {}".format(self.name, self.status)

class auditionRounds(models.Model):
    roundno = models.IntegerField(default=1)
    candidate = models.ForeignKey(Candidates, on_delete=models.CASCADE, related_name='inductees')

    def __str__(self):
        return "Round: {}".format(self.roundno)

class auditionQuestions(models.Model):
    roundno = models.IntegerField(default=1)
    serialno = models.IntegerField(default=1)
    question = models.CharField(max_length=5000)
    round = models.ForeignKey(auditionRounds, on_delete=models.CASCADE, related_name='round')

    class Meta:
        unique_together = ('roundno', 'serialno',)
        ordering = ['roundno', 'serialno']

    def __str__(self):
        return "Round {}, qno {} : {}".format(self.roundno, self.serialno, self.question)

class auditionAnswers(models.Model):
    q = models.ForeignKey(auditionQuestions, on_delete=models.CASCADE, related_name='problem')
    ans = models.CharField(max_length=5000)
    ansby = models.ForeignKey(Candidates, on_delete=models.CASCADE, related_name='candidate')
    anstime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Round {} q: {}, answered by {}".format(self.q.roundno , self.q.serialno, self.ansby.name)





