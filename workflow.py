from metaflow import FlowSpec, step
import get_repo_metadata
import get_issues
import process_ingested_data
import extract_entities
import extract_phrase_chunks
import get_contributors
import get_issue_comments
import compute_issue_comment_stats
import os

class ForeachFlow(FlowSpec):
    infrastructure = Parameter('infra', help='select databricks or local', default='local')

    @step
    def start(self):
        print("Starting workflow on ",self.infrastructure)
        self.next(self.get_metadata_step)

    @step
    def get_metadata_step(self):
        res = get_repo_metadata.get_metadata()
        print('Job status from metadata ingestion ',res)
        self.next(self.get_contributors_step)

    @step
    def get_contributors_step(self):
        res = get_contributors.get_contributors()
        print('Job status from get contributors ',res)
        self.next(self.get_issues_step)

    @step
    def get_issues_step(self):
        res = get_issues.get_github_issues()
        print('Job status from GitHub issues ingestion step ',res)
        self.next(self.process_ingested_data_step)

    @step
    def process_ingested_data_step(self):
        res = process_ingested_data.process()
        print('Job status from data process step ',res)
        self.next(self.extract_entities_step, self.extract_phrase_chunks_step)

    @step
    def extract_entities_step(self):
        res = extract_entities.extract()
        print('Job status from extract entities step ',res)
        self.next(self.get_issue_comments_step)

    @step
    def extract_phrase_chunks_step(self):
        res = extract_phrase_chunks.extract()
        print('Job status from extract phrase chunks step',res)
        self.next(self.get_issue_comments_step)

    @step
    def get_issue_comments_step(self, inputs):
        res = get_issue_comments.get_issue_comments()
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
