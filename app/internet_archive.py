import os

import internetarchive

class InternetArchive(object):
    # Docs at https://archive.org/services/docs/api/
    def __init__(self, access_key, secret_key):
        self.__access_key = access_key
        self.__secret_key = secret_key

    # TODO: check key is filename but not path
    # TODO: check key doesn't contain leading dots
    def upload(self, item, file, key):
        internetarchive.upload(
            identifier=item,
            files={key: file},
            access_key=self.__access_key,
            secret_key=self.__secret_key,
        )[0]

    @staticmethod
    def get_public_url(item, key):
        return (
            'https://archive.org/download/{identifier}/{key}'
            .format(
                identifier=item,
                key=key
            )
        )

