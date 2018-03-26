from collections import namedtuple
from recordclass import recordclass

# Constants
BASE_HP = 10

BODY_LOCATIONS = 'total head torso larm lhand rarm rhand lleg lfoot rleg rfoot'.split(' ')
BODY_INDEX = dict()
for i, loc in enumerate(BODY_LOCATIONS):
    BODY_INDEX[loc] = i

# Profile - Name, Weight, Height, Description, Pronouns
    # NAME         The name of the character
    # WEIGHT       The weight of the character
    # HEIGHT       The height of the character
    # DESCRIPTION  The description of the character
    # PRONOUNS     The pronouns used by the character (e.g. he/him/his)
Profile = recordclass('Profile', 'name weight height description pronouns'.split(' '))
# AbilityScores - Strength, Dexterity, Constitution, Intelligence, Charisma
    # STRENGTH      represents physical power and impacts damage dealt with melee weapons
    # DEXTERITY     represents kinesthetic skill and impacts dodging and accuracy
    # CONSTITUTION  represents toughness and impacts how much damage can be taken
    # INTELLIGENCE  represents... intelligence and impacts decision making
    # CHARISMA      represents conversational skill and impacts ability to persuade others
AbilityScores = recordclass('AbilityScores', 'strength dexterity constitution intelligence charisma'.split(' '))
# Weapons - Main, Secondary, Ranged, Ammo
    # MAIN       The primary weapon used by this character
    # SECONDARY  The secondary weapon used by this character
    # RANGED     The ranged weapon used by this character
    # AMMO       How much ammo the character has for his/her ranged weapon
Weapons = recordclass('Weapons', 'main secondary ranged ammo'.split(' '))
# Skills - TBD
# Armor - Head, Torso, Arms, Hands, Legs, Feet
    # HEAD   The armor worn on the head
    # TORSO  The armor worn on the torso
    # ARMS   The armor worn on the arms
    # HANDS  The armor worn on the hands
    # LEGS   The armor worn on the legs
    # FEET   The armor worn on the feet
Armor = recordclass('Armor', 'head torso arms hands legs feet'.split(' '))
# Hitpoints - Head, Torso, Neck, LArm, LHand, RArm, RHand, Waist, LLeg, LFoot, RLeg, RFoot
Hitpoints = recordclass('hitpoints', BODY_LOCATIONS)

class Tribute:
    """
    The tribute class represents an entity that is participating
    in the Hunger Games. Tributes have stats (Str, Dex, Con, etc.)
    and equipment (Weapons, Armor, etc.). A tribute enters the Hunger
    Games without any equipment, unless otherwise specified.
    """
    def __init__(self, profile, ability_scores, weapons, armor, hitpoints):
        self.profile = profile
        self.ability_scores = ability_scores
        self.weapons = weapons
        self.armor = armor
        self.max_hitpoints = self._calc_hitpoints()
        self.hitpoints = self.max_hitpoints

    def __str__(self):
        return "%s\n%s\n%s\n%s\n%s" % (str(self.profile),
                                       str(self.ability_scores),
                                       str(self.weapons),
                                       str(self.armor),
                                       str(self.hitpoints))

    def __getitem__(self, position):
        return self.hitpoints[position]

    def __setitem__(self, position, value):
        self.hitpoints[position] = value
    
    def __len__(self):
        return len(self.hitpoints)

    def _calc_hitpoints(self):
        """
        Determines the max hitpoints of each of the character's body parts
        """
        head = self._calc_hp(0, 4, 1)
        torso = self._calc_hp(1.5, 3, 2)
        arms = self._calc_hp(1, 2, 1.5)
        hands = self._calc_hp(0, 2, 1)
        legs = self._calc_hp(1, 3, 1.5)
        feet = self._calc_hp(0, 2, 1)
        total = sum([head, torso, arms * 2, hands * 2, legs * 2, feet * 2]) / 4
        return Hitpoints( total, head, torso, arms, hands, arms, hands, legs, feet, legs, feet )
    
    def _calc_hp(self, str_mult, con_mult, base_mult):
        return int(self.ability_scores.strength * str_mult + self.ability_scores.constitution * con_mult + BASE_HP * base_mult)

    def _is_alive(self):
        return self.hitpoints.total > 0 and \
               self.hitpoints.head > 0 and \
               self.hitpoints.torso > 0

    def take_damage(self, amount, locations):
        for location in locations:
            self[BODY_INDEX[location]] = max(self[BODY_INDEX[location]] - amount, 0)
            self[0] = max(self[0] - amount, 0)
            if not self._is_alive():
                print("%s is dead!" % self.profile.name)
                break
            else:
                print("%s hitpoints: %d" % (location, self[BODY_INDEX[location]]))
                print("%s hitpoints: %d" % ('total', self[0]))

        

donny = Tribute( Profile("Donny Dingle", 180, 72, "An accomplished warrior.", "he/him/his".split('/') ),
                 AbilityScores(16, 12, 16, 8, 10),
                 Weapons("fists", "fists", "fists", 69),
                 Armor("leather", "steel", "leather", "leather", "steel", "steel"),
                 Hitpoints(100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100) )

print( '\n' + str(donny) )
donny.take_damage(18, 'head larm rarm lleg torso'.split(' '))
