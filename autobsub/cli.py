"""Console script for autobsub."""

import typer

app = typer.Typer()

def main():
    """Main entrypoint."""
    typer.echo("autobsub")
    typer.echo("=" * len("autobsub"))
    typer.echo("automatically submit LSF jobs")


if __name__ == "__main__":
   app(main)