from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        # Add your dependencies here if any
        # ('your_app', 'previous_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=255)),
                ('source_language', models.CharField(max_length=10)),
                ('target_language', models.CharField(max_length=10)),
                ('start_time', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tasks',
            },
        ),
    ]
