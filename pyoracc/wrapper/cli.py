import os
import time

import click
from multiprocessing import Pool
from stat import ST_MODE, S_ISREG

from pyoracc.wrapper.segment import Segmentor

from pyoracc.atf.common.atffile import check_atf


def check_atf_message((segpathname, atftype, verbose)):
    click.echo('\n Info: Parsing {0}.'.format(segpathname))
    try:
        check_atf(segpathname, atftype, verbose)
        click.echo('Info: Correctly parsed {0}.'.format(segpathname))
    except (SyntaxError, IndexError, AttributeError,
            UnicodeDecodeError) as e:
        click.echo("Info: Failed with message: {0} in {1}"
                   .format(e, segpathname))
        return -1


def check_and_process(pathname, atftype, whole, verbose=False):
    mode = os.stat(pathname)[ST_MODE]
    if S_ISREG(mode) and pathname.lower().endswith('.atf'):
        # It's a file, call the callback function
        if verbose:
            click.echo('Info: Parsing {0}.'.format(pathname))
        try:
            if not whole:
                pool = Pool()
                segmentor = Segmentor(pathname, verbose)
                outfolder = segmentor.convert()
                if verbose:
                    click.echo('Info: Segmented into {0}.'.format(outfolder))

                files = map(lambda f: os.path.join(outfolder, f), os.listdir(outfolder))
                count_files = len(files)
                atftypelist = [atftype]*count_files
                verboselist = [verbose]*count_files
                pool.map(check_atf_message, zip(files, atftypelist, verboselist))
                pool.close()
            else:
                check_atf_message((pathname, atftype, verbose))
            click.echo('Info: Finished parsing {0}.'.format(pathname))
            return 1
        except (SyntaxError, IndexError, AttributeError,
                UnicodeDecodeError) as e:
            click.echo("Info: Failed with message: {0} in {1}"
                       .format(e, pathname))
            return -1


@click.command()
@click.option('--input_path', '-i',
              type=click.Path(exists=True, writable=True), prompt=True,
              required=True,
              help='Input the file/folder name.')
@click.option('--atf_type', '-f', type=click.Choice(['cdli', 'oracc']),
              prompt=True, required=True,
              help='Input the atf file type.')
@click.option('--whole', '-w', default=False, required=False, is_flag=True,
              help='Disables the segmentation of the atf file and run as a whole.')
@click.option('--verbose', '-v', default=False, required=False, is_flag=True,
              help='Enables verbose mode.')
@click.version_option()
def main(input_path, atf_type, whole, verbose):
    """My Tool does one work, and one work well."""
    tsbegin = time.time()
    if os.path.isdir(input_path):
        failures = 0
        successes = 0
        with click.progressbar(os.listdir(input_path),
                               label='Info: Checking the files') as bar:
            for index, f in enumerate(bar):
                pathname = os.path.join(input_path, f)
                try:
                    check_and_process(pathname, atf_type, whole, verbose)
                    successes += 1
                    click.echo('Info: Correctly parsed {0}.'.format(pathname))
                except (SyntaxError, IndexError, AttributeError,
                        UnicodeDecodeError) as e:
                    failures += 1
                    click.echo("Info: Failed with message: {0} in {1}"
                               .format(e, pathname))
                finally:
                    try:
                        click.echo("Failed with {0} out of {1} ({2}%)"
                                   .format(failures, failures + successes, failures * 100.0 / (failures + successes)))
                    except ZeroDivisionError:
                        click.echo("Empty files to process")
    else:
        check_and_process(input_path, atf_type, whole, verbose)
    tsend = time.time()
    click.echo("Total time taken: {0} minutes".format((tsend-tsbegin)/60.0))
