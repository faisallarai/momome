from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exec, context):
  response = exception_handler(exec, context)
  
  if response is not None:
    return response
  
  exec_list = str(exec).split('DETAIL ')
  return Response({'error': exec_list[-1]}, status=403)