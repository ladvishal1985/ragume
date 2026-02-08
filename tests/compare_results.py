"""
RAGAS Results Comparison Dashboard

This script compares RAGAS evaluation results across different runs to track
improvements over time. It shows before/after comparisons and visualizes progress.

Usage:
    python tests/compare_results.py
"""

import json
import os
from datetime import datetime
from pathlib import Path


class ResultsComparator:
    def __init__(self, results_dir="tests"):
        self.results_dir = Path(results_dir)
        self.results_file = self.results_dir / "ragas_results.json"
        self.history_file = self.results_dir / "ragas_history.json"
    
    def load_current_results(self):
        """Load the most recent RAGAS results."""
        if not self.results_file.exists():
            print("❌ No results file found. Run evaluation first:")
            print("   python tests/evaluate_with_ragas.py")
            return None
        
        with open(self.results_file) as f:
            return json.load(f)
    
    def load_history(self):
        """Load historical results."""
        if not self.history_file.exists():
            return []
        
        with open(self.history_file) as f:
            return json.load(f)
    
    def save_to_history(self, results):
        """Save current results to history."""
        history = self.load_history()
        
        # Add current results to history
        history.append(results)
        
        # Keep only last 20 runs
        history = history[-20:]
        
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)
        
        print(f"✓ Saved to history ({len(history)} runs tracked)")
    
    def compare_latest_two(self):
        """Compare the two most recent runs."""
        history = self.load_history()
        
        if len(history) < 2:
            print("❌ Need at least 2 runs to compare")
            print(f"   Current runs: {len(history)}")
            return
        
        before = history[-2]
        after = history[-1]
        
        print("\n" + "="*60)
        print("BEFORE vs AFTER COMPARISON")
        print("="*60)
        
        print(f"\nBefore: {before['timestamp']}")
        print(f"After:  {after['timestamp']}")
        
        print("\n" + "-"*60)
        print(f"{'Metric':<30} {'Before':>10} {'After':>10} {'Change':>10}")
        print("-"*60)
        
        metrics = before['metrics']
        total_improvement = 0
        
        for metric_name in metrics.keys():
            if metric_name == "overall":
                continue
            
            before_score = before['metrics'][metric_name]
            after_score = after['metrics'][metric_name]
            change = after_score - before_score
            total_improvement += change
            
            # Format change with color indicator
            change_str = f"{change:+.4f}"
            if change > 0:
                indicator = "↑"
            elif change < 0:
                indicator = "↓"
            else:
                indicator = "="
            
            print(f"{metric_name:<30} {before_score:>10.4f} {after_score:>10.4f} {change_str:>9} {indicator}")
        
        # Overall comparison
        before_overall = before['metrics']['overall']
        after_overall = after['metrics']['overall']
        overall_change = after_overall - before_overall
        
        print("-"*60)
        print(f"{'OVERALL':<30} {before_overall:>10.4f} {after_overall:>10.4f} {overall_change:>+10.4f}")
        
        # Summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        
        if overall_change > 0:
            print(f"✓ Overall improvement: {overall_change:+.2%}")
            print("  Great work! The changes improved accuracy.")
        elif overall_change < 0:
            print(f"✗ Overall decline: {overall_change:+.2%}")
            print("  Consider reverting recent changes.")
        else:
            print("= No change in overall score")
        
        # Biggest improvements/declines
        changes = {
            metric: after['metrics'][metric] - before['metrics'][metric]
            for metric in metrics.keys() if metric != "overall"
        }
        
        best_improvement = max(changes.items(), key=lambda x: x[1])
        worst_change = min(changes.items(), key=lambda x: x[1])
        
        print(f"\nBiggest improvement: {best_improvement[0]} ({best_improvement[1]:+.4f})")
        print(f"Biggest decline: {worst_change[0]} ({worst_change[1]:+.4f})")
    
    def show_all_history(self):
        """Show all historical results."""
        history = self.load_history()
        
        if not history:
            print("❌ No history found")
            return
        
        print("\n" + "="*60)
        print("EVALUATION HISTORY")
        print("="*60)
        print(f"Total runs: {len(history)}\n")
        
        print(f"{'#':<4} {'Date':<20} {'Overall':>10} {'Faithfulness':>12} {'Relevancy':>10}")
        print("-"*60)
        
        for i, result in enumerate(history, 1):
            timestamp = result['timestamp'][:19]  # Remove microseconds
            overall = result['metrics']['overall']
            faithfulness = result['metrics'].get('faithfulness', 0)
            relevancy = result['metrics'].get('answer_relevancy', 0)
            
            print(f"{i:<4} {timestamp:<20} {overall:>10.4f} {faithfulness:>12.4f} {relevancy:>10.4f}")
        
        # Show trend
        if len(history) >= 2:
            first_overall = history[0]['metrics']['overall']
            last_overall = history[-1]['metrics']['overall']
            total_change = last_overall - first_overall
            
            print("\n" + "-"*60)
            print(f"Total progress: {total_change:+.4f} ({total_change/first_overall:+.1%})")
    
    def generate_markdown_report(self):
        """Generate a markdown report for easy viewing."""
        history = self.load_history()
        
        if len(history) < 2:
            print("❌ Need at least 2 runs for report")
            return
        
        before = history[-2]
        after = history[-1]
        
        report = f"""# RAGAS Evaluation Comparison Report

## Run Details

- **Before**: {before['timestamp']}
- **After**: {after['timestamp']}

## Metrics Comparison

| Metric | Before | After | Change | Status |
|--------|--------|-------|--------|--------|
"""
        
        for metric_name in before['metrics'].keys():
            if metric_name == "overall":
                continue
            
            before_score = before['metrics'][metric_name]
            after_score = after['metrics'][metric_name]
            change = after_score - before_score
            
            if change > 0:
                status = "✅ Improved"
            elif change < 0:
                status = "⚠️ Declined"
            else:
                status = "➖ No change"
            
            report += f"| {metric_name} | {before_score:.4f} | {after_score:.4f} | {change:+.4f} | {status} |\n"
        
        # Overall
        before_overall = before['metrics']['overall']
        after_overall = after['metrics']['overall']
        overall_change = after_overall - before_overall
        
        if overall_change > 0:
            overall_status = "✅ Improved"
        elif overall_change < 0:
            overall_status = "⚠️ Declined"
        else:
            overall_status = "➖ No change"
        
        report += f"| **OVERALL** | **{before_overall:.4f}** | **{after_overall:.4f}** | **{overall_change:+.4f}** | **{overall_status}** |\n"
        
        # Summary
        report += f"""
## Summary

**Overall Change**: {overall_change:+.2%}

"""
        
        if overall_change > 0:
            report += "✅ **Great work!** The changes improved overall accuracy.\n\n"
        elif overall_change < 0:
            report += "⚠️ **Warning**: Overall accuracy declined. Consider reviewing recent changes.\n\n"
        
        # Recommendations
        report += "## Recommendations\n\n"
        
        for metric_name, score in after['metrics'].items():
            if metric_name == "overall":
                continue
            
            if score < 0.75:
                report += f"- **{metric_name}** is low ({score:.4f}). "
                
                if metric_name == "faithfulness":
                    report += "Focus on reducing hallucination. Improve prompt to use only provided context.\n"
                elif metric_name == "answer_relevancy":
                    report += "Answers not addressing questions well. Review prompt engineering.\n"
                elif metric_name == "context_precision":
                    report += "Retrieving irrelevant documents. Consider re-ranking or better embeddings.\n"
                elif metric_name == "context_recall":
                    report += "Missing relevant information. Increase k or improve chunking.\n"
        
        # Save report
        report_file = self.results_dir / "comparison_report.md"
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"\n✓ Report saved to {report_file}")
        
        return report


def main():
    comparator = ResultsComparator()
    
    # Load current results
    current = comparator.load_current_results()
    
    if not current:
        return
    
    print("\n" + "="*60)
    print("RAGAS RESULTS COMPARISON TOOL")
    print("="*60)
    
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
