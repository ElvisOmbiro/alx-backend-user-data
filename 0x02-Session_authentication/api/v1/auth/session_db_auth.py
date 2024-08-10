#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
base for session authentication
"""
from models.user_session import UserSession
from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """
    Class SessionDBAuth that inherits from SessionExpAuth
    """
    def create_session(self, user_id=None):
        """
        Method that creates a new session for a given user_id
        """
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        kwargs = {
            'user_id': user_id,
            'session_id': session_id
        }
        user_session = UserSession(**kwargs)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Method that returns the user_id for a given session_id
        """
        if session_id is None:
            return None

        user_sessions = UserSession.search({'session_id': session_id})

        if not user_sessions:
            return None

        user_session = user_sessions[0]

        expires = user_session.created_at + timedelta(
                seconds=self.session_duration)

        if expires < datetime.utcnow():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """
        Method that destroys a session for a given user id
        """
        if not request:
            return False

        session_id = self.session_cookie(request)

        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        user_sessions = UserSession.search({'session_id': session_id})

        if not user_sessions:
            return False

        user_session = user_sessions[0]

        try:
            user_session.remove()
        except Exception:
            return False

        return True
