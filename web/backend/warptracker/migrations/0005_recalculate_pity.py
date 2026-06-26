from django.db import migrations


def recalculate_pity(apps, schema_editor):
    Warp = apps.get_model('warptracker', 'Warp')
    GachaType = apps.get_model('warptracker', 'GachaType')

    for g in GachaType.objects.all():
        warps = Warp.objects.filter(gacha_id__gacha_type=g.id).order_by('warp_id')

        current_pity = 0
        updates = []

        for warp in warps:
            current_pity += 1
            warp.pity = current_pity
            updates.append(warp)

            if warp.item_id.rarity == 5:
                current_pity = 0

        if updates:
            Warp.objects.bulk_update(updates, ['pity'])


class Migration(migrations.Migration):

    dependencies = [
        ('warptracker', '0004_calculate_pity'),
    ]

    operations = [
        migrations.RunPython(recalculate_pity),
    ]
