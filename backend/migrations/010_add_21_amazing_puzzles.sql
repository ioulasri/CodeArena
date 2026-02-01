-- Migration: Add 21 spectacular new puzzles (Days 11-31)
-- Each puzzle features rich narratives, clear explanations, and diverse algorithms

BEGIN;

-- Day 11: The Crystal Cave Mapper (Easy - Graph Traversal)
INSERT INTO puzzles (day, title, description, story, sample_input, sample_output, difficulty, generator_type, generator_params)
VALUES
(11, 'The Crystal Cave Mapper',
 E'# The Challenge\n\n'
 'You''re exploring a magical crystal cave lit by bioluminescent crystals. The crystals connect in mysterious patterns, forming chambers of varying sizes. Your task is to find the **largest chamber** of connected crystals.\n\n'
 '## Input Format\n'
 'First line: `rows cols`\n'
 'Next rows lines: Grid where `#` = crystal, `.` = empty space\n'
 'Crystals connect horizontally and vertically (not diagonally)\n\n'
 '## Your Mission\n'
 'Find the size of the largest connected group of crystals.\n\n'
 '## Example Explained\n'
 'In the sample, several crystal groups exist. Count each connected region and return the largest one.',
 'Deep beneath the Whispering Mountains lies a network of crystal caverns that cartographers have tried—and failed—to map for centuries. The crystals pulse with ancient energy, forming vast interconnected chambers that shift subtly over time.\n\n'
 'You''ve been hired by the Royal Geographic Society to map these caves. But there''s a catch: the largest chamber is said to contain the legendary Heartstone, a crystal of immense power. Your rival explorer has entered from another entrance.\n\n'
 'Whoever correctly identifies the largest crystal chamber first will earn the right to claim the Heartstone. The caverns are vast, the formations complex. Speed and precision are your only allies in this underground race.',
 E'5 6\n##.##.\n#..###\n##.###\n......\n.####.',
 '7',
 'easy',
 'crystal_cave',
 '{"rows": 100, "cols": 100, "density": 0.4}'::jsonb),

-- Day 12: Time Traveler's Dilemma (Hard - DP/TSP)
(12, 'Time Traveler''s Dilemma',
 E'# The Challenge\n\n'
 'Your time machine has limited fuel. Each jump between time periods consumes fuel proportional to the temporal distance. You must visit certain required periods, but can skip others.\n\n'
 '## Input Format\n'
 'Line 1: `N K START` - N total periods, K required visits, starting period\n'
 'Line 2: Period numbers (headers)\n'
 'Next N lines: N×N cost matrix where entry [i][j] = fuel cost from period i to j\n'
 'Last line: Required periods to visit\n\n'
 '## Your Mission\n'
 'Find the **minimum fuel** needed to visit all required periods (can visit in any order).\n\n'
 '## Strategy Tip\n'
 'This is a variation of the Traveling Salesman Problem. Use dynamic programming with bitmasks for optimal solution.',
 'In 2847, humanity finally cracked time travel. But the technology is expensive—each jump drains enormous amounts of chronon fuel, and fuel reserves are critically low. The Temporal Research Institute needs data from specific historical periods to prevent a catastrophic timeline collapse.\n\n'
 'You and a rival time operative have been given the same mission: visit the required periods and return with the data. The operative who completes the mission with the least fuel consumption wins not only glory but the coveted position of Chief Temporal Navigator.\n\n'
 'The timeline branches before you, each jump carrying a cost. Chart your course carefully—every unit of fuel matters. The past and future wait for no one, and your rival''s ship is already warming up their temporal drive.',
 E'4 3 1\n  1  2  3  4\n1 0  5  10 15\n2 5  0  8  12\n3 10 8  0  6\n4 15 12 6  0\nRequired: 1 2 4',
 '17',
 'hard',
 'time_traveler',
 '{"n": 12, "k": 8}'::jsonb),

