# Generated by Django 4.2.5 on 2023-12-30 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Blog", "0006_group_created_by_alter_group_admins"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofilepic",
            name="firebase_uid",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
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
                ],
                default="",
                max_length=30,
                null=True,
            ),
        ),
    ]
