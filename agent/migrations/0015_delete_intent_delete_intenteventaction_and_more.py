# Generated by Django 4.2.5 on 2023-10-04 22:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("agent", "0014_remove_entitytypes_agent_and_more"),
        ("chat", "0005_alter_message_intent"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Intent",
        ),
        migrations.DeleteModel(
            name="IntentEventAction",
        ),
        migrations.DeleteModel(
            name="IntentExample",
        ),
        migrations.DeleteModel(
            name="IntentResponseEvent",
        ),
        migrations.DeleteModel(
            name="ResponseText",
        ),
    ]