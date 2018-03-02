from django.contrib.auth.models import User
from oauth2_provider.models import AccessToken, Application
from braces.views import CsrfExemptMixin
from oauth2_provider.views.mixins import OAuthLibMixin
from oauth2_provider.settings import oauth2_settings
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class TokenView(APIView, CsrfExemptMixin, OAuthLibMixin):
    permission_classes = (permissions.AllowAny,)

    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def post(self, request):
        username = request.POST.get('username')
        print request.POST.get('password'),username, request.POST.get('client_secret'), request.POST.get('client_id')
        try:
            if username is None:
                raise User.DoesNotExist
            AccessToken.objects.filter(user=User.objects.get(username=username), application=Application.objects.get(name="Retail")).delete()
        except Exception as e:
            return Response(e.message,status=400)

        url, headers, body, status = self.create_token_response(request)
        return Response(body, status=status, headers=headers)