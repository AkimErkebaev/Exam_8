from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
# Create your views here.
from django.utils.http import urlencode
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, UpdateView, DeleteView, CreateView

from webapp.views.base_view import FormView as CustomFormView
from webapp.forms import ReviewForm, SearchForm, ReviewDeleteForm
from webapp.models import Review, Product


class IndexView(ListView):
    model = Review
    template_name = "reviews/index.html"
    context_object_name = "reviews"
    ordering = "-updated_at"
    paginate_by = 5
    permission_required = "webapp.view_review"

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Review.objects.filter(
                Q(name__icontains=self.search_value))
        return Review.objects.all()

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


class CreateReview(LoginRequiredMixin, CreateView):
    form_class = ReviewForm
    template_name = "reviews/create.html"

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("webapp:product_view", kwargs={"pk": self.object.product.pk})

    # def form_valid(self, form):
    #     self.review = form.save()
    #     return super().form_valid(form)
    #
    # def get_redirect_url(self):
    #     return redirect("webapp:product_view", pk=self.review.pk)


class UpdateReview(PermissionRequiredMixin, UpdateView):
    form_class = ReviewForm
    template_name = "reviews/update.html"
    model = Review
    permission_required = "webapp.change_review"

    def has_permission(self):
        return super().has_permission() or self.request.user in self.get_object().project.users.all()


class DeleteReview(PermissionRequiredMixin, DeleteView):
    model = Review
    template_name = "reviews/delete.html"
    success_url = reverse_lazy('webapp:index')
    form_class = ReviewDeleteForm
    permission_required = "webapp.delete_review"

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().project.users.all()

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=self.get_object())
        if form.is_valid():
            return self.delete(request, *args, **kwargs)
        else:
            return self.get(request, *args, **kwargs)
