import os

from django.core.asgi import get_asgi_application

from livevil_blog.websocket import websocket_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'livevil_blog.settings.production')

http_application = get_asgi_application()


async def https_application():
    pass


async def application(scope, receive, send):
    if scope['type'] == 'http':
        await http_application(scope, receive, send)
    elif scope['type'] == 'websocket':
        await websocket_application(scope, receive, send)
    elif scope['type'] == 'https':
        await https_application(scope, receive, send)
    else:
        raise Exception('unknown scope type' + scope['type'])
