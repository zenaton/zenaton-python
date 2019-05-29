<p align="center">
  <a href="https://zenaton.com" target="_blank">
    <img src="https://user-images.githubusercontent.com/36400935/58254828-e5176880-7d6b-11e9-9094-3f46d91faeee.png" target="_blank" />
  </a><br>
  Easy Asynchronous Jobs Manager for Developers <br>
  <a href="https://zenaton.com/documentation/python/getting-started/" target="_blank">
    <strong> Explore the docs » </strong>
  </a> <br>
  <a href="https://zenaton.com" target="_blank"> Website </a>
    ·
  <a href="https://github.com/zenaton/examples-python" target="_blank"> Examples in Python </a>
    ·
  <a href="https://app.zenaton.com/tutorial/python" target="_blank"> Tutorial in Python </a>
</p>


# Zenaton library for Python

[Zenaton](https://zenaton.com) helps developers to easily run, monitor and orchestrate background jobs on your workers without managing a queuing system. In addition to this, a monitoring dashboard shows you in real-time tasks executions and helps you to handle errors.

The Zenaton library for Python lets you code and launch tasks using Zenaton platform, as well as write workflows as code. You can sign up for an account on [Zenaton](https://zenaton.com) and go through the [tutorial in python](https://app.zenaton.com/tutorial/python).

## Requirements

This package has been tested with Python 3.5.

## Python Documentation

You can find all details on [Zenaton's website](https://zenaton.com/documentation/python/getting-started).

<details>
  <summary><strong>Table of contents</strong></summary>

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Getting started](#getting-started)
  - [Installation](#installation)
    - [Install the Zenaton Agent](#install-the-zenaton-agent)
    - [Install the library](#install-the-library)
    - [Framework integration](#framework-integration)
  - [Quick start](#quick-start)
    - [Client Initialization](#client-initialization)
    - [Executing a background job](#executing-a-background-job)
  - [Orchestrating background jobs](#orchestrating-background-jobs)
    - [Using workflows](#using-workflows)
- [Getting help](#getting-help)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

</details>

## Getting started

### Installation

#### Install the Zenaton Agent

To install the Zenaton agent, run the following command:

```sh
curl https://install.zenaton.com/ | sh
```

Then, you need your agent to listen to your application.
To do this, you need your **Application ID** and **API Token**.
You can find both on [your Zenaton account](https://app.zenaton.com/api).

```sh
zenaton listen --app_id=YourApplicationId --api_token=YourApiToken --app_env=YourApplicationEnv
```

#### Install the library

To add the latest version of the library to your project, run the following command:

```Python
pip install zenaton
```

#### Framework integration

If you are using **Django**, please refer to our dedicated documentation to get started:

- [Getting started with Django](https://zenaton.com/documentation/python/agents#django)


### Quick start

#### Client Initialization

To start, you need to initialize the client. To do this, you need your **Application ID** and **API Token**.
You can find both on [your Zenaton account](https://app.zenaton.com/api).

Then, initialize your Zenaton client:

```Python
import os
from dotenv import load_dotenv

# LOADING CONFIG FROM .env file
load_dotenv()
app_id = os.getenv('ZENATON_APP_ID')
api_token = os.getenv('ZENATON_API_TOKEN')
app_env = os.getenv('ZENATON_APP_ENV')
```
#### Executing a background job

A background job in Zenaton is a class implementing the `Zenaton.abstracts.workflow.Workflow` interface.

Let's start by implementing a first task printing something, and returning a value:

```python
from zenaton.abstracts.workflow import Workflow
from zenaton.traits.zenatonable import Zenatonable

class HelloWorldTask(Workflow, Zenatonable):

        def handle(self):
            echo "Hello World\n";
            return mt_rand(0, 1);
```

Now, when you want to run this task as a background job, you need to do the following:

```python
HelloWorldTask().dispatch()
```

That's all you need to get started. With this, you can run many background jobs.
However, the real power of Zenaton is to be able to orchestrate these jobs. The next section will introduce you to job orchestration.

### Orchestrating background jobs

Job orchestration is what allows you to write complex business workflows in a simple way.
You can execute jobs sequentially, in parallel, conditionally based on the result of a previous job,
and you can even use loops to repeat some tasks.

We wrote about some use-cases of job orchestration, you can take a look at [these articles](https://medium.com/zenaton/tagged/python)
to see how people use job orchestration.

#### Using workflows

A workflow in Zenaton is a class implementing the `Zenaton.abstracts.workflow.Workflow` interface.

We will implement a very simple workflow:

First, it will execute the `HelloWorld` task.
The result of the first task will be used to make a condition using an `if` statement.
When the returned value will be greater than `0`, we will execute a second task named `FinalTask`.
Otherwise, we won't do anything else.

One important thing to remember is that your workflow implementation **must** be idempotent.
You can read more about that in our [documentation](https://zenaton.com/documentation/python/workflow-basics/#implementation).

The implementation looks like this:

```python
from zenaton.abstracts.workflow import Workflow
from zenaton.traits.zenatonable import Zenatonable

class MyFirstWorkflow(Workflow, Zenatonable):

    def handle(self):
        $n = HelloWorldTask().execute()

        if $n > 0:
            FinalTask().execute()
```

Now that your workflow is implemented, you can execute it by calling the `dispatch` method:

```python
MyFirstWorkflow().dispatch()
```

If you really want to run this example, you will need to implement the `FinalTask` task.

There are many more features usable in workflows in order to get the orchestration done right. You can learn more
in our [documentation](https://zenaton.com/documentation/python/workflow-basics/#implementation).

## Getting help

**Need help**? Feel free to contact us by chat on [Zenaton](https://zenaton.com/).

**Found a bug?** You can open a [GitHub issue](https://github.com/zenaton/zenaton-python/issues).


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
