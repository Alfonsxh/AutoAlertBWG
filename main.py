#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import pathlib
from datetime import datetime
from enum import Enum
from typing import Optional

from src.monitor import get_used_info, convert_to_size_str
from src.email import send_email, EmailInfoModel
from src.scheduler import scheduler


class TimeTypeEnum(int, Enum):
    hour = 1
    day = 2
    week = 3


data_max_bytes = {
    TimeTypeEnum.hour: 1 << 30,
    TimeTypeEnum.day: 10 << 30,
    TimeTypeEnum.week: 80 << 30
}

current_dir = pathlib.Path(__file__).parent


def get_last_used_size_by_time_type(time_type: TimeTypeEnum) -> Optional[int]:
    size_file = current_dir / time_type.name
    if size_file.exists():
        return int(size_file.read_text().strip())
    else:
        return None


def set_last_used_size_by_time_type(time_type: TimeTypeEnum, last_used_size_byte: int) -> None:
    (current_dir / time_type.name).write_text(data=str(last_used_size_byte))


def monitor():
    size_model = get_used_info()

    contents = f"流量已使用: {convert_to_size_str(size_num=size_model.used_size_byte, decimal=3)}"
    send_email(email_obj=EmailInfoModel(subject=f"流量使用情况",
                                        contents=contents))
    print(contents)


def alert_once(time_type: TimeTypeEnum):
    size_model = get_used_info()
    print(f"{time_type.name} 获取到 {size_model=}")

    last_used_size_byte: Optional[int] = get_last_used_size_by_time_type(time_type=time_type)
    if last_used_size_byte is not None and size_model.used_size_byte - last_used_size_byte > data_max_bytes[time_type]:
        try:
            contents = f"过去 1{time_type.name} 使用了 {convert_to_size_str(size_num=size_model.used_size_byte - last_used_size_byte, decimal=3)}!"
            send_email(email_obj=EmailInfoModel(subject=f"流量使用({time_type.name})超标，警告！",
                                                contents=contents))

            print(f"发送流量告警邮件 {contents=}")
        except Exception as e:
            print(f"发送流量告警邮件出现异常{e}")

    set_last_used_size_by_time_type(time_type=time_type, last_used_size_byte=size_model.used_size_byte)


if __name__ == '__main__':
    scheduler.add_job(func=alert_once, args=(TimeTypeEnum.hour,), next_run_time=datetime.now(), trigger="interval", hours=1)
    scheduler.add_job(func=alert_once, args=(TimeTypeEnum.day,), next_run_time=datetime.now(), trigger="interval", days=1, seconds=30)
    scheduler.add_job(func=alert_once, args=(TimeTypeEnum.week,), next_run_time=datetime.now(), trigger="interval", weeks=1, seconds=20)

    scheduler.add_job(func=monitor, next_run_time=datetime.now(), trigger="interval", weeks=1, seconds=50)

    while True:
        time.sleep(10)
