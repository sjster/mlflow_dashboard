from metaflow import FlowSpec, step
import get_repo_metadata
import get_issues
import process_ingested_data
import extract_entities
import extract_phrase_chunks
import os

class ForeachFlow(FlowSpec):

    @step
    def start(self):
        print("Starting workflow")
        self.next(self.get_metadata)

    @step
    def get_metadata(self):
        res = get_repo_metadata.get_metadata()
        print('Job status from metadata ingestion ',res)
        self.next(self.get_issues)

    @step
    def get_issues(self):
        res = get_issues.get_github_issues()
        print('Job status from GitHub issues ingestion step',res)
        self.next(self.process_ingested_data)

    @step
    def process_ingested_data(self):
        res = process_ingested_data.process()
        print('Job status from data process step',res)
        self.next(self.extract_entities, self.extract_phrase_chunks)

    @step
    def extract_entities(self):
        res = extract_entities.extract()
        print('Job status from extract entities step',res)
        self.next(self.end)

    @step
    def extract_phrase_chunks(self):
        res = extract_phrase_chunks.extract()
        print('Job status from extract phrase chunks step',res)
        self.next(self.end)

    @step
    def end(self, inputs):
        print("Done")

if __name__ == '__main__':
    ForeachFlow()
