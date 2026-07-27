from django.db import migrations
from django.db.models import Count


def deduplicate_immobile_codes(apps, schema_editor):
    """
    Renomeia códigos duplicados de imóveis adicionando sufixo incremental.
    Preserva todos os registros e suas imagens.
    """
    Immobile = apps.get_model('locacao', 'Immobile')

    # Find codes that appear more than once
    dupes = (
        Immobile.objects.values('code')
        .annotate(cnt=Count('id'))
        .filter(cnt__gt=1)
    )

    for d in dupes:
        imoveis = Immobile.objects.filter(code=d['code']).order_by('id')
        for i, im in enumerate(imoveis):
            if i > 0:
                im.code = f"{im.code}-{i + 1}"
                im.save(update_fields=['code'])


class Migration(migrations.Migration):

    dependencies = [
        ('locacao', '0004_alter_client_email_alter_client_name_and_more'),
    ]

    operations = [
        migrations.RunPython(deduplicate_immobile_codes),
    ]
