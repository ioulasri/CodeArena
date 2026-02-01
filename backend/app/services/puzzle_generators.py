"""
Puzzle Generator Service
Generates unique puzzle inputs and calculates expected answers for different puzzle types.
Each puzzle type has its own generator that creates randomized but solvable problems.
"""

import random
import string
from typing import Dict, Tuple, List
from abc import ABC, abstractmethod


class PuzzleGenerator(ABC):
    """Base class for all puzzle generators"""
    
    @abstractmethod
    def generate(self, params: Dict) -> Tuple[str, str]:
        """
        Generate a puzzle instance.
        Returns: (input_data, expected_answer)
        """
        pass
    
    @abstractmethod
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        """
        Generate a small sample puzzle for explanation.
        Returns: (sample_input, sample_answer)
        """
        pass


class CrystalSumGenerator(PuzzleGenerator):
    """
    Day 1: Find sum of all numbers that are multiples of 3 or 5
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        min_count = params.get('min_count', 50)
        max_count = params.get('max_count', 100)
        range_val = params.get('range', 1000)
        
        count = random.randint(min_count, max_count)
        numbers = [random.randint(1, range_val) for _ in range(count)]
        
        # Calculate expected answer
        total = sum(n for n in numbers if n % 3 == 0 or n % 5 == 0)
        
        # Format input data
        input_data = '\n'.join(map(str, numbers))
        
        return input_data, str(total)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample_numbers = [3, 5, 7, 9, 10, 15, 20, 22]
        # Multiples of 3 or 5: 3, 5, 9, 10, 15, 20 = 62
        total = sum(n for n in sample_numbers if n % 3 == 0 or n % 5 == 0)
        input_data = '\n'.join(map(str, sample_numbers))
        return input_data, str(total)


class PatternCounterGenerator(PuzzleGenerator):
    """
    Day 2: Count occurrences of a pattern in text (including overlaps)
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        text_length = params.get('text_length', 500)
        pattern_length = params.get('pattern_length', 5)
        
        # Generate random pattern
        pattern = ''.join(random.choices(string.ascii_lowercase, k=pattern_length))
        
        # Generate text with random pattern insertions
        chars = list(string.ascii_lowercase)
        text_parts = []
        occurrences = random.randint(5, 15)
        
        # Build text with known number of occurrences
        remaining_length = text_length
        for i in range(occurrences):
            # Add random text before pattern
            if remaining_length > pattern_length:
                filler_length = random.randint(5, min(30, remaining_length - pattern_length))
                text_parts.append(''.join(random.choices(chars, k=filler_length)))
                remaining_length -= filler_length
            
            # Add pattern
            text_parts.append(pattern)
            remaining_length -= pattern_length
        
        # Fill remaining space
        if remaining_length > 0:
            text_parts.append(''.join(random.choices(chars, k=remaining_length)))
        
        text = ''.join(text_parts)
        
        # Count overlapping occurrences
        count = 0
        for i in range(len(text) - len(pattern) + 1):
            if text[i:i+len(pattern)] == pattern:
                count += 1
        
        # Format input
        input_data = f"Pattern: {pattern}\nText:\n{text}"
        
        return input_data, str(count)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        pattern = "aba"
        text = "ababaababa"
        # Overlapping: positions 0, 2, 5, 7 = 4 occurrences
        count = 0
        for i in range(len(text) - len(pattern) + 1):
            if text[i:i+len(pattern)] == pattern:
                count += 1
        input_data = f"Pattern: {pattern}\nText:\n{text}"
        return input_data, str(count)


class GridPathGenerator(PuzzleGenerator):
    """
    Day 3: Find maximum sum path from top-left to bottom-right (only right/down moves)
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        rows = params.get('rows', 10)
        cols = params.get('cols', 10)
        max_value = params.get('max_value', 100)
        
        # Generate grid
        grid = [[random.randint(1, max_value) for _ in range(cols)] for _ in range(rows)]
        
        # Calculate maximum path using dynamic programming
        dp = [[0] * cols for _ in range(rows)]
        dp[0][0] = grid[0][0]
        
        # Fill first row
        for j in range(1, cols):
            dp[0][j] = dp[0][j-1] + grid[0][j]
        
        # Fill first column
        for i in range(1, rows):
            dp[i][0] = dp[i-1][0] + grid[i][0]
        
        # Fill rest of the grid
        for i in range(1, rows):
            for j in range(1, cols):
                dp[i][j] = max(dp[i-1][j], dp[i][j-1]) + grid[i][j]
        
        max_sum = dp[rows-1][cols-1]
        
        # Format input
        input_data = '\n'.join([' '.join(map(str, row)) for row in grid])
        
        return input_data, str(max_sum)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
        # Optimal path: 1->3->5->2->1 = 12
        input_data = '\n'.join([' '.join(map(str, row)) for row in grid])
        return input_data, "12"


class SequenceFinderGenerator(PuzzleGenerator):
    """
    Day 4: Find the next numbers in a sequence
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        sequence_length = params.get('sequence_length', 8)
        
        # Choose a random sequence type
        sequence_types = ['arithmetic', 'geometric', 'fibonacci', 'squares', 'cubes']
        seq_type = random.choice(sequence_types)
        
        if seq_type == 'arithmetic':
            start = random.randint(1, 20)
            diff = random.randint(2, 10)
            sequence = [start + i * diff for i in range(sequence_length + 3)]
            
        elif seq_type == 'geometric':
            start = random.randint(2, 5)
            ratio = random.randint(2, 3)
            sequence = [start * (ratio ** i) for i in range(sequence_length + 3)]
            
        elif seq_type == 'fibonacci':
            a, b = random.randint(1, 5), random.randint(1, 5)
            sequence = [a, b]
            for _ in range(sequence_length + 1):
                sequence.append(sequence[-1] + sequence[-2])
                
        elif seq_type == 'squares':
            start = random.randint(1, 10)
            sequence = [(start + i) ** 2 for i in range(sequence_length + 3)]
            
        else:  # cubes
            start = random.randint(1, 5)
            sequence = [(start + i) ** 3 for i in range(sequence_length + 3)]
        
        # Take first sequence_length as input, rest as answer
        input_sequence = sequence[:sequence_length]
        next_three = sequence[sequence_length:sequence_length + 3]
        
        # Format input
        input_data = ' '.join(map(str, input_sequence))
        answer = ' '.join(map(str, next_three))
        
        return input_data, answer
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        # Fibonacci example
        sequence = [1, 1, 2, 3, 5, 8, 13, 21]
        next_three = [34, 55, 89]
        input_data = ' '.join(map(str, sequence))
        answer = ' '.join(map(str, next_three))
        return input_data, answer


