import json
from datetime import datetime
import os

class LocalizationQAReportGenerator:
    def __init__(self, report_dir: str = 'localization_reports'):
        self.report_dir = report_dir
        os.makedirs(report_dir, exist_ok=True)
    
    def generate_report(self, localization_data: dict) -> str:
        report_filename = os.path.join(
            self.report_dir, 
            f'localization_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        
        with open(report_filename, 'w') as report_file:
            json.dump({
                'text_overflows': localization_data.get('textOverflows', {}),
                'rtl_support': localization_data.get('isRTLLayout', False),
                'supported_languages': localization_data.get('supportedLanguages', [])
            }, report_file, indent=4)
        
        return report_filename
