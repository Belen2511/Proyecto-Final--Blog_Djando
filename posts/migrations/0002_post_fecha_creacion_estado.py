from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='creado',
            new_name='fecha_creacion',
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-fecha_creacion']},
        ),
        migrations.AddField(
            model_name='post',
            name='estado',
            field=models.CharField(choices=[('borrador', 'Borrador'), ('publicado', 'Publicado'), ('archivado', 'Archivado')], default='borrador', max_length=10),
        ),
    ]
