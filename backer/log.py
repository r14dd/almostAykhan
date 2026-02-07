import json
from datetime import datetime, timezone
from backer.db import connection


def log_qa(_question: str, _answer: str, _sources: list):
    """
    Input: question, answer, sources of answer
    Output: ()
    """

    conn = connection()
    cur = conn.cursor()
    created_at = datetime.now(timezone.utc).isoformat()
    sources_json = json.dumps(_sources, ensure_ascii=False)

    cur.execute(
        "INSERT INTO qa_logs (question, answer, sources, created_at) VALUES (?, ?, ?, ?)",
        (_question, _answer, sources_json, created_at),
    )
    conn.commit()
    conn.close()


def get_stats():
    """
    Input: ()
    Output: dict with stats
    """

    conn = connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM qa_logs")
    total = cur.fetchone()[0]


    cur.execute(
        """
        SELECT substr(created_at, 1, 10) AS day, COUNT(*)
        FROM qa_logs
        GROUP BY day
        ORDER BY day DESC
        LIMIT 7
        """
    )

    rows = cur.fetchall()
    conn.close()


    reversed_per_day = []
    i = len(rows) - 1
    while i >= 0:
        day = rows[i][0]
        count = rows[i][1]
        reversed_per_day.append({"day": day, "count": count})
        i -= 1

    return {"total": total, "per_day": reversed_per_day}

