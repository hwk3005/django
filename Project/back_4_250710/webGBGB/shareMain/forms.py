# forms.py
from django import forms
from .models import ReadingGroup

class ReadingGroupForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput())  # ✅ 중요!

    book_title = forms.CharField(widget=forms.HiddenInput())
    book_author = forms.CharField(widget=forms.HiddenInput())
    book_cover = forms.CharField(widget=forms.HiddenInput())
    book_isbn = forms.CharField(widget=forms.HiddenInput())
    tag = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = ReadingGroup
        fields = ['group_name', 'description', 'is_public', 'password',
                  'book_title', 'book_author', 'book_cover', 'book_isbn', 'tag']

    def clean(self):
        cleaned_data = super().clean()
        is_public = cleaned_data.get('is_public')
        password = cleaned_data.get('password')

        if str(is_public) == "1" or is_public in [1, True, "True"]:
            if not password:
                self.add_error('password', '비밀번호를 입력해주세요.')

        if not cleaned_data.get('book_title') or not cleaned_data.get('book_isbn'):
            raise forms.ValidationError("책을 선택해주세요.")


