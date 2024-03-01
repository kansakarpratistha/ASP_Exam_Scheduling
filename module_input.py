from main import Module
import csv

class ModuleInput:
    def addModule(self, modules_data):
        modules_data = modules_data.to_dict(orient="records")
        modules = []
        for item in modules_data:
            modules.append(Module(mod_code = item['Module_code'], exam_len = int(item['Duration']), course_id = item['Course_ID']))
        return modules
    
