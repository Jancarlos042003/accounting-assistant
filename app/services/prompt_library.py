from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class PromptLibrary:
    def __init__(self):
        # Calcula la ruta absoluta del directorio "prompts" dentro del proyecto
        base_dir = Path(__file__).resolve().parent.parent / "prompts"
        self.env = Environment(loader=FileSystemLoader(str(base_dir)))

    def render(self, template_name: str, **kwargs):
        template = self.env.get_template(template_name)
        return template.render(**kwargs)
