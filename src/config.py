#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from pydantic import BaseModel, Field


class BaseConfig(BaseModel):
    API_ID: str = Field(default=os.environ["API_ID"])
    API_KEY: str = Field(default=os.environ["API_KEY"])

    email_address: str = Field(default=os.environ["EMAIL_USER"])
    email_password: str = Field(default=os.environ["EMAIL_PASSWORD"])
    email_host: str = Field(default=os.environ["EMAIL_HOST"])

    receive_email: str = Field(default=os.environ["RECEIVE_EMAIL"])


base_config = BaseConfig()
