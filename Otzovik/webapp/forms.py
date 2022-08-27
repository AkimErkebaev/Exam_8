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
            "description": widgets.Textarea(attrs={"placeholder": "Введите описание"})
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', "review", "mark", "bool"]
        widgets = {
            "review": widgets.Textarea(attrs={"placeholder": "Введите отзыв"})
        }

    def clean_mark(self):
        mark = self.cleaned_data.get("mark")
        if mark > 5:
            raise ValidationError("Оценка не должна быть больше 5")
        if mark < 1:
            raise ValidationError("Оценка не должна быть меньше 1")
        return mark


class ProductDeleteForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name"]

    def clean_title(self):
        name = self.cleaned_data.get("name")
        if self.instance.name != name:
            raise ValidationError("Названия не совпадают")
        return name


class ReviewDeleteForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["review"]

    def clean_title(self):
        review = self.cleaned_data.get("review")
        if self.instance.name != review:
            raise ValidationError("Названия не совпадают")
        return review
