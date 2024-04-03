# Generated by Django 5.0.3 on 2024-04-03 03:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Blog", "0012_chatroom"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofilepic",
            name="branch",
            field=models.CharField(
                blank=True,
                choices=[
                    ("CSE", "Computer Science and Engineering"),
                    ("CSE_DS", "Computer Science and Engineering (Data Science)"),
                    ("CSE_CS", "Computer Science and Engineering (Cyber Security)"),
                    ("ISE", "Information Science and Engineering"),
                    ("EE", "Electrical Engineering"),
                    ("ME", "Mechanical Engineering"),
                    ("TE", "Telecommunication Engineering"),
                    ("IEM", "Industrial Engineering and Management"),
                    ("AIML", "Artificial Intelligence and Machine Learning"),
                    ("AE", "Aerospace Engineering"),
                    ("MCA", "Masters of Computer Applications"),
                    ("ECE", "Electronics and Telecommunication Engineering"),
                    ("EIE", "Electronics and Instrumentation Engineering"),
                    ("EEE", "Electrical and Electronics Engineering"),
                    ("CE", "Chemical Engineering"),
                    ("CV", "Civil Engineering"),
                    ("BT", "Biotechnology"),
                    ("RVC", "RV Connect"),
                ],
                default="",
                max_length=30,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="userprofilepic",
            name="college",
            field=models.CharField(
                blank=True,
                choices=[
                    ("RVCE", "R.V. College of Engineering"),
                    ("RVU", "R.V. University"),
                    ("HW", "Hogwarts School of Witchcraft and Wizardry"),
                ],
                default="",
                max_length=30,
                null=True,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="membership",
            unique_together={("user", "group")},
        ),
    ]