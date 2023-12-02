# Generated by Django 4.2.5 on 2023-10-04 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("agent", "0011_rename_intentresponse_intentresponseevent_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="eventaction",
            name="event",
        ),
        migrations.AddField(
            model_name="eventaction",
            name="intentResponseEvent",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="agent.intentresponseevent"
            ),
        ),
    ]
