from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms


class MemberListView(ListView):
    model = models.Member
    template_name = 'member_list.html'
    context_object_name = 'members'

    def get_queryset(self):
        queryset = super().get_queryset()
        person_name = self.request.GET.get('person_name')

        if person_name:
            queryset = queryset.filter(person__full_name__icontains=person_name)
        
        return queryset


class MemberCreateView(CreateView):
    model = models.Member
    template_name = 'member_create.html'
    form_class = forms.MemberForm
    success_url = reverse_lazy('member_list')


class MemberDetailView(DetailView):
    model = models.Member
    template_name = 'member_detail.html'
    context_object_name = 'member'


class MemberUpdateView(UpdateView):
    model = models.Member
    template_name = 'member_update.html'
    form_class = forms.MemberForm
    context_object_name = 'member'
    success_url = reverse_lazy('member_list')


class MemberDeleteView(DeleteView):
    model = models.Member
    template_name = 'member_delete.html'
    success_url = reverse_lazy('member_list')
