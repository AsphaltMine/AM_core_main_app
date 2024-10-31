from django.db import migrations


def move_curator_members_back_to_default(apps, schema_editor):
    Group = apps.get_model("auth", "Group")

    curator_group = Group.objects.filter(name="curator").first()
    default_group, _ = Group.objects.get_or_create(name="default")

    if curator_group:
        for user in curator_group.user_set.all():
            user.groups.add(default_group)
            user.groups.remove(curator_group)


def move_default_members_to_curator(apps, schema_editor):
    Group = apps.get_model("auth", "Group")

    default_group = Group.objects.filter(name="default").first()
    curator_group, _ = Group.objects.get_or_create(name="curator")

    if default_group:
        for user in default_group.user_set.all():
            user.groups.add(curator_group)
            user.groups.remove(default_group)


class Migration(migrations.Migration):

    dependencies = [
        ("core_main_app", "0010_read_only_default_group"),
    ]

    operations = [
        migrations.RunPython(
            move_curator_members_back_to_default,
            move_default_members_to_curator,
        ),
    ]
