from django import forms
from .models import ReadingGroup

class ReadingGroupForm(forms.ModelForm):
    book_isbn = forms.CharField(widget=forms.HiddenInput())  # JS에서 선택한 책 isbn 넣어줌

    class Meta:
        model = ReadingGroup
        fields = ['group_name', 'book_isbn',]  # 필요한 필드들 추가