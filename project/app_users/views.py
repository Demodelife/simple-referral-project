from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from app_users.common import generate_invite_code
from app_users.forms import CodeConfirmForm
from app_users.models import CustomUser
from app_users.serializers import CustomUserSerializer, FindCustomUserSerializer


class CustomLoginListCreateAPIView(ListCreateAPIView):
    """
    API view for getting list of users(so convenient to test login) and login.
    """

    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.order_by('pk').prefetch_related('guests')

    def create(self, request, *args, **kwargs):
        """
        Method for creating a new user of system
        or logging in with an existing one.
        """

        phone = request.data['phone']
        user, created = CustomUser.objects.get_or_create(phone=phone, username=phone)
        if created:
            invite_code = generate_invite_code()
            user.invite_code = invite_code
            user.save()

        user_auth = authenticate(self.request, username=user.username)
        login(self.request, user=user_auth)

        return redirect(reverse('app_users:confirm', kwargs={'pk': user.pk}))


class CustomLogoutRetrieveAPIView(RetrieveAPIView):
    """
    API view to log out.
    """

    def retrieve(self, request, *args, **kwargs):
        """
        Method to log out with login link.
        """

        logout(self.request)

        return Response(
            {
                'message': 'You are logged out.',
                'login': self.request.build_absolute_uri(settings.LOGIN_URL),
            }
        )


class CustomUserCodeConfirmFormView(FormView):
    """
    View for confirm code.
    """

    form_class = CodeConfirmForm
    template_name = 'app_users/code_confirm.html'

    def get_success_url(self, **kwargs):
        """
        Return the URL to redirect to after processing a valid form.
        """

        return reverse(
            'app_users:sending-code',
            kwargs={'pk': self.kwargs['pk']}
        )


class SimulateSendingCodeTemplateView(TemplateView):
    """
    Simulate Sending View.
    """

    template_name = 'app_users/simulate_sending_code.html'


class CustomUserRetrieveAPIView(LoginRequiredMixin, RetrieveAPIView):
    """
    API view for getting user details and searching for other users by invite code.
    """

    serializer_class = FindCustomUserSerializer
    queryset = CustomUser.objects.order_by('pk').prefetch_related('guests')

    def retrieve(self, request, *args, **kwargs):
        """
        Method for getting user details and found user details.
        """

        response = super().retrieve(request, *args, **kwargs)

        curr_user = self.request.user
        curr_user_profile = {
            'phone': curr_user.phone,
            'invite_code': curr_user.invite_code,
            'guests': [guest.phone for guest in curr_user.guests.all()],
        }

        response.data.setdefault('my_profile', curr_user_profile)
        response.data = dict(sorted(response.data.items(), reverse=True))

        # to avoid duplication
        if response.data['found_profile'] == response.data['my_profile']:
            response.data.pop('found_profile')

        response.data['logout'] = self.request.build_absolute_uri(settings.LOGOUT_URL)

        return response

    def post(self, request, *args, **kwargs):
        """
        Method to send post request with invite code.
        """

        invite_code = self.request.data['invite_code']
        curr_user = self.request.user
        found_user = get_object_or_404(CustomUser, invite_code=invite_code)

        if found_user == curr_user:
            return Response({'message': 'This is your invite code.'})

        if curr_user in found_user.guests.all():
            return redirect(reverse('app_users:user-info', kwargs={'pk': found_user.pk}))

        found_user.guests.add(curr_user)
        found_user.save()

        return redirect(reverse('app_users:user-info', kwargs={'pk': found_user.pk}))
