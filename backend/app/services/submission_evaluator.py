"""
Submission Evaluator Service
Orchestrates the evaluation of code submissions against test cases
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.submission import Submission
from app.models.problem import Problem
from app.core.database import SessionLocal
from .code_executor import CodeExecutor, ExecutionResult


class TestCase:
    """Represents a test case for evaluation"""
    def __init__(self, input_data: str, expected_output: str, is_sample: bool = False):
        self.input_data = input_data
        self.expected_output = expected_output
        self.is_sample = is_sample


class SubmissionEvaluator:
    """Evaluates code submissions against test cases"""
    
    def __init__(self):
        self.executor = CodeExecutor()
    
    async def evaluate_submission(self, submission_id: int):
        """
        Evaluate a submission by running it against all test cases
        
        Args:
            submission_id: ID of the submission to evaluate
        """
        db = SessionLocal()
        try:
            # Get submission
            submission = db.query(Submission).filter(Submission.id == submission_id).first()
            if not submission:
                print(f"Submission {submission_id} not found")
                return
            
            # Update status to running
            submission.status = "RUNNING"
            db.commit()
            
            # Get problem
            problem = db.query(Problem).filter(Problem.id == submission.problem_id).first()
            if not problem:
                submission.status = "ERROR"
                submission.error_message = "Problem not found"
                db.commit()
                return
            
            # Get test cases (for now, parse from problem examples)
            test_cases = self._get_test_cases(problem)
            
            if not test_cases:
                submission.status = "ERROR"
                submission.error_message = "No test cases found for this problem"
                db.commit()
                return
            
            # Run against each test case
            passed = 0
            total = len(test_cases)
            max_execution_time = 0.0
            max_memory = 0.0
            
            for i, test_case in enumerate(test_cases):
                result = await self.executor.execute(
                    code=submission.code,
                    language=submission.language,
                    input_data=test_case.input_data,
                    time_limit_ms=problem.time_limit_ms or 2000,
                    memory_limit_mb=problem.memory_limit_mb or 128
                )
                
                # Track metrics
                max_execution_time = max(max_execution_time, result.execution_time_ms)
                max_memory = max(max_memory, result.memory_used_mb)
                
                # Check for errors
                if result.status == "TIME_LIMIT_EXCEEDED":
                    submission.status = "TIME_LIMIT_EXCEEDED"
                    submission.error_message = result.error
                    break
                
                if result.status == "RUNTIME_ERROR":
                    submission.status = "RUNTIME_ERROR"
                    submission.error_message = result.error
                    break
                
                if result.status == "COMPILATION_ERROR":
                    submission.status = "COMPILATION_ERROR"
                    submission.error_message = result.error
                    break
                
                if result.status == "ERROR":
                    submission.status = "ERROR"
                    submission.error_message = result.error
                    break
                
                # Compare output
                if self._compare_output(result.output, test_case.expected_output):
                    passed += 1
                else:
                    # Wrong answer
                    submission.status = "WRONG_ANSWER"
                    submission.error_message = f"Failed on test case {i+1}"
                    if test_case.is_sample:
                        submission.error_message += f"\nExpected: {test_case.expected_output}\nGot: {result.output}"
                    break
            
            # All tests passed
            if passed == total:
                submission.status = "ACCEPTED"
                submission.error_message = None
            
            # Update submission metrics
            submission.test_cases_passed = passed
            submission.test_cases_total = total
            submission.execution_time_ms = max_execution_time
            submission.memory_used_mb = max_memory
            
            db.commit()
            
            print(f"Submission {submission_id}: {submission.status} ({passed}/{total} passed)")
            
        except Exception as e:
            print(f"Error evaluating submission {submission_id}: {e}")
            submission = db.query(Submission).filter(Submission.id == submission_id).first()
            if submission:
                submission.status = "ERROR"
                submission.error_message = f"Evaluation error: {str(e)}"
                db.commit()
        finally:
            db.close()
    
    def _get_test_cases(self, problem: Problem) -> List[TestCase]:
        """
        Get test cases for a problem
        For now, extract from problem examples (JSONB field)
        Later: query from test_cases table
        """
        test_cases = []
        
        if problem.examples:
            for example in problem.examples:
                if isinstance(example, dict) and 'input' in example and 'output' in example:
                    test_cases.append(TestCase(
                        input_data=str(example['input']),
                        expected_output=str(example['output']),
                        is_sample=True
                    ))
        
        return test_cases
    
    def _compare_output(self, actual: str, expected: str) -> bool:
        """
        Compare actual output with expected output
        Handles whitespace differences
        """
        # Normalize: strip whitespace, lowercase for comparison
        actual_normalized = actual.strip().replace('\r\n', '\n')
        expected_normalized = expected.strip().replace('\r\n', '\n')
        
        return actual_normalized == expected_normalized
