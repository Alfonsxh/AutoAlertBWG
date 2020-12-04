#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import traceback

import yagmail
from pydantic import BaseModel, Field

from src.config import base_config


class EmailInfoModel(BaseModel):
    to_email: str = Field(default=base_config.receive_email, description="接收方email地址")
    from_email: str = Field(default=base_config.email_host, description="发送方email地址")
    subject:str = Field(default="New email from Bangwagon.", description="Email标题")
    contents: str = Field(default="")
    # image: Union[List[str], str] = Field(default=None)


mail_sender = yagmail.SMTP(user=base_config.email_address,
                           password=base_config.email_password,
                           host=base_config.email_host)  # 初始化邮件发送实例


def send_email(email_obj: EmailInfoModel, try_number=3):
    """
    向email发送消息
    :param email_obj: email对象
    :param try_number: 尝试重新发送的次数
    :return:
    """
    for i in range(try_number):
        try:
            content_list = list()
            content_list.append(email_obj.contents)

            mail_sender.send(to=email_obj.to_email, subject=email_obj.subject, contents=content_list)

            print(f"email({email_obj.subject}) to ({email_obj.to_email}) 发送成功！")
            break
        except:
            print(f"email({email_obj.subject}) to ({email_obj.to_email}) 第{i}次发送失败！\n{traceback.format_exc()}")
            time.sleep(3)
            continue
