from accounts.forms import RegistrationForm, LoginForm
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView
import boto3



class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm


class RegistrationView(CreateView):
    template_name = 'accounts/registration.html'
    form_class = RegistrationForm
    
    success_url = '/accounts/login'
    def form_valid(self, form):
        response = super().form_valid(form)
        self.send_sns_subsription(form.instance)
        return response

    def send_sns_subsription(self, user):
        sns_client = boto3.client('sns')
        response = sns_client.subscribe(
                TopicArn='arn:aws:sns:us-east-1:564782978045:account-topic',
                Protocol='email', 
                Endpoint=user.email 
            )
        

def logout_view(request):
    logout(request)
    return redirect(reverse('login'))
