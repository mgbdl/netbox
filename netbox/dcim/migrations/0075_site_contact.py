# Generated by Django 2.2.4 on 2019-09-25 01:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
        ('dcim', '0074_increase_field_length_platform_name_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sites', to='contacts.Contact'),
        ),
    ]
