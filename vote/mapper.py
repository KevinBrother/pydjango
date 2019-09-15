from bpmappers.djangomodel import ModelMapper
from vote.models import Subject

class SubjectMapper(ModelMapper):
    class Meta:
        model = Subject