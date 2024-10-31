from django.db import migrations


def migrate_default_members_to_curator(apps, schema_editor):
    Group = apps.get_model("auth", "Group")

    default_group = Group.objects.filter(name="default").first()
    curator_group, _ = Group.objects.get_or_create(name="curator")
    Group.objects.get_or_create(name="read_only")

    if default_group:
        curator_group.permissions.add(*default_group.permissions.all())
        for user in default_group.user_set.all():
            user.groups.add(curator_group)
            user.groups.remove(default_group)


def reverse_default_members_from_curator(apps, schema_editor):
    Group = apps.get_model("auth", "Group")

    curator_group = Group.objects.filter(name="curator").first()
    default_group, _ = Group.objects.get_or_create(name="default")

    if curator_group:
        for user in curator_group.user_set.all():
            user.groups.add(default_group)
            user.groups.remove(curator_group)

    Group.objects.filter(name="read_only").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core_main_app", "0009_template_formats"),
        ("auth", "__latest__"),
    ]

    operations = [
        migrations.RunPython(
            migrate_default_members_to_curator,
            reverse_default_members_from_curator,
        ),
    ]