-- Day 13: The Recipe Optimizer (Medium - Knapsack)
(13, 'The Recipe Optimizer',
 E'# The Challenge\n\n'
 'You''re a master chef with limited ingredients. Each recipe produces a dish with a profit value but requires specific amounts of ingredients. Maximize your total profit!\n\n'
 '## Input Format\n'
 'Line 1: `N recipes, M ingredients`\n'
 'Line 2: Available ingredients with quantities\n'
 'Next N lines: Recipe details with profit and required ingredients\n\n'
 '## Your Mission\n'
 'Select which recipes to make (can make each at most once) to maximize profit while staying within ingredient limits.\n\n'
 '## Example\n'
 'If you have 10 flour and 8 sugar, and Recipe 1 needs 5 flour + 2 sugar for 50 profit, check if you can make it and others without exceeding supplies.',
 'The Grand Culinary Competition is tonight, and you''re facing off against the kingdom''s most renowned chef. The rules are brutal: both chefs receive the same limited ingredients, the same recipe book, and three hours to prepare dishes for the royal judges.\n\n'
 'Each recipe in the book has been assigned a profit value based on complexity, rarity, and presentation. The chef whose dishes collectively earn the highest profit wins the Golden Ladle and a permanent position as the Royal Chef.\n\n'
 'Your opponent is a master of strategy, known for optimal resource allocation. The ingredients are limited, the recipes numerous. Every decision matters. Choose wisely—your culinary career hangs in the balance. The clock starts... now.',
 E'3 recipes, 2 ingredients\nIngredients: [10 flour, 8 sugar]\nRecipe 1: profit=50, needs [5 flour, 2 sugar]\nRecipe 2: profit=60, needs [6 flour, 4 sugar]\nRecipe 3: profit=40, needs [3 flour, 3 sugar]',
 '90',
 'medium',
 'recipe_optimizer',
 '{"n_recipes": 50, "n_ingredients": 5}'::jsonb),

-- Day 14: Digital Root Sequences (Medium - Math/Number Theory)
(14, 'Digital Root Sequences',
 E'# The Challenge\n\n'
 'Ancient mathematicians discovered that repeatedly summing a number''s digits reveals hidden patterns called "digital roots." Your task: count how many numbers in a range [L, R] have a specific digital root.\n\n'
 '## What is a Digital Root?\n'
 'Keep summing digits until you get a single digit:\n'
 '- 38 → 3+8 = 11 → 1+1 = 2 (digital root is 2)\n'
 '- 14 → 1+4 = 5 (digital root is 5)\n\n'
 '## Input Format\n'
 '`L=lower_bound, R=upper_bound, D=target_root`\n\n'
 '## Your Mission\n'
 'Count integers in [L, R] with digital root equal to D.\n\n'
 '## Math Tip\n'
 'Digital root formula: `dr(n) = 1 + ((n-1) mod 9)` for n > 0\n'
 'Use this for efficient counting!',
 'In the lost Library of Babylon, scholars preserved an ancient mathematical secret: the Digital Root Codex. This mystical text claims that numbers with matching digital roots resonate with cosmic energy, and counting these numbers across vast ranges reveals patterns in the universe itself.\n\n'
 'Two rival mathematicians have been tasked by the Academy of Numbers to verify sections of the Codex. Each must count numbers with specific digital roots across enormous ranges—billions of numbers in mere moments.\n\n'
 'The mathematician who delivers accurate counts first will be named Grand Calculator and gain access to the Codex''s deepest secrets, said to contain proofs of unsolved millennium problems. Your opponent is already calculating. Can you find the pattern that makes this possible?',
 E'L=10, R=30, D=5',
 '2',
 'medium',
 'digital_root',
 '{"l": 1000000, "r": 100000000, "d": 7}'::jsonb),

