import traceback
import logging
import argparse
from os import makedirs, sep

from configuration.configuration import Configuration
from datastore.mysql_datastore import MySqlDataStore
from cloudstore.dropbox_cloudstore import DropboxCloudstore

logger = logging.getLogger('Main')


def main():
    # Initializing
    args = __argparser__()
    __setup_log__(args.log, args.debug)
    logger.info("Starting")
    # Load the configuration
    configuration = Configuration(config_src=args.config_file)
    # Init the Cloudstore
    cloud_store = DropboxCloudstore(api_key=configuration.get_cloudstore()['api_key'])
    # Init the Datastore
    data_store = MySqlDataStore(**configuration.get_datastore())

    print(data_store.show_tables())
    data_store.__exit__()

    print(cloud_store.ls(path='').keys())


def __setup_log__(log_path: str, debug: bool = False) -> None:
    if log_path is None:
        log_path = 'logs/out.log'

    log_path = log_path.split(sep)
    if len(log_path) > 1:

        try:
            makedirs((sep.join(log_path[:-1])))
        except FileExistsError:
            pass
    log_filename = sep.join(log_path)
    # noinspection PyArgumentList
    logging.basicConfig(level=logging.INFO if debug is not True else logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[
                            logging.FileHandler(log_filename),
                            # logging.handlers.TimedRotatingFileHandler(log_filename, when='midnight', interval=1),
                            logging.StreamHandler()
                        ]
                        )


def __argparser__() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='A description of the project',
        add_help=False)
    # Required Args
    required_arguments = parser.add_argument_group('required arguments')
    config_file_params = {
        'type': argparse.FileType('r'),
        'required': True,
        'help': "The configuration yml file"
    }
    required_arguments.add_argument('-m', '--run-mode', choices=['run_mode_1', 'run_mode_2', 'run_mode_3'],
                                    required=True,
                                    default='run_mode_1',
                                    help='Description of the run modes')
    required_arguments.add_argument('-c', '--config-file', **config_file_params)
    required_arguments.add_argument('-l', '--log', help="Name of the output log file")
    # Optional args
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('-d', '--debug', action='store_true', help='enables the debug log messages')
    optional.add_argument("-h", "--help", action="help", help="Show this help message and exit")

    return parser.parse_args()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(str(e) + '\n' + str(traceback.format_exc()))
        raise e
