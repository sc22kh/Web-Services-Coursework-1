from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Creature, Mutation, Skill, Anatomy, BodyPart, BodyPartCount

class QudSpeciesTestSuite(APITestCase):

    def setUp(self):
        # Setup User for Authenticated Routes
        self.user = User.objects.create_user(username='admin', password='password123')
        
        # Setup Base Data
        self.mutation = Mutation.objects.create(
            name="Flaming Ray", internal_name="FlamingRay", type="physical", cost=4
        )
        self.skill = Skill.objects.create(
            name="Axe Proficiency", internal_name="Axe_Prof", cost=100, 
            skilltree="axe", attribute="strength"
        )
        
        # Setup Anatomy & BodyParts
        self.head = BodyPart.objects.create(part_name="Head", integral=True, mortal=True)
        self.anatomy = Anatomy.objects.create(name="Humanoid")
        self.part_count = BodyPartCount.objects.create(
            anatomy=self.anatomy, body_part=self.head, count=1
        )

        # Setup Initial Creatures (Variety for Analytics)
        self.creature = Creature.objects.create(
            name="Snapjaw Scavenger", type="tier_1", hitpoints=15, level="2",
            strength="18,1d3", species="Snapjaw", anatomy=self.anatomy
        )
        # Add Many-to-Many data to the first creature
        self.creature.mutations.add(self.mutation)
        self.creature.skills.add(self.skill)

        Creature.objects.create(
            name="Snapjaw Warlord", type="tier_3", hitpoints=45, level="10",
            strength="24,1d4", species="Snapjaw", anatomy=self.anatomy
        )
        Creature.objects.create(
            name="Dromad Merchant", type="merchants", hitpoints=100, level="15",
            strength="20,1d2", species="Dromad", anatomy=self.anatomy
        )
        Creature.objects.create(
            name="Meh-Amet", type="npc", hitpoints=200, level="30",
            strength="30,2d6", species="Seeker", anatomy=self.anatomy
        )

        self.list_url = reverse('creature-list')

    # UNIT TESTS

    def test_model_string_representations(self):
        # Verifies that __str__ methods work for documentation clarity.
        self.assertEqual(str(self.creature), "Snapjaw Scavenger")
        self.assertEqual(str(self.mutation), "Flaming Ray")
        self.assertIn("1 x Head", str(self.part_count))

    def test_anatomy_relationship_logic(self):
        # Verifies the through-table relationship between Anatomy and BodyParts.
        self.assertEqual(self.anatomy.parts.count(), 1)
        self.assertEqual(self.anatomy.parts.first().part_name, "Head")

    # SECURITY AND INTEGRATION TESTS

    def test_creature_create_security(self):
        # Test Security: Unauthenticated users must be blocked from POSTing.
        data = {"name": "Hacker Bot", "type": "tier_1"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_can_create_creature(self):
        # Verify that an authenticated admin can successfully POST a new creature.
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "Salt-Hopper",
            "type": "tier_2",
            "hitpoints": 25,
            "level": "4",
            "strength": "16", "agility": "20", "toughness": "14",
            "intelligence": "10", "willpower": "10", "ego": "10",
            "species": "Insect"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Creature.objects.count(), 5) 

    def test_creature_delete_authenticated(self):
        # Test CRUD: Admin can DELETE an existing creature.
        self.client.force_authenticate(user=self.user)
        url = reverse('creature-detail', args=[self.creature.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # ANALYTICS AND FILTERING TESTS

    def test_summary_stats_logic(self):
        # Verify the custom @action returns accurate species counts.
        url = reverse('creature-summary-stats')
        response = self.client.get(url)
        snapjaw_data = next(item for item in response.data['by_species'] if item['species'] == 'Snapjaw')
        self.assertEqual(snapjaw_data['count'], 2)

    def test_stat_averages_per_type(self):
        # Check that power-level averages group correctly by type/tier.
        url = reverse('creature-stat-averages-per-type')
        response = self.client.get(url)
        tier_1 = next(item for item in response.data if item['type'] == 'tier_1')
        self.assertEqual(tier_1['avg_hp'], 15.0)

    def test_attribute_sorting_complex_values(self):
        # Verifies that the custom SQL Cast handles Qud's '18,1d3' attribute strings.
        # Sorting by strength_base (ascending)
        response = self.client.get(self.list_url, {'ordering': 'strength_base'})
        # Snapjaw Scavenger (18) should come before Meh-Amet (30)
        names = [item['name'] for item in response.data]
        self.assertTrue(names.index("Snapjaw Scavenger") < names.index("Meh-Amet"))