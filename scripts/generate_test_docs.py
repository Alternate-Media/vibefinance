#!/usr/bin/env python3
import os
import re
from pathlib import Path
from typing import List, Dict, NamedTuple

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
TESTS_DIR = PROJECT_ROOT / "backend" / "tests"
GLOBAL_REPORT_PATH = PROJECT_ROOT / "docs" / "reports" / "TEST_CASES.md"

# Ensure reports directory exists
GLOBAL_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

class TestCase(NamedTuple):
    file_path: Path
    line_number: int
    category: str
    description: str
    expectation: str

def parse_file(file_path: Path) -> List[TestCase]:
    """Scans a file for @TESTCASE annotations."""
    cases = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    current_case = {}
    
    # Regex to capture the @TESTCASE line
    # Matches: # @TESTCASE: Category - Description
    regex_header = re.compile(r"^\s*#\s*@TESTCASE:\s*(.*?)\s*-\s*(.*)")
    # Regex to capture the Expectation line
    # Matches: # Expectation: ...
    regex_expectation = re.compile(r"^\s*#\s*Expectation:\s*(.*)")

    for i, line in enumerate(lines):
        match_header = regex_header.match(line)
        if match_header:
            current_case = {
                "line": i + 1,
                "category": match_header.group(1).strip(),
                "description": match_header.group(2).strip(),
                "expectation": "N/A" # Default
            }
            # Look ahead for expectation or other details if needed
            # For now, we assume the very next comment line *might* be expectation 
            # or it might be separated. Let's look at the next few lines?
            # The spec said:
            # # @TESTCASE: ...
            # # Expectation: ...
            # So likely immediately following.
            continue

        if current_case:
            match_expect = regex_expectation.match(line)
            if match_expect:
                current_case["expectation"] = match_expect.group(1).strip()
                # Case complete
                cases.append(TestCase(
                    file_path=file_path,
                    line_number=current_case["line"],
                    category=current_case["category"],
                    description=current_case["description"],
                    expectation=current_case["expectation"]
                ))
                current_case = {} # Reset
            elif not line.strip().startswith("#"):
                # If we hit code without finding Expectation, we save what we have?
                # Or require Expectation? 
                # The prompt example showed them together. 
                # Let's save it if we hit a def or non-comment.
                cases.append(TestCase(
                    file_path=file_path,
                    line_number=current_case["line"],
                    category=current_case["category"],
                    description=current_case["description"],
                    expectation=current_case.get("expectation", "Not specified")
                ))
                current_case = {}

    return cases

def generate_markdown(cases: List[TestCase], title: str) -> str:
    if not cases:
        return f"# {title}\n\n*No test cases found.*\n"
    
    md = f"# {title}\n\n"
    md += f"**Total Test Cases:** {len(cases)}\n\n"
    
    # Group by file
    files = sorted(list(set(c.file_path for c in cases)))
    
    for fp in files:
        rel_path = fp.relative_to(PROJECT_ROOT)
        md += f"## 📄 `{rel_path}`\n\n"
        file_cases = [c for c in cases if c.file_path == fp]
        
        md += "| Category | Test Case | Expectation | Line |\n"
        md += "|----------|-----------|-------------|------|\n"
        
        for c in file_cases:
            md += f"| **{c.category}** | {c.description} | {c.expectation} | [Go]({fp.name}#L{c.line_number}) |\n"
        md += "\n"
        
    return md

def main():
    print(f"🔍 Scanning {TESTS_DIR} for @TESTCASE tags...")
    
    all_cases = []
    cases_by_dir: Dict[Path, List[TestCase]] = {}

    for root, _, files in os.walk(TESTS_DIR):
        root_path = Path(root)
        dir_cases = []
        
        for file in files:
            if file.endswith(".py") or file.endswith(".ts") or file.endswith(".js"):
                fp = root_path / file
                found = parse_file(fp)
                if found:
                    dir_cases.extend(found)
                    all_cases.extend(found)
        
        if dir_cases:
            cases_by_dir[root_path] = dir_cases

    # 1. Generate Global Report
    print(f"📝 Generating Global Report: {GLOBAL_REPORT_PATH}")
    global_md = generate_markdown(all_cases, "Global Test Case Report")
    with open(GLOBAL_REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(global_md)

    # 2. Generate Module Reports
    for dir_path, cases in cases_by_dir.items():
        report_path = dir_path / "README.md"
        print(f"📝 Generating Module Report: {report_path}")
        rel_dir = dir_path.relative_to(PROJECT_ROOT)
        module_md = generate_markdown(cases, f"Test Cases: {rel_dir}")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(module_md)

    print("✅ Done!")

if __name__ == "__main__":
    main()
