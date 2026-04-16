from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms


class CellMemberListView(ListView):
    model = models.CellMember
    template_name = 'cell_member_list.html'
    context_object_name = 'cell_members'

    def get_queryset(self):
        queryset = super().get_queryset()
        member_name = self.request.GET.get('member_name')

        if member_name:
            queryset = queryset.filter(
                member__person__full_name__icontains=member_name
            )

        return queryset.select_related('member__person', 'cell', 'role')


class CellMemberCreateView(CreateView):
    model = models.CellMember
    template_name = 'cell_member_create.html'
    form_class = forms.CellMemberForm
    success_url = reverse_lazy('cell_member_list')


class CellMemberDetailView(DetailView):
    model = models.CellMember
    template_name = 'cell_member_detail.html'
    context_object_name = 'cell_member'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'member__person', 'cell__area', 'role'
        )


class CellMemberUpdateView(UpdateView):
    model = models.CellMember
    template_name = 'cell_member_update.html'
    form_class = forms.CellMemberForm
    context_object_name = 'cell_member'
    success_url = reverse_lazy('cell_member_list')


class CellMemberDeleteView(DeleteView):
    model = models.CellMember
    template_name = 'cell_member_delete.html'
    success_url = reverse_lazy('cell_member_list')
