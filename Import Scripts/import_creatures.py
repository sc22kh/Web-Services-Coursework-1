import os
import re
import xml.etree.ElementTree as ET
from django.db import transaction
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qud_species_project.settings")
django.setup()

from qud_species_app.models import Creature, Anatomy, Mutation, Skill

XML_FILE = "Creatures.XML"

TYPE_MAPPING = {
    "Base creature objects": "base_creature",
    "Tier 1 creatures": "tier_1",
    "Tier 2 creatures": "tier_2",
    "Tier 3 creatures": "tier_3",
    "Tier 4 creatures": "tier_4",
    "Tier 5 creatures": "tier_5",
    "Tier 6 creatures": "tier_6",
    "Tier 7 creatures": "tier_7",
    "Tier 8 creatures": "tier_8",
    "Tier X creatures": "tier_x",
    "Merchants": "merchants",
    "NPCs": "npc",
}


def clean_xml(xml_file):
    with open(xml_file, "r", encoding="utf-8", errors="ignore") as f:
        data = f.read()

    data = re.sub(r'&#(0|[1-8]|11|12|1[4-9]|2[0-9]|3[0-1]);', '', data)

    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    return ET.fromstring(data, parser=parser)


def detect_type(comment):
    comment = (comment or "").strip()
    for key, val in TYPE_MAPPING.items():
        if key in comment:
            return val
    return None


def parse_creatures(root):

    creatures = {}
    current_type = "base_creature"

    for elem in root:

        if elem.tag is ET.Comment:
            new_type = detect_type(elem.text)
            if new_type:
                current_type = new_type
            continue

        if elem.tag != "object":
            continue

        name = elem.attrib.get("Name")
        inherits = elem.attrib.get("Inherits")

        stats = {}
        tags = {}
        mutations = []
        skills = []

        for child in elem:

            if child.tag == "stat":

                stat_name = child.attrib.get("Name")
                val = child.attrib.get("Value") or child.attrib.get("sValue")

                if stat_name and val:
                    stats[stat_name.lower()] = val

            elif child.tag == "tag":

                tag_name = child.attrib.get("Name")
                val = child.attrib.get("Value")

                if tag_name and val:
                    tags[tag_name.lower()] = val

            elif child.tag == "part":

                # Faction extraction
                faction_str = child.attrib.get("Factions")
                if faction_str:
                    faction = faction_str.split("-")[0]
                    tags["faction"] = faction

                # Anatomy extraction
                anatomy = child.attrib.get("Anatomy")
                if anatomy:
                    tags["anatomy"] = anatomy

            elif child.tag == "mutation":

                internal = child.attrib.get("Name") or child.attrib.get("Class")
                if internal:
                    mutations.append(internal)

            elif child.tag == "skill":

                skill_name = child.attrib.get("Name")
                if skill_name:
                    skills.append(skill_name)

        creatures[name] = {
            "type": current_type,
            "inherits": inherits,
            "stats": stats,
            "tags": tags,
            "mutations": mutations,
            "skills": skills,
        }

    return creatures


def resolve_inheritance(creatures):

    resolved = {}

    def build(name):

        if name in resolved:
            return resolved[name]

        data = creatures[name]

        stats = dict(data["stats"])
        tags = dict(data["tags"])

        parent_name = data["inherits"]

        if parent_name and parent_name in creatures:

            parent = build(parent_name)

            for k, v in parent["stats"].items():
                stats.setdefault(k, v)

            for k, v in parent["tags"].items():
                tags.setdefault(k, v)

        result = {
            "type": data["type"],
            "stats": stats,
            "tags": tags,
            "mutations": data["mutations"],
            "skills": data["skills"],
        }

        resolved[name] = result
        return result

    for name in creatures:
        build(name)

    return resolved


def create_db_entries(resolved):

    created = {}

    for name, data in resolved.items():

        stats = data["stats"]
        tags = data["tags"]

        creature = Creature.objects.create(
            name=name,
            type=data["type"],

            strength=str(stats.get("strength", "")),
            agility=str(stats.get("agility", "")),
            toughness=str(stats.get("toughness", "")),
            intelligence=str(stats.get("intelligence", "")),
            willpower=str(stats.get("willpower", "")),
            ego=str(stats.get("ego", "")),

            hitpoints=int(stats.get("hitpoints", 0)),
            av=int(stats.get("av", 0)),
            dv=int(stats.get("dv", 0)),

            level=str(stats.get("level", "")),

            heat_resistance=int(stats.get("heatresistance", 0)),
            cold_resistance=int(stats.get("coldresistance", 0)),
            electric_resistance=int(stats.get("electricresistance", 0)),
            acid_resistance=int(stats.get("acidresistance", 0)),

            species=tags.get("species", ""),
            faction=tags.get("faction", ""),

            anatomy=Anatomy.objects.filter(
                name=tags.get("anatomy")
            ).first() if tags.get("anatomy") else None
        )

        mut_objs = []

        for m in data["mutations"]:
            try:
                mut_objs.append(Mutation.objects.get(internal_name=m))
            except Mutation.DoesNotExist:
                print("Missing mutation:", m)

        creature.mutations.set(mut_objs)

        skill_objs = []

        for s in data["skills"]:
            obj, _ = Skill.objects.get_or_create(name=s, defaults={"cost": 0})
            skill_objs.append(obj)

        creature.skills.set(skill_objs)

        created[name] = creature

    return created


@transaction.atomic
def import_creatures():

    root = clean_xml(XML_FILE)

    parsed = parse_creatures(root)

    resolved = resolve_inheritance(parsed)

    created = create_db_entries(resolved)

    print("Imported", len(created), "creatures")


if __name__ == "__main__":
    import_creatures()
