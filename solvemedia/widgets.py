from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe
from solvemedia import SolveMedia

class SolveMediaCaptcha(forms.widgets.Widget):
	def render(self, name, value, attrs=None):
		sm = SolveMedia(settings.SM_CKEY, settings.SM_VKEY, settings.SM_HKEY)
		return mark_safe(sm.get_html() + "<br>")

	def value_from_datadict(self, data, files, name):
		return {'challenge': data.get('adcopy_challenge', ''), 'response': data.get('adcopy_response', '')}
