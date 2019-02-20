import os

import internetarchive

class InternetArchive(object):
    # Docs at https://archive.org/services/docs/api/
    def __init__(self, access_key, secret_key):
        self.__access_key = access_key
        self.__secret_key = secret_key

    def upload(self, item, filepath):
        response = internetarchive.upload(
            identifier=item,
            files=filepath,
            access_key=self.__access_key,
            secret_key=self.__secret_key,
        )[0]
        return response

    @staticmethod
    def get_public_url(item, filepath):
        return (
            'https://archive.org/download/{identifier}/{filename}'
            .format(
                identifier=item,
                filename=os.path.basename(filepath)
            )
        )

