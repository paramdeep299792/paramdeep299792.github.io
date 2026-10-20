import json
import jinja2
from pathlib import Path
import argparse
import sys
import logging
import subprocess
import shutil

from .core.utils.general import exception_handler
from .core.utils.logging_config import setup_logging

logger = logging.getLogger(__name__)

def main(args: argparse.Namespace) -> None:
    try:
        cv = args.cv
        website = args.website
        bio = args.bio

        if cv:
            src_dir = Path(__file__).resolve().parent
            root_dir = src_dir.parent

            # 1. Load the JSON data
            with open(root_dir / 'params.json', 'r') as f:
                data = json.load(f)

            templates_dir = root_dir / 'src' / 'templates'

            setup_logging(
                log_file=root_dir / "build.log",
                reset_log=True
            )
            
            # 2. Configure Jinja2
            latex_jinja_env = jinja2.Environment(
                block_start_string=r'\BLOCK{',
                block_end_string='}',
                variable_start_string=r'\VAR{',
                variable_end_string='}',
                comment_start_string=r'\#{',
                comment_end_string='}',
                trim_blocks=True,
                autoescape=False,
                loader=jinja2.FileSystemLoader(templates_dir)
            )

            template = latex_jinja_env.get_template('cv.tex')
            rendered_tex = template.render(data)

            with open(root_dir / 'main.tex', 'w') as f:
                f.write(rendered_tex)

            output_dir = root_dir / "tmp"
            output_dir.mkdir(exist_ok=True)

            final_destination = root_dir / "docs" / "assets" / "CV.pdf"

            try:
                subprocess.run(
                    [
                        "latexmk",
                        "-pdf",
                        "-interaction=nonstopmode",
                        "-jobname=CV",
                        f"-outdir={output_dir}",
                        str(root_dir / "main.tex")
                    ], 
                    cwd=root_dir, 
                    check=True
                )
                source_pdf = output_dir / "CV.pdf"
    
                if source_pdf.exists():
                    shutil.copy2(source_pdf, final_destination)
                    logger.info(f"Success! PDF copied to {final_destination}")
            finally:
                subprocess.run(
                    [
                        "latexmk",
                        "-c",
                        "-jobname=CV",
                        f"-outdir={output_dir}",
                        str(root_dir / "main.tex")
                    ], 
                    cwd=root_dir, 
                    check=False
                )

            logger.info("Resume generated successfully!")

        if website:
            src_dir = Path(__file__).resolve().parent
            root_dir = src_dir.parent
            setup_logging(
                log_file=root_dir / "build.log"
            )

            templates_dir = root_dir / 'src' / 'templates'
            docs_dir = root_dir / 'docs'
            docs_dir.mkdir(exist_ok=True)

            with open(root_dir / 'params.json', 'r') as f:
                data = json.load(f)

            md_jinja_env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(templates_dir),
                trim_blocks=True,
                lstrip_blocks=True,
                autoescape=False
            )

            pages = {
                'index.md': 'index.md',
                'experience.md': 'experience.md',
                'projects.md': 'projects.md',
                'achievements.md': 'achievements.md',
                'references.md': 'references.md'
            }

            for template_name, output_name in pages.items():
                template = md_jinja_env.get_template(template_name)
                rendered_md = template.render(data)
                
                output_path = docs_dir / output_name
                with open(output_path, 'w') as f:
                    f.write(rendered_md)
                    
                logger.info(f"Generated: docs/{output_name}")

            logger.info("MkDocs Markdown generation complete!")

        if bio:
            src_dir = Path(__file__).resolve().parent
            root_dir = src_dir.parent
            json_filename = root_dir / 'params.json'
            output_filename = root_dir / 'outputs' / 'bio.txt'
            
            try:
                data = load_data(json_filename)
            except FileNotFoundError:
                logger.error(f"Error: Please ensure your JSON data is saved as '{json_filename}' in the same directory.")
                return
            except json.JSONDecodeError:
                logger.error("Error: The JSON file is improperly formatted.")
                return

            github_readme = generate_github_readme(data)
            social_bios = generate_social_bios(data)
            linkedin_about = generate_linkedin_about(data)
            
            final_output = (
                "================ GITHUB PROFILE README ================\n\n" +
                github_readme +
                "\n\n================ SOCIAL MEDIA BIOS ================\n\n" +
                social_bios +
                "\n\n================ LINKEDIN SECTION ================\n\n" +
                linkedin_about
            )
            
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(final_output)
                
            logger.info(f"Success! Your profiles have been generated and saved to '{output_filename}'.")
    except Exception as e:
        exception_handler(e)

def cli() -> None:
    parser = argparse.ArgumentParser(
        description="This script is used to build the portfolio from params.json file. You must provide a valid flag to run."
    )

    parser.add_argument("-website", "--website", action="store_true", help="To create the website.")
    parser.add_argument("-cv", "--cv", action="store_true", help="To create CV.")
    parser.add_argument("-bio", "--bio", action="store_true", help="To create bio.")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    main(args)
    
if __name__ == "__main__":
    cli()