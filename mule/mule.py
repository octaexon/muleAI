#!/usr/bin/env python3
import click
import yaml
import os
import sys
import logging.config

from mule import ROOT, LOG_CFG_TAG, DRV_CFG_TAG
from mule.logging import load_config
from mule.drive import parse_config, create_protoparts
from mule.drive.vehicle import Vehicle
import mule.calibrate.devices as calibrators

logger = logging.getLogger(__name__)

@click.group()
@click.option('--logcfg', 'ref',
              default=LOG_CFG_REF)
              #type=click.Path(exists=True, readable=True))
def cli(ref):
    config = load_config(ref)
    logging.config.dictConfig(config)

    logger.debug(f'Loaded logging config: {}')


@cli.command()
@click.option('--device')
def calibrate(device):
    calibrators.registry[device]()

@cli.command()
@click.option('--cfg', 'ref',
              default=DRV_CFG_REF,
              type=click.STRING)
              # type=click.Path(exists=True, readable=True))
@click.option('--model_path', type=click.Path(exists=True), required=False)
def drive(ref, model_path):

    config = parse_config(ref)

    #TODO: Refactor passing model path cleanly!
    if model_path:
        logging.debug("Model: {}".format(model_path))
        for part in config['parts']:
            #print(part)
            for key in part.keys():
                if key == 'ai':
                    part['ai']['arguments']['model_path'] = model_path
    else:
        logging.debug("No model specified.".format())

    protoparts = create_protoparts(config['parts'])

    logging.info('Creating vehicle from loaded configuration')

    mule = Vehicle.from_config(protoparts)

    logging.info('Start your engines ...')

    mule.start(config)

    logging.info('Initiating drive loop')

    mule.drive(
        freq_hertz=config['drive']['freq_hertz'],
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