class TowerBlocksGenerator(PuzzleGenerator):
    """
    Day 5: Maximum value by removing blocks (can only remove if blocks above are removed)
    This is essentially finding the maximum sum subarray ending at any position.
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        height = params.get('height', 15)
        max_value = params.get('max_value', 50)
        
        # Generate blocks (some can be negative to make it interesting)
        blocks = [random.randint(-max_value // 2, max_value) for _ in range(height)]
        
        # Calculate maximum value (Kadane's algorithm variant)
        # We can take any contiguous sequence from the top
        max_sum = 0
        current_sum = 0
        
        for value in blocks:
            current_sum = max(0, current_sum + value)
            max_sum = max(max_sum, current_sum)
        
        # Format input
        input_data = '\n'.join(map(str, blocks))
        
        return input_data, str(max_sum)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample_blocks = [10, -5, 20, -15, 30, 5]
        max_sum = 50  # 10 + (-5) + 20 + (-15) + 30 + 5
        input_data = '\n'.join(map(str, sample_blocks))
        return input_data, str(max_sum)


class SkyIslandsGenerator(PuzzleGenerator):
    """
    The Sky Islands Navigator: Navigate through floating islands with portal connections.
    Find shortest path considering portal jumps and energy costs.
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        num_islands = params.get('num_islands', 150)
        num_portals = params.get('num_portals', 200)
        
        # Generate island connections (edges in graph)
        connections = []
        for _ in range(num_portals):
            from_island = random.randint(1, num_islands)
            to_island = random.randint(1, num_islands)
            if from_island != to_island:
                energy_cost = random.randint(1, 100)
                connections.append(f"{from_island} {to_island} {energy_cost}")
        
        # Calculate shortest path using Dijkstra's algorithm (from island 1 to island num_islands)
        graph = {}
        for conn in connections:
            parts = conn.split()
            from_i, to_i, cost = int(parts[0]), int(parts[1]), int(parts[2])
            if from_i not in graph:
                graph[from_i] = []
            graph[from_i].append((to_i, cost))
        
        # Dijkstra's algorithm
        import heapq
        dist = {i: float('inf') for i in range(1, num_islands + 1)}
        dist[1] = 0
        pq = [(0, 1)]
        
        while pq:
            current_dist, u = heapq.heappop(pq)
            if current_dist > dist[u]:
                continue
            if u not in graph:
                continue
            for v, weight in graph[u]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    heapq.heappush(pq, (dist[v], v))
        
        answer = dist[num_islands] if dist[num_islands] != float('inf') else -1
        
        # Format input
        input_data = f"{num_islands} {num_portals}\n" + '\n'.join(connections)
        
        return input_data, str(int(answer))
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample_input = """5 7
1 2 10
1 3 5
2 4 15
3 2 2
3 4 8
2 5 20
4 5 5"""
        # Path: 1 -> 3 (5) -> 2 (2) -> 4 (15) -> 5 (5) = 27
        # Or: 1 -> 3 (5) -> 4 (8) -> 5 (5) = 18
        return sample_input, "18"


class QuantumGardenGenerator(PuzzleGenerator):
    """
    The Quantum Garden: Plants grow in quantum superposition.
    Each plant has growth states and interaction rules with neighbors.
    Calculate final garden state after N days.
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        rows = params.get('rows', 30)
        cols = params.get('cols', 30)
        days = params.get('days', 10)
        
        # Initial garden state (0=empty, 1=seed, 2=sprout, 3=flower)
        garden = [[random.randint(0, 2) for _ in range(cols)] for _ in range(rows)]
        
        # Simulate garden growth for N days
        for day in range(days):
            new_garden = [[0] * cols for _ in range(rows)]
            for i in range(rows):
                for j in range(cols):
                    cell = garden[i][j]
                    # Count flowering neighbors
                    flower_neighbors = 0
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == 0 and dj == 0:
                                continue
                            ni, nj = i + di, j + dj
                            if 0 <= ni < rows and 0 <= nj < cols:
                                if garden[ni][nj] == 3:
                                    flower_neighbors += 1
                    
                    # Growth rules
                    if cell == 0 and flower_neighbors >= 2:
                        new_garden[i][j] = 1  # Empty becomes seed near flowers
                    elif cell == 1:
                        new_garden[i][j] = 2  # Seed becomes sprout
                    elif cell == 2 and flower_neighbors >= 1:
                        new_garden[i][j] = 3  # Sprout becomes flower near flowers
                    elif cell == 3:
                        new_garden[i][j] = 3  # Flower stays flower
                    else:
                        new_garden[i][j] = cell  # No change
            garden = new_garden
        
        # Count total flowers
        flower_count = sum(row.count(3) for row in garden)
        
        # Format input
        input_lines = [f"{rows} {cols} {days}"]
        for row in garden:
            input_lines.append(' '.join(map(str, row)))
        input_data = '\n'.join(input_lines)
        
        return input_data, str(flower_count)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample_input = """5 5 3
