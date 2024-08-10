#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
expiry to the user authenticated session
"""
from os import getenv
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Class that defines a session expiration auth module"""
    def __init__(self):
        """Constructor"""
        super().__init__()
        session_duration = getenv("SESSION_DURATION")
        try:
            self.session_duration = int(session_duration)
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creates a session"""
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
                }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves the user_id for a given session_id"""
        if session_id is None:
            return None

        session_info = self.user_id_by_session_id.get(session_id)

        if session_info is None:
            return None

        user_id = session_info.get('user_id')

        if self.session_duration <= 0:
            return user_id

        created_at = session_info.get('created_at')

        if created_at is None:
            return None

        expiration_time = created_at + timedelta(
            seconds=self.session_duration)

        if expiration_time < datetime.now():
            return None

        return user_id
