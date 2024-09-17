# Script to create modules and tasks automatically
from django.db import models

class Module(models.Model):
    module_name = models.CharField(max_length=50)
    total_hours = models.PositiveIntegerField()

    def __str__(self):
        return self.module_name

class Task(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='tasks')
    task_name = models.CharField(max_length=50)
    hours = models.PositiveIntegerField()

    def __str__(self):
        return self.task_name



# Creating modules
module_a = Module.objects.create(module_name='Module A', total_hours=24)
module_b = Module.objects.create(module_name='Module B', total_hours=60)
module_c = Module.objects.create(module_name='Module C', total_hours=60)
module_d = Module.objects.create(module_name='Module D', total_hours=30)
module_e = Module.objects.create(module_name='Module E', total_hours=48)
module_f = Module.objects.create(module_name='Module F', total_hours=60)
module_g = Module.objects.create(module_name='Module G', total_hours=60)
module_h = Module.objects.create(module_name='Module H', total_hours=78)
module_i = Module.objects.create(module_name='Module I', total_hours=60)
module_j = Module.objects.create(module_name='Module J', total_hours=72)
module_k = Module.objects.create(module_name='Module K', total_hours=60)

# Creating tasks for Module A (Example)
Task.objects.create(module=module_a, task_name='A1', hours=24)

# Similarly, for Module B
Task.objects.create(module=module_b, task_name='B1', hours=60)
# Repeat for B2, B3, ..., B14



modules_data = {
    'A': {'total_hours': 24, 'tasks': [('A1', 24)]},
    'B': {'total_hours': 60, 'tasks': [('B1', 60)]},
    'C': {'total_hours': 60, 'tasks': [('C1', 60)]},
    'D': {'total_hours': 30, 'tasks': [('D1', 30)]},
    'E': {'total_hours': 48, 'tasks': [('E1', 48)]},
    'F': {'total_hours': 60, 'tasks': [('F1', 60)]},
    'G': {'total_hours': 60, 'tasks': [('G1', 60)]},
    'H': {'total_hours': 78, 'tasks': [('H1', 78)]},
    'I': {'total_hours': 60, 'tasks': [('I1', 60)]},
    'J': {'total_hours': 72, 'tasks': [('J1', 72)]},
    'K': {'total_hours': 60, 'tasks': [('K1', 60)]},
}

for module_name, data in modules_data.items():
    module = Module.objects.create(module_name=f"Module {module_name}", total_hours=data['total_hours'])
    for task_name, hours in data['tasks']:
        Task.objects.create(module=module, task_name=task_name, hours=hours)

