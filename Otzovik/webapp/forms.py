from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import Product, Review


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Найти')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "description", "image"]
        widgets = {
            "category": widgets.CheckboxSelectMultiple,
            "description": widgets.Textarea(attrs={"placeholder": "Введите описание"})
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["otziv", "mark", "bool", "image"]
        widgets = {
            "otziv": widgets.Textarea(attrs={"placeholder": "Введите отзыв"})
        }

    def clean_mark(self):
        mark = self.cleaned_data.get("mark")
        if mark > 5:
            raise ValidationError("Оценка не должна быть больше 5")
        if mark < 1:
            raise ValidationError("Оценка не должна быть меньше 1")
        return mark

