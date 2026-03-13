import os
import django
import xml.etree.ElementTree as ET

# --- Django setup ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qud_species_project.settings")
django.setup()

from qud_species_app.models import Anatomy, BodyPart, BodyPartCount

# --- Flatten function ---
def flatten_parts(elem):
    """
    Yields BodyPart names from a <part> element and its children.
    Just grabs the 'Type' attribute.
    """
    part_type = elem.get("Type")
    if part_type:
        yield part_type
    for child in elem.findall("part"):
        yield from flatten_parts(child)

# --- Main import ---
def import_anatomies(xml_path="Bodies.xml"):
    tree = ET.parse(xml_path)
    root = tree.getroot()  # root should be <anatomies>

    # Use relative path to find all direct <anatomy> children
    for anatomy_elem in root.findall("./anatomies/anatomy"):

        name = anatomy_elem.get("Name")
        if not name:
            continue

        print(f"Importing Anatomy: {name}")
        anatomy, _ = Anatomy.objects.get_or_create(name=name)

        # Count how many of each BodyPart appear
        part_counts = {}
        for part_elem in anatomy_elem.findall("part"):
            for part_name in flatten_parts(part_elem):
                part_counts[part_name] = part_counts.get(part_name, 0) + 1

        # Create BodyPartCount entries
        for part_name, count in part_counts.items():
            body_part = BodyPart.objects.filter(part_name=part_name).first()
            if not body_part:
                print(f"Warning: BodyPart '{part_name}' not found for anatomy '{name}'")
                continue

            BodyPartCount.objects.update_or_create(
                anatomy=anatomy,
                body_part=body_part,
                defaults={"count": count}
            )

    print("Anatomies imported successfully!")

if __name__ == "__main__":
    import_anatomies()
