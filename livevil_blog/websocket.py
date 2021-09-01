async def websocket_application(scope, receive, send):
    event = await receive()

    if event['type'] == 'websocket.connect':
        await send({'type': 'websocket.accept', 'text': ''})