0 1 0 2 0
1 0 2 0 1
0 2 0 1 0
2 0 1 0 2
0 1 0 2 0"""
        # After 3 days, calculate flower count (example answer)
        return sample_input, "6"


class AncientLibraryGenerator(PuzzleGenerator):
    """
    The Ancient Library Cipher: Books are arranged on shelves with encoded titles.
    Each book references others through a special cipher system.
    Find the total wisdom value of all correctly decoded books.
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        num_books = params.get('num_books', 200)
        
        books = []
        wisdom_values = []
        
        for i in range(num_books):
            # Generate encoded title (letter shift cipher)
            shift = random.randint(1, 25)
            title_length = random.randint(5, 15)
            original = ''.join(random.choices(string.ascii_uppercase, k=title_length))
            encoded = ''.join(chr((ord(c) - ord('A') + shift) % 26 + ord('A')) for c in original)
            
            # Wisdom value calculation: sum of letter positions after decoding
            wisdom = sum(ord(c) - ord('A') + 1 for c in original)
            wisdom_values.append(wisdom)
            
            # Each book has: encoded_title shift_key num_references [reference_indices]
            num_refs = random.randint(0, min(3, i))
            refs = random.sample(range(i), num_refs) if i > 0 else []
            
            book_line = f"{encoded} {shift} {num_refs}"
            if refs:
                book_line += " " + " ".join(map(str, refs))
            books.append(book_line)
        
        # Books are "correctly decoded" if they can be reached from book 0
        # through references (connected component)
        visited = set([0])
        queue = [0]
        
        while queue:
            current = queue.pop(0)
            book_data = books[current].split()
            num_refs = int(book_data[2])
            if num_refs > 0:
                refs = [int(book_data[3 + i]) for i in range(num_refs)]
                for ref in refs:
                    if ref not in visited:
                        visited.add(ref)
                        queue.append(ref)
        
        total_wisdom = sum(wisdom_values[i] for i in visited)
        
        # Format input
        input_data = f"{num_books}\n" + '\n'.join(books)
        
        return input_data, str(total_wisdom)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample_input = """4
EFGHI 1 0
BCDEFG 2 1 0
XYZ 3 0
NOPQR 4 1 1"""
        # Book 0: DEFGH (shift 1) -> wisdom = 4+5+6+7+8 = 30, refs: none
        # Book 1: ZABCD (shift 2) -> wisdom = 26+1+2+3+4 = 36, refs: [0]
        # Book 2: UVW (shift 3) -> wisdom = 21+22+23 = 66, refs: none (not reachable)
        # Book 3: JKLMN (shift 4) -> wisdom = 10+11+12+13+14 = 60, refs: [1]
        # Reachable from 0: books 0, 1, 3 -> total wisdom = 30 + 36 + 60 = 126
        return sample_input, "126"


class DragonMarketGenerator(PuzzleGenerator):
    """
    The Dragon Market Economy: Dragons trade precious gems with fluctuating values.
    Each dragon has a buying price and selling price for each gem type.
    Find maximum profit through optimal trading sequence.
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        num_dragons = params.get('num_dragons', 100)
        num_gem_types = params.get('num_gem_types', 5)
        starting_gold = params.get('starting_gold', 1000)
        
        # Generate dragon trades: each dragon can buy/sell certain gems
        dragons = []
        for _ in range(num_dragons):
            gem_type = random.randint(0, num_gem_types - 1)
            buy_price = random.randint(10, 100)
            sell_price = random.randint(buy_price + 5, buy_price + 50)
            dragons.append(f"{gem_type} {buy_price} {sell_price}")
        
        # Find maximum profit using dynamic programming
        # State: (current_gold, [gems_owned])
        # Simplified: track max gold achievable
        
        # Greedy approach: find best buy-sell pairs
        gem_prices = [[] for _ in range(num_gem_types)]
        for dragon in dragons:
            parts = dragon.split()
            gem_type, buy, sell = int(parts[0]), int(parts[1]), int(parts[2])
            gem_prices[gem_type].append((buy, sell))
        
        max_gold = starting_gold
        for gem_type in range(num_gem_types):
            if not gem_prices[gem_type]:
                continue
            # Find cheapest buy and most expensive sell
            min_buy = min(price[0] for price in gem_prices[gem_type])
            max_sell = max(price[1] for price in gem_prices[gem_type])
            if max_sell > min_buy:
                # Calculate how many gems we can buy and profit
                gems_bought = starting_gold // min_buy
                profit = gems_bought * (max_sell - min_buy)
                max_gold = max(max_gold, starting_gold + profit)
        
        # Format input
        input_data = f"{num_dragons} {num_gem_types} {starting_gold}\n" + '\n'.join(dragons)
        
        return input_data, str(max_gold)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample_input = """5 3 100
0 10 25
1 15 40
0 8 20
2 20 30
1 12 35"""
        # Best strategy: Buy gem 0 at 8 gold, sell at 25 gold
        # Can buy 100/8 = 12 gems, profit = 12 * (25-8) = 204
        # Final gold = 100 + 204 = 304
        return sample_input, "304"


class TimeCrystalGenerator(PuzzleGenerator):
    """
    The Time Crystal Resonance: Crystals vibrate at different frequencies.
    When crystals resonate (frequency sum is prime), they create harmonic energy.
    Find all resonant pairs and calculate total harmonic energy.
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        num_crystals = params.get('num_crystals', 500)
        max_frequency = params.get('max_frequency', 1000)
        
        # Generate crystal frequencies
        frequencies = [random.randint(1, max_frequency) for _ in range(num_crystals)]
        
        # Helper function to check if number is prime
        def is_prime(n):
            if n < 2:
                return False
            if n == 2:
                return True
            if n % 2 == 0:
                return False
            for i in range(3, int(n ** 0.5) + 1, 2):
                if n % i == 0:
                    return False
            return True
        
        # Find all resonant pairs and calculate energy
        total_energy = 0
        for i in range(len(frequencies)):
            for j in range(i + 1, len(frequencies)):
                freq_sum = frequencies[i] + frequencies[j]
                if is_prime(freq_sum):
                    # Energy is the product of the two frequencies
                    energy = frequencies[i] * frequencies[j]
                    total_energy += energy
        
        # Format input
        input_data = f"{num_crystals}\n" + '\n'.join(map(str, frequencies))
        
        return input_data, str(total_energy)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample_input = """5
2
3
5
8
10"""
        # Pairs with prime sums:
        # 2+3=5 (prime): energy = 2*3 = 6
        # 2+5=7 (prime): energy = 2*5 = 10
        # 3+8=11 (prime): energy = 3*8 = 24
        # 5+8=13 (prime): energy = 5*8 = 40
        # Total: 6 + 10 + 24 + 40 = 80
        return sample_input, "80"


