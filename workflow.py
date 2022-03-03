from metaflow import FlowSpec, step
import get_repo_metadata
import get_issues
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
        self.next(self.end)

    @step
    def end(self):
        print("Done")

if __name__ == '__main__':
    ForeachFlow()
