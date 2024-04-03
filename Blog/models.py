from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import strip_tags



class Post(models.Model):
    COLOR_CHOICES = (
        ('red', 'Red'),
        ('green', 'Green'),
        ('blue', 'Blue'),
        ('yellow', 'Yellow'),
        ('pink', 'Pink'),
        ('purple', 'Purple'),
    )

    mentioned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentioned_in_posts', blank=True, null=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    color_code = models.CharField(max_length=10, choices=COLOR_CHOICES, default='red')

    def save(self, *args, **kwargs):
        # Basic sanitization: stripping HTML tags from the content
        self.content = strip_tags(self.content)

        super().save(*args, **kwargs)

#post like
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_liked = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} liked {self.post}"

    class Meta:
        unique_together = ('user', 'post')

# random-chat
class ChatRoom(models.Model):
    group_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"({self.group_id})"

class UserProfilePic(models.Model):
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science and Engineering'),
        ('CSE_DS', 'Computer Science and Engineering (Data Science)'),
        ('CSE_CS', 'Computer Science and Engineering (Cyber Security)'),
        ('ISE', 'Information Science and Engineering'),
        ('EE', 'Electrical Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('TE', 'Telecommunication Engineering'),
        ('IEM', 'Industrial Engineering and Management'),
        ('AIML', 'Artificial Intelligence and Machine Learning'),
        ('AE', 'Aerospace Engineering'),
        ('MCA', 'Masters of Computer Applications'),
        ('ECE', 'Electronics and Telecommunication Engineering'),
        ('EIE', 'Electronics and Instrumentation Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('CE', 'Chemical Engineering'),
        ('CV', 'Civil Engineering'),
        ('BT', 'Biotechnology'),
        ('RVC', 'RV Connect')
    ]

    COLLEGE_CHOICES = [
        ('RVCE', 'R.V. College of Engineering'),
        ('RVU', 'R.V. University'),
        ('HW', 'Hogwarts School of Witchcraft and Wizardry')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.CharField(max_length=300, default='', blank=True, null=True)
    branch = models.CharField(max_length=30, choices=BRANCH_CHOICES, default='', blank=True, null=True)
    college = models.CharField(max_length=30, choices=COLLEGE_CHOICES, default='', blank=True, null=True)
    firebase_uid = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return f"{self.user.username} - {self.get_branch_display()}"


class Comments(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, null=True)
    user_commented = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    upvote = models.BooleanField(default=False)
    downvote = models.BooleanField(default=False)
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(upvote=False) | models.Q(downvote=False),
                name='upvote-downvote exclusive',
                violation_error_message='You cannot simultaneously upvote and downvote this comment.',
            )
        ]


class Friendship(models.Model):
    friendship_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friendships')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_friendships')
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('unfriended', 'Unfriended'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.friend.username}: {self.status}"

class FriendRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=('pending', 'Pending'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}: {self.status}"


class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, through='Membership')
    created_by = models.ForeignKey(User, related_name='created_groups', null=True, on_delete=models.CASCADE)
    admin = models.OneToOneField(User, related_name='admin_group', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new_group = self.pk is None
        super().save(*args, **kwargs)

        if is_new_group:
            # Add logic for newly created group
            pass


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'group']  # Unique constraint on user and group combination

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"




