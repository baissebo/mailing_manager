import secrets

from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'mailings.can_disable_mailing'

    def get_queryset(self):
        return User.objects.filter(is_staff=False).order_by('-id')


class UserBlockView(PermissionRequiredMixin, UpdateView):
    model = User
    permission_required = 'mailings.can_disable_mailing'

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return redirect('users:user_list')


class UserUnblockView(PermissionRequiredMixin, UpdateView):
    model = User
    permission_required = 'mailings.can_disable_mailing'

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = True
        user.save()
        return redirect('users:user_list')


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject="Подтверждение почты",
            message=f"Здравствуйте! Ваш email был указан для регистрации в приложении 'Mailing manager'."
                    f" Если это не вы, то проигнорируйте это письмо. "
                    f"Иначе нужно перейти по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_profile.html'

    def get_object(self):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users:logout')
    slug_field = 'email'
    slug_url_kwarg = 'email'


class NewPasswordView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = "users/new_password.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            password = secrets.token_urlsafe(10)
            send_mail(
                subject="Новый пароль",
                message=f"Здравствуйте! Новый пароль для входа в ваш аккаунт: {password}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
            user.set_password(password)
            user.save()
            messages.success(self.request, "Новый пароль отправлен на электронную почту")
            return redirect(self.success_url)

        except User.DoesNotExist:
            messages.error(self.request, "Пользователь с таким email не найден")
            return super().form_invalid(form)
