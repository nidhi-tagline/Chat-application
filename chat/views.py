from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from .models import Room 


# signup view for new user creation
class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    
# index view for all rooms and enter a room
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    context_object_name = 'rooms'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rooms"] = Room.objects.all()
        return context

# room view of a specific room for chat
class RoomView(LoginRequiredMixin, TemplateView):
    template_name = 'room.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat_room, created = Room.objects.get_or_create(name=self.kwargs['room_name'])
        context['room'] = chat_room
        return context
