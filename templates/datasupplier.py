from Automation.tcc.models import *

fieldID = User.objects.get(fieldID=request.GET['fieldID'])
testID = Test.objects.filter(field_id = fieldID)

