from modeltranslation.translator import translator, TranslationOptions
from .models import FlatPage

class FlatPageTranslationOptions(TranslationOptions):
    fields = ('slug', 'title', 'content')

translator.register(FlatPage, FlatPageTranslationOptions)