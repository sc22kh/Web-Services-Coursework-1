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
            internal_name = power.get("Class")  # <-- set internal_name from XML

            Skill.objects.get_or_create(
                name=name,
                defaults={
                    "skilltree": skilltree,
                    "cost": cost,
                    "attribute": attribute,
                    "internal_name": internal_name,
                }
            )

            print(f"Added skill: {name} ({internal_name})")


if __name__ == "__main__":
    import_skills("Skills.xml")
