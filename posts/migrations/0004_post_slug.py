from django.db import migrations, models
from django.utils.text import slugify


def poblar_slugs(apps, schema_editor):
    Post = apps.get_model("posts", "Post")
    usados = set()
    for post in Post.objects.order_by("pk"):
        base = slugify(post.titulo)[:200] or "post"
        slug, n = base, 2
        while slug in usados:
            slug = f"{base}-{n}"
            n += 1
        usados.add(slug)
        post.slug = slug
        post.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0003_comentario"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="slug",
            field=models.SlugField(blank=True, default="", max_length=220),
            preserve_default=False,
        ),
        migrations.RunPython(poblar_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.SlugField(blank=True, max_length=220, unique=True),
        ),
    ]
