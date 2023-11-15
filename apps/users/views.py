from django.shortcuts import render
from django.contrib.auth import get_user_model

# Create your views here.
def register(request):
    print('func')
    create_user()
    return render(request, 'users/register.html')

def create_user():
    User = get_user_model()
    user = User.objects.create_user(
        username='ulan', 
        password='ulan', 
        first_name='fn',
        last_name='ln')
    user.save()