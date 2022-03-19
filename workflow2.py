from metaflow import FlowSpec, Parameter, step
import get_repo_metadata
import get_issues
import process_ingested_data
import extract_entities
import extract_phrase_chunks
import get_contributors
import get_issue_comments
import read_credentials
import compute_issue_comment_stats
import os


class ForeachFlow(FlowSpec):
    infrastructure = Parameter('infra', help='select databricks or local', default='local')
    credentials_path = Parameter('credentials', help='path to credentials file', default='~/.github/credentials')

    @step
    def start(self):
        print(f"Starting workflow on {self.infrastructure} with credentials from {self.credentials_path}")
        read_credentials.get_credentials(self.credentials_path)
        self.next(self.get_issue_comments_step)

    @step
    def get_issue_comments_step(self):
        res = get_issue_comments.get_issue_comments(self.credentials_path)
        print('Job status from issue comments ingestion ',res)
        self.next(self.compute_issue_comment_stats_step)

    @step
    def compute_issue_comment_stats_step(self):
        res = compute_issue_comment_stats.compute_stats()
        print('Job status from comment stats ',res)
        self.next(self.end)

    @step
    def end(self):
            print("Done")


if __name__ == '__main__':
    ForeachFlow()
