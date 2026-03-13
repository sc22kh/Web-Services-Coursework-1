import os
import django
import xml.etree.ElementTree as ET
from django.db import transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qud_species_project.settings")
django.setup()

from qud_species_app.models import Mutation

XML_FILE = "Mutations.XML"

# Map XML category names to Mutation.type choices
CATEGORY_TYPE_MAP = {
    "Physical": "physical",
    "PhysicalDefects": "physical_defect",
    "Mental": "mental",
    "Morphotypes": "morphotypes",
}

def parse_mutations_xml(xml_file):
    # Read XML safely, ignoring invalid chars
    with open(xml_file, "r", encoding="utf-8", errors="ignore") as f:
        data = f.read()

    root = ET.fromstring(data)  # <mutations>
    created_mutations = []

    for category in root.findall("category"):
        cat_name = category.attrib.get("Name", "")
        mutation_type = CATEGORY_TYPE_MAP.get(cat_name, "physical")

        for mut_elem in category.findall("mutation"):
            name = mut_elem.attrib.get("Name")
            internal_name = mut_elem.attrib.get("Class")
            cost = mut_elem.attrib.get("Cost")
            if cost is not None:
                try:
                    cost = int(cost)
                except ValueError:
                    cost = None

            if internal_name:  # Must have a class to insert
                m, created = Mutation.objects.update_or_create(
                    internal_name=internal_name,  # lookup by unique internal_name
                    defaults={
                        "name": name,
                        "cost": cost,
                        "type": mutation_type
                    }
                )
                created_mutations.append(m)

    return created_mutations

@transaction.atomic
def import_mutations():
    mutations = parse_mutations_xml(XML_FILE)
    print(f"Imported {len(mutations)} mutations.")

if __name__ == "__main__":
    import_mutations()