-- Day 15: The Network Repair Team (Easy - Union-Find)
(15, 'The Network Repair Team',
 E'# The Challenge\n\n'
 'A computer network has suffered damage, leaving connections broken. Computers can only communicate if they''re in the same connected component. Your job: determine the **minimum number of cables** needed to connect all computers.\n\n'
 '## Input Format\n'
 'Line 1: `N computers`\n'
 'Line 2: `M connections` (current working connections)\n'
 'Next M lines: Pairs of connected computers (bidirectional)\n\n'
 '## Your Mission\n'
 'Count how many separate network components exist, then calculate minimum cables needed to connect them all.\n\n'
 '## Formula\n'
 'If there are C components, you need C-1 cables to connect them all.',
 'It''s 3 AM when the alert comes in: GlobalNet''s primary data center has suffered a cascading failure. Fiber optic cables are severed, switches are down, and the network has fragmented into isolated islands of computers that can''t communicate.\n\n'
 'You and a rival network engineer have been called in for emergency repairs. Corporate HQ has authorized emergency funds for new cables, but they''re expensive—every cable costs $50,000. Whoever determines the minimum number of cables needed first gets the lucrative consulting contract and a fat bonus.\n\n'
 'The network topology is complex, with thousands of computers and countless broken connections. Time is money, and every second counts. Fire up your terminals—the network waits for no one.',
 E'6 computers\n3 connections\n1-2\n3-4\n5-6',
 '2',
 'easy',
 'network_repair',
 '{"n": 5000, "m": 10000}'::jsonb),

-- Day 16: The Palindrome Factory (Medium - DP/LCS)
(16, 'The Palindrome Factory',
 E'# The Challenge\n\n'
 'You run a factory that produces palindrome strings (strings that read the same forwards and backwards). Given a string, what''s the **minimum number of characters to remove** to make it a palindrome?\n\n'
 '## Input Format\n'
 'A string S containing lowercase letters\n\n'
 '## Your Mission\n'
 'Find the minimum deletions needed. Alternatively, find the longest palindromic subsequence and subtract from string length.\n\n'
 '## Examples\n'
 '- "racecar" → Already palindrome, 0 deletions\n'
 '- "abcdef" → Keep any single char, delete 5 others\n'
 '- "character" → Keep "carac" or similar, delete rest\n\n'
 '## Algorithm Hint\n'
 'Use dynamic programming: compare string with its reverse to find longest common subsequence (LCS).',
 'Welcome to PalindromeWorks Inc., the galaxy''s premier manufacturer of symmetrical strings. Our clients—cryptographers, poets, and AI systems—demand perfection. But raw string material is expensive, and every character deletion costs money.\n\n'
 'You''ve been promoted to Production Optimizer, competing with a rival analyst for the position of VP of Operations. Corporate has challenged both of you: given strings of increasing length and complexity, determine the minimum deletions needed to meet palindrome specifications.\n\n'
 'The analyst who processes strings most efficiently wins the promotion. Your opponent has a PhD in algorithms. The strings are getting longer—some reaching thousands of characters. Time to prove your optimization skills are superior.',
 E'racecar',
 '0',
 'medium',
 'palindrome_factory',
 '{"length": 500}'::jsonb),

-- Day 17: The Robot Warehouse (Hard - Bipartite Matching)
(17, 'The Robot Warehouse',
 E'# The Challenge\n\n'
 'Robots must move boxes from their current positions to storage locations. Each robot can handle one box. Calculate the **minimum total distance** all robots must travel (to pick up boxes + deliver to storage).\n\n'
 '## Input Format\n'
 'Grid dimensions\n'
 'N robot positions\n'
 'N box positions\n'
 'N storage positions\n\n'
 '## Your Mission\n'
 'Optimally assign robots to boxes and boxes to storage spots to minimize total Manhattan distance traveled.\n\n'
 '## Algorithm\n'
 'This is a bipartite matching problem. Use Hungarian algorithm or greedy assignment for approximation.',
 'In the year 2156, FutureStore''s fully automated warehouse relies on precision robotics. Tonight''s inventory redistribution involves moving thousands of boxes—but there''s a problem. The warehouse AI has malfunctioned, and manual override is needed.\n\n'
 'Two competing logistics algorithms—yours and your rival''s—are being tested to replace the AI. The algorithm that moves all boxes to storage with minimum total distance wins a contract worth millions.\n\n'
 'The robots are powered on, boxes are scattered, and storage bays await. Every meter traveled costs energy and time. Your rival''s algorithm is already running simulations. Can you optimize better?',
 E'4×4 grid\n2 robots at: (0,0), (3,3)\n2 boxes at: (1,1), (2,2)\n2 storage at: (0,3), (3,0)',
 '12',
 'hard',
 'robot_warehouse',
 '{"n": 10, "grid_size": 20}'::jsonb),