class CrystalCaveGenerator(PuzzleGenerator):
    """
    Puzzle 11: Find largest connected component of crystals in grid
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        rows = params.get('rows', 100)
        cols = params.get('cols', 100)
        density = params.get('density', 0.4)  # Probability of crystal
        
        # Generate grid
        grid = []
        for _ in range(rows):
            row = ['#' if random.random() < density else '.' for _ in range(cols)]
            grid.append(''.join(row))
        
        # Find largest connected component using BFS
        visited = [[False] * cols for _ in range(rows)]
        max_size = 0
        
        def bfs(start_r, start_c):
            if visited[start_r][start_c] or grid[start_r][start_c] == '.':
                return 0
            queue = [(start_r, start_c)]
            visited[start_r][start_c] = True
            size = 0
            while queue:
                r, c = queue.pop(0)
                size += 1
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] == '#':
                        visited[nr][nc] = True
                        queue.append((nr, nc))
            return size
        
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == '#' and not visited[i][j]:
                    size = bfs(i, j)
                    max_size = max(max_size, size)
        
        # Format input
        input_data = f"{rows} {cols}\n" + '\n'.join(grid)
        return input_data, str(max_size)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample = """5 6
##.##.
#..###
##.###
......
.####."""
        return sample, "7"


class TimeTravelerGenerator(PuzzleGenerator):
    """
    Puzzle 12: Minimum cost TSP to visit required time periods
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        n = params.get('n', 12)  # Reduced for DP bitmask
        k = params.get('k', min(n, 8))
        start = 1
        
        # Generate cost matrix
        costs = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                cost = random.randint(5, 20)
                costs[i][j] = cost
                costs[j][i] = cost
        
        # Select random required periods
        required = sorted(random.sample(range(2, n + 1), k - 1))
        required = [start] + required
        
        # DP with bitmask to find minimum cost
        req_set = set(required)
        req_to_idx = {v: i for i, v in enumerate(required)}
        m = len(required)
        
        # dp[mask][i] = min cost to visit nodes in mask, ending at required[i]
        INF = float('inf')
        dp = [[INF] * m for _ in range(1 << m)]
        dp[1][0] = 0  # Start at required[0] with only it visited
        
        for mask in range(1 << m):
            for i in range(m):
                if dp[mask][i] == INF:
                    continue
                if not (mask & (1 << i)):
                    continue
                for j in range(m):
                    if mask & (1 << j):
                        continue
                    new_mask = mask | (1 << j)
                    cost = costs[required[i]][required[j]]
                    dp[new_mask][j] = min(dp[new_mask][j], dp[mask][i] + cost)
        
        min_cost = min(dp[(1 << m) - 1])
        
        # Format input
        lines = [f"{n} {k} {start}"]
        lines.append("  " + " ".join(str(i) for i in range(1, n + 1)))
        for i in range(1, n + 1):
            line = f"{i} " + " ".join(str(costs[i][j]) for j in range(1, n + 1))
            lines.append(line)
        lines.append("Required: " + " ".join(map(str, required)))
        
        return '\n'.join(lines), str(min_cost)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample = """4 3 1
  1  2  3  4
1 0  5  10 15
2 5  0  8  12
3 10 8  0  6
4 15 12 6  0
Required: 1 2 4"""
        return sample, "17"


class RecipeOptimizerGenerator(PuzzleGenerator):
    """
    Puzzle 13: Multi-dimensional knapsack for recipe optimization
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        n_recipes = params.get('n_recipes', 50)
        n_ingredients = params.get('n_ingredients', 5)
        
        # Generate ingredient supplies
        supplies = [random.randint(50, 200) for _ in range(n_ingredients)]
        
        # Generate recipes
        recipes = []
        for _ in range(n_recipes):
            profit = random.randint(30, 150)
            needs = [random.randint(0, 30) for _ in range(n_ingredients)]
            recipes.append((profit, needs))
        
        # Solve with DP (simplified - check each subset feasibility)
        # For large n, use greedy approximation
        max_profit = 0
        
        # Try greedy: sort by profit/resource ratio
        for mask in range(1 << min(n_recipes, 20)):  # Limit computation
            used = [0] * n_ingredients
            profit = 0
            valid = True
            for i in range(min(n_recipes, 20)):
                if mask & (1 << i):
                    p, needs = recipes[i]
                    for j in range(n_ingredients):
                        used[j] += needs[j]
                        if used[j] > supplies[j]:
                            valid = False
                            break
                    if not valid:
                        break
                    profit += p
            if valid:
                max_profit = max(max_profit, profit)
        
        # Format input
        lines = [f"{n_recipes} recipes, {n_ingredients} ingredients"]
        lines.append("Ingredients: [" + ", ".join(f"{s} ing{i}" for i, s in enumerate(supplies)) + "]")
        for i, (profit, needs) in enumerate(recipes):
            needs_str = ", ".join(f"{n} ing{j}" for j, n in enumerate(needs))
            lines.append(f"Recipe {i + 1}: profit={profit}, needs [{needs_str}]")
        
        return '\n'.join(lines), str(max_profit)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample = """3 recipes, 2 ingredients
Ingredients: [10 flour, 8 sugar]
Recipe 1: profit=50, needs [5 flour, 2 sugar]
Recipe 2: profit=60, needs [6 flour, 4 sugar]
Recipe 3: profit=40, needs [3 flour, 3 sugar]"""
        return sample, "90"


