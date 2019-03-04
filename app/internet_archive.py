import internetarchive


class InternetArchiveError(Exception):
    pass


class KeyExists(InternetArchiveError):
    def __init__(self, identifier, key):
        super().__init__()
        self._identifier = identifier
        self._key = key

    def __str__(self):
        return f'Key "{self._key}" already exists in item "{self._identifier}"'


# TODO: add tests
class InternetArchive(object):
    """Wrapper for internetachive library https://archive.org/services/docs/api/internetarchive/index.html

    You can retrieve S3 keys here: https://archive.org/account/s3.php
    """

    def __init__(self, access_key, secret_key):
        config = dict(s3=dict(access=access_key, secret=secret_key))
        self._session = internetarchive.get_session(config)
        self._items = {}

    def get_item(self, identifier):
        try:
            return self._items[identifier]
        except KeyError:
            self._items[identifier] = self._session.get_item(identifier)
            return self._items[identifier]

    # TODO: check key is filename but not path
    # TODO: check key doesn't contain leading dots
    def upload(self, identifier, file, key, force=False):
        """Upload file to InternetArchive.org
        
        :param identifier: Identifier of archive.org item
        :type identifier: str
        
        :param file: The filepath or file-like object to upload.
        
        :param key: Remote filename
        :type key: str
        
        :param force: Force to upload file, even if it exists, defaults to False
        :param force: bool, optional
        """
        item = self.get_item(identifier)
        if not force and item.get_file(key).exists:
            raise KeyExists(identifier=identifier, key=key)
        return item.upload_file(file, key)

    @staticmethod
    def get_public_url(identifier, key):
        return f'https://archive.org/download/{identifier}/{key}'
