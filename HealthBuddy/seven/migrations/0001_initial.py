
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [

    ]

    operations = [
        migrations.CreateModel(
            name='TestPres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('test', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.Prescription')),
            ],
        ),
    ]
