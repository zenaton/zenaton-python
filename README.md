# Zenaton library for Python

This Zenaton library for Python lets you code and launch workflows using Zenaton platform. You can sign up for an account at [https://zenaton/com](http://zenaton.com)

**DISCLAIMER** The Python library is currently in public beta. Please open an
issue if you find any bugs.

## Requirements

This package has been tested with Python 3.5.

## Installation

Install from pip

```Python
pip install zenaton
```

## Usage in plain Python

For more detailed examples, please check [Zenaton Python examples](https://github.com/zenaton/examples-Python).

### Client Initialization

You will need to export three environment variables: `ZENATON_APP_ID`, `ZENATON_API_TOKEN`, `ZENATON_APP_ENV`. You'll find them [here](https://zenaton/app/api).

Then you can initialize your Zenaton client:
```Python
import os
from dotenv import load_dotenv

# LOADING CONFIG FROM .env file
load_dotenv()
app_id = os.getenv('ZENATON_APP_ID')
api_token = os.getenv('ZENATON_API_TOKEN')
app_env = os.getenv('ZENATON_APP_ENV')
```

### Writing Workflows and Tasks

Writing a workflow is as simple as:

```Python
class MyWorkflow(Workflow, Zenatonable):

    def handle(self):
        # Your Workflow implementation
        MyTask().execute() # For example
```

We can create a workflow in `workflows/my_workflow.py`.

Note that your workflow implementation should be idempotent. See [documentation](https://zenaton.com/app/documentation#workflow-basics-implementation).

Writing a task is as simple as:
```Python
class MyTask(Task, Zenatonable):

    def handle(self):
        # Your Task implementation

```

And we can create a task in `tasks/my_task.py`.

### Launching a workflow

Once your Zenaton client is initialized, you can start a workflow with

```Python
MyWorkflow().dispatch()
```

### Lauching a workflow

We can start a workflow from anywhere in our application code with:
```Python
MyWorkflow().dispatch()
```

### Worker Installation

Your workflow's tasks will be executed on your worker servers. Please install a Zenaton worker on it:

    $ curl https://install.zenaton.com | sh

that you can start and configure with

    $ zenaton start && zenaton listen --env=.env --boot=boot.py

where `.env` is the env file containing your credentials, and `boot.py` is a file that will be included before each task execution - this file should load all workflow classes.


## Documentation

Please see https://zenaton.com/documentation for complete documentation.

## Usage Examples

### Theorical Examples
[Python examples repo](https://github.com/zenaton/examples-python)

### Real-life Examples
__Triggering An Email After 3 Days of Cold Weather__ ([Medium Article](https://medium.com/zenaton/triggering-an-email-after-3-days-of-cold-weather-f7bed6f2df16), [Source Code](https://github.com/zenaton/articles-python/tree/master/triggering-an-email-after-3-days-of-cold-weather))



## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/zenaton/zenaton-Python. This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [Contributor Covenant](http://contributor-covenant.org) code of conduct.

## License

The package is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).

## Code of Conduct

Everyone interacting in the zenaton-Python project’s codebases, issue trackers, chat rooms and mailing lists is expected to follow the [code of conduct](https://github.com/zenaton/zenaton-Python/blob/master/CODE_OF_CONDUCT.md).
