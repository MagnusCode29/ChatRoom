# Generated by Django 4.2.4 on 2024-02-15 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baseApp', '0004_rename_grdescriptionn_group_groupdescriptionn_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['-createdTime']},
        ),
        migrations.RenameField(
            model_name='group',
            old_name='GroupDescriptionn',
            new_name='GroupDescription',
        ),
    ]