-- Day 18: Mountain Peak Counter (Easy - Array Processing)
(18, 'Mountain Peak Counter',
 E'# The Challenge\n\n'
 'Analyze satellite terrain data to identify mountain peaks. A cell is a **peak** if its height is strictly greater than all 8 surrounding neighbors (including diagonals).\n\n'
 '## Input Format\n'
 'First line: `rows cols`\n'
 'Next rows: Grid of integer heights\n\n'
 '## Your Mission\n'
 'Count how many peaks exist in the terrain.\n\n'
 '## Example\n'
 'In a 3×3 grid, the center cell is a peak only if it''s taller than all 8 neighbors.',
 'The National Geographic Institute is mapping the Himalayan range using new satellite technology. Accurate peak identification is crucial for climbers, but also for the prestigious Atlas of Earth''s Highest Points.\n\n'
 'Two rival cartographers—you and your competitor—have been given the same satellite data. Whoever correctly identifies all peaks first will have their name published in the Atlas''s credits, a career-defining achievement.\n\n'
 'The data is massive: hundreds of thousands of elevation data points. Your rival has started processing. The mountains wait for no one.',
 E'3 3\n1 3 1\n2 5 2\n1 3 1',
 '1',
 'easy',
 'mountain_peak',
 '{"rows": 300, "cols": 300}'::jsonb),

-- Day 19: The Spell Combiner (Medium - Greedy/Heap)
(19, 'The Spell Combiner',
 E'# The Challenge\n\n'
 'Combine spell scrolls to create one ultimate spell. Combining two scrolls creates a new scroll with power = sum of both, but costs mana = sum of both. Find the **minimum total mana** to combine all scrolls.\n\n'
 '## Input Format\n'
 'Line 1: N (number of scrolls)\n'
 'Line 2: N space-separated power levels\n\n'
 '## Your Mission\n'
 'Always combine the two smallest scrolls to minimize total mana cost.\n\n'
 '## Example\n'
 'Powers [1, 2, 3, 4]:\n'
 '- Combine 1+2=3 (cost 3), remaining [3,3,4]\n'
 '- Combine 3+3=6 (cost 6), remaining [6,4]\n'
 '- Combine 4+6=10 (cost 10)\n'
 'Total: 19',
 'The Grand Arcanum Academy holds its annual Spell Crafting Championship. Apprentice mages are given identical sets of spell scrolls and must combine them into a single legendary spell—but magical energy isn''t free. Every combination drains mana from the caster.\n\n'
 'You face your rival apprentice, a cunning strategist known for efficiency. The judge watches both of you carefully. The mage who creates the ultimate spell with the least mana expenditure wins the Championship Medallion and a full scholarship to the Master''s program.\n\n'
 'The scrolls glow with potential. Your rival has already picked up the first two. Think fast—there''s an optimal strategy here, and mana is precious.',
 E'4\n1 2 3 4',
 '19',
 'medium',
 'spell_combiner',
 '{"n": 50000}'::jsonb),

-- Day 20: The Password Cracker (Medium - String DP)
(20, 'The Password Cracker',
 E'# The Challenge\n\n'
 'You intercepted an encrypted message—it''s a concatenation of dictionary words with no spaces. Can you break it into valid words?\n\n'
 '## Input Format\n'
 'Line 1: String S (the encrypted message)\n'
 'Line 2: Dictionary of known words\n\n'
 '## Your Mission\n'
 'Determine if S can be segmented into dictionary words. Return "YES" or "NO".\n\n'
 '## Example\n'
 'S = "catsanddog", Dictionary = ["cat", "cats", "and", "sand", "dog"]\n'
 'Valid: "cats" + "and" + "dog" → YES',
 'International Intelligence Agency intercepts thousands of encrypted messages daily. The latest batch uses a clever encoding: remove all spaces and punctuation, creating strings that appear random but are actually concatenated dictionary words.\n\n'
 'You and a rival codebreaker are competing for promotion to Chief Cryptanalyst. Both of you have the same dictionary and encrypted strings. Whoever cracks more messages wins the promotion—and access to the agency''s most classified projects.\n\n'
 'Your rival is already typing furiously. The strings are long, the dictionary large. There''s a pattern here—a way to quickly test if segmentation is possible. Find it, or fall behind.',
 E'S = "catsanddog"\nDictionary = ["cat", "cats", "and", "sand", "dog"]',
 'YES',
 'medium',
 'password_cracker',
 '{"dict_size": 500}'::jsonb),

