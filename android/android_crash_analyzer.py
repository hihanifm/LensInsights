"""Android Crash Analyzer - Detects FATAL_EXCEPTION crashes with AI-powered analysis.

This insight detects Android crashes by searching for "FATAL EXCEPTION" patterns
and captures 10 lines of context after each crash for better analysis.
Uses AI to provide crash summaries, root cause analysis, and fix recommendations.
"""

import logging
from typing import List, Optional, Callable, Awaitable
import asyncio
import os

from app.core.insight_base import Insight
from app.core.models import InsightResult, ProgressEvent
from app.utils.ripgrep import is_ripgrep_available, ripgrep_search

logger = logging.getLogger(__name__)


class AndroidCrashAnalyzer(Insight):
    """Detects Android FATAL_EXCEPTION crashes with context and AI analysis."""
    
    @property
    def id(self) -> str:
        return "android_crash_analyzer"
    
    @property
    def name(self) -> str:
        return "Android Crash Analyzer"
    
    @property
    def description(self) -> str:
        return "Detects FATAL EXCEPTION crashes with stack traces and AI-powered analysis"
    
    @property
    def folder(self) -> Optional[str]:
        return "android"
    
    @property
    def ai_enabled(self) -> bool:
        """Enable AI analysis for crash reports."""
        return True
    
    @property
    def ai_auto(self) -> bool:
        """Auto-trigger AI analysis after crash detection."""
        return True
    
    @property
    def ai_prompt_type(self) -> str:
        """Use custom prompt for Android crash analysis."""
        return "custom"
    
    @property
    def ai_custom_prompt(self) -> Optional[str]:
        """Custom prompt for analyzing Android crashes."""
        return """You are an expert Android developer and crash analyzer.

Analyze the following Android crash logs and provide:

1. **Root Cause**: What caused each crash? Explain in simple terms.
2. **Affected Components**: Which Android components, activities, or services are involved?
3. **Severity Assessment**: How critical is each crash? (Critical/High/Medium/Low)
4. **Fix Recommendations**: Specific code changes or fixes needed for each crash.
5. **Prevention Tips**: Best practices to prevent similar crashes in the future.

Be concise, actionable, and prioritize the most critical crashes first.

{result_content}"""
    
    async def analyze(
        self,
        file_paths: List[str],
        cancellation_event: Optional[asyncio.Event] = None,
        progress_callback: Optional[Callable[[ProgressEvent], Awaitable[None]]] = None
    ) -> InsightResult:
        """
        Analyze Android log files for FATAL_EXCEPTION crashes.
        
        Args:
            file_paths: List of log file paths to analyze
            cancellation_event: Optional event to cancel analysis
            progress_callback: Optional callback for progress updates
            
        Returns:
            InsightResult with crash details and context
        """
        import time
        start_time = time.time()
        
        logger.info(f"AndroidCrashAnalyzer: Starting analysis of {len(file_paths)} file(s)")
        
        all_crashes = []
        total_crashes = 0
        files_with_crashes = 0
        
        for file_idx, file_path in enumerate(file_paths, 1):
            # Check for cancellation
            if cancellation_event and cancellation_event.is_set():
                logger.info("AndroidCrashAnalyzer: Analysis cancelled")
                from app.services.file_handler import CancelledError
                raise CancelledError("Analysis cancelled")
            
            # Emit progress
            if progress_callback:
                try:
                    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
                    await progress_callback(ProgressEvent(
                        type="file_open",
                        message=f"Analyzing file {file_idx}/{len(file_paths)}: {os.path.basename(file_path)}",
                        task_id="",
                        insight_id="",
                        file_path=file_path,
                        file_index=file_idx,
                        total_files=len(file_paths),
                        file_size_mb=file_size_mb
                    ))
                except Exception as e:
                    logger.error(f"AndroidCrashAnalyzer: Error emitting progress: {e}")
            
            # Search for crashes with context
            try:
                file_crashes = await self._find_crashes_in_file(file_path, cancellation_event)
                
                if file_crashes:
                    all_crashes.append({
                        "file": file_path,
                        "crashes": file_crashes
                    })
                    crash_count = len(file_crashes)
                    total_crashes += crash_count
                    files_with_crashes += 1
                    logger.info(f"AndroidCrashAnalyzer: Found {crash_count} crash(es) in {file_path}")
                else:
                    logger.debug(f"AndroidCrashAnalyzer: No crashes found in {file_path}")
                    
            except Exception as e:
                logger.error(f"AndroidCrashAnalyzer: Error processing {file_path}: {e}", exc_info=True)
                continue
        
        # Format results
        content = self._format_results(all_crashes, total_crashes, files_with_crashes)
        
        elapsed = time.time() - start_time
        logger.info(f"AndroidCrashAnalyzer: Analysis complete in {elapsed:.2f}s - {total_crashes} crash(es) found")
        
        return InsightResult(
            result_type="text",
            content=content,
            metadata={
                "total_crashes": total_crashes,
                "files_with_crashes": files_with_crashes,
                "total_files": len(file_paths)
            }
        )
    
    async def _find_crashes_in_file(
        self,
        file_path: str,
        cancellation_event: Optional[asyncio.Event] = None
    ) -> List[str]:
        """
        Find FATAL_EXCEPTION crashes in a file with context.
        
        Args:
            file_path: Path to log file
            cancellation_event: Optional cancellation event
            
        Returns:
            List of crash blocks (each with 10 lines of context)
        """
        crashes = []
        
        # Use ripgrep if available, otherwise fall back to manual search
        if is_ripgrep_available():
            logger.debug(f"AndroidCrashAnalyzer: Using ripgrep for {file_path}")
            
            # Run ripgrep in executor to avoid blocking
            loop = asyncio.get_event_loop()
            
            def run_ripgrep():
                """Run ripgrep with context lines."""
                crash_lines = []
                try:
                    # Search for FATAL EXCEPTION with 10 lines of context after
                    for line in ripgrep_search(
                        file_path,
                        r"FATAL\s+EXCEPTION",
                        context_after=10
                    ):
                        crash_lines.append(line)
                except Exception as e:
                    logger.error(f"AndroidCrashAnalyzer: Ripgrep error: {e}")
                    raise
                return crash_lines
            
            try:
                all_lines = await loop.run_in_executor(None, run_ripgrep)
                
                # Group lines into crash blocks (separated by "--" from ripgrep context)
                current_crash = []
                for line in all_lines:
                    if line == "--":
                        if current_crash:
                            crashes.append("\n".join(current_crash))
                            current_crash = []
                    else:
                        current_crash.append(line)
                
                # Add last crash if exists
                if current_crash:
                    crashes.append("\n".join(current_crash))
                    
            except Exception as e:
                logger.error(f"AndroidCrashAnalyzer: Ripgrep failed: {e}, falling back to manual search")
                crashes = await self._manual_search(file_path, cancellation_event)
        else:
            logger.debug(f"AndroidCrashAnalyzer: Ripgrep not available, using manual search for {file_path}")
            crashes = await self._manual_search(file_path, cancellation_event)
        
        return crashes
    
    async def _manual_search(
        self,
        file_path: str,
        cancellation_event: Optional[asyncio.Event] = None
    ) -> List[str]:
        """
        Manually search for crashes when ripgrep is not available.
        
        Args:
            file_path: Path to log file
            cancellation_event: Optional cancellation event
            
        Returns:
            List of crash blocks with context
        """
        import re
        crashes = []
        pattern = re.compile(r"FATAL\s+EXCEPTION", re.IGNORECASE)
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines):
                # Check for cancellation periodically
                if cancellation_event and cancellation_event.is_set():
                    from app.services.file_handler import CancelledError
                    raise CancelledError("Analysis cancelled")
                
                if pattern.search(line):
                    # Capture the crash line + 10 lines after
                    crash_block = []
                    for j in range(i, min(i + 11, len(lines))):
                        crash_block.append(lines[j].rstrip())
                    crashes.append("\n".join(crash_block))
                    
        except Exception as e:
            logger.error(f"AndroidCrashAnalyzer: Error reading file {file_path}: {e}")
            raise
        
        return crashes
    
    def _format_results(
        self,
        all_crashes: List[dict],
        total_crashes: int,
        files_with_crashes: int
    ) -> str:
        """
        Format crash results into readable output.
        
        Args:
            all_crashes: List of crash data per file
            total_crashes: Total number of crashes found
            files_with_crashes: Number of files containing crashes
            
        Returns:
            Formatted crash report
        """
        content = "Android Crash Analysis\n"
        content += "=" * 80 + "\n\n"
        
        if total_crashes == 0:
            content += "No FATAL_EXCEPTION crashes found.\n"
            return content
        
        content += f"Total Crashes: {total_crashes}\n"
        content += f"Files with Crashes: {files_with_crashes}\n\n"
        
        # Show each crash with context
        crash_number = 1
        for file_data in all_crashes:
            file_path = file_data["file"]
            crashes = file_data["crashes"]
            
            content += "=" * 80 + "\n"
            content += f"File: {os.path.basename(file_path)}\n"
            content += f"Path: {file_path}\n"
            content += f"Crashes Found: {len(crashes)}\n"
            content += "=" * 80 + "\n\n"
            
            for crash in crashes:
                content += f"--- Crash #{crash_number} ---\n"
                content += crash + "\n\n"
                crash_number += 1
        
        return content


# Standalone execution support
if __name__ == "__main__":
    import sys
    import asyncio
    
    async def run_standalone():
        """Run insight standalone for testing."""
        if len(sys.argv) < 2:
            print("Usage: python android_crash_analyzer.py <log_file_path>")
            sys.exit(1)
        
        file_path = sys.argv[1]
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Run insight
        insight = AndroidCrashAnalyzer()
        print(f"\nRunning {insight.name}...")
        print(f"Analyzing: {file_path}\n")
        
        try:
            result = await insight.analyze([file_path])
            print(result.content)
            
            if result.metadata:
                print("\nMetadata:")
                for key, value in result.metadata.items():
                    print(f"  {key}: {value}")
                    
        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    asyncio.run(run_standalone())

