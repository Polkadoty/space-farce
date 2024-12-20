from ship_gen import ShipGenerator

generator = ShipGenerator()

# Test basic ship creation
destroyer = generator.create_ship('SOE', name='DD1')
print(f"Destroyer stats: {destroyer}")

# Test carrier with small craft
carrier = generator.create_ship('VVVEE', carrier_contents='F,F,B,B,F,F', name='CV1')
print(f"Carrier stats: {carrier}")

# Test fleet generation
fleet = generator.generate_fleet(50)
generator.save_fleet(fleet, 'Python/output-tests/fleet2.json')