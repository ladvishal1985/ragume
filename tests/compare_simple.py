"""
Simple RAG Evaluation Comparison Dashboard

Compares RAG evaluation results across different runs to track improvements.
Works without RAGAS - just compares your answers to ground truth.
"""

import json
import os
from datetime import datetime
from pathlib import Path


class SimpleComparator:
    def __init__(self, base_dir="tests"):
        self.base_dir = Path(base_dir)
        self.reports_dir = self.base_dir / "reports"
        self.reports_dir.mkdir(exist_ok=True)
        
        self.results_file = self.reports_dir / "rag_evaluation_results.json"
        self.history_file = self.reports_dir / "rag_evaluation_history.json"
    
    def load_current_results(self):
        """Load the most recent evaluation results"""
        if not self.results_file.exists():
            print("X No results file found. Run evaluation first:")
            print("   python tests/evaluate_simple.py")
            return None
        
        with open(self.results_file) as f:
            return json.load(f)
    
    def load_history(self):
        """Load historical results"""
        if not self.history_file.exists():
            return []
        
        with open(self.history_file) as f:
            return json.load(f)
    
    def save_to_history(self, results):
        """Save current results to history"""
        history = self.load_history()
        history.append(results)
        history = history[-20:]  # Keep last 20 runs
        
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)
        
        print(f"OK Saved to history ({len(history)} runs tracked)")
    
    def compare_latest_two(self):
        """Compare the two most recent runs"""
        history = self.load_history()
        
        if len(history) < 2:
            print("❌ Need at least 2 runs to compare")
            print(f"   Current runs: {len(history)}")
            return
        
        before = history[-2]
        after = history[-1]
        
        print("\n" + "="*70)
        print("BEFORE vs AFTER COMPARISON")
        print("="*70)
        
        print(f"\nBefore: {before['timestamp'][:19]}")
        print(f"After:  {after['timestamp'][:19]}")
        
        print("\n" + "-"*70)
        print(f"{'Question':<50} {'Before':>8} {'After':>8}")
        print("-"*70)
        
        improvements = 0
        declines = 0
        
        for i, (b_result, a_result) in enumerate(zip(before['results'], after['results'])):
            question = b_result['question'][:47] + "..."
            before_match = b_result['match']
            after_match = a_result['match']
            
            if before_match == "?" and after_match == "OK":
                improvements += 1
                change = "^"
            elif before_match == "OK" and after_match == "?":
                declines += 1
                change = "v"
            else:
                change = "="
            
            print(f"{question:<50} {before_match:>8} {after_match:>8} {change}")
        
        print("-"*70)
        print(f"\nImprovements: {improvements}")
        print(f"Declines: {declines}")
        print(f"No change: {len(before['results']) - improvements - declines}")
        
        if improvements > declines:
            print("\nOK Overall: IMPROVED! ")
        elif declines > improvements:
            print("\n!  Overall: DECLINED")
        else:
            print("\n= Overall: NO CHANGE")
    
    def show_all_history(self):
        """Show all historical results"""
        history = self.load_history()
        
        if not history:
            print("❌ No history found")
            return
        
        print("\n" + "="*70)
        print("EVALUATION HISTORY")
        print("="*70)
        print(f"Total runs: {len(history)}\n")
        
        print(f"{'#':<4} {'Date':<20} {'Total':>7} {'Matches':>8} {'%':>6}")
        print("-"*70)
        
        for i, result in enumerate(history, 1):
            timestamp = result['timestamp'][:19]
            total = result['total_questions']
            matches = sum(1 for r in result['results'] if r['match'] == "OK")
            percentage = (matches / total * 100) if total > 0 else 0
            
            print(f"{i:<4} {timestamp:<20} {total:>7} {matches:>8} {percentage:>5.1f}%")
        
        if len(history) >= 2:
            first_matches = sum(1 for r in history[0]['results'] if r['match'] == "OK")
            last_matches = sum(1 for r in history[-1]['results'] if r['match'] == "OK")
            total = history[0]['total_questions']
            
            first_pct = (first_matches / total * 100) if total > 0 else 0
            last_pct = (last_matches / total * 100) if total > 0 else 0
            change = last_pct - first_pct
            
            print("\n" + "-"*70)
            print(f"Total progress: {change:+.1f}% ({first_pct:.1f}% -> {last_pct:.1f}%)")
    
    def generate_markdown_report(self):
        """Generate a markdown comparison report"""
        history = self.load_history()
        
        if len(history) < 2:
            print("❌ Need at least 2 runs for report")
            return
        
        before = history[-2]
        after = history[-1]
        
        report = f"""# RAG Evaluation Comparison Report

## Run Details

- **Before**: {before['timestamp']}
- **After**: {after['timestamp']}

## Question-by-Question Comparison

| # | Question | Before | After | Change |
|---|----------|--------|-------|--------|
"""
        
        for i, (b_result, a_result) in enumerate(zip(before['results'], after['results']), 1):
            question = b_result['question'][:60]
            before_match = b_result['match']
            after_match = a_result['match']
            
            if before_match == "?" and after_match == "OK":
                change = "✅ Improved"
            elif before_match == "OK" and after_match == "?":
                change = "! Declined"
            else:
                change = "➖ No change"
            
            report += f"| {i} | {question} | {before_match} | {after_match} | {change} |\n"
        
        # Summary
        improvements = sum(1 for b, a in zip(before['results'], after['results']) 
                          if b['match'] == "?" and a['match'] == "OK")
        declines = sum(1 for b, a in zip(before['results'], after['results']) 
                      if b['match'] == "OK" and a['match'] == "?")
        
        report += f"""
## Summary

- **Improvements**: {improvements}
- **Declines**: {declines}
- **No change**: {len(before['results']) - improvements - declines}

"""
        
        if improvements > declines:
            report += "✅ **Overall**: System improved!\n\n"
        elif declines > improvements:
            report += "! **Overall**: System declined.\n\n"
        else:
            report += "➖ **Overall**: No significant change.\n\n"
        
        # Detailed answers
        report += "## Detailed Answers\n\n"
        
        for i, (b_result, a_result) in enumerate(zip(before['results'], after['results']), 1):
            if b_result['match'] != a_result['match']:  # Only show changed ones
                report += f"### {i}. {b_result['question']}\n\n"
                report += f"**Ground Truth**: {b_result['ground_truth'][:200]}...\n\n"
                report += f"**Before** ({b_result['match']}): {b_result['rag_answer'][:200]}...\n\n"
                report += f"**After** ({a_result['match']}): {a_result['rag_answer'][:200]}...\n\n"
                report += "---\n\n"
        
        # Save report
        report_file = self.reports_dir / "simple_comparison_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\nOK Report saved to {report_file}")
        
        return report


def main():
    comparator = SimpleComparator()
    
    # Load current results
    current = comparator.load_current_results()
    
    if not current:
        return
    
    print("\n" + "="*70)
    print("SIMPLE RAG EVALUATION COMPARISON")
    print("="*70)
    
    # Save to history
    comparator.save_to_history(current)
    
    # Show comparison
    comparator.compare_latest_two()
    
    # Show full history
    comparator.show_all_history()
    
    # Generate markdown report
    comparator.generate_markdown_report()


if __name__ == "__main__":
    main()
