import requests
from django.http import JsonResponse
from django.conf import settings
from functools import wraps


def auth_required(view_func):
    """
    Decorador para rotas protegidas que valida o token de autenticação
    com um microservice externo.
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # 1. Tenta obter o token do cabeçalho Authorization
        auth_header = request.headers.get('Authorization', None)

        if not auth_header:
            return JsonResponse(
                {"detail": "Token de autenticação não fornecido."},
                status=401
            )

        token = auth_header.replace('Bearer ', '')

        try:
            # 2. Faz uma requisição POST para o microservice de autenticação
            #    para validar o token.
            auth_service_url = f"{settings.AUTH_SERVICE_URL}/api/v1/authenticate"

            # Conforme a sua API, o token é enviado no corpo da requisição
            response = requests.post(auth_service_url, json={"token": token})

            if response.status_code == 200:
                # 3. Se o token for válido, executa a view original
                return view_func(request, *args, **kwargs)
            else:
                # 4. Se o token for inválido, retorna a resposta de erro
                return JsonResponse(response.json(), status=response.status_code)

        except requests.exceptions.RequestException:
            # Em caso de erro de conexão com o microservice
            return JsonResponse(
                {"detail": "Não foi possível conectar ao serviço de autenticação."},
                status=503
            )

    return wrapper
