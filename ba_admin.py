# Admin Views
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from flask_admin.contrib.peewee import ModelView

class SummernoteTextArea(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' summernote'
        else:
            kwargs.setdefault('class', 'summernote')
        return super(SummernoteTextArea, self).__call__(field, **kwargs)

class SummernoteTextAreaField(TextAreaField):
    widget = SummernoteTextArea()

class BadAzureLevelAdminView(ModelView):
    page_size = 50
    extra_js = ['//cdnjs.cloudflare.com/ajax/libs/summernote/0.8.12/summernote.js']
    extra_css = ['//cdnjs.cloudflare.com/ajax/libs/summernote/0.8.12/summernote.css']

    column_list = ['level_no', 'level_instructions', 'intro_text', 'hint_1_text', 'hint_2_text']

    form_overrides = {
        'level_instructions': SummernoteTextAreaField,
        'intro_text': SummernoteTextAreaField,
        'hint_1_text': SummernoteTextAreaField,
        'hint_2_text': SummernoteTextAreaField
    }