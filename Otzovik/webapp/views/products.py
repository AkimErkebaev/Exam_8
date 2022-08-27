from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy

# Create your views here.
from django.utils.http import urlencode

from webapp.forms import ProductForm, SearchForm, ProductDeleteForm
from webapp.models import Product
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class IndexViewProducts(ListView):
    model = Product
    template_name = "products/index.html"
    context_object_name = "products"
    ordering = "-updated_at"
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Product.objects.filter(
                Q(name__icontains=self.search_value) | Q(description__icontains=self.search_value))
        return Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})  # search=dcsdvsdvsd
            context['query'] = query
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class ProductView(DetailView):
    template_name = "products/product_view.html"
    model = Product
    context_object_name = "products"
    ordering = "-updated_at"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.order_by("-created_at")
        return context

    # def has_permission(self):
    #     return super().has_permission() and self.request.user in self.get_object().users.all() or \
    #            super().has_permission() and self.request.user.groups.filter(name__in=("Moderator",)).exists()


class CreateProduct(PermissionRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = "products/create.html"
    permission_required = "webapp.add_project"

    def has_permission(self):
        return self.request.user.has_perm("webapp.change_product")

    # def form_valid(self, form):
    #     project = form.save(commit=False)
    #     project.save()
    #     form.save_m2m()
    #     return redirect("webapp:project_view", pk=project.pk)


class UpdateProduct(PermissionRequiredMixin, UpdateView):
    form_class = ProductForm
    template_name = "products/update.html"
    model = Product
    permission_required = "webapp.change_product"


class DeleteProduct(PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = "products/delete.html"
    success_url = reverse_lazy('webapp:index_product')
    form_class = ProductDeleteForm
    permission_required = "webapp.delete_product"
