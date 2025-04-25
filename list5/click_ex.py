from ex5 import find_file, load_data, random_station, statistics as stat
import click 

# python click_ex.py -p "NO2" -f "1g" -s 2023-01-01 -e 2023-01-09 statistics --station "DsJelGorOgin"
# python click_ex.py -p "NO2" -f "1g" -s 2023-01-01 -e 2023-01-09 station

@click.group()
@click.option('-p', '--parameter', required=True, help='Measured parameter (e.g., As(PM10), NO2, O3)')
@click.option('-f', '--frequency', required=True, type=click.Choice(['1g', '24g']), help='Measurement frequency')
@click.option('-s', '--start', required=True, help='Start date (yyyy-mm-dd)')
@click.option('-e', '--end', required=True, help='End date (yyyy-mm-dd)')
@click.pass_context
def cli(ctx, parameter, frequency, start, end):
    ctx.ensure_object(dict)
    ctx.obj['parameter'] = parameter
    ctx.obj['frequency'] = frequency
    ctx.obj['start'] = start
    ctx.obj['end'] = end

@cli.command(help="Random station with measurements")
@click.pass_context
def station(ctx):
    click.echo(f"[station] Param: {ctx.obj}")
    file = find_file(ctx.obj['parameter'], ctx.obj['frequency'])
    df = load_data(file, ctx.obj['start'], ctx.obj['end'])
    random_station(file, df)

@cli.command(help="Statistics for a specific station")
@click.option('--station', required=True, help='Station name')
@click.pass_context
def statistics(ctx, station):
    click.echo(f"[statistics] Param: {ctx.obj}, Station: {station}")
    file = find_file(ctx.obj['parameter'], ctx.obj['frequency'])
    
    df = load_data(file, ctx.obj['start'], ctx.obj['end'])

    stat(df, station, file)

if __name__ == '__main__':
    cli(obj={})