class DigitalRootGenerator(PuzzleGenerator):
    """
    Puzzle 14: Count numbers with specific digital root in range
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        l = params.get('l', random.randint(1, 10**6))
        r = params.get('r', l + random.randint(10**6, 10**7))
        d = params.get('d', random.randint(1, 9))
        
        # Digital root formula: dr(n) = 1 + ((n-1) % 9) for n > 0
        # Count numbers in [L, R] with digital root D
        def count_with_dr(limit, target):
            if limit < target:
                return 0
            # Numbers with dr=target: target, target+9, target+18, ...
            return (limit - target) // 9 + 1
        
        count = count_with_dr(r, d) - count_with_dr(l - 1, d)
        
        return f"L={l}, R={r}, D={d}", str(count)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        return "L=10, R=30, D=5", "2"


class NetworkRepairGenerator(PuzzleGenerator):
    """
    Puzzle 15: Find minimum cables to connect all components
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        n = params.get('n', 5000)
        m = params.get('m', min(n * 2, 10000))
        
        # Generate random connections
        edges = set()
        while len(edges) < m:
            a = random.randint(1, n)
            b = random.randint(1, n)
            if a != b:
                edges.add((min(a, b), max(a, b)))
        
        # Union-Find to count components
        parent = list(range(n + 1))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        for a, b in edges:
            union(a, b)
        
        components = len(set(find(i) for i in range(1, n + 1)))
        answer = components - 1  # Need (components - 1) edges to connect all
        
        # Format input
        lines = [f"{n} computers", f"{m} connections"]
        for a, b in list(edges)[:1000]:  # Limit output size
            lines.append(f"{a}-{b}")
        if len(edges) > 1000:
            lines.append(f"... ({len(edges) - 1000} more connections)")
        
        return '\n'.join(lines), str(answer)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample = """6 computers
3 connections
1-2
3-4
5-6"""
        return sample, "2"


class PalindromeFactoryGenerator(PuzzleGenerator):
    """
    Puzzle 16: Minimum deletions to make palindrome (LPS)
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        length = params.get('length', 500)
        
        # Generate random string
        s = ''.join(random.choices(string.ascii_lowercase, k=length))
        
        # Find longest palindromic subsequence
        n = len(s)
        dp = [[0] * n for _ in range(n)]
        
        for i in range(n):
            dp[i][i] = 1
        
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j]:
                    dp[i][j] = dp[i + 1][j - 1] + 2 if i + 1 <= j - 1 else 2
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
        
        lps_length = dp[0][n - 1]
        deletions = n - lps_length
        
        return s, str(deletions)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        return "racecar", "0"


class RobotWarehouseGenerator(PuzzleGenerator):
    """
    Puzzle 17: Minimum cost bipartite matching for robot warehouse
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        n = params.get('n', 10)  # Number of robots/boxes/storage
        grid_size = params.get('grid_size', 20)
        
        # Generate positions
        positions = random.sample([(i, j) for i in range(grid_size) for j in range(grid_size)], n * 3)
        robots = positions[:n]
        boxes = positions[n:2*n]
        storage = positions[2*n:3*n]
        
        # Calculate minimum cost using greedy assignment
        # Simplified: robot -> nearest box -> storage
        total_cost = 0
        used_boxes = set()
        used_storage = set()
        
        for robot in robots:
            # Find nearest unassigned box
            min_dist = float('inf')
            best_box_idx = 0
            for i, box in enumerate(boxes):
                if i not in used_boxes:
                    dist = abs(robot[0] - box[0]) + abs(robot[1] - box[1])
                    if dist < min_dist:
                        min_dist = dist
                        best_box_idx = i
            
            used_boxes.add(best_box_idx)
            box = boxes[best_box_idx]
            
            # Find nearest unassigned storage
            min_dist2 = float('inf')
            best_storage_idx = 0
            for i, stor in enumerate(storage):
                if i not in used_storage:
                    dist = abs(box[0] - stor[0]) + abs(box[1] - stor[1])
                    if dist < min_dist2:
                        min_dist2 = dist
                        best_storage_idx = i
            
            used_storage.add(best_storage_idx)
            total_cost += min_dist + min_dist2
        
        # Format input
        lines = [f"{grid_size}×{grid_size} grid"]
        lines.append(f"{n} robots at: " + ", ".join(f"({r},{c})" for r, c in robots))
        lines.append(f"{n} boxes at: " + ", ".join(f"({r},{c})" for r, c in boxes))
        lines.append(f"{n} storage at: " + ", ".join(f"({r},{c})" for r, c in storage))
        
        return '\n'.join(lines), str(total_cost)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample = """4×4 grid
2 robots at: (0,0), (3,3)
2 boxes at: (1,1), (2,2)
2 storage at: (0,3), (3,0)"""
        return sample, "12"


class MountainPeakGenerator(PuzzleGenerator):
    """
    Puzzle 18: Count local maxima in 2D grid
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        rows = params.get('rows', 300)
        cols = params.get('cols', 300)
        
        # Generate height grid
        grid = [[random.randint(1, 100) for _ in range(cols)] for _ in range(rows)]
        
        # Count peaks
        peaks = 0
        for i in range(rows):
            for j in range(cols):
                is_peak = True
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = i + di, j + dj
                        if 0 <= ni < rows and 0 <= nj < cols:
                            if grid[ni][nj] >= grid[i][j]:
                                is_peak = False
                                break
                    if not is_peak:
                        break
                if is_peak:
                    peaks += 1
        
        # Format input
        lines = [f"{rows} {cols}"]
        for row in grid[:100]:  # Limit output
            lines.append(' '.join(map(str, row)))
        if rows > 100:
            lines.append(f"... ({rows - 100} more rows)")
        
        return '\n'.join(lines), str(peaks)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample = """3 3
1 3 1
2 5 2
1 3 1"""
        return sample, "1"


class SpellCombinerGenerator(PuzzleGenerator):
    """
    Puzzle 19: Minimum cost to merge all elements (Huffman-style)
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        n = params.get('n', 50000)
        
        # Generate spell powers
        spells = [random.randint(1, 100) for _ in range(n)]
        
        # Use heap to always combine smallest two
        import heapq
        heap = spells.copy()
        heapq.heapify(heap)
        
        total_cost = 0
        while len(heap) > 1:
            first = heapq.heappop(heap)
            second = heapq.heappop(heap)
            cost = first + second
            total_cost += cost
            heapq.heappush(heap, cost)
        
        # Format input
        input_str = f"{n}\n" + ' '.join(map(str, spells[:1000]))
        if n > 1000:
            input_str += f"\n... ({n - 1000} more values)"
        
        return input_str, str(total_cost)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        return "4\n1 2 3 4", "19"


