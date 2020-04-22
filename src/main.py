import traceback
import logging
import argparse
from os import makedirs, sep

from configuration.configuration import Configuration
from datastore.mysql_datastore import MySqlDataStore
from cloudstore.dropbox_cloudstore import DropboxCloudstore

logger = logging.getLogger('Main')


def _setup_log(log_path: str = '../logs/out.log', debug: bool = False) -> None:
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


def _argparser() -> argparse.Namespace:
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


def main():
    """
    :Example:
    python main.py -m run_mode_1
                   -c ../confs/template_conf.yml
                   -l ../logs/out.log
    """

    # Initializing
    args = _argparser()
    _setup_log(args.log, args.debug)
    logger.info("Starting")
    # Load the configuration
    configuration = Configuration(config_src=args.config_file)
    # Init the Cloudstore
    cloud_store = DropboxCloudstore(api_key=configuration.get_cloudstore()['api_key'])
    # Init the Datastore
    data_store = MySqlDataStore(**configuration.get_datastore())

    logger.info("Tables in current DB: {0}".format(list(data_store.show_tables())))
    logger.info("List of files in Dropbox root: {0}".format(list(cloud_store.ls(path='').keys())))

    data_store.__exit__()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(str(e) + '\n' + str(traceback.format_exc()))
        raise e
