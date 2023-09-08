import shutil
import click
import pathlib
from pathlib import Path
import json
import jinja2
import sys

@click.command()
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))
@click.option('-o', '--output', 'output_dir', type=click.Path(), help='Output directory.')
@click.option('-v', '--verbose', is_flag=True, help='Print more output.')

def main(input_dir, output_dir, verbose):
    """Templated static website generator."""
    input_dir = pathlib.Path(input_dir)
    try:
        if output_dir and Path(output_dir).exists():
            raise FileExistsError(f"Error: '{output_dir}' already exists.")
        print(f"DEBUG input_dir={input_dir}")



        #1. Read configuration file (e.g., hello/config.json)
        config_file_path = Path(input_dir / "config.json")
        if not config_file_path.exists():
            raise FileNotFoundError(f"{config_file_path} not found")
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
            if not output_dir:
                output_dir = input_dir/"html"
            else:
                output_dir = pathlib.Path(output_dir)
            url = config_item["url"].lstrip("/")  
            output_path = output_dir/url/"index.html"
            if not output_dir.exists():
                output_dir.mkdir()
            with open(output_path, "w") as output_file:
                output_file.write(rendered_template)                

        #3. Copy static directory:hello_css/static to hello_css/html
        static_sub_dir = input_dir /'static'
        if static_sub_dir.exists():
            shutil.copytree(static_sub_dir, output_dir, dirs_exist_ok=True)
            if(verbose):
                print(f"Copied {static_sub_dir} -> {output_dir}")
                print("Rendered " + str(config_item["template"]) + " -> " + str(output_path))
    
    except FileExistsError as err:
        sys.exit(f"Error: {err}")
    except FileNotFoundError as err:
        sys.exit(f"Error: {err}")
    except jinja2.exceptions.TemplateError as err:
        sys.exit("Error: '" + str(config_item["template"]) + "'\n{err}")
    except json.decoder.JSONDecodeError as err:
        sys.exit(f"Error: '{config_file_path}'\n{err}")
    


if __name__ == "__main__":
    main()
