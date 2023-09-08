import shutil
import click
import pathlib
from pathlib import Path
import json
import jinja2
import os

@click.command()
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))

def main(input_dir):
    #1. Read configuration file (e.g., hello/config.json)
    input_dir = pathlib.Path(input_dir)
    print(f"DEBUG input_dir={input_dir}")
    config_file_path = Path(input_dir / "config.json")
    with open(config_file_path, "r") as config_file:
        config_data = json.load(config_file)
    
    #2. Render templates
    template_dir = input_dir / 'templates'
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(template_dir)),
        autoescape=jinja2.select_autoescape(['html', 'xml']),
        )
    for config_item in config_data:
        #2.1)Read template(e.g.,hello/templates/index.html)
        template = template_env.get_template(config_item["template"])

        #2.2)Render template with context
        rendered_template = template.render(config_item["context"])

        #2.3)Write the rendered template to an output file
        url = config_item["url"].lstrip("/")  
        output_dir = input_dir/"html"
        output_path = output_dir/url/"index.html"
        if not output_dir.exists():
            output_dir.mkdir()
        with open(output_path, "w") as output_file:
            output_file.write(rendered_template)

    #3. Copy static directory:hello_css/static to hello_css/html
    static_sub_dir = input_dir /'static'
    print(static_sub_dir)
    print(output_dir)
    if static_sub_dir.exists():
        shutil.copytree(static_sub_dir, output_dir, dirs_exist_ok=True)
    

    


if __name__ == "__main__":
    main()