class PasswordCrackerGenerator(PuzzleGenerator):
    """
    Puzzle 20: Word break / string segmentation
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        dict_size = params.get('dict_size', 500)
        
        # Generate dictionary
        words = []
        for _ in range(dict_size):
            word_len = random.randint(2, 8)
            word = ''.join(random.choices(string.ascii_lowercase, k=word_len))
            words.append(word)
        
        # Create string from random words
        num_words_in_string = random.randint(5, 15)
        selected = random.choices(words, k=num_words_in_string)
        s = ''.join(selected)
        
        # Check if breakable using DP
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True
        word_set = set(words)
        
        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and s[j:i] in word_set:
                    dp[i] = True
                    break
        
        answer = "YES" if dp[n] else "NO"
        
        # Format input
        lines = [f'S = "{s[:100]}"']
        if len(s) > 100:
            lines[0] = f'S = "{s[:100]}..." (length {len(s)})'
        lines.append(f"Dictionary ({dict_size} words): [{', '.join(words[:20])}...]")
        
        return '\n'.join(lines), answer
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample = '''S = "catsanddog"
Dictionary = ["cat", "cats", "and", "sand", "dog"]'''
        return sample, "YES"


class AsteroidBeltGenerator(PuzzleGenerator):
    """
    Puzzle 21: Binary search on time with simulation
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        belt_length = params.get('length', 100000)
        n_asteroids = params.get('n', 500)
        ship_speed = params.get('ship_speed', 100)
        
        # Generate asteroids
        asteroids = []
        for _ in range(n_asteroids):
            pos = random.randint(0, belt_length)
            vel = random.randint(-50, 50)
            size = random.randint(1, 10)
            asteroids.append((pos, vel, size))
        
        # Binary search on time
        def can_pass(time):
            ship_pos = ship_speed * time
            if ship_pos < belt_length:
                return False
            for pos, vel, size in asteroids:
                asteroid_pos = pos + vel * time
                if abs(ship_pos - asteroid_pos) < size:
                    return False
            return True
        
        left, right = 0, belt_length * 2 // ship_speed
        answer = -1
        while left <= right:
            mid = (left + right) // 2
            if can_pass(mid):
                answer = mid
                right = mid - 1
            else:
                left = mid + 1
        
        # Format input
        lines = [f"Belt length: {belt_length}"]
        lines.append(f"{n_asteroids} asteroids:")
        for pos, vel, size in asteroids[:20]:
            lines.append(f"  Pos={pos}, Vel={vel}, Size={size}")
        if n_asteroids > 20:
            lines.append(f"  ... ({n_asteroids - 20} more)")
        lines.append(f"Ship: Pos=0, Speed={ship_speed}")
        
        return '\n'.join(lines), str(answer)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample = """Belt length: 100
3 asteroids:
  Pos=20, Vel=5, Size=3
  Pos=50, Vel=-2, Size=2
  Pos=80, Vel=3, Size=4
Ship: Pos=0, Speed=10"""
        return sample, "7"


class StockTraderGenerator(PuzzleGenerator):
    """
    Puzzle 22: Maximum profit with K transactions
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        n = params.get('n', 5000)
        k = params.get('k', 50)
        
        # Generate stock prices
        prices = [random.randint(10, 200) for _ in range(n)]
        
        # DP for stock trading
        if k >= n // 2:
            # Unlimited transactions
            profit = sum(max(prices[i + 1] - prices[i], 0) for i in range(n - 1))
        else:
            # Limited transactions
            buy = [-prices[0]] * (k + 1)
            sell = [0] * (k + 1)
            
            for price in prices:
                for j in range(k, 0, -1):
                    sell[j] = max(sell[j], buy[j] + price)
                    buy[j] = max(buy[j], sell[j - 1] - price)
            
            profit = sell[k]
        
        # Format input
        prices_str = ' '.join(map(str, prices[:100]))
        if n > 100:
            prices_str += f" ... ({n - 100} more)"
        input_str = f"Prices: [{prices_str}]\nK = {k}"
        
        return input_str, str(profit)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample = """Prices: [3, 2, 6, 5, 0, 3]
K = 2"""
        return sample, "7"


class IslandBridgeGenerator(PuzzleGenerator):
    """
    Puzzle 23: Minimum Spanning Tree
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        n = params.get('n', 500)
        
        # Generate island coordinates
        islands = [(random.randint(0, 10000), random.randint(0, 10000)) for _ in range(n)]
        
        # Generate all edges with Manhattan distance
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                dist = abs(islands[i][0] - islands[j][0]) + abs(islands[i][1] - islands[j][1])
                edges.append((dist, i, j))
        
        # Kruskal's algorithm
        edges.sort()
        parent = list(range(n))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
                return True
            return False
        
        total_cost = 0
        edges_used = 0
        for cost, i, j in edges:
            if union(i, j):
                total_cost += cost
                edges_used += 1
                if edges_used == n - 1:
                    break
        
        # Format input
        lines = [f"{n} islands"]
        for i, (x, y) in enumerate(islands[:20]):
            lines.append(f"Island {i}: ({x}, {y})")
        if n > 20:
            lines.append(f"... ({n - 20} more islands)")
        
        return '\n'.join(lines), str(total_cost)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample = """4 islands
(0,0) (2,0) (0,2) (2,2)"""
        return sample, "6"


