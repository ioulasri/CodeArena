-- Migration: Add sample fields and seed beautiful new puzzles
BEGIN;

-- Add sample_input and sample_output columns to puzzles table
ALTER TABLE puzzles ADD COLUMN IF NOT EXISTS sample_input TEXT;
ALTER TABLE puzzles ADD COLUMN IF NOT EXISTS sample_output TEXT;

-- Clear existing test puzzles and add new narrative-rich ones
DELETE FROM puzzles;

-- Day 6: The Sky Islands Navigator
INSERT INTO puzzles (day, title, description, story, sample_input, sample_output, difficulty, generator_type, generator_params)
VALUES
(6, 'The Sky Islands Navigator',
 E'# The Challenge\n\n'
 'You are a sky sailor navigating between floating islands connected by magical portals. Each portal has an energy cost to traverse. Your airship starts at **Island 1** and needs to reach the **final island**.\n\n'
 '## Input Format\n'
 'First line: `N P` where N is the number of islands and P is the number of portals\n'
 'Next P lines: `from_island to_island energy_cost`\n\n'
 '## Your Mission\n'
 'Find the **minimum total energy** needed to travel from Island 1 to Island N.\n'
 'If no path exists, return **-1**.\n\n'
 '## Example Explained\n'
 'With 5 islands and 7 portals:\n'
 '- Path 1→3 costs 5 energy\n'
 '- Path 3→2 costs 2 energy\n'
 '- Path 2→4 costs 15 energy\n'
 '- Path 4→5 costs 5 energy\n'
 '**Optimal route:** 1→3→4→5 with total cost of 18 energy\n\n'
 '⚡ **Speed matters!** Race your opponent to solve it first!',
 'The sky archipelago stretches endlessly before you. Ancient portals shimmer with ethereal energy, connecting hundreds of floating islands. The wind whispers of treasures on the furthest island, but the journey is treacherous. Every portal demands energy from your ship''s crystal core.\n\n'
 'Your rival navigator has the same map. Whoever calculates the most efficient route and reaches the distant island first will claim the legendary Sky Pearl. The portals shift and change with each journey—no two navigators face the same paths.\n\n'
 'Chart your course wisely, sky sailor. The winds of fortune favor the swift and clever.',
 E'5 7\n1 2 10\n1 3 5\n2 4 15\n3 2 2\n3 4 8\n2 5 20\n4 5 5',
 '18',
 'hard',
 'sky_islands',
 '{"num_islands": 150, "num_portals": 200}'::jsonb),

-- Day 7: The Quantum Garden
(7, 'The Quantum Garden',
 E'# The Challenge\n\n'
 'In this mystical garden, plants exist in quantum states and interact with their neighbors. Your task is to simulate the garden''s evolution over several days.\n\n'
 '## Plant States\n'
 '- **0**: Empty soil\n'
 '- **1**: Seed\n'
 '- **2**: Sprout\n'
 '- **3**: Flower\n\n'
 '## Growth Rules (applied each day)\n'
 '1. Empty soil becomes a **seed** if it has 2+ flowering neighbors\n'
 '2. Seeds always become **sprouts**\n'
 '3. Sprouts become **flowers** if they have 1+ flowering neighbors\n'
 '4. Flowers remain **flowers**\n'
 '5. Otherwise, plants stay in their current state\n\n'
 '## Input Format\n'
 'First line: `rows cols days`\n'
 'Next rows: space-separated plant states\n\n'
 '## Your Mission\n'
 'Calculate how many **flowers** (state 3) exist after all days of growth.\n\n'
 '## Example\n'
 'In a 5×5 garden after 3 days, count all the flowers that have bloomed.',
 'Deep in the Forest of Perpetual Twilight lies a garden unlike any other. The plants here don''t follow the normal rules of nature—they exist in quantum superposition, their states entangled with those around them. Magical energy flows between neighbors, causing seeds to sprout and flowers to bloom in mesmerizing patterns.\n\n'
 'The ancient druids who tend this garden speak of a prophecy: when the correct number of flowers bloom, a gateway to the Emerald Realm will open. But the garden''s state changes with each cycle of the moon, and time is not on your side.\n\n'
 'Your opponent seeks the same knowledge. Only the one who correctly predicts the garden''s final state will gain the druids'' blessing and passage through the gateway.',
 E'5 5 3\n0 1 0 2 0\n1 0 2 0 1\n0 2 0 1 0\n2 0 1 0 2\n0 1 0 2 0',
 '6',
 'hard',
 'quantum_garden',
 '{"rows": 30, "cols": 30, "days": 10}'::jsonb),

