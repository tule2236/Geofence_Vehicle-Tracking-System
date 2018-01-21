from django import forms
from django.shortcuts import render_to_response

from geofence.models import Driver, Child,Geofence, Vehicle

# class MyModelChoiceField(forms.ModelChoiceField):
#     def label_from_instance(self, obj):
#         return "%s" % obj.geofence

# class PollSelectionForm(forms.Form):
#     polls = MyModelChoiceField( queryset=Poll.objects.all() )

# class ParentResults(forms.Form):
#     def __init__(self, newid, *args, **kwargs):
#         super(ChoiceResults, self).__init__(*args, **kwargs)

#         self.fields['choice'] = forms.TextField( initial="" )

GEOTYPE_CHOICES = (('1', 'Entered'), ('2', 'Exit'))
class DriverForm(forms.Form):
    driver = forms.ModelChoiceField(queryset = Driver.objects.all(), widget=forms.Select())
    # def __init__(self,company, *args, **kwargs):
    # 	company = kwargs.pop('company', None)
    # 	super(DriverForm, self).__init__(company,*args, **kwargs)
    # 	if company:
    # 		self.fields['driver'].queryset = Vehicle.objects.filter(company = company)



# class DriverForm(forms.ModelForm):
# 	def __init__(self, company, *args, **kwargs):
# 		super(DriverForm, self).__init__( company, *args, **kwargs)

# 		self.fields['driver'].queryset = Driver.objects.filter(cpn = company)
# 	class Meta:
# 		model = Vehicle
# 		fields=['driver']

class ChildForm(forms.Form):
    child = forms.ModelChoiceField(queryset = Child.objects.all(), widget=forms.Select())
    child_geotype = forms.CharField(max_length = 100)
class GeofenceForm(forms.Form):
    geofence = forms.ModelChoiceField(queryset = Geofence.objects.all(), widget=forms.Select())
    geotype = forms.CharField(max_length = 100)
    # def clean_driver(self):
    #     data = self.clean_driver['driver']
    #     return data
#     def __init__(self, *args, **kwargs):
#         company_id = kwargs.pop('company', None)
#         super(DriverForm, self).__init__(*args, **kwargs)

#         if company_id:
#             self.fields['company'].queryset = Driver.objects.filter(company = company_id)
# company_id = Vehicle.objects.filter 

# class GeoForm(forms.Form):
#     parent=forms.ModelChoiceField(Geofence.objects.all(), widget=forms.CheckboxSelectMultiple)
#     children=forms.ModelChoiceField(Child.objects.none())

#     def __init__(self, *args, **kwargs):
#         forms.Form.__init__(self, *args, **kwargs)
#         parents= Geofence.objects.all()

#         if len(parents)==1:
#             self.fields['parent'].initial=parents[0].pk

#         parent_id=self.fields['parent'].initial or self.initial.get('parent') \
#                   or self._raw_value('parent')
#         if parent_id:
#             # parent is known. Now I can display the matching children.
#             children = Child.objects.filter(parent__id=parent_id)
#             self.fields['children'].queryset=children
#             if len(children)==1:
#                 self.fields['children'].initial=children[0].pk