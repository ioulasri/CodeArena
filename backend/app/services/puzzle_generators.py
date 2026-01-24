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


class PuzzleGeneratorFactory:
    """Factory to get the appropriate generator for a puzzle type"""
    
    _generators = {
        'crystal_sum': CrystalSumGenerator(),
        'pattern_counter': PatternCounterGenerator(),
        'grid_path': GridPathGenerator(),
        'sequence_finder': SequenceFinderGenerator(),
        'tower_blocks': TowerBlocksGenerator(),
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
