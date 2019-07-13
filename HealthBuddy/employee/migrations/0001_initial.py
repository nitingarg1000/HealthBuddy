
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('desig', models.CharField(max_length=50)),
                ('dept', models.CharField(max_length=50)),
                ('office', models.CharField(max_length=50)),
                ('tel', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('blood_group', models.CharField(max_length=10)),
                ('resid', models.CharField(max_length=50)),
            ],
        ),
    ]
