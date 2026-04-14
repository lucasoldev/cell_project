from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms


class LeadershipRoleListView(ListView):
    model = models.LeadershipRole
    template_name = 'leadership_role_list.html'
    context_object_name = 'leadership_roles'

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get('title')

        if title:
            queryset = queryset.filter(title__icontains=title)
        
        return queryset


class LeadershipRoleCreateView(CreateView):
    model = models.LeadershipRole
    template_name = 'leadership_role_create.html'
    form_class = forms.LeadershipRoleForm
    success_url = reverse_lazy('leadership_role_list')


class LeadershipRoleDetailView(DetailView):
    model = models.LeadershipRole
    template_name = 'leadership_role_detail.html'
    context_object_name = 'leadership_role'


class LeadershipRoleUpdateView(UpdateView):
    model = models.LeadershipRole
    template_name = 'leadership_role_update.html'
    form_class = forms.LeadershipRoleForm
    success_url = reverse_lazy('leadership_role_list')
    context_object_name = 'leadership_role'


class LeadershipRoleDeleteView(DeleteView):
    model = models.LeadershipRole
    template_name = 'leadership_role_delete.html'
    success_url = reverse_lazy('leadership_role_list')