-- Day 21: Asteroid Belt Navigation (Medium - Binary Search)
(21, 'Asteroid Belt Navigation',
 E'# The Challenge\n\n'
 'Navigate through an asteroid belt. Asteroids move predictably. Find the **earliest time** your ship can safely pass through.\n\n'
 '## Input Format\n'
 'Belt length\n'
 'N asteroids: position, velocity, size\n'
 'Ship: starting position, speed\n\n'
 '## Your Mission\n'
 'Binary search on time. For each time T, simulate asteroid positions and check if ship can pass without collision.\n\n'
 '## Strategy\n'
 'If you can pass at time T, you might pass earlier. If you can''t, try later times.',
 'You''re piloting a cargo freighter through the notorious Kepler Belt, a region of space littered with moving asteroids. Your rival captain is taking the same route in a parallel lane, both racing to deliver supplies to Mars Station Alpha.\n\n'
 'The first ship to dock gets the lucrative contract renewal. But the belt is treacherous—asteroids drift at different velocities, and collision means mission failure. Your ship''s computer can calculate safe passage windows, but time is limited.\n\n'
 'Your rival''s ship has already entered the belt''s edge. The asteroids tumble through space unpredictably. Calculate the earliest safe passage time, or risk losing the contract—and your reputation.',
 E'Belt length: 100\n3 asteroids:\n  Pos=20, Vel=5, Size=3\n  Pos=50, Vel=-2, Size=2\n  Pos=80, Vel=3, Size=4\nShip: Pos=0, Speed=10',
 '7',
 'medium',
 'asteroid_belt',
 '{"length": 100000, "n": 500, "ship_speed": 100}'::jsonb),

-- Day 22: The Stock Trader (Hard - DP Optimization)
(22, 'The Stock Trader',
 E'# The Challenge\n\n'
 'You have historical stock prices and can make at most K buy-sell transactions. What''s the maximum profit?\n\n'
 '## Input Format\n'
 'Line 1: Array of daily prices\n'
 'Line 2: K = maximum transactions\n\n'
 '## Transaction Rules\n'
 '- Must sell before buying again (no parallel holdings)\n'
 '- One transaction = one buy + one sell\n\n'
 '## Example\n'
 'Prices [3,2,6,5,0,3], K=2\n'
 'Buy at 2, sell at 6 (profit 4)\n'
 'Buy at 0, sell at 3 (profit 3)\n'
 'Total: 7',
 'Wall Street, 1987. You''re a junior analyst at a prestigious trading firm, competing with a rival analyst for a promotion to Senior Trader. The boss has given both of you a test: historical stock data and a transaction limit. Generate the maximum possible profit.\n\n'
 'This isn''t just about money—it''s about proving you can optimize under constraints, a crucial skill for high-frequency trading. Your rival graduated from MIT with honors. The data is complex, the transaction limit tight.\n\n'
 'The trading floor buzzes with activity. Your rival is already scribbling algorithms. The clock is ticking. Show them you''re the better trader.',
 E'Prices: [3, 2, 6, 5, 0, 3]\nK = 2',
 '7',
 'hard',
 'stock_trader',
 '{"n": 5000, "k": 50}'::jsonb),

