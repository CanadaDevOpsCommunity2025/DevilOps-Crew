#!/usr/bin/env python
"""
Topic Deep Dive Research Example

Performs comprehensive research on a specific topic for special segments,
documentaries, or in-depth coverage.

Usage (Docker):
    docker compose run --rm tv-crew python examples/topic_research.py

Custom topic:
    docker compose run --rm tv-crew python -c "
    from examples.topic_research import research_topic
    research_topic('AI in Healthcare')
    "
"""

import sys
from datetime import datetime
from tv_research.crew import TVResearchCrew


def research_topic(topic="Climate Change and Renewable Energy"):
    """
    Research a specific topic in depth.

    Args:
        topic: The topic to research
    """
    print("\n" + "="*80)
    print(f"🔬 DEEP DIVE RESEARCH: {topic}")
    print("="*80 + "\n")

    # Configure for in-depth topic research
    inputs = {
        'channel_type': f'Special Report on {topic}',
        'time_slot': 'Prime Time Documentary/Special Segment',
        'audience_demographic': 'Educated general audience interested in ' + topic,
        'production_timeline': '1-2 weeks for comprehensive coverage',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'research_focus': topic
    }

    print("🎯 Research Configuration:")
    print(f"   Topic: {topic}")
    print(f"   Format: In-depth special segment")
    print(f"   Audience: {inputs['audience_demographic']}")
    print(f"   Timeline: {inputs['production_timeline']}")
    print(f"   Started: {inputs['timestamp']}")
    print("\n" + "-"*80 + "\n")

    print(f"🚀 Conducting comprehensive research on '{topic}'...\n")
    print("This will include:")
    print("   • Current trends and developments")
    print("   • Expert opinions and interviews")
    print("   • Historical context and future outlook")
    print("   • Visual storytelling opportunities")
    print("   • Multiple story angles for diverse coverage\n")

    crew = TVResearchCrew().crew()
    result = crew.kickoff(inputs=inputs)

    print("\n" + "="*80)
    print("✅ DEEP DIVE RESEARCH COMPLETE!")
    print("="*80)
    print(f"\n📄 Comprehensive report on '{topic}' is ready!\n")
    print("💡 Your report includes:")
    print("   • Detailed topic analysis with multiple perspectives")
    print("   • Expert interview recommendations")
    print("   • Story arc suggestions for compelling narrative")
    print("   • B-roll and visual element requirements")
    print("   • Production roadmap for full coverage\n")

    return result


def main():
    # Check if topic provided as command line argument
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = "Climate Change and Renewable Energy"

    return research_topic(topic)


if __name__ == "__main__":
    main()
