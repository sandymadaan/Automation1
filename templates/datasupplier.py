from Automation.tcc.models import *

query =request.GET.get('material')
test = Test.objects.all().filter(material_id = 5)
print(test)
