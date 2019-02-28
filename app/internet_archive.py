import os

import internetarchive

class InternetArchive(object):
    # Docs at https://archive.org/services/docs/api/
    def __init__(self, access_key, secret_key):
        self.__access_key = access_key
        self.__secret_key = secret_key

    # TODO: check key is filename but not path
    # TODO: check key doesn't contain leading dots
    # TODO: check key existence
    def upload(self, identifier, file, key, force=False):
        internetarchive.upload(
            identifier=identifier,
            files={key: file},
            access_key=self.__access_key,
            secret_key=self.__secret_key,
        )[0]

    @staticmethod
    def get_public_url(identifier, key):
        return f'https://archive.org/download/{identifier}/{key}'
