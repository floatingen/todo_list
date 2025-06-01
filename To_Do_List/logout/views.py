from django.shortcuts import redirect
from django.contrib.auth import logout
from rest_framework.views import APIView


class LogoutView(APIView):

    def get(self, request, *args, **kwargs):
        print('Logout get')
        pass

    def post(self, request, *args, **kwargs):
        logout(request)
        print('Logout post')
        # return redirect('/login/', )
        # return render(request, 'login/login.html', {})
        return redirect('/login/')
