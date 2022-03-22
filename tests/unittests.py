import sys
sys.path.append('.')
import numpy as np
import pytest
import get_repo_metadata
import get_contributors
import get_issues
import process_ingested_data
import extract_entities
import extract_phrase_chunks
import get_issue_comments
import compute_issue_comment_stats
import read_credentials


@pytest.fixture(scope='module')
def get_creds():
    token = read_credentials.get_credentials()
    yield token

@pytest.fixture(scope='module')
def get_creds_path():
    yield '/Users/srijith.rajamohan/.github/credentials'

def test_get_creds():
    token = read_credentials.get_credentials()
    assert(token is not None)

def test_get_creds_path(get_creds_path):
    token = read_credentials.get_credentials(get_creds_path)
    assert(token is not None)

def test_get_repo_metadata(get_creds_path):
   res = get_repo_metadata.get_metadata(credentials_path=get_creds_path)
   assert(res == 0)

def test_get_contributors(get_creds_path):
   res = get_contributors.get_contributors(credentials_path=get_creds_path, TEST=True)
   assert(res == 0)

def test_get_issues(get_creds_path):
   res = get_issues.get_github_issues(credentials_path=get_creds_path, TEST=True)
   assert(res == 0)

def test_process_ingested_data():
   res = process_ingested_data.process()
   assert(res == 0)

def test_extract_entities():
   res = extract_entities.extract()
   assert(res == 0)

def test_extract_phrase_chunks():
   res = extract_phrase_chunks.extract()
   assert(res == 0)

def test_get_issue_comments(get_creds_path):
   res = get_issue_comments.get_issue_comments(credentials_path=get_creds_path, TEST=True)
   assert(res == 0)

def compute_issue_comment_stats():
   res = compute_issue_comment_stats.compute_stats()
   assert(res == 0)
