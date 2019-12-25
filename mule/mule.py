#!/usr/bin/env python3
import click
import yaml
import os
import sys
import logging.config

from mule import ROOT

from mule.utils import configure as configutil
from mule.drive.vehicle import Vehicle

DEFAULT_LOGCFG = os.path.join(ROOT, 'log/config/default.yml')
DEFAULT_DRVCFG = os.path.join(ROOT, 'drive/config/default.yml')

@click.group()
@click.option('--logcfg', default=DEFAULT_LOGCFG, type=click.Path(exists=True, readable=True))
def cli(logcfg):
    print('Opening {}'.format(logcfg))
    with open(logcfg, 'r') as fd:
        config = yaml.load(fd)
        logging.config.dictConfig(config)

    logging.info('Logging brought to you by {}'.format(logcfg))

@cli.command()
def calibrate():
    pass

@cli.command()
@click.option('--cfg', default=DEFAULT_DRVCFG, type=click.Path(exists=True, readable=True))
@click.option('--model_path', type=click.Path(exists=True),required=False)
def drive(cfg, model_path):

    #print(model_path)
    #raise

    config = configutil.parse_config(cfg)

    #TODO: Refactor passing model path cleanly!
    if model_path:
        logging.debug("Model: {}".format(model_path))
        for part in config['parts']:
            #print(part)
            for key in part.keys():
                if key=='ai':
                    part['ai']['arguments']['model_path'] = model_path
    else:
        logging.debug("No model specified.".format())

    #print(config)
    #raise
    protoparts = configutil.create_protoparts(config['parts'])

    logging.info('Creating vehicle from loaded configuration')

    mule = Vehicle.from_config(protoparts)

    logging.info('Start your engines ...')

    mule.start(config)

    logging.info('Initiating drive loop')

    mule.drive(freq_hertz=config['drive']['freq_hertz'],
               verbose=config['drive']['verbose'],
               verbosity=config['drive']['verbosity'],
               )

    logging.info('Killing engine')

    mule.stop()
    logging.info("Done with this driving session, exiting python.")


@cli.command()
def train():
    pass

if __name__ == '__main__':
    print('*** Welcome to Mule.AI ***')
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    print("Current working directory", os.getcwd())
    cli()
