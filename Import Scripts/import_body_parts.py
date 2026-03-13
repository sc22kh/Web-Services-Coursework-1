import os
import django
import xml.etree.ElementTree as ET

# --- Django setup ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qud_species_project.settings")
django.setup()

from qud_species_app.models import BodyPart

# --- Main import function ---
def import_body_parts(xml_path="Bodies.xml"):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    created = {}

    # --- Base body parts ---
    for elem in root.find("bodyparttypes"):
        part_name = elem.get("Type")
        part = BodyPart.objects.create(
            part_name=part_name,
            integral=elem.get("Integral", "false").lower() == "true",
            appendage=elem.get("Appendage", "false").lower() == "true",
            plural=elem.get("Plural", "false").lower() == "true",
            mortal=elem.get("Mortal", "false").lower() == "true",
        )
        created[part_name] = part

    # --- Link UsuallyOn ---
    for elem in root.find("bodyparttypes"):
        part_name = elem.get("Type")
        usually_on = elem.get("UsuallyOn")
        if usually_on and usually_on in created:
            part = created[part_name]
            part.usually_on = created[usually_on]
            part.save()

    # --- Variants ---
    for elem in root.find("bodyparttypevariants"):
        name = elem.get("Type")
        base_name = elem.get("VariantOf")
        base_part = created.get(base_name)

        if not base_part:
            print(f"Base part '{base_name}' for variant '{name}' not found")
            continue

        # inherit from base
        integral = base_part.integral
        appendage = base_part.appendage
        plural = base_part.plural
        mortal = base_part.mortal
        usually_on = base_part.usually_on

        # override with variant XML if specified
        plural = elem.get("Plural", str(plural)).lower() == "true"

        part = BodyPart.objects.create(
            part_name=name,
            integral=integral,
            appendage=appendage,
            plural=plural,
            mortal=mortal,
            usually_on=usually_on,
            requires_part=base_part,
        )
        created[name] = part

    print("Body parts imported successfully")

if __name__ == "__main__":
    import_body_parts()
