import requests
from django.conf import settings
from django.http import JsonResponse


def protected_route(view_func):
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return JsonResponse({"detail": "Token de autenticação não fornecido."}, status=401)

        try:
            auth_service_url = f"{settings.AUTH_SERVICE_URL}/validate/"
            headers = {"Authorization": auth_header}
            response = requests.get(auth_service_url, headers=headers)

            if response.status_code != 200:
                return JsonResponse(response.json(), status=response.status_code)

            return view_func(request, *args, **kwargs)
        except requests.exceptions.RequestException:
            return JsonResponse({"detail": "Não foi possível conectar ao serviço de autenticação."}, status=503)

    return wrapper