#!/usr/bin/env python
import sys
from datetime import datetime
from tv_research.crew import TVResearchCrew
from tv_research.models import ResearchResult, get_db, init_db
import os


def run(topic=None, store_in_db=False):
    """
    Run the TV Channel Research crew.

    Args:
        topic: The specific topic to research (optional, defaults to trending topics)
        store_in_db: Whether to store the result in database (default: False)
    """
    print("\n" + "="*80)
    if topic:
        print(f"🎬 TV CHANNEL RESEARCH & REPORTING TOOL - TOPIC: {topic}")
    else:
        print("🎬 TV CHANNEL RESEARCH & REPORTING TOOL - TRENDING TOPICS")
    print("="*80 + "\n")

    # Default inputs for general news research or topic-specific research
    if topic:
        inputs = {
            'channel_type': f'Special Report on {topic}',
            'time_slot': 'Prime Time Documentary/Special Segment',
            'audience_demographic': f'Educated general audience interested in {topic}',
            'production_timeline': '1-2 weeks for comprehensive coverage',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'research_focus': topic
        }
    else:
        inputs = {
            'channel_type': 'News and Entertainment',
            'time_slot': 'Prime Time',
            'audience_demographic': 'General audience aged 25-54',
            'production_timeline': '24-48 hours',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    print("📋 Research Parameters:")
    print(f"   Channel Type: {inputs['channel_type']}")
    print(f"   Time Slot: {inputs['time_slot']}")
    print(f"   Target Audience: {inputs['audience_demographic']}")
    print(f"   Production Timeline: {inputs['production_timeline']}")
    print(f"   Research Time: {inputs['timestamp']}")
    print("\n" + "-"*80 + "\n")

    print("🚀 Initializing AI research crew...")
    print("   - Trend Researcher: Identifying trending topics")
    print("   - News Aggregator: Gathering breaking news")
    print("   - Content Strategist: Developing story angles")
    print("   - Reporting Analyst: Compiling final report")
    print("\n" + "-"*80 + "\n")

    start_time = datetime.utcnow()

    try:
        crew = TVResearchCrew().crew()
        print("✅ Crew initialized successfully!")
        print("\n🔍 Starting research process...\n")

        result = crew.kickoff(inputs=inputs)

        end_time = datetime.utcnow()
        execution_time = int((end_time - start_time).total_seconds())

        print("\n" + "="*80)
        print("✅ RESEARCH COMPLETE!")
        print("="*80)
        print(f"\n📄 Report saved to: reports/tv_research_report_*.md")
        print(f"⏱️  Total execution time: {execution_time} seconds")
        print("\n💡 The crew has completed comprehensive research on trending topics")
        print("   and compiled actionable recommendations for your TV channel.\n")

        # Store result in database if requested
        if store_in_db:
            try:
                db = get_db()
                research_result = ResearchResult(
                    topic=topic,
                    status='completed',
                    completed_at=end_time,
                    result_content=str(result),
                    execution_time=execution_time
                )
                db.add(research_result)
                db.commit()
                print(f"📊 Result stored in database with ID: {research_result.id}")
            except Exception as db_error:
                print(f"⚠️  Warning: Failed to store result in database: {db_error}")
            finally:
                db.close()

        return result

    except Exception as e:
        print("\n" + "="*80)
        print("❌ ERROR OCCURRED")
        print("="*80)
        print(f"\n{str(e)}\n")

        # Store error in database if requested
        if store_in_db:
            try:
                db = get_db()
                research_result = ResearchResult(
                    topic=topic,
                    status='failed',
                    completed_at=datetime.utcnow(),
                    error_message=str(e),
                    execution_time=0
                )
                db.add(research_result)
                db.commit()
                print(f"📊 Error stored in database with ID: {research_result.id}")
            except Exception as db_error:
                print(f"⚠️  Warning: Failed to store error in database: {db_error}")
            finally:
                db.close()

        sys.exit(1)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'channel_type': 'News and Entertainment',
        'time_slot': 'Prime Time',
        'audience_demographic': 'General audience aged 25-54',
        'production_timeline': '24-48 hours',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    try:
        TVResearchCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        TVResearchCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and return the results.
    """
    inputs = {
        'channel_type': 'News and Entertainment',
        'time_slot': 'Prime Time',
        'audience_demographic': 'General audience aged 25-54',
        'production_timeline': '24-48 hours',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    try:
        TVResearchCrew().crew().test(
            n_iterations=int(sys.argv[1]),
            openai_model_name=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == "__main__":
    # Check if topic provided as command line argument or environment variable
    topic = None
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        import os
        topic = os.getenv('RESEARCH_TOPIC')

    run(topic)