-- Day 23: Island Bridge Builder (Easy - MST)
(23, 'Island Bridge Builder',
 E'# The Challenge\n\n'
 'Connect all islands with bridges. Bridge cost = Manhattan distance between islands. Find the **minimum total cost** to connect all islands.\n\n'
 '## Input Format\n'
 'Line 1: N islands\n'
 'Next N lines: (x, y) coordinates\n\n'
 '## Your Mission\n'
 'Build a Minimum Spanning Tree. Use Kruskal''s or Prim''s algorithm.\n\n'
 '## Example\n'
 'Four islands at corners of a square: connect three edges for minimum cost.',
 'The Pacific Federation needs to connect its scattered island territories with a network of bridges. Budget is tight, and every meter of bridge costs thousands. Two rival engineering firms—yours and your competitor''s—have submitted proposals.\n\n'
 'The firm that designs a bridge network connecting all islands with the lowest total construction cost wins the contract, worth billions. Your rival firm has cutting-edge software and decades of experience.\n\n'
 'The islands are plotted, coordinates measured. It''s a graph problem, and the optimal solution is out there. The Federation Board reviews proposals tomorrow. Time to prove your optimization skills.',
 E'4 islands\n(0,0) (2,0) (0,2) (2,2)',
 '6',
 'easy',
 'island_bridge',
 '{"n": 500}'::jsonb),

-- Day 24: The Cipher Wheel (Medium - String Matching)
(24, 'The Cipher Wheel',
 E'# The Challenge\n\n'
 'Determine if one string is a rotation or Caesar shift of another.\n\n'
 '## Input Format\n'
 'E = encrypted string\n'
 'D = decrypted string\n\n'
 '## Your Mission\n'
 'Check if D is:\n'
 '1. A rotation of E (e.g., "abc" → "bca")\n'
 '2. A Caesar cipher shift of E\n'
 'Return "YES" or "NO"\n\n'
 '## Trick\n'
 'To check rotation: see if D appears in E+E\n'
 'Caesar shift: check all 26 possible shifts',
 'Renaissance Italy, 1502. You''ve discovered a collection of encrypted manuscripts in the Vatican archives. Legend says they contain Leonardo da Vinci''s lost inventions, encoded with simple ciphers: rotations and Caesar shifts.\n\n'
 'A rival historian is also decoding the manuscripts. Whoever decrypts the collection first gains access to publish the findings—career-making scholarship. The manuscripts are numerous, the ciphers varied.\n\n'
 'Your rival has cryptographic training. You have algorithmic thinking. The texts await. Every second counts in this race through history.',
 E'E = "abc"\nD = "bcd"',
 'YES',
 'medium',
 'cipher_wheel',
 '{"length": 50000}'::jsonb),

-- Day 25: Rain Water Collector (Medium - Two Pointers)
(25, 'Rain Water Collector',
 E'# The Challenge\n\n'
 'Given terrain elevation, calculate total rainwater trapped in valleys.\n\n'
 '## Input Format\n'
 'Array of heights representing terrain elevation\n\n'
 '## Your Mission\n'
 'For each position, water level = min(max_left, max_right). Trapped water = water_level - height.\n\n'
 '## Algorithm\n'
 'Use two pointers from both ends, tracking max heights, for O(n) solution.',
 'You''re a civil engineer designing a rainwater harvesting system for a desert city. The terrain is complex, with valleys and peaks. Your rival engineering firm is bidding on the same project with their own calculations.\n\n'
 'The city council will award the contract to the firm that accurately calculates the maximum water that can be collected—they need precise numbers for infrastructure planning. Your rival has expensive simulation software.\n\n'
 'You have the elevation data and your algorithmic skills. The terrain stretches for kilometers, thousands of elevation points. Calculate fast, calculate accurately. The city''s water future depends on getting this right.',
 E'[0,1,0,2,1,0,1,3,2,1,2,1]',
 '6',
 'medium',
 'rain_water',
 '{"n": 50000}'::jsonb),

