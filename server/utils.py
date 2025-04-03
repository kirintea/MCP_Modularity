import json

def rounding_dumps(obj, *args, precision=2, **kwargs):
    """
    备注: 将对象序列化为JSON字符串, 并将浮点数四舍五入到指定精度
    :param obj: 要序列化的对象
    :param args: 其他参数
    :param precision: 浮点数精度, 默认2位小数
    :param kwargs: 其他参数
    :return: 序列化后的JSON字符串
    """
    # 先将对象序列化为JSON字符串, 然后再将字符串反序列化为对象, 最后再将对象序列化为JSON字符串
    # 这样可以避免浮点数精度丢失的问题
    # 但是会导致字符串中的浮点数精度丢失, 所以需要将字符串中的浮点数四舍五入到指定精度

    d1 = json.dumps(obj, *args, **kwargs)
    l1 = json.loads(d1, parse_float=lambda x: round(float(x), precision))
    return json.dumps(l1, *args, **kwargs)