from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from . import forms, models


class LeadershipListView(ListView):
    model = models.Leadership
    template_name = 'leadership_list.html'
    context_object_name = 'leaderships'

    def get_queryset(self):
        queryset = super().get_queryset()
        person_name = self.request.GET.get('person_name')

        if person_name:
            queryset = queryset.filter(
                person__full_name__icontains=person_name
            )

        return queryset.select_related('person', 'role', 'area', 'cell')


class LeadershipCreateView(CreateView):
    model = models.Leadership
    template_name = 'leadership_create.html'
    form_class = forms.LeadershipForm
    success_url = reverse_lazy('leadership_list')


class LeadershipDetailView(DetailView):
    model = models.Leadership
    template_name = 'leadership_detail.html'
    context_object_name = 'leadership'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'person', 'role', 'area', 'cell'
        )


class LeadershipUpdateView(UpdateView):
    model = models.Leadership
    template_name = 'leadership_update.html'
    form_class = forms.LeadershipForm
    context_object_name = 'leadership'
    success_url = reverse_lazy('leadership_list')


class LeadershipDeleteView(DeleteView):
    model = models.Leadership
    template_name = 'leadership_delete.html'
    success_url = reverse_lazy('leadership_list')
