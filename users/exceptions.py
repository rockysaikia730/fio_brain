from rest_framework.exceptions import APIException
from rest_framework import status


class GeneralException(APIException):
    default_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        'error': 'Something went wrong. Please try again'
    }

    def __init__(self, detail=None, status_code=None):

        if detail:
            self.detail = {
                'error': detail
            }

        if status_code:
            self.default_code = status_code
