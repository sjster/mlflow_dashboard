

### Workflow

![Workflow](graph.png)

### Usage 

#### Run the streamlit app locally

```
streamlit run streamlit_dashboard.py
```

#### Show the workflow steps

```
python workflow.py show
```

#### Run the workflow

```
python workflow.py run --infra ['databricks'|'local'] --credential '.github/credentials' 
```

#### Resume a workflow

```
python workflow.py resume
```

### Documentation

#### Generate workflow graph from metaflow using 

```
python workflow.py output-dot | dot -Tpng -o graph.png
```

#### Run metaflow check to make sure that the flow works	

```
python workflow.py check
```

#### Use pdoc to generate the documentation in HTML

This generate the HTML documentation in ./docs

1. Copy source files to ./source
2. 
```
pdoc -o docs source
```

#### OAuth authentication 

Use the following syntax for authenticating with the personal authentication token

```
curl -i -u sjster https://api.github.com/users/octocat
```

Enter personal authentication token when prompted

Or provide it on the same line as 

```
curl -i -u "sjster:TOKEN" https://api.github.com/users/octocat
```
