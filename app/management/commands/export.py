from django.core.management.base import BaseCommand
from django.apps import apps
import json
import os

class Command(BaseCommand):
    help = 'Export data from specified models to JSON files'

    def handle(self, *args, **options):
        models = [
            {'model_name': 'CompanyPlan', 'app_name': 'app', 'file_name': 'CompanyPlan.json'},
            {'model_name': 'CompanyPlanLimits', 'app_name': 'app', 'file_name': 'CompanyPlanLimits.json'},
            {'model_name': 'AssetType', 'app_name': 'app', 'file_name': 'AssetType.json'},
            {'model_name': 'Mode', 'app_name': 'app', 'file_name': 'Mode.json'},
             {'model_name': 'BuildingType', 'app_name': 'app', 'file_name': 'BuildingType.json'},  
              {'model_name': 'Duration', 'app_name': 'app', 'file_name': 'Duration.json'},  
            #  add units also
            
        ]

        output_folder = 'exported_data'  
        os.makedirs(output_folder, exist_ok=True)  

        for model_info in models:
            Model = apps.get_model(model_info['app_name'], model_info['model_name'])
            data = list(Model.objects.all().values())

            file_path = os.path.join(output_folder, model_info['file_name'])
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)

            self.stdout.write(self.style.SUCCESS(f'Data exported for {model_info["model_name"]}.'))

        self.stdout.write(self.style.SUCCESS('All data exported successfully.'))
