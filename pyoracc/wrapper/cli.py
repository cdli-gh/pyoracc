import os
import time
import codecs
import click
from multiprocessing import Pool
from stat import ST_MODE, S_ISREG

from pyoracc.wrapper.segment import Segmentor

from pyoracc.atf.common.atffile import check_atf
from pyoracc.tools.logtemplate import LogTemplate
from pyoracc.tools.errors_template import ErrorsTemplate
log_tmp=LogTemplate()
error_tmp=ErrorsTemplate()

def output_error(error_list, summary, pathname, whole, summary_str,orig_map):
    if len(summary) > 0 and os.path.isdir(summary) and (not whole):
        summary = summary if summary[-1]=='/' else summary+'/'
        file = open(summary+"PyOracc.log", "a+")
        error_idx=0
        # error:tuple (errors,atf_id,segpathname)
        for error in error_list:
            pos_renew = orig_map[error[1]] if (error[1] in orig_map) else 0
            if len(error[0])  > 0:
                head_str = log_tmp.head_default(error_idx,error[1],error[2])
                click.echo(head_str)
                file.write(head_str + '\n')
                error_idx+=1
            # tmp_err:
            for tmp_err in error[0]:
                err_str = (" "*(len(str(error_idx))+4) + error_tmp.error2str(pos_renew,tmp_err))
                click.echo(err_str)
                file.write(err_str + '\n')
        file.write(summary_str + '\n')
        file.close()
    else:
        error_idx=0
        # error:tuple (errors,atf_id,segpathname)
        for error in error_list:
            pos_renew = orig_map[error[1]] if (error[1] in orig_map) else 0
            if len(error[0])  > 0:
                head_str = log_tmp.head_default(error_idx,error[1],error[2])
                click.echo(head_str)
                error_idx+=1
            # tmp_err:
            for tmp_err in error[0]:
                err_str = (" "*6 + error_tmp.error2str(pos_renew,tmp_err))
                click.echo(err_str)
        if not os.path.isdir(summary) and (not whole):
            click.echo(log_tmp.wrong_path(summary))
    click.echo(summary_str)


def check_atf_message((segpathname, atftype, verbose,skip)): # this tuple parameters format no longer support in python3
    # click.echo('\n Info: Parsing {0}.'.format(segpathname))
    atf_id = (segpathname.split('/')[-1]).split('.')[0]# extract atf_id(e.g. P136211) 
    # print(atf_id)
    errors= check_atf(segpathname, atftype, verbose,skip,atf_id)
    return (errors,atf_id,segpathname)


def check_and_process(pathname,summary,atftype, whole, verbose=False):
    mode = os.stat(pathname)[ST_MODE]
    error_list = None
    if S_ISREG(mode) and pathname.lower().endswith('.atf'):
        # It's a file, call the callback function
        if verbose:
            click.echo('Info: Parsing {0}.'.format(pathname))
        try:
            segmentor = Segmentor(pathname, verbose)
            if not whole:
                pool = Pool()
                # segmentor = Segmentor(pathname, verbose)
                outfolder = segmentor.convert()
                if verbose:
                    click.echo('Info: Segmented into {0}.'.format(outfolder))

                files = map(lambda f: os.path.join(outfolder, f), os.listdir(outfolder))
                count_files = len(files)
                atftypelist = [atftype]*count_files
                verboselist = [verbose]*count_files
                skiplist = [not whole]*count_files
                error_list = pool.map(check_atf_message, zip(files, atftypelist, verboselist,skiplist)) # get error list
                pool.close()
            else:
                error_list = [check_atf_message((pathname, atftype, verbose,(not whole)))] # get error list
            num_error = 0
            for error in error_list:
                num_error += len(error[0])
            summary_str = log_tmp.summary_num(num_error,pathname)
            if num_error == 0:
                click.echo(summary_str)
            else:
                output_error(error_list,summary,pathname,whole,summary_str,segmentor.col_map)
            click.echo(log_tmp.summary_end(pathname))
            return 1
        except (SyntaxError, IndexError, AttributeError,
                UnicodeDecodeError) as e:
            click.echo(log_tmp.raise_error(e, pathname))
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
@click.option('--summary', '-s', type=click.STRING,default='', required=False,
                help='Folder path for log and summary of parser, only useful when run file without -w/--whole')
@click.version_option()
def main(input_path, atf_type, whole, verbose,summary):
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
                    check_and_process(pathname, summary, atf_type, whole, verbose)
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
        check_and_process(input_path, summary, atf_type, whole, verbose)
    tsend = time.time()
    click.echo("Total time taken: {0} minutes".format((tsend-tsbegin)/60.0))