-- Day 8: The Ancient Library Cipher
(8, 'The Ancient Library Cipher',
 E'# The Challenge\n\n'
 'You''ve discovered an ancient library where books contain encoded wisdom. Each book references other books through a cipher system.\n\n'
 '## Input Format\n'
 'First line: `N` (number of books)\n'
 'Next N lines: `ENCODED_TITLE SHIFT NUM_REFS [ref1 ref2 ...]`\n'
 '- ENCODED_TITLE: uppercase letters shifted by SHIFT positions in alphabet\n'
 '- SHIFT: how many positions each letter was shifted (Caesar cipher)\n'
 '- NUM_REFS: number of books this one references (by index, 0-based)\n\n'
 '## Wisdom Calculation\n'
 'Each book''s wisdom = sum of (letter_position) of decoded title\n'
 '(A=1, B=2, ..., Z=26)\n\n'
 '## Your Mission\n'
 'Books are "correctly decoded" if they can be reached from **Book 0** through references (think of it as a connected network). Sum the wisdom values of all correctly decoded books.\n\n'
 '## Example\n'
 'Book 0 references nothing, Book 1 references Book 0, Book 3 references Book 1.\n'
 'Books 0, 1, 3 are connected → sum their wisdom.\n'
 'Book 2 is isolated → don''t count it.',
 'The Forbidden Library of Alexandria was never destroyed—it was hidden in a pocket dimension, accessible only to those who can decipher its secrets. Thousands of books line the endless shelves, each one encoded by ancient scholars to protect dangerous knowledge from those unworthy to possess it.\n\n'
 'But here''s the twist: the books themselves form a network of references. Only the books connected to the Master Tome (Book 0) contain true wisdom. The others are clever forgeries designed to mislead treasure hunters.\n\n'
 'Your rival scholar has entered the library from another entrance. Whoever calculates the total wisdom first will earn the right to ask the library one question—and receive one true answer from the universe itself.',
 E'4\nEFGHI 1 0\nZCDEFG 2 1 0\nXYZ 3 0\nNOPQR 4 1 1',
 '126',
 'hard',
 'ancient_library',
 '{"num_books": 200}'::jsonb),

-- Day 9: The Dragon Market Economy
(9, 'The Dragon Market Economy',
 E'# The Challenge\n\n'
 'Welcome to the Grand Dragon Bazaar! Dragons trade precious gems, each with different buying and selling prices. You start with a fixed amount of gold and want to maximize your wealth.\n\n'
 '## Input Format\n'
 'First line: `num_dragons num_gem_types starting_gold`\n'
 'Next num_dragons lines: `gem_type buy_price sell_price`\n\n'
 '## Trading Rules\n'
 '- You can buy gems from dragons at their **buy_price**\n'
 '- You can sell gems back at their **sell_price**\n'
 '- You can trade with multiple dragons\n'
 '- Gem types range from 0 to (num_gem_types - 1)\n\n'
 '## Your Mission\n'
 'Find the **maximum gold** you can have after optimal trading.\n\n'
 '## Strategy Tip\n'
 'Look for dragons with the cheapest buying price and the highest selling price for the same gem type!',
 'Once per century, the dragons gather for the Grand Bazaar—a spectacular market where fortunes are made and lost in moments. Merchants from across the realm bring gold to trade for the dragons'' legendary gems: Starfire Rubies, Moonlight Sapphires, and Eternal Emeralds.\n\n'
 'But dragons are shrewd traders. Each sets their own prices, and the market is chaos. Some dragons sell cheaply but buy for even less. Others hoard gems and sell at exorbitant prices. The secret to wealth lies in finding the right trading patterns.\n\n'
 'You and your rival merchant have the same starting capital. Whoever ends the day with the most gold will be declared Grand Merchant and receive a dragon''s favor—worth more than all the gold in the kingdom.',
 E'5 3 100\n0 10 25\n1 15 40\n0 8 20\n2 20 30\n1 12 35',
 '304',
 'medium',
 'dragon_market',
 '{"num_dragons": 100, "num_gem_types": 5, "starting_gold": 1000}'::jsonb),

-- Day 10: The Time Crystal Resonance
(10, 'The Time Crystal Resonance',
 E'# The Challenge\n\n'
 'You''ve discovered a cave filled with time crystals that vibrate at different frequencies. When two crystals resonate together (their frequencies sum to a **prime number**), they release harmonic energy.\n\n'
 '## Input Format\n'
 'First line: `N` (number of crystals)\n'
 'Next N lines: one frequency value per line\n\n'
 '## Energy Calculation\n'
 'For each pair of crystals (i, j) where i < j:\n'
 '- If frequency[i] + frequency[j] is **prime**, they resonate!\n'
 '- Energy released = frequency[i] × frequency[j]\n\n'
 '## Your Mission\n'
 'Calculate the **total harmonic energy** from all resonant pairs.\n\n'
 '## Prime Numbers\n'
 'Remember: A prime number is only divisible by 1 and itself (2, 3, 5, 7, 11, 13, ...)\n\n'
 '## Example\n'
 'With crystals at frequencies [2, 3, 5, 8, 10]:\n'
 '- 2+3=5 (prime) → energy: 2×3=6\n'
 '- 2+5=7 (prime) → energy: 2×5=10\n'
 '- 3+8=11 (prime) → energy: 3×8=24\n'
 '- 5+8=13 (prime) → energy: 5×8=40\n'
 '**Total: 80**',
 'In the Cavern of Eternal Echoes, time crystals have formed over millennia, each vibrating at a unique frequency determined by the temporal anomalies that created it. Scholars have long known that when certain crystals resonate, they release pulses of pure chronological energy—powerful enough to glimpse past and future.\n\n'
 'The resonance pattern follows an ancient mathematical law: only pairs whose frequencies sum to prime numbers can achieve harmonic synchronization. The total energy released reveals the answer to a question about the timeline.\n\n'
 'You and your chronomancer rival must calculate the resonance before the temporal window closes. Whoever solves it first gains the power to ask the crystals one question about time itself.',
 E'5\n2\n3\n5\n8\n10',
 '80',
 'medium',
 'time_crystal',
 '{"num_crystals": 500, "max_frequency": 1000}'::jsonb);

COMMIT;
