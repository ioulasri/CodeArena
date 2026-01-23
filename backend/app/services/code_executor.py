"""
Code Execution Service
Runs user code in isolated Docker containers with time/memory limits
"""
import docker
import tempfile
import os
import time
import json
from typing import Dict, Optional
from pathlib import Path


class ExecutionResult:
    """Result of code execution"""
    def __init__(
        self,
        success: bool,
        output: str = "",
        error: str = "",
        execution_time_ms: float = 0.0,
        memory_used_mb: float = 0.0,
        status: str = "PENDING"
    ):
        self.success = success
        self.output = output.strip()
        self.error = error.strip()
        self.execution_time_ms = execution_time_ms
        self.memory_used_mb = memory_used_mb
        self.status = status


class CodeExecutor:
    """Executes code in isolated Docker containers"""
    
    # Language configurations
    LANGUAGE_CONFIG = {
        "python": {
            "image": "python:3.11-slim",
            "file_extension": ".py",
            "compile_command": None,
            "run_command": "python solution.py"
        },
        "javascript": {
            "image": "node:18-slim",
            "file_extension": ".js",
            "compile_command": None,
            "run_command": "node solution.js"
        },
        "java": {
            "image": "openjdk:17-slim",
            "file_extension": ".java",
            "compile_command": "javac Solution.java",
            "run_command": "java Solution"
        },
        "cpp": {
            "image": "gcc:12-slim",
            "file_extension": ".cpp",
            "compile_command": "g++ -o solution solution.cpp -std=c++17",
            "run_command": "./solution"
        }
    }
    
    def __init__(self):
        try:
            self.client = docker.from_env()
        except Exception as e:
            print(f"Warning: Docker connection failed: {e}")
            self.client = None
    
    async def execute(
        self,
        code: str,
        language: str,
        input_data: str,
        time_limit_ms: int = 2000,
        memory_limit_mb: int = 128
    ) -> ExecutionResult:
        """
        Execute code with given input in isolated container
        
        Args:
            code: The source code to execute
            language: Programming language (python, javascript, java, cpp)
            input_data: Input to pass to the program via stdin
            time_limit_ms: Maximum execution time in milliseconds
            memory_limit_mb: Maximum memory usage in MB
            
        Returns:
            ExecutionResult with output, errors, and metrics
        """
        if not self.client:
            return ExecutionResult(
                success=False,
                error="Docker is not available",
                status="ERROR"
            )
        
        language = language.lower()
        if language not in self.LANGUAGE_CONFIG:
            return ExecutionResult(
                success=False,
                error=f"Unsupported language: {language}",
                status="ERROR"
            )
        
        config = self.LANGUAGE_CONFIG[language]
        
        # Create temporary directory for code execution
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Write code to file
                filename = f"solution{config['file_extension']}"
                if language == "java":
                    filename = "Solution.java"
                
                file_path = os.path.join(temp_dir, filename)
                with open(file_path, 'w') as f:
                    f.write(code)
                
                # Write input data
                input_path = os.path.join(temp_dir, "input.txt")
                with open(input_path, 'w') as f:
                    f.write(input_data)
                
                # Compile if needed
                if config['compile_command']:
                    compile_result = self._run_in_container(
                        config['image'],
                        config['compile_command'],
                        temp_dir,
                        "",
                        time_limit_ms * 2,  # More time for compilation
                        memory_limit_mb
                    )
                    
                    if not compile_result.success:
                        return ExecutionResult(
                            success=False,
                            error=compile_result.error,
                            status="COMPILATION_ERROR"
                        )
                
                # Execute code
                start_time = time.time()
                result = self._run_in_container(
                    config['image'],
                    config['run_command'],
                    temp_dir,
                    input_data,
                    time_limit_ms,
                    memory_limit_mb
                )
                execution_time = (time.time() - start_time) * 1000  # Convert to ms
                
                result.execution_time_ms = execution_time
                return result
                
            except Exception as e:
                return ExecutionResult(
                    success=False,
                    error=f"Execution error: {str(e)}",
                    status="ERROR"
                )
    
    def _run_in_container(
        self,
        image: str,
        command: str,
        work_dir: str,
        input_data: str,
        time_limit_ms: int,
        memory_limit_mb: int
    ) -> ExecutionResult:
        """Run command in Docker container with resource limits"""
        try:
            # Pull image if not present
            try:
                self.client.images.get(image)
            except docker.errors.ImageNotFound:
                print(f"Pulling Docker image: {image}")
                self.client.images.pull(image)
            
            # Configure resource limits
            timeout_seconds = time_limit_ms / 1000.0
            mem_limit = f"{memory_limit_mb}m"
            
            # Run container
            container = self.client.containers.run(
                image,
                command=f'bash -c "{command}"',
                volumes={work_dir: {'bind': '/workspace', 'mode': 'rw'}},
                working_dir='/workspace',
                stdin_open=True,
                detach=True,
                remove=False,
                mem_limit=mem_limit,
                network_disabled=True,  # Security: no network access
                cap_drop=['ALL'],  # Security: drop all capabilities
                security_opt=['no-new-privileges']  # Security
            )
            
            try:
                # Wait for container with timeout
                exit_code = container.wait(timeout=timeout_seconds + 1)
                
                # Get output
                logs = container.logs(stdout=True, stderr=True).decode('utf-8')
                
                # Get stats
                stats = container.stats(stream=False)
                memory_used = stats['memory_stats'].get('usage', 0) / (1024 * 1024)  # MB
                
                # Clean up
                container.remove(force=True)
                
                if exit_code['StatusCode'] == 0:
                    return ExecutionResult(
                        success=True,
                        output=logs,
                        memory_used_mb=memory_used,
                        status="SUCCESS"
                    )
                else:
                    return ExecutionResult(
                        success=False,
                        error=logs,
                        memory_used_mb=memory_used,
                        status="RUNTIME_ERROR"
                    )
                    
            except Exception as e:
                # Timeout or other error - kill container
                try:
                    container.kill()
                    container.remove(force=True)
                except:
                    pass
                
                if "timeout" in str(e).lower():
                    return ExecutionResult(
                        success=False,
                        error=f"Time limit exceeded ({time_limit_ms}ms)",
                        status="TIME_LIMIT_EXCEEDED"
                    )
                else:
                    return ExecutionResult(
                        success=False,
                        error=f"Runtime error: {str(e)}",
                        status="RUNTIME_ERROR"
                    )
                    
        except Exception as e:
            return ExecutionResult(
                success=False,
                error=f"Container error: {str(e)}",
                status="ERROR"
            )
