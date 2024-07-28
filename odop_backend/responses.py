from rest_framework.response import Response
from rest_framework import status

def ModelDoesNotExists(model, param="required"):
    return Response(data=dict(
        success=False,
        message="{} does not exists. Please make sure your provide '{}' in request body.".format(model, param)
    ), status=status.HTTP_200_OK)
    
def ResponseSuccess(response={}, message="success"):
    data = dict(
        success=True,
        message=message,
    )
    data.update(response)
    
    return Response(data=data, status=status.HTTP_200_OK)

def ResponseError(message="success"):
    data = dict(
        success=False,
        message=message,
    )
    
    return Response(data=data, status=status.HTTP_200_OK)

def NotAuthorized():
    return Response(data=dict(
        success=False,
        message="You are not authorized to make this request."
    ), status=status.HTTP_403_FORBIDDEN)