class CipherWheelGenerator(PuzzleGenerator):
    """
    Puzzle 24: Rotation detection
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        length = params.get('length', 50000)
        
        # Generate original string
        original = ''.join(random.choices(string.ascii_lowercase, k=length))
        
        # Decide if rotation or Caesar shift
        if random.random() < 0.5:
            # Rotation
            shift_amount = random.randint(1, length - 1)
            encrypted = original[shift_amount:] + original[:shift_amount]
            answer = "YES"
        else:
            # Caesar shift
            shift = random.randint(1, 25)
            encrypted = ''.join(chr((ord(c) - ord('a') + shift) % 26 + ord('a')) for c in original)
            answer = "YES"
        
        # Format input
        e_str = encrypted[:100] + ("..." if len(encrypted) > 100 else "")
        d_str = original[:100] + ("..." if len(original) > 100 else "")
        return f'E = "{e_str}"\nD = "{d_str}"', answer
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        return 'E = "abc"\nD = "bcd"', "YES"


class RainWaterGenerator(PuzzleGenerator):
    """
    Puzzle 25: Trapping rainwater
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        n = params.get('n', 50000)
        
        # Generate heights
        heights = [random.randint(0, 100) for _ in range(n)]
        
        # Calculate trapped water using two pointers
        left, right = 0, n - 1
        left_max, right_max = 0, 0
        water = 0
        
        while left < right:
            if heights[left] < heights[right]:
                if heights[left] >= left_max:
                    left_max = heights[left]
                else:
                    water += left_max - heights[left]
                left += 1
            else:
                if heights[right] >= right_max:
                    right_max = heights[right]
                else:
                    water += right_max - heights[right]
                right -= 1
        
        # Format input
        heights_str = ','.join(map(str, heights[:100]))
        if n > 100:
            heights_str += f",... ({n - 100} more)"
        return f"[{heights_str}]", str(water)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        return "[0,1,0,2,1,0,1,3,2,1,2,1]", "6"


class MeetingSchedulerGenerator(PuzzleGenerator):
    """
    Puzzle 26: Minimum meeting rooms needed
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        n = params.get('n', 50000)
        
        # Generate meetings
        meetings = []
        for _ in range(n):
            start = random.randint(0, 10000)
            duration = random.randint(10, 100)
            end = start + duration
            meetings.append((start, end))
        
        # Sweep line algorithm
        events = []
        for start, end in meetings:
            events.append((start, 1))
            events.append((end, -1))
        events.sort()
        
        max_rooms = 0
        current_rooms = 0
        for time, delta in events:
            current_rooms += delta
            max_rooms = max(max_rooms, current_rooms)
        
        # Format input
        lines = [f"{n} meetings"]
        for start, end in meetings[:20]:
            lines.append(f"[{start}, {end}]")
        if n > 20:
            lines.append(f"... ({n - 20} more)")
        
        return '\n'.join(lines), str(max_rooms)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample = """4 meetings
[0, 30]
[5, 10]
[15, 20]
[25, 35]"""
        return sample, "2"


class MazeRunnerGenerator(PuzzleGenerator):
    """
    Puzzle 27: BFS with teleportation
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        rows = params.get('rows', 50)
        cols = params.get('cols', 50)
        k = params.get('k', 20)
        
        # Generate maze
        maze = [['.' for _ in range(cols)] for _ in range(rows)]
        
        # Add walls
        for _ in range(rows * cols // 4):
            r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
            maze[r][c] = '#'
        
        # Set start and end
        maze[0][0] = 'S'
        maze[rows - 1][cols - 1] = 'E'
        
        # Generate teleporters
        teleporters = []
        for _ in range(k):
            r1, c1 = random.randint(0, rows - 1), random.randint(0, cols - 1)
            r2, c2 = random.randint(0, rows - 1), random.randint(0, cols - 1)
            if maze[r1][c1] != '#' and maze[r2][c2] != '#':
                teleporters.append(((r1, c1), (r2, c2)))
        
        # BFS
        from collections import deque
        queue = deque([(0, 0, 0)])  # (r, c, dist)
        visited = {(0, 0)}
        teleport_map = {}
        for (r1, c1), (r2, c2) in teleporters:
            teleport_map[(r1, c1)] = (r2, c2)
        
        answer = -1
        while queue:
            r, c, dist = queue.popleft()
            if r == rows - 1 and c == cols - 1:
                answer = dist
                break
            
            # Check teleporter
            if (r, c) in teleport_map:
                nr, nc = teleport_map[(r, c)]
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, dist))
            
            # Normal moves
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and maze[nr][nc] != '#':
                    visited.add((nr, nc))
                    queue.append((nr, nc, dist + 1))
        
        # Format input
        lines = [f"{rows} {cols}"]
        for row in maze:
            lines.append(''.join(row))
        lines.append(f"Teleporters: " + ", ".join(f"({r1},{c1})→({r2},{c2})" for (r1, c1), (r2, c2) in teleporters[:10]))
        
        return '\n'.join(lines), str(answer)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample = """5 5
S....
.###.
.#E#.
.###.
.....
Teleporters: (0,0)→(2,4), (2,4)→(2,2)"""
        return sample, "1"


class SubsetSumGenerator(PuzzleGenerator):
    """
    Puzzle 28: Subset sum decision problem
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        n = params.get('n', 80)
        max_val = params.get('max_val', 500)
        
        # Generate gems
        gems = [random.randint(1, max_val) for _ in range(n)]
        
        # Create target that might be achievable
        if random.random() < 0.7:
            # Make it achievable
            subset_size = random.randint(2, min(5, n))
            subset = random.sample(gems, subset_size)
            target = sum(subset)
        else:
            # Random target
            target = random.randint(1, sum(gems))
        
        # DP for subset sum
        dp = [False] * (target + 1)
        dp[0] = True
        
        for gem in gems:
            for t in range(target, gem - 1, -1):
                if dp[t - gem]:
                    dp[t] = True
        
        answer = "YES" if dp[target] else "NO"
        
        # Format input
        gems_str = ', '.join(map(str, gems))
        return f"Gems: [{gems_str}]\nTarget: {target}", answer
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample = """Gems: [3, 34, 4, 12, 5, 2]
Target: 9"""
        return sample, "YES"


class TowerBuilderGenerator(PuzzleGenerator):
    """
    Puzzle 29: Box stacking (LIS in 2D)
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        n = params.get('n', 80)
        
        # Generate blocks with 3 dimensions
        blocks = []
        for _ in range(n):
            w = random.randint(1, 50)
            d = random.randint(1, 50)
            h = random.randint(1, 50)
            blocks.append((w, d, h))
        
        # Generate all possible orientations
        rotations = []
        for w, d, h in blocks:
            rotations.append((w, d, h))
            rotations.append((w, h, d))
            rotations.append((d, h, w))
        
        # Sort by base area (descending)
        rotations.sort(key=lambda x: x[0] * x[1], reverse=True)
        
        # DP for maximum height
        m = len(rotations)
        dp = [rot[2] for rot in rotations]  # Initialize with own height
        
        for i in range(1, m):
            for j in range(i):
                if rotations[j][0] > rotations[i][0] and rotations[j][1] > rotations[i][1]:
                    dp[i] = max(dp[i], dp[j] + rotations[i][2])
        
        max_height = max(dp)
        
        # Format input
        lines = [f"{n} blocks"]
        for i, (w, d, h) in enumerate(blocks[:20]):
            lines.append(f"Block {i + 1}: {w}×{d}×{h}")
        if n > 20:
            lines.append(f"... ({n - 20} more)")
        
        return '\n'.join(lines), str(max_height)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample = """3 blocks
Block 1: 4×6×7
Block 2: 1×2×3
Block 3: 4×5×6"""
        return sample, "13"


