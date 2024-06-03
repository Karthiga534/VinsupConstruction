# your_app/templatetags/file_filters.py

from django import template
import os
from django.core.files import File
from django.db.models.fields.files import FieldFile
from app.utils import truncate_file_text ,truncate_text

register = template.Library()

@register.filter
def filename(value):
    filename = ""
    if isinstance(value, (File, FieldFile)):
        filename =  os.path.basename(value.name)
    elif isinstance(value, str):
        filename = os.path.basename(value)
    else :
        filename =None

    return truncate_file_text(filename)



@register.filter
def truncate(value,char =15):
    if value:
        return truncate_text(value,char)
    return value



@register.filter
def truncate_description(value,char =100):
    if value:
        return truncate_text(value,char) +"..."
    return value

# @register.filter
# def truncate_work_done(value,char =100):
#     if value:
#         return truncate_text(value,char) +"..."
#     return value



