from django.db import models

class Creature(models.Model):

    TYPE_CHOICES = [
        ("base_creature", "Base creature objects"),
        ("tier_1", "Tier 1 creatures"),
        ("tier_2", "Tier 2 creatures"),
        ("tier_3", "Tier 3 creatures"),
        ("tier_4", "Tier 4 creatures"),
        ("tier_5", "Tier 5 creatures"),
        ("tier_6", "Tier 6 creatures"),
        ("tier_7", "Tier 7 creatures"),
        ("tier_8", "Tier 8 creatures"),
        ("tier_x", "Tier X creatures"),
        ("merchants", "Merchants"),
        ("npc", "NPCs"),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    # Combat stats
    av = models.IntegerField(null=True, blank=True)
    dv = models.IntegerField(null=True, blank=True)
    hitpoints = models.IntegerField(null=True, blank=True)
    level = models.CharField(max_length=50)

    # Attributes
    strength = models.CharField(max_length=50)
    agility = models.CharField(max_length=50)
    toughness = models.CharField(max_length=50)
    intelligence = models.CharField(max_length=50)
    willpower = models.CharField(max_length=50)
    ego = models.CharField(max_length=50)

    # Resistances
    heat_resistance = models.IntegerField(null=True, blank=True)
    cold_resistance = models.IntegerField(null=True, blank=True)
    electric_resistance = models.IntegerField(null=True, blank=True)
    acid_resistance = models.IntegerField(null=True, blank=True)

    # Species and Faction
    species = models.CharField(max_length=50, blank=True) # Mod friendly
    faction = models.CharField(max_length=50, blank=True) # Mod friendly

    # Relationships
    anatomy = models.ForeignKey(
        "Anatomy",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    mutations = models.ManyToManyField("Mutation", blank=True)
    skills = models.ManyToManyField("Skill", blank=True)

    def __str__(self):
        return self.name

class Mutation(models.Model):

    TYPE_CHOICES = [
        ("morphotypes", "Morphotypes"),
        ("physical", "Physical"),
        ("physical_defect", "Physical Defect"),
        ("mental", "Mental"),
        ("mental_defect", "Mental Defect")
    ]

    name = models.CharField(max_length=100, unique=True)
    internal_name = models.CharField(max_length=100, unique=True)
    cost = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name

class BodyPart(models.Model):

    part_name = models.CharField(max_length=100, unique=True)
    integral = models.BooleanField(default=False)
    appendage = models.BooleanField(default=False)
    plural = models.BooleanField(default=False)
    mortal = models.BooleanField(default=False)

    usually_on = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.SET_NULL, related_name="subparts"
    )
    requires_part = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.SET_NULL, related_name="required_by"
    )

    def __str__(self):
        return self.part_name

class Anatomy(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parts = models.ManyToManyField(
        BodyPart, through='BodyPartCount', related_name="anatomies"
    )

    def __str__(self):
        return self.name

class BodyPartCount(models.Model):
    anatomy = models.ForeignKey(Anatomy, on_delete=models.CASCADE)
    body_part = models.ForeignKey(BodyPart, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('anatomy', 'body_part')
    
    def __str__(self):
        return f"{self.count} x {self.body_part.part_name} in {self.anatomy.name}"

class Skill(models.Model):
    SKILLTREE_CHOICES = [
        ("acrobatics", "Acrobatics"),
        ("axe", "Axe"),
        ("bow_and_rifle", "Bow and Rifle"),
        ("cooking_and_gathering", "Cooking and Gathering"),
        ("cudgel", "Cudgel"),
        ("customs_and_folklore", "Customs and Folklore"),
        ("endurance", "Endurance"),
        ("heavy_weapon", "Heavy Weapon"),
        ("long_blade", "Long Blade"),
        ("multiweapon_fighting", "Multiweapon Fighting"),
        ("persuasion", "Persuasion"),
        ("physic", "Physic"),
        ("pistol", "Pistol"),
        ("self_discipline", "Self-discipline"),
        ("shield", "Shield"),
        ("short_blade", "Short Blade"),
        ("single_weapon_fighting", "Single Weapon Fighting"),
        ("tactics", "Tactics"),
        ("tinkering", "Tinkering"),
        ("wayfaring", "Wayfaring"),
        ("nonlinearity", "Nonlinearity"),
    ]

    ATTRIBUTE_CHOICES = [
        ("strength", "Strength"),
        ("agility", "Agility"),
        ("toughness", "Toughness"),
        ("willpower", "Willpower"),
        ("intelligence", "Intelligence"),
        ("ego", "Ego"),
    ]
    
    skilltree = models.CharField(
        max_length=100,
        choices=SKILLTREE_CHOICES,
        help_text="The skill tree/category this skill belongs to"
    )
    name = models.CharField(max_length=100, unique=True)
    internal_name = models.CharField(max_length=100, unique=True)
    cost = models.PositiveIntegerField()
    attribute = models.CharField(
        max_length=50,
        choices=ATTRIBUTE_CHOICES,
        help_text="Primary attribute this skill is associated with"
    )

    def __str__(self):
        return self.name