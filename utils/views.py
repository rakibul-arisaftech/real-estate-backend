from django.http import JsonResponse

def error_404(request, exception):
    message = 'This is not a valid endpoint'

    response = JsonResponse(data={
        'status_code': 404,
        'message': message
        })
    response.status_code = 404
    return response

def error_500(request):
    message = 'An error has occurred'
    response = JsonResponse(data={
        'status_code': 500,
        'message': message
        })
    response.status_code = 500
    return response