-- Day 26: The Meeting Scheduler (Easy - Interval Sweep)
(26, 'The Meeting Scheduler',
 E'# The Challenge\n\n'
 'Schedule N meetings in conference rooms. Find the **minimum number of rooms** needed so no meetings overlap.\n\n'
 '## Input Format\n'
 'N meetings\n'
 'Each meeting: [start_time, end_time]\n\n'
 '## Your Mission\n'
 'Count maximum simultaneous meetings at any point in time.\n\n'
 '## Algorithm\n'
 'Use sweep line: create events for starts (+1) and ends (-1), track maximum concurrent count.',
 'Corporate headquarters is hosting the annual Global Summit, with hundreds of meetings scheduled throughout the day. Two event planners—you and your rival—must determine how many conference rooms to book. Book too few, and meetings will conflict. Book too many, and you waste money.\n\n'
 'The planner who calculates the exact minimum number of rooms needed wins the permanent position as Chief Event Coordinator. Your rival has years of experience, but you have algorithmic precision.\n\n'
 'The meeting schedule is complex, with overlapping time slots and tight intervals. Get it right, and you''re promoted. Get it wrong, and you''re back to organizing office birthday parties.',
 E'4 meetings\n[0, 30]\n[5, 10]\n[15, 20]\n[25, 35]',
 '2',
 'easy',
 'meeting_scheduler',
 '{"n": 50000}'::jsonb),

-- Day 27: The Maze Runner (Medium - BFS with Teleports)
(27, 'The Maze Runner',
 E'# The Challenge\n\n'
 'Escape a maze with teleporters. Find the **shortest path** from Start to Exit.\n\n'
 '## Input Format\n'
 'Grid dimensions\n'
 'Maze grid: `.`=walkable, `#`=wall, `S`=start, `E`=exit\n'
 'K teleporter pairs: entering cell A instantly teleports to cell B\n\n'
 '## Your Mission\n'
 'Use BFS treating teleporters as 0-cost edges in the graph.\n\n'
 '## Strategy\n'
 'When stepping on a teleporter, add the destination to the queue with same distance.',
 'You''re trapped in the Labyrinth of Doors, an ancient maze filled with magical teleportation portals. Legend says the maze rearranges itself for each visitor. Your rival adventurer entered from the opposite side—both of you seeking the legendary Exit Key.\n\n'
 'The maze is vast, the portals confusing. Some portals help, others hinder. Whoever reaches the exit first claims the Key and escapes to fame and fortune. The other remains trapped until the next fool enters.\n\n'
 'Your rival has a map. You have your wit and algorithmic thinking. The maze walls shift, the portals glow. Find the shortest path, or wander forever.',
 E'5 5\nS....\n.###.\n.#E#.\n.###.\n.....\nTeleporters: (0,0)→(2,4), (2,4)→(2,2)',
 '1',
 'medium',
 'maze_runner',
 '{"rows": 50, "cols": 50, "k": 20}'::jsonb),

-- Day 28: The Subset Summer (Medium - Subset Sum)
(28, 'The Subset Summer',
 E'# The Challenge\n\n'
 'Given N gems with power values, can you find a subset that sums exactly to target T?\n\n'
 '## Input Format\n'
 'Line 1: Array of gem powers\n'
 'Line 2: Target sum T\n\n'
 '## Your Mission\n'
 'Return "YES" if possible, "NO" otherwise.\n\n'
 '## Algorithm\n'
 'Dynamic programming: dp[i] = true if sum i is achievable.\n'
 'For each gem, update dp array in reverse.',
 'The Royal Treasury has been robbed! The thief left a cryptic note: "I took gems worth exactly N gold coins." You''re the Royal Investigator, racing against a rival detective to determine which gems were stolen.\n\n'
 'The thief was clever—the gem values are complex, and thousands of combinations are possible. Whoever figures out if a valid subset exists (and finds it) first solves the case and earns the King''s reward: a massive bounty.\n\n'
 'Your rival detective is methodical and experienced. You have algorithmic insight. The gem inventory is extensive, the target sum specific. The King grows impatient. Solve it fast, or lose the reward—and your reputation.',
 E'Gems: [3, 34, 4, 12, 5, 2]\nTarget: 9',
 'YES',
 'medium',
 'subset_sum',
 '{"n": 80, "max_val": 500}'::jsonb),

