import ipaddress


def get_client_ip(request):
    """
    返回可信的客户端 IP。

    X-Forwarded-For 左侧的值由客户端自行声明、可以伪造，只有最后一项
    是自家反向代理追加的，故只取最后一项；无法解析时返回 None，
    由调用方决定回退值。
    """
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        candidate = forwarded.split(',')[-1].strip()
    else:
        candidate = request.META.get('REMOTE_ADDR', '')
    try:
        return str(ipaddress.ip_address(candidate))
    except ValueError:
        return None
