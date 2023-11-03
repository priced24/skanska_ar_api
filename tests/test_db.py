import pytest
from sqlalchemy import text
import sqlite3

# Add test for closing the database

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('api.database.init_db', fake_init_db)
    result = runner.invoke(args=['init_db'])
    assert 'Database Initialized' in result.output
    assert Recorder.called