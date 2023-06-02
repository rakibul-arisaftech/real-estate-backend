from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    handlers = {
        # 'ValidationError': _handle_validation_error,
        'Http404': _handle_generic_error,
        'PermissionDenied': _handle_permission_error,
        'NotAuthenticated': _handle_authentication_error
    }

    response = exception_handler(exc, context)

    if response is not None:

        # if 'UserAPIView' in str(context['view']) and exc.status_code == 401:
        #     response.status_code = 200
        #     response.data = {
        #         'status_code': response.status_code,
        #         'is_logged_in': False
        #         }
        #     # return response
        response.data['status_code'] = response.status_code

    exception_class=exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response


def _handle_authentication_error(exc, context, response):

    response.data = {
        'status_code': response.status_code,
        'message': 'Please login to proceed'
    }

    return response


def _handle_generic_error(exc, context, response):
    
    return response

def _handle_permission_error(exc, context, response):
    message = [field_errors for field_name, field_errors in response.data.items()]
    response.data = {
        'status_code': response.status_code,
        'message': message[0]
    }
    return response

# def _handle_validation_error(exc, context, response):

#     return response