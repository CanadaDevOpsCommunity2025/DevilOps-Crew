#!/usr/bin/env python
"""
Daily News Brief Example

Generates a comprehensive daily briefing for morning or evening news programs.
Perfect for quick updates on trending topics and breaking news.

Usage (Docker):
    docker compose run --rm tv-crew python examples/daily_news_brief.py
"""

from datetime import datetime
from tv_research.crew import TVResearchCrew


def main():
    print("\n" + "="*80)
    print("📰 DAILY NEWS BRIEF GENERATOR")
    print("="*80 + "\n")

    # Configure for daily news briefing
    inputs = {
        'channel_type': 'Morning/Evening News',
        'time_slot': 'Morning (6-9 AM) or Evening (6-8 PM)',
        'audience_demographic': 'General news audience, working professionals',
        'production_timeline': '2-4 hours',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    print("🎯 Briefing Configuration:")
    print(f"   Type: Daily News Brief")
    print(f"   Target Slot: {inputs['time_slot']}")
    print(f"   Audience: {inputs['audience_demographic']}")
    print(f"   Turnaround: {inputs['production_timeline']}")
    print(f"   Generated: {inputs['timestamp']}")
    print("\n" + "-"*80 + "\n")

    print("🚀 Starting research for daily briefing...\n")

    crew = TVResearchCrew().crew()
    result = crew.kickoff(inputs=inputs)

    print("\n" + "="*80)
    print("✅ DAILY BRIEF COMPLETE!")
    print("="*80)
    print("\n📄 Check the reports/ directory for your comprehensive briefing.\n")
    print("💡 This briefing includes:")
    print("   • Top trending topics with engagement metrics")
    print("   • Breaking news stories with verified sources")
    print("   • Story angles optimized for news broadcast")
    print("   • Production recommendations and timelines\n")

    return result


if __name__ == "__main__":
    main()
