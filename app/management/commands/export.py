import os
import json
from django.apps import apps
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Export data from specified models to JSON files'

    def handle(self, *args, **options):
        models = [
            {'model_name': 'CompanyPlan', 'app_name': 'app', 'file_name': 'CompanyPlan.json'},
            {'model_name': 'CompanyPlanLimits', 'app_name': 'app', 'file_name': 'CompanyPlanLimits.json'},
            {'model_name': 'AssetType', 'app_name': 'app', 'file_name': 'AssetType.json'},
          
            #  add units also

             {'model_name': 'WorkStatus', 'app_name': 'app', 'file_name': 'WorkStatus.json'},
            {'model_name': 'PaymentStatus', 'app_name': 'app', 'file_name': 'PaymentStatus.json'},
            {'model_name': 'PaymentMethod', 'app_name': 'app', 'file_name': 'PaymentMethod.json'},
          
           {'model_name': 'ContractType', 'app_name': 'app', 'file_name': 'ContractType.json'},
            {'model_name': 'Duration', 'app_name': 'app', 'file_name': 'Duration.json'},
            {'model_name': 'Priority', 'app_name': 'app', 'file_name': 'Priority.json'},

            {'model_name': 'PaymentSchedule', 'app_name': 'app', 'file_name': 'PaymentSchedule.json'},
            {'model_name': 'ProcessStatus', 'app_name': 'app', 'file_name': 'ProcessStatus.json'},

            # Plot Sale
            
            {'model_name': 'Area', 'app_name': 'plotsale', 'file_name': 'Area.json'},
            {'model_name': 'PropertyType', 'app_name': 'plotsale', 'file_name': 'PropertyType.json'},
            {'model_name': 'PlotType', 'app_name': 'plotsale', 'file_name': 'PlotType.json'},
            {'model_name': 'SoilType', 'app_name': 'plotsale', 'file_name': 'SoilType.json'},
            {'model_name': 'Status', 'app_name': 'plotsale', 'file_name': 'Status.json'},


             
          
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





