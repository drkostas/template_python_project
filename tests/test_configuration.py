import unittest
from jsonschema.exceptions import ValidationError
import logging

from configuration.configuration import Configuration


class TestConfiguration(unittest.TestCase):
    logger = logging.getLogger('TestConfiguration')

    def test_schema_validation(self):
        try:
            self.logger.info('Loading the correct Configuration..')
            configuration = Configuration(config_src='test_data/test_configuration/minimal_conf_correct.yml',
                                          config_schema_path='../../tests/test_data/test_configuration/minimal_yml_schema.json')
        except Exception as e:
            self.logger.error('Error validating the correct yml: &s', e)
        else:
            self.logger.info('First yml validated successfully.')

        with self.assertRaises(ValidationError):
            self.logger.info('Loading the wrong Configuration..')
            configuration = Configuration(config_src='test_data/test_configuration/minimal_conf_wrong.yml',
                                          config_schema_path='../../tests/test_data/test_configuration/minimal_yml_schema.json')
            self.logger.info('Second yml failed to validate successfully.')

    def test_to_json(self):
        self.logger.info('Loading Configuration..')
        configuration = Configuration(config_src='test_data/test_configuration/template_conf.yml',
                                      config_schema_path='../../tests/test_data/test_configuration/yml_schema.json')
        expected_json = {'tag': 'production', 'datatore': {
            'config': {'hostname': 'host123', 'username': 'user1', 'password': 'pass2', 'db_name': 'db3', 'port': 3306},
            'type': 'mysql'}, 'cloudstore': {'config': {'api_key': 'apiqwerty'}, 'type': 'dropbox'}}
        # Compare
        self.logger.info('Comparing the results..')
        self.assertDictEqual(expected_json, configuration.to_json())

    def test_to_yaml(self):
        self.logger.info('Loading Configuration..')
        configuration = Configuration(config_src='test_data/test_configuration/template_conf.yml',
                                      config_schema_path='../../tests/test_data/test_configuration/yml_schema.json')
        # Modify and export yml
        self.logger.info('Changed the host and the api_key..')
        configuration.datastore['config']['hostname'] = 'changedhost'
        configuration.cloudstore['config']['api_key'] = 'changed_api'
        self.logger.info('Exporting to yaml..')
        configuration.to_yaml('test_data/test_configuration/actual_output_to_yaml.yml', include_tag=True)
        # Load the modified yml
        self.logger.info('Loading the exported yaml..')
        modified_configuration = Configuration(config_src='test_data/test_configuration/actual_output_to_yaml.yml',
                                      config_schema_path='../../tests/test_data/test_configuration/yml_schema.json')
        # Compare
        self.logger.info('Comparing the results..')
        expected_json = {'tag': 'production', 'datatore': {
            'config': {'hostname': 'changedhost', 'username': 'user1', 'password': 'pass2', 'db_name': 'db3', 'port': 3306},
            'type': 'mysql'}, 'cloudstore': {'config': {'api_key': 'changed_api'}, 'type': 'dropbox'}}
        self.assertDictEqual(expected_json, modified_configuration.to_json())

    @staticmethod
    def _setup_log(debug: bool = False) -> None:
        # noinspection PyArgumentList
        logging.basicConfig(level=logging.INFO if debug is not True else logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            handlers=[logging.StreamHandler()
                                      ]
                            )

    @classmethod
    def setUp(self) -> None:
        pass

    @classmethod
    def tearDown(self) -> None:
        pass

    # noinspection PyArgumentList
    @classmethod
    def setUpClass(cls):
        cls._setup_log()

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()
