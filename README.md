# sleepful
A configurable and extendable, database agnostic REST API generator based on Flask

## Basic useage:
Write up a `config.json` file and run the `driver.py`.

- For reference on the expected `json` structure of the `config` file, check out the [struct file](https://github.com/54696d654a6f6c74/sleepful/blob/master/config.struct).
- For an example `config` you can have a look at the [example confing file](https://github.com/54696d654a6f6c74/sleepful/blob/master/config.json).

## How does it work?
`sleepful` parses the `config.json` file and generates an internal structure of the API. There are 3 core components to in this process:
- Behaviors
- DataHandlers
- Middleware

Each `model` consists of containers. Each container is assigned a unique Flask blueprint.
Those blueprints are registed into the Flask `app` and exposed as API endpoints.

Containers help separate groups of `behavior`s that don't share middleware.

### Behaviors:
##### Classes that contain the functionality of a model.
- A `Behavior` is a class that must implement a function `_bind` which binds funcetions to REST endpoints. When a request is made to an endpoint, the function
bound to that endpoint is called. A single `Behavior` can bind multiple functions to multiple endpoints.

- When sleepful generates the internal structure of the API, multiple containers consiting of `Behavior`s are amalgamated into a `model`.

- `Behavior`s can require `init_params` to be succssefully initilized.

**Note:** Behaviors allow for inheritance, as a result, only the **highest level** Behavior necessary should be specified in the `config.json` to avoid MRO complications.

**For example:** if a model should be `Listable`, it should not also be `Indexable` since `Listable` is derived from `Indexable` and already carries its functionality.

### Data handlers:
##### Classes that abstract interactions with databases.
A `DataHandler` abstracts away interactions with a database or any data source (as shown by the `FilesysData` implementation) for `Behavior`s.
This allows `sleepful` to be database agnostic.

### Middleware
###### Functions that run prior to behaviors such as validators and authenticators
`Middleware`s are classes that contain a `_run` function which called prior to executing a `Behavior`. Under the hood they are registered as a `before_request` function for the Flask Blueprint associated with the container in which they're declared.
You can find more details in the [Flask docs](https://flask.palletsprojects.com/en/2.0.x/api/#flask.Flask.before_request).

`Middleware` classes may require `init_params` similarly to `Behaviors`.

**Note:** `Middleware`s are called in the order they are declared.

## Advanced usage:
`sleepful` allows for external `Authorizer`s, `Behavior`s and `DataHandler`s to be imported.

### Writing your own extensions

##### Behavior:
All a custom `Behavior` must do is inherit from an existing `Behavior` or from the base `Behavior` class.

##### Data handler:
All a custom `DataHandler` must do is inherit from an existing `DataHandler` or the base `DataHandler` class.

##### Middleware:
All a custom `Middleware` must do is inherit from an existing `Middleware` or the base `Middleware` class.
