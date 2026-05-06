from __future__ import annotations

import sqlite3
import os
from datetime import datetime
from typing import Optional
from flask import Flask, request, jsonify, g
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE = os.path.join(os.path.dirname(__file__), 'history.db')


def get_db() -> sqlite3.Connection:
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_db(exception: Optional[Exception] = None) -> None:
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db() -> None:
    if not os.path.exists(DATABASE):
        with app.app_context():
            db = get_db()
            db.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id VARCHAR(50) NOT NULL,
                    title VARCHAR(100) NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            db.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    role VARCHAR(20) NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
                )
            ''')
            db.commit()


@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    sort = request.args.get('sort', 'recent')
    page = request.args.get('page', 1, type=int)
    per_page = 15
    offset = (page - 1) * per_page

    db = get_db()
    order = 'DESC' if sort == 'recent' else 'ASC'

    cursor = db.execute(f'''
        SELECT id, session_id, title, created_at
        FROM conversations
        ORDER BY created_at {order}
        LIMIT ? OFFSET ?
    ''', (per_page, offset))
    conversations = [dict(row) for row in cursor.fetchall()]

    cursor = db.execute('SELECT COUNT(*) as total FROM conversations')
    total = cursor.fetchone()['total']

    return jsonify({
        'conversations': conversations,
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': (total + per_page - 1) // per_page
    })


@app.route('/api/conversations/<int:conversation_id>', methods=['GET'])
def get_conversation(conversation_id: int):
    db = get_db()

    cursor = db.execute(
        'SELECT id, session_id, title, created_at FROM conversations WHERE id = ?',
        (conversation_id,)
    )
    conversation = cursor.fetchone()

    if conversation is None:
        return jsonify({'error': 'Conversation not found'}), 404

    cursor = db.execute(
        'SELECT id, role, content, created_at FROM messages WHERE conversation_id = ? ORDER BY created_at ASC',
        (conversation_id,)
    )
    messages = [dict(row) for row in cursor.fetchall()]

    return jsonify({
        'conversation': dict(conversation),
        'messages': messages
    })


@app.route('/api/conversations', methods=['POST'])
def create_conversation():
    data = request.get_json()

    if not data or 'session_id' not in data or 'messages' not in data:
        return jsonify({'error': 'Missing session_id or messages'}), 400

    session_id = data['session_id']
    messages_data = data['messages']

    if not messages_data:
        return jsonify({'error': 'Messages cannot be empty'}), 400

    first_message = messages_data[1]['content'][:20] if len(messages_data) > 1 else messages_data[0]['content'][:20]
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
    title = f'"{first_message}..." {timestamp}'

    db = get_db()
    cursor = db.execute(
        'INSERT INTO conversations (session_id, title) VALUES (?, ?)',
        (session_id, title)
    )
    conversation_id = cursor.lastrowid

    for msg in messages_data:
        db.execute(
            'INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)',
            (conversation_id, msg['role'], msg['content'])
        )

    db.commit()

    return jsonify({
        'id': conversation_id,
        'title': title,
        'created_at': datetime.now().isoformat()
    }), 201


@app.route('/api/conversations/<int:conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id: int):
    db = get_db()

    cursor = db.execute('SELECT id FROM conversations WHERE id = ?', (conversation_id,))
    if cursor.fetchone() is None:
        return jsonify({'error': 'Conversation not found'}), 404

    db.execute('DELETE FROM messages WHERE conversation_id = ?', (conversation_id,))
    db.execute('DELETE FROM conversations WHERE id = ?', (conversation_id,))
    db.commit()

    return jsonify({'success': True})


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5056, debug=True)
