import os
import django
import xml.etree.ElementTree as ET

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qud_species_project.settings")
django.setup()

from qud_species_app.models import Skill


def to_snake_case(name):
    return name.lower().replace(" ", "_").replace("-", "_")


def import_skills(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for skill in root.findall("skill"):
        skilltree = to_snake_case(skill.get("Name"))

        for power in skill.findall("power"):
            name = power.get("Name")
            cost = int(power.get("Cost"))
            attribute = power.get("Attribute").lower()

            Skill.objects.get_or_create(
                name=name,
                defaults={
                    "skilltree": skilltree,
                    "cost": cost,
                    "attribute": attribute,
                }
            )

            print(f"Added skill: {name}")


if __name__ == "__main__":
    import_skills("Skills.xml")
