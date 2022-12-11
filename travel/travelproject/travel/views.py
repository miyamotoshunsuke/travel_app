from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from .consts import ITEM_PER_PAGE
from django.db.models import Avg
from django.views.generic import (
    ListView,
    DetailView, 
    CreateView, 
    DeleteView, 
    UpdateView,
    )
from .models import Travel, Review

class ListTravelView(LoginRequiredMixin, ListView):
    template_name = 'travel/travel_list.html'
    model = Travel
    paginate_by = ITEM_PER_PAGE

class DetailTravelView(LoginRequiredMixin, DetailView):
    template_name = 'travel/travel_detail.html'
    model = Travel

class CreateTravelView(LoginRequiredMixin, CreateView):
    template_name = 'travel/travel_create.html'
    model = Travel
    fields = ('title', 'text', 'category', 'thumnail')
    success_url = reverse_lazy('list-travel')

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)

class DeleteTravelView(LoginRequiredMixin, DeleteView):
    template_name = 'travel/travel_confirm_delete.html'
    model = Travel
    success_url = reverse_lazy('list-travel')

class UpdateTravelView(LoginRequiredMixin, UpdateView):
    template_name = 'travel/travel_update.html'
    fields = (['title', 'text', 'category', 'thumnail'])
    model = Travel

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user:
            raise PermissionDenied

        return obj

    def get_success_url(self):
        return reverse('detail-travel', kwargs={'pk':self.object.id})

def index_view(request):
    object_list = Travel.objects.order_by('-id')
    
    ranking_list = Travel.objects.annotate(avg_rating=Avg('review__rate')).order_by('-avg_rating')
    
    paginator = Paginator(ranking_list, ITEM_PER_PAGE)
    page_number = request.GET.get('page',1)
    page_obj = paginator.page(page_number)

    return render(
        request,
        'travel/index.html',
        {'object_list':object_list, 'ranking_list':ranking_list, 'page_obj':page_obj },
        )

class CreateReviewView(CreateView):
    model = Review
    fields = ('travel', 'title', 'text', 'rate')
    template_name = 'travel/review_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['travel'] = Travel.objects.get(pk=self.kwargs['travel_id'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail-travel', kwargs={'pk':self.object.travel_id})