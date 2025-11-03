from src.tv_research.models import ResearchResult, get_db

try:
    db = get_db()
    results = db.query(ResearchResult).all()

    print("Research Results in Database:")
    for r in results:
        print(f"ID: {r.id}, Status: {r.status}, Topic: {r.topic}")
        if r.completed_at:
            print(f"  Completed: {r.completed_at}")
        if r.error_message:
            print(f"  Error: {r.error_message}")

    db.close()

except Exception as e:
    print(f"Error: {e}")
