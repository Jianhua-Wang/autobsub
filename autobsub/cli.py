"""Console script for autosbatch."""

import logging
from pathlib import Path
from typing import List, Optional

import typer
from autobsub import LSFPool, __version__
from rich.console import Console

# from autobsub.logger import logger

logger = logging.getLogger("autobsub")

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
app = typer.Typer(context_settings=CONTEXT_SETTINGS, add_completion=False)

# config = {
#     'logging_level': logging.WARNING,
# }


@app.command()
def single_job(
    ncpus: int = typer.Option(1, "--ncpus", "-n", help="Number of cpus."),
    node: str = typer.Option(None, "--node", "-N", help="Node to submit job to."),
    queue: str = typer.Option(None, "--queue", "-Q", help="Queue to submit jobs to."),
    job_name: str = typer.Option("job", "--job-name", "-j", help="Name of the job."),
    cmd: List[str] = typer.Argument(..., help="Command to run."),
):
    """Submit a single job to LSF cluster."""
    cmd = [" ".join(cmd)]
    if node:
        node_list: Optional[List] = [node]
    else:
        node_list = None
    p = LSFPool(
        pool_size=1,
        ncpus_per_job=ncpus,
        node_list=node_list,
        queue=queue,
    )
    p.multi_submit(cmds=cmd, job_name=job_name)


@app.command()
def multi_job(
    pool_size: int = typer.Option(
        None, "--pool-size", "-p", min=0, max=1000, help="Number of jobs to submit at the same time."
    ),
    ncpus_per_job: int = typer.Option(1, "--ncpus-per-job", "-n", help="Number of cpus per job."),
    max_jobs_per_node: int = typer.Option(
        None, "--max-jobs-per-node", "-m", help="Maximum number of jobs to submit to a single node."
    ),
    node_list: List[str] = typer.Option(
        None, "--node-list", "-l", help='List of nodes to submit jobs to. e.g. "-l node1 -l node2 -l node3"'
    ),
    queue: str = typer.Option(None, "--queue", "-Q", help="Queue to submit jobs to."),
    job_name: str = typer.Option("job", "--job-name", "-j", help="Name of the job."),
    cmdfile: Path = typer.Argument(..., help="Path to the command file."),
):
    """Submit multiple jobs to LSF cluster."""
    with open(cmdfile, "r") as f:
        cmds = f.readlines()
    cmds = [cmd.strip() for cmd in cmds]

    p = LSFPool(
        pool_size=pool_size,
        ncpus_per_job=ncpus_per_job,
        max_jobs_per_node=max_jobs_per_node,
        node_list=node_list,
        queue=queue,
    )
    p.multi_submit(cmds=cmds, job_name=job_name)


@app.command()
def clean():
    """Remove all scripts and logs."""
    LSFPool.clean()
    # logger.setLevel(config['logging_level'])
    logger.setLevel(logging.INFO)
    logger.info("Cleaned all scripts and logs.")


@app.callback(invoke_without_command=True, no_args_is_help=True)
def main(
    version: bool = typer.Option(False, "--version", "-V", help="Show version."),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show verbose info."),
    dev: bool = typer.Option(False, "--dev", help="Show dev info."),
):
    """Submit jobs to slurm cluster, without writing slurm script files."""
    console = Console()
    console.rule("[bold blue]Autobsub[/bold blue]")
    if version:
        typer.echo(f"Autobsub version: {__version__}")
        raise typer.Exit()
    if verbose:
        logger.setLevel(logging.INFO)
        logger.info("Verbose mode is on.")
    if dev:
        logger.setLevel(logging.DEBUG)
        logger.debug("Dev mode is on.")


if __name__ == "__main__":
    app()
