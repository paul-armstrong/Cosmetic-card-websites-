
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_merge_20240506_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
    ]
