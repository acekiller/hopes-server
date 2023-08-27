import datetime
from flask_sqlalchemy.model import Model

def clear_none_data(data):
    if data is None:
        return None
    elif isinstance(data, list):
        return list(filter(lambda x: x is not None, map(clear_none_data, data)))
    elif not isinstance(data, dict):
        return data
    else:
        r = dict(
                filter(lambda x: x[1] is not None,
                    map(lambda x: (x[0], clear_none_data(x[1])),
                        data.items())))
        return r if bool(r) else None
    

def model_to_dict(model: Model, fields = None, exchange_fields = None, exclude_fields: list = None) -> dict:
    """
    将Flask SQLAlchemy的模型对象转换为字典类型
    :param: model : 模型对象
    :param: fields : 需要获取的字段列表，默认为 None，获取全部字段
    :param: exchange_fields : 需要替换名字的字段，{'数据库字段':'前端展示字段'}，有些数据库字段名在展示时需要修改成前端需要的名字
    :return: 返回字典类型
    """
    #传递空值时
    if not model:
        return {}
    
    if fields is None:
        # 获取所有列名
        columns = [column.name for column in model.__table__.columns]
        # 排除掉relationships 设置的反向查询字段
        relations = getattr(model.__class__, '__mapper__').relationships
        exclude_cols = [rel.key for rel in relations]
        # print(exclude_cols,'要剔除的反向查询字段')
        #拿到所有列名-排除的列名
        cols = set(columns) - set(exclude_cols)
        fields = list(cols)
 
    obj_dict = {}
    
    for field in fields:
        if exclude_fields is not None and field in exclude_fields:
            continue
        if field not in model.__dict__:
            continue
 
        value = model.__dict__[field]

        #1、对时间字段进行操作
        if isinstance(value, datetime.datetime):
            #字段类型是datetime的，格式化
            value = value.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(value,datetime.date):
            #字段类型是date的，格式化
            value = value.strftime('%Y-%m-%d')
        #2、将所有可以进行反序列化的进行反序列化(将json字符串转成python结构数据类型)
        if isinstance(value,str):
            try:
                value = json.loads(value)
            except Exception as _:
                pass
        #3、替换展示的字段
        if type(exchange_fields) == dict:
            for db_field,show_field in exchange_fields.items():
                #db_field 是数据库字段，show_field是展示字段名
                if field==db_field:
                    field = show_field
 
        obj_dict[field] = value
 
    return obj_dict


__all__ = [
    "clear_none_data",
    "model_to_dict",
]