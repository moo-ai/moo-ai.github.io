# Machine Learning On OpenLab

The repo for AI model deployment on openlab

## How to use

Visit the [page](http://moo-ai.github.io/workflow.html) to upload your AI training or
inference data.

Your data is usually be a ZIP file or a link which can reference your ZIP file.

The ZIP file must contain the files following:
  * A YAML file describe your data.
  * The training set to train your model.
  * The scripts you wrote for the specified AI framework. For example, the `py`
    file for `tensorflow`.

The YAML file should contain some key-value paris to describe your model. It
includes:
  * **framework** : Framework's name, version and runtime.
  * **entry_point** : The entry file for your scripts.
  * **output_folder**(optional) : The output place for saving the training or
    inference result. This is the folder which your script using for storing
    the trained model or something specified.

Here is an example:

```
framework:
  name: tensorflow
  version: 1.0.0
  runtime: python2.7
model:
  name: EMNIST
entry_point: training_test.py
output_folder: training_result
```

Once the ZIP file or the ZIP link is submitted, You will receive an IP address
of the VM which is running your training or inference task. Once the task is
down, you can receive an URL where you can get the task's result, and the
related logs as well. During the task, you can ssh to the VM to take a look at
the environment and have a try.
