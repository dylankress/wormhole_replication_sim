"""Console script for wormhole_replication_sim."""
import wormhole_replication_sim

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for wormhole_replication_sim."""
    console.print("Replace this message by putting your code into "
               "wormhole_replication_sim.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    


if __name__ == "__main__":
    app()
