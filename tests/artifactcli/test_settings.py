import unittest
from copy import copy
from StringIO import StringIO
from artifactcli import *


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.default_opts = {'access_key': None, 'force': False, 'bucket': None, 'region': None,
                             'print_only': False, 'secret_key': None, 'config': '~/.artifact-cli', 'output': None}
        self.full_opts = {'access_key': 'ACCESS_KEY', 'force': True, 'bucket': 'BUCKET', 'region': None,
                          'print_only': True, 'secret_key': 'SECRET_KEY', 'config': 'xxx', 'output': None}

    def _updated_opts(self, updates):
        d = copy(self.default_opts)
        d.update(updates)
        return d

    def test_parse_args_empty(self):
        self.assertEqual(Settings().parse_args(['art']), Settings())

    def test_parse_args_list(self):
        s = Settings().parse_args(['art', 'list', 'gid'])
        self.assertEqual(s, Settings(operation=ListOperation('gid', []), options=self.default_opts))

    def test_parse_args_list_full(self):
        s = Settings().parse_args(
            ['art', 'list', 'gid', '--config', 'xxx', '--check', '--force', '--access', 'ACCESS_KEY', '--secret',
             'SECRET_KEY', '--bucket', 'BUCKET'])
        self.assertEqual(s, Settings(operation=ListOperation('gid', []), options=self.full_opts))

    def test_parse_args_list_error(self):
        self.assertEqual(Settings().parse_args(['art', 'list']), Settings())

    def test_parse_args_upload(self):
        s = Settings().parse_args(['art', 'upload', 'gid', '/path/to/xxx'])
        self.assertEqual(s, Settings(operation=UploadOperation('gid', ['/path/to/xxx'], False, False),
                                     options=self.default_opts))

    def test_parse_args_upload_full(self):
        s = Settings().parse_args(
            ['art', 'upload', 'gid', '/path/to/xxx', '--config', 'xxx', '--check', '--force', '--access',
             'ACCESS_KEY', '--secret', 'SECRET_KEY', '--bucket', 'BUCKET'])
        self.assertEqual(s, Settings(operation=UploadOperation('gid', ['/path/to/xxx'], True, True),
                                     options=self.full_opts))

    def test_parse_args_upload_error(self):
        self.assertEqual(Settings().parse_args(['art', 'upload']), Settings())
        self.assertEqual(Settings().parse_args(['art', 'upload', 'gid']), Settings())

    def test_parse_args_download(self):
        s = Settings().parse_args(['art', 'download', 'gid', '/path/to/xxx', '123'])
        self.assertEqual(s, Settings(operation=DownloadOperation(
            'gid', ['/path/to/xxx', '123'], False), options=self.default_opts))

        s = Settings().parse_args(['art', 'download', 'gid', '/path/to/xxx', 'latest'])
        self.assertEqual(s, Settings(operation=DownloadOperation(
            'gid', ['/path/to/xxx', 'latest'], False), options=self.default_opts))

    def test_parse_args_download_full(self):
        s = Settings().parse_args(
            ['art', 'download', 'gid', '/path/to/xxx', '123', '--config', 'xxx', '--check', '--force', '--access',
             'ACCESS_KEY', '--secret', 'SECRET_KEY', '--bucket', 'BUCKET'])
        self.assertEqual(s, Settings(operation=DownloadOperation(
            'gid', ['/path/to/xxx', '123'], True), options=self.full_opts))

        s = Settings().parse_args(
            ['art', 'download', 'gid', '/path/to/xxx', 'latest', '--config', 'xxx', '--check', '--force', '--access',
             'ACCESS_KEY', '--secret', 'SECRET_KEY', '--bucket', 'BUCKET'])
        self.assertEqual(s, Settings(operation=DownloadOperation(
            'gid', ['/path/to/xxx', 'latest'], True), options=self.full_opts))

    def test_parse_args_download_error(self):
        self.assertEqual(Settings().parse_args(['art', 'download']), Settings())
        self.assertEqual(Settings().parse_args(['art', 'download', 'gid']), Settings())
        self.assertEqual(Settings().parse_args(['art', 'download', 'gid', '/path/to/xxx']), Settings())
        self.assertEqual(Settings().parse_args(['art', 'download', 'gid', '/path/to/xxx', '']), Settings())
        self.assertEqual(Settings().parse_args(['art', 'download', 'gid', '/path/to/xxx', 'a']), Settings())
        self.assertEqual(Settings().parse_args(['art', 'download', 'gid', '/path/to/xxx', 'abc']), Settings())
        self.assertEqual(Settings().parse_args(['art', 'download', 'gid', '/path/to/xxx', '1.0']), Settings())
        self.assertEqual(Settings().parse_args(['art', 'download', 'gid', '/path/to/xxx', 'LATEST']), Settings())

    def test_parse_args_info(self):
        s = Settings().parse_args(['art', 'info', 'gid', 'xxx', '123'])
        self.assertEqual(s, Settings(operation=InfoOperation(
            'gid', ['xxx', '123'], None), options=self.default_opts))

        s = Settings().parse_args(['art', 'info', 'gid', 'xxx', 'latest'])
        self.assertEqual(s, Settings(operation=InfoOperation(
            'gid', ['xxx', 'latest'], None), options=self.default_opts))

    def test_parse_args_info_full(self):
        s = Settings().parse_args(
            ['art', 'info', 'gid', 'xxx', '123', '--config', 'xxx', '--check', '--force', '--access',
             'ACCESS_KEY', '--secret', 'SECRET_KEY', '--bucket', 'BUCKET', '--output', 'text'])
        o = self._updated_opts({
            'access_key': 'ACCESS_KEY', 'force': True, 'bucket': 'BUCKET',
            'print_only': True, 'secret_key': 'SECRET_KEY', 'config': 'xxx',
            'output': 'text'})
        self.assertEqual(s, Settings(operation=InfoOperation('gid', ['xxx', '123'], 'text'), options=o))

        s = Settings().parse_args(
            ['art', 'info', 'gid', 'xxx', 'latest', '--config', 'xxx', '--check', '--force', '--access',
             'ACCESS_KEY', '--secret', 'SECRET_KEY', '--bucket', 'BUCKET'])
        o = self._updated_opts({
            'access_key': 'ACCESS_KEY', 'force': True, 'bucket': 'BUCKET',
            'print_only': True, 'secret_key': 'SECRET_KEY', 'config': 'xxx', 'output': None})
        self.assertEqual(s, Settings(operation=InfoOperation('gid', ['xxx', 'latest'], None), options=o))

        s = Settings().parse_args(
            ['art', 'info', 'gid', 'xxx', 'latest', '--config', 'xxx', '--check', '--force', '--access',
             'ACCESS_KEY', '--secret', 'SECRET_KEY', '--bucket', 'BUCKET', '--output', 'json'])
        o = self._updated_opts({
            'access_key': 'ACCESS_KEY', 'force': True, 'bucket': 'BUCKET',
            'print_only': True, 'secret_key': 'SECRET_KEY', 'config': 'xxx', 'output': 'json'})
        self.assertEqual(s, Settings(operation=InfoOperation('gid', ['xxx', 'latest'], 'json'), options=o))

    def test_parse_args_info_error(self):
        self.assertEqual(Settings().parse_args(['art', 'info']), Settings())
        self.assertEqual(Settings().parse_args(['art', 'info', 'gid']), Settings())
        self.assertEqual(Settings().parse_args(['art', 'info', 'gid', 'xxx']), Settings())
        self.assertEqual(Settings().parse_args(['art', 'info', 'gid', 'xxx', '']), Settings())
        self.assertEqual(Settings().parse_args(['art', 'info', 'gid', 'xxx', 'a']), Settings())
        self.assertEqual(Settings().parse_args(['art', 'info', 'gid', 'xxx', 'abc']), Settings())
        self.assertEqual(Settings().parse_args(['art', 'info', 'gid', 'xxx', '1.0']), Settings())
        self.assertEqual(Settings().parse_args(['art', 'info', 'gid', 'xxx', 'LATEST']), Settings())

    def test_parse_args_command_error(self):
        self.assertEqual(Settings().parse_args(['art', 'xxx', 'gid']), Settings())

    def test_parse_args_unknown_option(self):
        try:
            Settings().parse_args(['art', '-x'])
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, 2)
        except Exception, e:
            self.fail('unexpected exception: %s' % e)
        else:
            self.fail('SystemExit exception expected')

    def test_load_config_none(self):
        ret = Settings().load_config()
        self.assertEqual(ret, Settings())

    def test_load_config_enough(self):
        s = Settings(
            operation=ListOperation('gid', []),
            options=self._updated_opts(
                {'access_key': 'ACCESS_KEY', 'secret_key': 'SECRET_KEY', 'bucket': 'BUCKET'})
        )
        t = Settings(
            operation=ListOperation('gid', []),
            options=self._updated_opts(
                {'access_key': 'ACCESS_KEY', 'secret_key': 'SECRET_KEY', 'bucket': 'BUCKET'}),
            repo=Repository(S3Driver('ACCESS_KEY', 'SECRET_KEY', 'BUCKET', 'gid'))
        )
        self.assertEqual(s.load_config(), t)

    def test_load_config_io_error(self):
        s = Settings(
            operation=ListOperation('gid', []),
            options=self._updated_opts({'config': 'tests/resources/test-artifact-cli.conf_no_such_file'}))
        self.assertEqual(s.load_config(), Settings())

    def test_load_config_missing(self):
        s = Settings(
            operation=ListOperation('gid', []),
            options=self._updated_opts({'config': 'tests/resources/test-artifact-cli.conf'}))
        self.assertEqual(s.load_config(), Settings())

    def test_load_config_ok(self):
        s = Settings(
            operation=ListOperation('gid', []),
            options=self._updated_opts({'config': 'tests/resources/test-artifact-cli.conf', 'bucket': 'bucket4art'}))
        t = Settings(
            operation=ListOperation('gid', []),
            options=self._updated_opts({'config': 'tests/resources/test-artifact-cli.conf', 'bucket': 'bucket4art'}),
            repo=Repository(S3Driver('XXX', 'YYY', 'bucket4art', 'gid'))
        )
        self.assertEqual(s.load_config(), t)

    def test_load_config_attribute_error(self):
        s = Settings(options=self.default_opts)
        self.assertEqual(s.load_config(), Settings())

    def test_read_aws_config_empty(self):
        s = StringIO('')
        self.assertEqual(Settings._read_aws_config(s, ''), (None, None, None))

    def test_read_aws_config_default_some(self):
        s = StringIO("""[default]\naws_access_key_id = abcdefghijklmnopqrstuvwxyz""")
        self.assertEqual(Settings._read_aws_config(s, 'mogproject'),
                         ('abcdefghijklmnopqrstuvwxyz', None, None))

    def test_read_aws_config_default_full(self):
        s = StringIO('\n'.join([
            '[default]',
            'aws_access_key_id = abcdefghijklmnopqrstuvwxyz',
            'aws_secret_access_key=ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'bucket = bucket-name',
            'region= ap-northeast-1',
        ]))
        self.assertEqual(Settings._read_aws_config(s, 'mogproject'),
                         ('abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'bucket-name'))

    def test_read_aws_config_non_default_full(self):
        s = StringIO('\n'.join([
            '[default]',
            'aws_access_key_id = abcdefghijklmnopqrstuvwxyz',
            'aws_secret_access_key=ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'bucket = bucket-name',
            '[my.group.id]',
            'aws_access_key_id = zyxwvutsrqponmlkjihgfedcba',
            'aws_secret_access_key=ZYXWVUTSRQPONMLKJIHGFEDCBA',
            'bucket = bucket-name-123',
        ]))
        self.assertEqual(Settings._read_aws_config(s, 'my.group.id'),
                         ('zyxwvutsrqponmlkjihgfedcba', 'ZYXWVUTSRQPONMLKJIHGFEDCBA', 'bucket-name-123'))

    def test_read_config_fallback(self):
        s = StringIO('\n'.join([
            '[default]',
            'aws_access_key_id = abcdefghijklmnopqrstuvwxyz',
            'aws_secret_access_key=ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'bucket = bucket-name',
            '[my.group.id]',
            'aws_access_key_id = zyxwvutsrqponmlkjihgfedcba',
            'aws_secret_access_key=ZYXWVUTSRQPONMLKJIHGFEDCBA',
            'bucket = bucket-name-123',
        ]))
        self.assertEqual(Settings._read_aws_config(s, 'mogproject'),
                         ('abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'bucket-name'))
