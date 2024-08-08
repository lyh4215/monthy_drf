from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTXAuthentication(JWTAuthentication):
    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        header = request.META.get('HTTP_X_AUTHORIZATION')

        if isinstance(header, str):
            header = header.encode('utf-8')

        return header