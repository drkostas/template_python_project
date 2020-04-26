import os
import logging
from typing import Dict, List, Tuple, Union
import json
import _io
from io import StringIO, TextIOWrapper
import re
import yaml
from jsonschema import validate as validate_json_schema


class Configuration:
    __slots__ = ('config', 'config_path', 'datastore', 'cloudstore', 'email_app', 'tag')

    config: Dict
    config_path: str
    datastore: Dict
    cloudstore: Dict
    email_app: Dict
    tag: str
    config_attributes: List = []
    env_variable_tag: str = '!ENV'
    env_variable_pattern: str = r'.*?\${(\w+)}.*?'  # ${var}
    logger = logging.getLogger('Configuration')

    def __init__(self, config_src: Union[TextIOWrapper, StringIO, str], config_schema_path: str = 'yml_schema.json'):
        """
        Tha basic constructor. Creates a new instance of a MySQL Datastore using the specified credentials

        :param config_src:
        """

        # Load the predefined schema of the configuration
        configuration_schema = self.load_configuration_schema(config_schema_path=config_schema_path)
        # Load the configuration
        self.config, self.config_path = self.load_yml(config_src=config_src, env_tag=self.env_variable_tag,
                                                      env_pattern=self.env_variable_pattern)
        # Validate the config
        validate_json_schema(self.config, configuration_schema)
        # Set the config properties as instance attributes
        self.tag = self.config['tag']
        all_config_attributes = ('datastore', 'cloudstore', 'email_app')
        for config_attribute in all_config_attributes:
            if config_attribute in self.config.keys():
                setattr(self, config_attribute, self.config[config_attribute])
                self.config_attributes.append(config_attribute)
            else:
                setattr(self, config_attribute, None)

    @staticmethod
    def load_configuration_schema(config_schema_path: str) -> Dict:
        with open('/'.join([os.path.dirname(os.path.realpath(__file__)), config_schema_path])) as f:
            configuration_schema = json.load(f)
        return configuration_schema

    @staticmethod
    def load_yml(config_src: Union[TextIOWrapper, StringIO, str], env_tag: str, env_pattern: str) -> Tuple[Dict, str]:
        pattern = re.compile(env_pattern)
        loader = yaml.SafeLoader
        loader.add_implicit_resolver(env_tag, pattern, None)

        def constructor_env_variables(loader, node):
            """
            Extracts the environment variable from the node's value
            :param yaml.Loader loader: the yaml loader
            :param node: the current node in the yaml
            :return: the parsed string that contains the value of the environment
            variable
            """
            value = loader.construct_scalar(node)
            match = pattern.findall(value)  # to find all env variables in line
            if match:
                full_value = value
                for g in match:
                    full_value = full_value.replace(
                        f'${{{g}}}', os.environ.get(g, g)
                    )
                return full_value
            return value

        loader.add_constructor(env_tag, constructor_env_variables)

        if isinstance(config_src, TextIOWrapper):
            config = yaml.load(config_src, Loader=loader)
            config_path = config_src.name
        elif isinstance(config_src, StringIO):
            config = yaml.load(config_src, Loader=loader)
            config_path = "StringIO"
        elif isinstance(config_src, str):
            with open(config_src) as f:
                config = yaml.load(f, Loader=loader)
            config_path = config_src
        else:
            raise TypeError('Config file must be TextIOWrapper or path to a file')
        return config, config_path

    def __getitem__(self, item):
        return self.__getattribute__(item)

    def get_datastore(self) -> Dict:
        if 'datastore' in self.config_attributes:
            return self.datastore['config']
        else:
            raise ConfigurationError('Config property datastore not set!')

    def get_cloudstore(self) -> Dict:
        if 'cloudstore' in self.config_attributes:
            return self.cloudstore['config']
        else:
            raise ConfigurationError('Config property cloudstore not set!')

    def get_email_app(self) -> Dict:
        if 'email_app' in self.config_attributes:
            return self.email_app['config']
        else:
            raise ConfigurationError('Config property email_app not set!')


    def to_yml(self, fn: Union[str, _io.TextIOWrapper], include_tag=False) -> None:
        """
        Writes the configuration to a stream. For example a file.

        :param fn:
        :param include_tag:
        :return: None
        """

        dict_conf = dict()
        for config_attribute in self.config_attributes:
            dict_conf[config_attribute] = getattr(self, config_attribute)
        if include_tag:
            dict_conf['tag'] = self.tag

        if isinstance(fn, str):
            with open(fn, 'w') as f:
                yaml.dump(dict_conf, f, default_flow_style=False)
        elif isinstance(fn, _io.TextIOWrapper):
            yaml.dump(dict_conf, fn, default_flow_style=False)
        else:
            raise TypeError('Expected str or _io.TextIOWrapper not %s' % (type(fn)))

    to_yaml = to_yml

    def to_json(self) -> Dict:
        dict_conf = dict()
        for config_attribute in self.config_attributes:
            dict_conf[config_attribute] = getattr(self, config_attribute)
        dict_conf['tag'] = self.tag
        return dict_conf


class ConfigurationError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
