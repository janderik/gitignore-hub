#!/usr/bin/env python3
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()
TEMPLATES_DIR = Path(__file__).parent / 'templates'

def list_templates():
    return [f.stem for f in sorted(TEMPLATES_DIR.glob('*.txt'))] if TEMPLATES_DIR.exists() else []

def get_template(name):
    p = TEMPLATES_DIR / f'{name}.txt'
    return p.read_text(encoding='utf-8') if p.exists() else None

def merge_templates(names):
    sections = []
    for name in names:
        content = get_template(name)
        if content:
            sections.append(content)
        else:
            console.print(f'[yellow]Template not found: {name}[/yellow]')
    return '\n\n'.join(sections)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('templates', nargs=-1)
@click.option('-o', '--output', default='.gitignore')
@click.option('-a', '--all', 'use_all', is_flag=True)
def generate(templates, output, use_all):
    content = get_template('all') if use_all else merge_templates(templates) if templates else None
    if not content:
        console.print('[red]Specify templates or use --all[/red]')
        return
    with open(output, 'w', encoding='utf-8') as f:
        f.write(content)
    console.print(f'[green]Generated {output} ({len(content.splitlines())} lines)[/green]')

@cli.command('list')
def list_cmd():
    table = Table(title='Available Templates')
    table.add_column('Template', style='cyan')
    descs = {'python': 'Python', 'node': 'Node.js', 'docker': 'Docker', 'java': 'Java', 'go': 'Go', 'rust': 'Rust', 'react': 'React', 'terraform': 'Terraform', 'aws': 'AWS', 'vscode': 'VS Code', 'flask': 'Flask', 'fastapi': 'FastAPI', 'kubernetes': 'Kubernetes', 'os-files': 'OS files'}
    for t in sorted(list_templates()):
        table.add_row(t, descs.get(t, ''))
    console.print(table)

if __name__ == '__main__':
    cli()
