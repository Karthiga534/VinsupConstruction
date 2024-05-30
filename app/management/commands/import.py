import os
import json
from django.core.management.base import BaseCommand
from django.apps import apps

# class Command(BaseCommand):
#     help = 'Import data from JSON files into specified models'

#     def handle(self, *args, **options):
#         data_folder = 'exported_data'  
#         for file_name in os.listdir(data_folder):
#             if file_name.endswith('.json'):
#                 file_path = os.path.join(data_folder, file_name)
#                 with open(file_path, 'r') as f:
#                     data = json.load(f)
#                     model_name = file_name.replace('.json', '')
#                     Model = apps.get_model('app', model_name)

#                     for item in data:
#                         item_data = {key: value for key, value in item.items() if key != 'id'}
#                         instance, created = Model.objects.get_or_create(**item_data, defaults=item)
#                         if not created:
#                             pass

#                 self.stdout.write(self.style.SUCCESS(f'Data imported for {model_name}.'))

#         self.stdout.write(self.style.SUCCESS('All data imported successfully.'))


import os
import json
from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Import data from JSON files into specified models'

    def handle(self, *args, **options):
        data_folder = 'exported_data'
        for file_name in os.listdir(data_folder):
            if file_name.endswith('.json'):
                file_path = os.path.join(data_folder, file_name)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    model_name = file_name.replace('.json', '')
                    Model = apps.get_model('app', model_name)

                    for item in data:
                        item_id = item.pop('id', None)
                        if item_id and Model.objects.filter(id=item_id).exists():
                            instance = Model.objects.get(id=item_id)
                            for key, value in item.items():
                                setattr(instance, key, value)
                            instance.save()
                        else:
                            instance = Model(**item)
                            if item_id:
                                instance.id = item_id
                            instance.save()

                self.stdout.write(self.style.SUCCESS(f'Data imported for {model_name}.'))

        self.stdout.write(self.style.SUCCESS('All data imported successfully.'))
