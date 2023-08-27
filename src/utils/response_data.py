from enum import Enum
from flask_sqlalchemy.model import Model
from utils import model_to_dict, clear_none_data

ErrorCode = Enum("ErrorCode", {
    "SUCCESS": 0, 
    "ParameterLoss": 1,
    "ParameterError": 2,
    "CommmonError": 3,
    "DataNotExists": 3,
    "NotLogin": 4,
    })


def parameter_loss(parameter_name: str):
    return {"code": ErrorCode.ParameterLoss.value, "msg": f"{parameter_name}参数缺失"}

def parameter_error(parameter_name: str):
    return {"code": ErrorCode.ParameterLoss.value, "msg": f"{parameter_name}参数错误"}

def dataNotExist(key: str):
    return {"code": ErrorCode.DataNotExists.value, "msg": f"数据{key}不存在"}

def notLogin() -> dict:
    return {"code": ErrorCode.NotLogin.value, "msg": "未登录"}

def common_error(msg: str):
    return {"code": ErrorCode.CommmonError.value, "msg": msg}

def custom_error(code: int, msg: str):
    return {"code": code, "msg": msg}

def response_data(data):
    if data is None:
        return {"code": ErrorCode.SUCCESS.value}
    if not isinstance(data, Model):
        return {"code": ErrorCode.SUCCESS.value, "data": data}
    return {"code": ErrorCode.SUCCESS.value, "data": clear_none_data(model_to_dict(data))}
    
def response_dataList(list):
        return {"code": ErrorCode.SUCCESS.value, "data": list}


__all__ = [
    "parameter_loss",
    "parameter_error",
    "dataNotExist",
    "notLogin",
    "common_error",
    "custom_error",
    "response_data",
    "response_dataList",
]