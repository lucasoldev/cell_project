from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from . import models, forms


class MemberMinistryListView(ListView):
    model = models.MemberMinistry
    template_name = 'member_ministry_list.html'
    context_object_name = 'member_ministries'

    def get_queryset(self):
        queryset = super().get_queryset()
        member_name = self.request.GET.get('member_name')

        if member_name:
            queryset = queryset.filter(
                member__person__full_name__icontains=member_name
            )

        return queryset.select_related('member__person', 'ministry')


class MemberMinistryCreateView(CreateView):
    model = models.MemberMinistry
    template_name = 'member_ministry_create.html'
    form_class = forms.MemberMinistryForm
    success_url = reverse_lazy('member_ministry_list')


class MemberMinistryDetailView(DetailView):
    model = models.MemberMinistry
    template_name = 'member_ministry_detail.html'
    context_object_name = 'member_ministry'
    success_url = reverse_lazy('member_ministry_list')


class MemberMinistryUpdateView(UpdateView):
    model = models.MemberMinistry
    template_name = 'member_ministry_update.html'
    form_class = forms.MemberMinistryForm
    context_object_name = 'member_ministry'
    success_url = reverse_lazy('member_ministry_list')


class MemberMinistryDeleteView(DeleteView):
    model = models.MemberMinistry
    template_name = 'member_ministry_delete.html'
    success_url = reverse_lazy('member_ministry_list')
