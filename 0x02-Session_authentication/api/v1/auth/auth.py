#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
the authentication start
"""
from os import getenv
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Require method

        Parameters
        ----------
        path
            Path to check
        excluded_paths
            Excluded paths

        Returns
        -------
        bool
            True if path is allowed
        """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        normalized_path = path if path.endswith('/') else path + '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                prefix = excluded_path[:-1]
                if normalized_path.startswith(prefix):
                    return False
            elif excluded_path.endswith('/'):
                if normalized_path == excluded_path:
                    return False
            elif normalized_path.startswith(excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Authorization header method

        Parameters
        ----------
        request
            Request object

        Returns
        -------
        str
            Authorization header
        """
        if request is None:
            return None

        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None

        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Current user method

        Parameters
        ----------
        request
            Request object

        Returns
        -------
        User
            User object
        """
        return None

    def session_cookie(self, request=None) -> str:
        """
        Session cookie method

        Parameters
        ----------
        request
            Request object

        Returns
        -------
        str
            Session cookie
        """
        if request is None:
            return None

        SESSION_NAME = getenv('SESSION_NAME')

        if SESSION_NAME is None:
            return None

        return request.cookies.get(SESSION_NAME)