class VirusSpreadGenerator(PuzzleGenerator):
    """
    Puzzle 30: Multi-source BFS for maximum distance
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        n = params.get('n', 5000)
        m = params.get('m', 10000)
        k = params.get('k', 5)
        
        # Generate random graph
        edges = set()
        while len(edges) < m:
            a = random.randint(1, n)
            b = random.randint(1, n)
            if a != b:
                edges.add((min(a, b), max(a, b)))
        
        # Build adjacency list
        graph = [[] for _ in range(n + 1)]
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)
        
        # Select random infected nodes
        infected = random.sample(range(1, n + 1), k)
        
        # Multi-source BFS
        from collections import deque
        queue = deque((node, 0) for node in infected)
        visited = set(infected)
        max_days = 0
        
        while queue:
            node, days = queue.popleft()
            max_days = max(max_days, days)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, days + 1))
        
        # Format input
        lines = [f"{n} nodes"]
        lines.append(f"{m} edges: " + ", ".join(f"{a}-{b}" for a, b in list(edges)[:20]))
        if m > 20:
            lines.append(f"... ({m - 20} more edges)")
        lines.append(f"Initially infected: {infected}")
        
        return '\n'.join(lines), str(max_days)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        sample = """7 nodes
6 edges: 1-2, 2-3, 3-4, 5-6, 6-7, 1-5
Initially infected: [1]"""
        return sample, "3"


class ParenthesesBalancerGenerator(PuzzleGenerator):
    """
    Puzzle 31: Minimum insertions to balance parentheses
    """
    
    def generate(self, params: Dict) -> Tuple[str, str]:
        length = params.get('length', 50000)
        
        # Generate random parentheses string
        s = ''.join(random.choices(['(', ')'], k=length))
        
        # Calculate minimum insertions
        open_needed = 0
        close_needed = 0
        
        for char in s:
            if char == '(':
                open_needed += 1
            else:  # ')'
                if open_needed > 0:
                    open_needed -= 1
                else:
                    close_needed += 1
        
        insertions = open_needed + close_needed
        
        # Format input
        s_display = s[:100] + ("..." if len(s) > 100 else "")
        return f'"{s_display}"', str(insertions)
    
    def generate_sample(self, params: Dict) -> Tuple[str, str]:
        return '"(()"', "1"


class PuzzleGeneratorFactory:
    """Factory to get the appropriate generator for a puzzle type"""
    
    _generators = {
        'crystal_sum': CrystalSumGenerator(),
        'pattern_counter': PatternCounterGenerator(),
        'grid_path': GridPathGenerator(),
        'sequence_finder': SequenceFinderGenerator(),
        'tower_blocks': TowerBlocksGenerator(),
        'sky_islands': SkyIslandsGenerator(),
        'quantum_garden': QuantumGardenGenerator(),
        'ancient_library': AncientLibraryGenerator(),
        'dragon_market': DragonMarketGenerator(),
        'time_crystal': TimeCrystalGenerator(),
        'crystal_cave': CrystalCaveGenerator(),
        'time_traveler': TimeTravelerGenerator(),
        'recipe_optimizer': RecipeOptimizerGenerator(),
        'digital_root': DigitalRootGenerator(),
        'network_repair': NetworkRepairGenerator(),
        'palindrome_factory': PalindromeFactoryGenerator(),
        'robot_warehouse': RobotWarehouseGenerator(),
        'mountain_peak': MountainPeakGenerator(),
        'spell_combiner': SpellCombinerGenerator(),
        'password_cracker': PasswordCrackerGenerator(),
        'asteroid_belt': AsteroidBeltGenerator(),
        'stock_trader': StockTraderGenerator(),
        'island_bridge': IslandBridgeGenerator(),
        'cipher_wheel': CipherWheelGenerator(),
        'rain_water': RainWaterGenerator(),
        'meeting_scheduler': MeetingSchedulerGenerator(),
        'maze_runner': MazeRunnerGenerator(),
        'subset_sum': SubsetSumGenerator(),
        'tower_builder': TowerBuilderGenerator(),
        'virus_spread': VirusSpreadGenerator(),
        'parentheses_balancer': ParenthesesBalancerGenerator(),
    }
    
    @classmethod
    def get_generator(cls, generator_type: str) -> PuzzleGenerator:
        """Get a puzzle generator by type"""
        generator = cls._generators.get(generator_type)
        if not generator:
            raise ValueError(f"Unknown generator type: {generator_type}")
        return generator
    
    @classmethod
    def generate_puzzle_instance(cls, generator_type: str, params: Dict) -> Tuple[str, str]:
        """
        Generate a puzzle instance.
        Returns: (input_data, expected_answer)
        """
        generator = cls.get_generator(generator_type)
        return generator.generate(params)
    
    @classmethod
    def generate_sample(cls, generator_type: str, params: Dict) -> Tuple[str, str]:
        """
        Generate a sample puzzle for explanation.
        Returns: (sample_input, sample_answer)
        """
        generator = cls.get_generator(generator_type)
        return generator.generate_sample(params)
