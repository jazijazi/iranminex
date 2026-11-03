from django.core.management.base import BaseCommand
from layers.models.models import LayersNames
from contracts.models.models import ContractDomin

class Command(BaseCommand):
    help = "Add layers name record for every layer group and ContractDomin"

    def handle(self, *args, **options):
        new_layers = [
            {"layername_en": "Face_Brick_Pg", "layername_fa": "سینه کار اکتشافی", "geometrytype": "fill"},
            {"layername_en": "Face_Brick_Pl", "layername_fa": "سینه کار اکتشافی", "geometrytype": "line"},
        ]

        # Get all unique layer groups
        layer_groups = LayersNames.objects.values('lyrgroup_en', 'lyrgroup_fa').distinct()

        # Get all ContractDomin objects
        all_dtyps = ContractDomin.objects.all()

        created_count = 0

        for lg in layer_groups:
            for dt in all_dtyps:
                for new_layer in new_layers:
                    # Avoid duplicates
                    exists = LayersNames.objects.filter(
                        dtyp=dt,
                        lyrgroup_en=lg['lyrgroup_en'],
                        lyrgroup_fa=lg['lyrgroup_fa'],
                        layername_en=new_layer['layername_en'],
                        layername_fa=new_layer['layername_fa'],
                    ).exists()

                    if not exists:
                        LayersNames.objects.create(
                            dtyp=dt,
                            lyrgroup_en=lg['lyrgroup_en'],
                            lyrgroup_fa=lg['lyrgroup_fa'],
                            layername_en=new_layer['layername_en'],
                            layername_fa=new_layer['layername_fa'],
                            geometrytype=new_layer['geometrytype']
                        )
                        created_count += 1
                        self.stdout.write(self.style.SUCCESS(f"layer with name {new_layer['layername_en']} and group {lg['lyrgroup_en']} created in {dt.title} with code {dt.code}"))

                    else:
                        self.stdout.write(self.style.WARNING(f"layer with name {new_layer['layername_en']} and group {lg['lyrgroup_en']} already exist in {dt.title} with code {dt.code}"))


        self.stdout.write(self.style.SUCCESS(f"Done! {created_count} new layer records added."))