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
- Authorizations (middleware)

Each `model` is assigned a unique pair of Flask blueprints (one for endpoints containing middleware and one for endpoints without middleware).

Those blueprints are registed into the Flask `app` and exposed as API endpoints.

### Behaviors:
##### Classes that contain the functionality of a model.
- A `Behavior` is a class that must implement a function `_bind` which binds funcetions to REST endpoints. When a request is made to an endpoint, the function
bound to that endpoint is called. A single `Behavior` can bind multiple functions to multiple endpoints.

- When sleepful generates the internal structure of the API, multiple `Behavior`s are amalgamated into a `model`.

- `Behavior`s can require `init_params` to be succssefully initilized.

**Note:** Behaviors allow for inheritance, but only the **highest level** necessary Behavior should be specified in the `config.json` to avoid MRO complications.
**Example:** if a model should be `Listable`, it should not also be `Indexable` since `Listable` is derived from `Indexable`

### Data handlers:
##### Classes that wrap interactions with databases.
A `DataHandler` abstracts away interactions with a database or any data source (as shown by the `FilesysData` implementation) for `Behavior`s.
This allows `sleepful` to be database agnostic.

### Authorization (middleware)
###### *W.I.P*
##### Packages that run functions prior to the functions bound to endpoints by `Behavior`s

## Advanced usage:
`sleepful` allows for external `Authorizer`s, `Behavior`s and `DataHandler`s to be imported.

### Writing your own extensions

##### Behavior:
All a custom `Behavior` must do is inherit from an existing `Behavior` or from the base `Behavior` class.

##### Data handler:
All a custom `DataHandler` must do is inherit from an existing `DataHandler` or the base `DataHandler` class.

##### Authorizer:
All a custmo `Authorizer` must do is contain an `auth` function, that will be ran as middleware.
