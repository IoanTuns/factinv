from django.db import models

def get_ContentTypes():
    appQ = models.Q(app_label='customers') #change value of app_label to match your app's name
    modelIsCatQ = models.Q(model='ContactPerson')
    modelIsChoice = models.Q(model='PeroanaJuridca')
    return appQ & ~modelIsCatQ & ~modelIsChoice