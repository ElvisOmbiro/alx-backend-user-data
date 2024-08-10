#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
module for user session
"""
from models.base import Base


class UserSession(Base):
    """
    UserSession model
    """
    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
