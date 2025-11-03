#!/usr/bin/env python
"""
Weekly Trending Report Example

Generates a comprehensive weekly roundup of trending topics perfect for
weekend programming, social media content, and next week's planning.

Usage (Docker):
    docker compose run --rm tv-crew python examples/weekly_trends.py
"""

from datetime import datetime
from tv_research.crew import TVResearchCrew


def main():
    print("\n" + "="*80)
    print("📊 WEEKLY TRENDS REPORT GENERATOR")
    print("="*80 + "\n")

    # Configure for weekly trends analysis
    inputs = {
        'channel_type': 'Weekend Programming / Social Media Content',
        'time_slot': 'Weekend Review Shows / Online Content',
        'audience_demographic': 'General audience, social media users',
        'production_timeline': '3-5 days for full production',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'report_type': 'weekly_trends'
    }

    print("🎯 Report Configuration:")
    print(f"   Type: Weekly Trends Roundup")
    print(f"   Target: Weekend shows and social content")
    print(f"   Audience: {inputs['audience_demographic']}")
    print(f"   Production Window: {inputs['production_timeline']}")
    print(f"   Generated: {inputs['timestamp']}")
    print("\n" + "-"*80 + "\n")

    print("🚀 Analyzing this week's trending topics...\n")
    print("Coverage includes:")
    print("   • Top viral moments and stories of the week")
    print("   • Social media engagement metrics")
    print("   • Emerging trends to watch")
    print("   • Entertainment, news, and pop culture highlights")
    print("   • Content ideas for next week\n")

    crew = TVResearchCrew().crew()
    result = crew.kickoff(inputs=inputs)

    print("\n" + "="*80)
    print("✅ WEEKLY TRENDS REPORT COMPLETE!")
    print("="*80)
    print("\n📄 Your comprehensive weekly roundup is ready!\n")
    print("💡 This report includes:")
    print("   • Week's top trending topics with engagement data")
    print("   • Social media highlights and viral moments")
    print("   • Story angles for weekend programming")
    print("   • Content calendar suggestions for next week")
    print("   • Cross-platform content opportunities\n")

    return result


if __name__ == "__main__":
    main()