-- Day 29: The Tower Builder (Hard - Box Stacking)
(29, 'The Tower Builder',
 E'# The Challenge\n\n'
 'Stack boxes to build the tallest tower. A box can only go on another if its base is strictly smaller in both dimensions.\n\n'
 '## Input Format\n'
 'N blocks with dimensions (width, depth, height)\n'
 'Blocks can be rotated to use any dimension as height\n\n'
 '## Your Mission\n'
 'Find maximum tower height.\n\n'
 '## Algorithm\n'
 'Generate all rotations, sort by base area, use DP to find longest increasing subsequence considering 2D constraints.',
 'The Annual Architects'' Challenge: build the tallest free-standing tower using provided blocks. No glue, no supports—just careful stacking following physics. You and a rival architect have identical block sets. Whoever builds taller wins a commission to design the city''s new skyscraper.\n\n'
 'The blocks vary in size and proportion. Each can be oriented three ways. The optimal configuration isn''t obvious—it requires careful mathematical analysis. Your rival has won three previous challenges.\n\n'
 'The blocks are delivered, the judges watch, the clock starts. Stack carefully. Every centimeter counts. Your architectural legacy depends on this moment.',
 E'3 blocks\nBlock 1: 4×6×7\nBlock 2: 1×2×3\nBlock 3: 4×5×6',
 '13',
 'hard',
 'tower_builder',
 '{"n": 80}'::jsonb),

-- Day 30: The Virus Spread Simulator (Easy - Multi-source BFS)
(30, 'The Virus Spread Simulator',
 E'# The Challenge\n\n'
 'A virus spreads through a computer network. Each day, infected nodes infect neighbors. How many days until all reachable nodes are infected?\n\n'
 '## Input Format\n'
 'N nodes, M bidirectional edges\n'
 'K initially infected nodes\n\n'
 '## Your Mission\n'
 'Use multi-source BFS starting from all infected nodes. Return the maximum distance (days) to reach the farthest node.\n\n'
 '## Example\n'
 'If infection starts at node 1, and spreads day by day, count until no new infections occur.',
 'It''s 2:47 AM. CyberCorp''s network is under siege by a sophisticated virus. Security teams are scrambling, but the virus spreads fast—each infected machine infects its neighbors daily. You''re the incident response analyst, racing to model the spread.\n\n'
 'A rival analyst is working on the same problem. Corporate needs to know: how long until the entire network is compromised? The answer determines whether to shut down immediately (costly) or implement targeted defenses.\n\n'
 'Whoever calculates the spread timeline accurately first influences the billion-dollar decision. Your rival has access to fancy simulation tools. You have graph algorithms. The network diagram glows on your screen. Model it fast.',
 E'7 nodes\n6 edges: 1-2, 2-3, 3-4, 5-6, 6-7, 1-5\nInitially infected: [1]',
 '3',
 'easy',
 'virus_spread',
 '{"n": 5000, "m": 10000, "k": 5}'::jsonb),

-- Day 31: The Parentheses Balancer (Easy - Stack/Greedy)
(31, 'The Parentheses Balancer',
 E'# The Challenge\n\n'
 'Debug code with mismatched parentheses. Find the **minimum insertions** needed to balance all parentheses.\n\n'
 '## Input Format\n'
 'String containing only `(` and `)`\n\n'
 '## Your Mission\n'
 'Count unmatched open and close parentheses.\n'
 '- Track open count as you scan\n'
 '- For `(`: increment open_count\n'
 '- For `)`: if open_count > 0, decrement; else need a `(`\n'
 '- At end, any remaining open_count needs `)`\n\n'
 '## Example\n'
 '"(()" → need 1 `)` at end\n'
 '"())" → need 1 `(` at start',
 'You''re a code reviewer at MegaSoft, working late to audit thousands of lines of legacy code before the morning deployment. The code is riddled with parentheses errors—mismatched, unbalanced, a nightmare. Your rival reviewer is handling the same files.\n\n'
 'The engineering director set a challenge: whoever develops the most efficient algorithm to calculate minimum fixes needed for all files gets the Senior Code Reviewer promotion—and a hefty raise.\n\n'
 'The files are massive, some with hundreds of thousands of parentheses. Brute force won''t cut it. Your rival is already processing files. You need a linear-time solution. The deployment clock ticks down. Fix it fast.',
 E'"(()"',
 '1',
 'easy',
 'parentheses_balancer',
 '{"length": 50000}'::jsonb);

COMMIT;
