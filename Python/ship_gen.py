class ShipGenerator:
    # Ship system mappings
    SYSTEMS = {
        'O': {'name': 'Beam Weapons', 'cost': 1, 'effect': '6+ to hit, 9+ vs. small craft'},
        '∧': {'name': 'Missile Weapons', 'cost': 1, 'effect': '6+ to hit, 9+ vs. EP No vs. small craft'},  # Using unicode triangle
        'S': {'name': 'Shields', 'cost': 1, 'effect': '6+ stops beam'},
        'A': {'name': 'Armor', 'cost': 1, 'effect': '6+ stops missile'},
        'E': {'name': 'Engines', 'cost': 1, 'effect': '1 pt/engine, Speed ratio'},
        'V': {'name': 'Small Craft Bays', 'cost': 1, 'effect': 'Holds 2 small craft'},
        'D': {'name': 'Close Defense System', 'cost': 1, 'effect': '6+ vs. small craft, 10 vs. missile'},
        'C': {'name': 'Cargo', 'cost': 1, 'effect': 'holds 10 MP, 1 BP, 1 PCF, or 1/10th EP'},
        'CMD': {'name': 'Command Center', 'cost': 1, 'effect': '+1 initiative'},
        '*': {'name': 'Survey', 'cost': 1, 'effect': 'allows survey of system'},
        '?': {'name': 'ECM', 'cost': 1, 'effect': '-2 to hit ship'},
        'Sy': {'name': 'Shipyard', 'cost': 3, 'effect': 'build/repair 3 spaces ship/month'},
        'PCF': {'name': 'PCF', 'cost': 1, 'effect': '6+ to hit, ride in cargo or Aslt Shtl'}
    }

    # Small craft types
    SMALL_CRAFT = {
        'F': {'name': 'Fighter', 'weapon': 'beam', 'vs_small': 6, 'vs_ship': 9},
        'B': {'name': 'Bomber', 'weapon': 'missile', 'vs_small': 9, 'vs_ship': 6},
        'R': {'name': 'Recon', 'weapon': 'beam', 'vs_small': 9, 'vs_ship': 9},
        'Sh': {'name': 'Shuttle', 'weapon': 'beam', 'vs_small': 9, 'vs_ship': None},
        'As': {'name': 'Assault Shuttle', 'weapon': 'missile', 'vs_small': 9, 'vs_ship': 9}
    }

    # Ship class costs and sizes
    SHIP_CLASSES = {
        'Patrol Craft': {'cost': 2, 'min_size': 2, 'max_size': 2},
        'Escort': {'cost': 2, 'min_size': 2, 'max_size': 2},
        'Destroyer': {'cost': 3, 'min_size': 3, 'max_size': 3},
        'Frigate': {'cost': 3, 'min_size': 3, 'max_size': 3},
        'Cruiser': {'cost': 6, 'min_size': 6, 'max_size': 6},
        'Battleship': {'cost': 9, 'min_size': 9, 'max_size': 9},
        'Carrier': {'cost': None, 'min_size': 3, 'max_size': 12},  # Special case
        'Dreadnought': {'cost': 12, 'min_size': 12, 'max_size': 12},
        'Monitor': {'cost': 12, 'min_size': 12, 'max_size': 12},
        'Base Station': {'cost': None, 'min_size': 6, 'max_size': 24}  # Variable size
    }

    def __init__(self):
        pass

    def create_ship(self, system_string, cargo_contents=None, carrier_contents=None, name=None):
        """
        Creates a ship from a string of system symbols
        cargo_contents: string of cargo contents (e.g., 'PCF,PCF,MP,MP')
        carrier_contents: string of small craft (e.g., 'F,F,B,B')
        """
        systems = self._parse_system_string(system_string)
        
        # Validate and parse contents
        cargo_capacity = systems.get('C', 0) * 10
        carrier_capacity = systems.get('V', 0) * 2
        
        parsed_cargo = self._parse_cargo_contents(cargo_contents, cargo_capacity)
        parsed_craft = self._parse_carrier_contents(carrier_contents, carrier_capacity)
        
        # Auto-determine ship class
        ship_class = self._determine_ship_class(systems, len(system_string))
        
        # Create ship dictionary
        ship = {
            'name': name or f"Ship_{id(self)}",
            'class': ship_class,
            'systems': systems,
            'cargo': parsed_cargo,
            'small_craft': parsed_craft,
            'total_spaces': len(system_string),
            'build_cost': self._calculate_build_cost(systems),
            'maintenance_cost': self._calculate_maintenance_cost(len(system_string)),
            'combat_stats': self._calculate_combat_stats(systems)
        }
        
        return ship

    def _determine_ship_class(self, systems, total_spaces):
        """Auto-determine ship class based on composition"""
        cargo_ratio = systems.get('C', 0) / total_spaces
        carrier_ratio = systems.get('V', 0) / total_spaces
        
        if cargo_ratio >= 0.3:
            return 'Transport'
        elif carrier_ratio >= 0.3:
            return 'Carrier'
        else:
            # Determine by size
            size_classes = {
                2: 'Patrol Craft',
                3: 'Destroyer',
                6: 'Cruiser',
                9: 'Battleship',
                12: 'Dreadnought'
            }
            return size_classes.get(total_spaces, 'Base Station')

    def _parse_cargo_contents(self, cargo_contents, cargo_capacity):
        """Parse cargo contents and validate against capacity"""
        if not cargo_contents:
            return []
        cargo_items = cargo_contents.split(',')
        if len(cargo_items) > cargo_capacity:
            raise ValueError("Cargo exceeds capacity")
        return cargo_items

    def _parse_carrier_contents(self, carrier_contents, carrier_capacity):
        """Parse small craft contents and validate against capacity"""
        if not carrier_contents:
            return []
        craft_items = carrier_contents.split(',')
        if len(craft_items) > carrier_capacity:
            raise ValueError("Small craft exceeds capacity")
        return craft_items

    def generate_fleet(self, total_ep, balance_weights=None):
        """
        Generate a balanced fleet given total EP (slots)
        balance_weights: dict controlling ship type distribution
        """
        if balance_weights is None:
            balance_weights = {
                'Destroyer': 0.3,    # 30% small ships
                'Cruiser': 0.4,      # 40% medium ships
                'Battleship': 0.2,   # 20% large ships
                'Dreadnought': 0.1   # 10% capital ships
            }
        
        fleet = []
        remaining_ep = total_ep
        
        while remaining_ep >= 3:  # Minimum 3 EP for destroyer
            # Choose ship type based on weights and remaining EP
            possible_types = {k: v for k, v in balance_weights.items() 
                            if self.SHIP_CLASSES[k]['cost'] <= remaining_ep}
            
            if not possible_types:
                break
                
            ship_type = self._weighted_choice(possible_types)
            ship_size = self.SHIP_CLASSES[ship_type]['cost']
            
            # Generate a valid configuration for this ship type
            ship = self._generate_ship_configuration(ship_type)
            fleet.append(ship)
            remaining_ep -= ship_size
            
        return fleet

    def _generate_ship_configuration(self, ship_type):
        """Generate a valid ship configuration for given type"""
        size = self.SHIP_CLASSES[ship_type]['cost']
        
        # Basic templates for different ship types
        templates = {
            'Destroyer': 'SOE',
            'Cruiser': 'SAOOEE',
            'Battleship': 'SSAOO∧∧EEE',
            'Dreadnought': 'SSAAOO∧∧CMDEEEE'
        }
        
        return self.create_ship(templates[ship_type], name=f"{ship_type}_{id(self)}")

    def save_fleet(self, fleet, filename):
        """Save fleet to JSON file"""
        import json
        with open(filename, 'w') as f:
            json.dump(fleet, f, indent=2)

    def _parse_system_string(self, system_string):
        """Parse the system string into a dictionary of systems and counts"""
        systems = {}
        i = 0
        while i < len(system_string):
            # Check for multi-character systems
            if system_string[i:i+3] in ['CMD', 'PCF', 'Sy']:
                current = system_string[i:i+3]
                i += 3
            else:
                current = system_string[i]
                i += 1
            
            if current in self.SYSTEMS:
                systems[current] = systems.get(current, 0) + 1
        
        return systems

    def _weighted_choice(self, weights):
        """Choose a random key based on weights dictionary"""
        import random
        total = sum(weights.values())
        r = random.uniform(0, total)
        cumsum = 0
        for item, weight in weights.items():
            cumsum += weight
            if r <= cumsum:
                return item
        return list(weights.keys())[0]  # Fallback

    def _calculate_build_cost(self, systems):
        """Calculate total build cost of all systems"""
        return sum(self.SYSTEMS[sys]['cost'] * count for sys, count in systems.items())

    def _calculate_maintenance_cost(self, total_spaces):
        """Calculate maintenance cost (1 per 6 spaces)"""
        return max(1, total_spaces // 6)

    def _calculate_combat_stats(self, systems):
        """Calculate combat-related statistics"""
        return {
            'attack': {
                'beam': systems.get('O', 0),
                'missile': systems.get('∧', 0),
                'close_defense': systems.get('D', 0)
            },
            'defense': {
                'shields': systems.get('S', 0),
                'armor': systems.get('A', 0),
                'ecm': systems.get('?', 0)
            },
            'speed': systems.get('E', 0),
            'small_craft_capacity': systems.get('V', 0) * 2,
            'cargo_capacity': systems.get('C', 0) * 10,
            'command_bonus': 1 if systems.get('CMD', 0) > 0 else 0,
            'can_survey': systems.get('*', 0) > 0,
            'shipyard_capacity': systems.get('Sy', 0) * 3
        }