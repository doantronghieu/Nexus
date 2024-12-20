
 
Table of contents
Opinions
Typer, the FastAPI of CLIs
Requirements
Installation
Example
Create it
Run it
Check it
Interactive API docs
Alternative API docs
Example upgrade
Interactive API docs upgrade
Alternative API docs upgrade
Recap
Performance
Dependencies
standard Dependencies
Without standard Dependencies
Additional Optional Dependencies
LicenseFastAPI framework, high performance, easy to learn, fast to code, ready for productionTest Coverage Package version Supported Python versionsDocumentation: https://fastapi.tiangolo.comSource Code: https://github.com/fastapi/
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.The key features are:Fast: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic). One of the fastest Python frameworks available.
Fast to code: Increase the speed to develop features by about 200% to 300%. *
Fewer bugs: Reduce about 40% of human (developer) induced errors. *
Intuitive: Great editor support. Completion everywhere. Less time debugging.
Easy: Designed to be easy to use and learn. Less time reading docs.
Short: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.
Robust: Get production-ready code. With automatic interactive documentation.
Standards-based: Based on (and fully compatible with) the open standards for APIs: OpenAPI (previously known as Swagger) and JSON Schema.
* estimation based on tests on an internal development team, building production applications.Sponsors¶
               Other 
Opinions¶
"[...] I'm using FastAPI a ton these days. [...] I'm actually planning to use it for all of my team's ML services at Microsoft. Some of them are getting integrated into the core Windows product and some Office products."Kabir Khan - Microsoft (ref)
"We adopted the FastAPI library to spawn a REST server that can be queried to obtain predictions. [for Ludwig]"Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - Uber (ref)
"Netflix is pleased to announce the open-source release of our crisis management orchestration framework: Dispatch! [built with FastAPI]"Kevin Glisson, Marc Vilanova, Forest Monsen - Netflix (ref)
"I’m over the moon excited about FastAPI. It’s so fun!"Brian Okken - Python Bytes podcast host (ref)
"Honestly, what you've built looks super solid and polished. In many ways, it's what I wanted Hug to be - it's really inspiring to see someone build that."Timothy Crosley - Hug creator (ref)
"If you're looking to learn one modern framework for building REST APIs, check out FastAPI [...] It's fast, easy to use and easy to learn [...]""We've switched over to FastAPI for our APIs [...] I think you'll like it [...]"Ines Montani - Matthew Honnibal - Explosion AI founders - spaCy creators (ref) - (ref)
"If anyone is looking to build a production Python API, I would highly recommend FastAPI. It is beautifully designed, simple to use and highly scalable, it has become a key component in our API first development strategy and is driving many automations and services such as our Virtual TAC Engineer."Deon Pillsbury - Cisco (ref)
Typer, the FastAPI of CLIs¶
If you are building a CLI app to be used in the terminal instead of a web API, check out Typer.Typer is FastAPI's little sibling. And it's intended to be the FastAPI of CLIs. ⌨️ 🚀Requirements¶
FastAPI stands on the shoulders of giants:Starlette for the web parts.
Pydantic for the data parts.
Installation¶
Create and activate a virtual environment and then install FastAPI:
fast →
pip inst
Note: Make sure you put "fastapi[standard]" in quotes to ensure it works in all terminals.Example¶
Create it¶
Create a file main.py with:from typing import Unionfrom fastapi import 
app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
Or use async def...
Run it¶
Run the server with:
About the command fastapi dev main.py...
Check it¶
Open your browser at http://127.0.0.1:8000/items/5q=somequery.You will see the JSON response as:
{"item_id": 5, "q": "somequery"}
You already created an API that:Receives HTTP requests in the paths / and /items/{item_id}.
Both paths take GET operations (also known as HTTP methods).
The path /items/{item_id} has a path parameter item_id that should be an int.
The path /items/{item_id} has an optional str query parameter q.
Interactive API docs¶
Now go to http://127.0.0.1:8000/docs.You will see the automatic interactive API documentation (provided by Swagger UI):Swagger UIAlternative API docs¶
And now, go to http://127.0.0.1:8000/redoc.You will see the alternative automatic documentation (provided by ReDoc):ReDocExample upgrade¶
Now modify the file main.py to receive a body from a PUT request.Declare the body using standard Python types, thanks to Pydantic.
from typing import Unionfrom fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None
@app.get("/")
def read_root():
    return {"Hello": "World"}
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
The fastapi dev server should reload automatically.Interactive API docs upgrade¶
Now go to http://127.0.0.1:8000/docs.The interactive API documentation will be automatically updated, including the new body:
Swagger UIClick on the button "Try it out", it allows you to fill the parameters and directly interact with the API:
Swagger UI interactionThen click on the "Execute" button, the user interface will communicate with your API, send the parameters, get the results and show them on the screen:
Swagger UI interactionAlternative API docs upgrade¶
And now, go to http://127.0.0.1:8000/redoc.The alternative documentation will also reflect the new query parameter and body:
ReDocRecap¶
In summary, you declare once the types of parameters, body, etc. as function parameters.You do that with standard modern Python types.You don't have to learn a new syntax, the methods or classes of a specific library, etc.Just standard Python.For example, for an int:
item_id: int
or for a more complex Item model:
item: Item
...and with that single declaration you get:Editor support, including:
Completion.
Type checks.
Validation of data:
Automatic and clear errors when the data is invalid.
Validation even for deeply nested JSON objects.
Conversion of input data: coming from the network to Python data and types. Reading from:
JSON.
Path parameters.
Query parameters.
Cookies.
Headers.
Forms.
Files.
Conversion of output data: converting from Python data and types to network data (as JSON):
Convert Python types (str, int, float, bool, list, etc).
datetime objects.
UUID objects.
Database models.
...and many more.
Automatic interactive API documentation, including 2 alternative user interfaces:
Swagger UI.
ReDoc.
Coming back to the previous code example, FastAPI will:Validate that there is an item_id in the path for GET and PUT requests.
Validate that the item_id is of type int for GET and PUT requests.
If it is not, the client will see a useful, clear error.
Check if there is an optional query parameter named q (as in http://127.0.0.1:8000/items/fooq=somequery) for GET requests.
As the q parameter is declared with = None, it is optional.
Without the None it would be required (as is the body in the case with PUT).
For PUT requests to /items/{item_id}, read the body as JSON:
Check that it has a required attribute name that should be a str.
Check that it has a required attribute price that has to be a float.
Check that it has an optional attribute is_offer, that should be a bool, if present.
All this would also work for deeply nested JSON objects.
Convert from and to JSON automatically.
Document everything with OpenAPI, that can be used by:
Interactive documentation systems.
Automatic client code generation systems, for many languages.
Provide 2 interactive documentation web interfaces directly.
We just scratched the surface, but you already get the idea of how it all works.Try changing the line with:
    return {"item_name": item.name, "item_id": item_id}
...from:
        ... "item_name": item.name ...
...to:
        ... "item_price": item.price ...
...and see how your editor will auto-complete the attributes and know their types:editor supportFor a more complete example including more features, see the Tutorial - User Guide.Spoiler alert: the tutorial - user guide includes:Declaration of parameters from other different places as: headers, cookies, form fields and files.
How to set validation constraints as maximum_length or regex.
A very powerful and easy to use Dependency Injection system.
Security and authentication, including support for OAuth2 with JWT tokens and HTTP Basic auth.
More advanced (but equally easy) techniques for declaring deeply nested JSON models (thanks to Pydantic).
GraphQL integration with Strawberry and other libraries.
Many extra features (thanks to Starlette) as:
WebSockets
extremely easy tests based on HTTPX and pytest
CORS
Cookie Sessions
...and more.
Performance¶
Independent TechEmpower benchmarks show FastAPI applications running under Uvicorn as one of the fastest Python frameworks available, only below Starlette and Uvicorn themselves (used internally by FastAPI). (*)To understand more about it, see the section Benchmarks.Dependencies¶
FastAPI depends on Pydantic and Starlette.standard Dependencies¶
When you install FastAPI with pip install "fastapi[standard]" it comes with the standard group of optional dependencies:Used by Pydantic:email-validator - for email validation.
Used by Starlette:httpx - Required if you want to use the TestClient.
jinja2 - Required if you want to use the default template configuration.
python-multipart - Required if you want to support form "parsing", with request.form().
Used by FastAPI / Starlette:uvicorn - for the server that loads and serves your application. This includes uvicorn[standard], which includes some dependencies (e.g. uvloop) needed for high performance serving.
fastapi-cli - to provide the fastapi command.
Without standard Dependencies¶
If you don't want to include the standard optional dependencies, you can install with pip install fastapi instead of pip install "fastapi[standard]".Additional Optional Dependencies¶
There are some additional dependencies you might want to install.Additional optional Pydantic dependencies:pydantic-settings - for settings management.
pydantic-extra-types - for extra types to be used with Pydantic.
Additional optional FastAPI dependencies:orjson - Required if you want to use ORJSONResponse.
ujson - Required if you want to use UJSONResponse. 
Table of contents
FastAPI Based on open standards
Automatic docs
Just Modern Python
Editor support
Short
Validation
Security and authentication
Dependency Injection
Unlimited "plug-ins"
Tested
Starlette Pydantic Features¶
FastAPI features¶
FastAPI gives you the following:Based on open standards¶
OpenAPI for API creation, including declarations of path operations, parameters, request bodies, security, etc.
Automatic data model documentation with JSON Schema (as OpenAPI itself is based on JSON Schema).
Designed around these standards, after a meticulous study. Instead of an afterthought layer on top.
This also allows using automatic client code generation in many languages.
Automatic docs¶
Interactive API documentation and exploration web user interfaces. As the framework is based on OpenAPI, there are multiple options, 2 included by default.Swagger UI, with interactive exploration, call and test your API directly from the browser.
Swagger UI interactionReDocJust Modern Python¶
It's all based on standard Python type declarations (thanks to Pydantic). No new syntax to learn. Just standard modern Python.If you need a 2 minute refresher of how to use Python types (even if you don't use FastAPI), check the short tutorial: Python Types.You write standard Python with types:
from datetime import datefrom pydantic import BaseModel# Declare a variable as a str
# and get editor support inside the function
def main(user_id: str):
    return user_id
# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
That can then be used like:
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}my_second_user: User = User(**second_user_data)
Info**second_user_data means:Pass the keys and values of the second_user_data dict directly as key-value arguments, equivalent to: User(id=4, name="Mary", joined="2018-11-30")Editor support¶
All the framework was designed to be easy and intuitive to use, all the decisions were tested on multiple editors even before starting development, to ensure the best development experience.In the Python developer surveys, it's clear that one of the most used features is "autocompletion".The whole FastAPI framework is based to satisfy that. Autocompletion works everywhere.You will rarely need to come back to the docs.Here's how your editor might help you:in Visual Studio Code:
editor supportin PyCharm:
editor supportYou will get completion in code you might even consider impossible before. As for example, the price key inside a JSON body (that could have been nested) that comes from a request.No more typing the wrong key names, coming back and forth between docs, or scrolling up and down to find if you finally used username or user_name.Short¶
It has sensible defaults for everything, with optional configurations everywhere. All the parameters can be fine-tuned to do what you need and to define the API you need.But by default, it all "just works".Validation¶
Validation for most (or all) Python data types, including:JSON objects (dict).
JSON array (list) defining item types.
String (str) fields, defining min and max lengths.
Numbers (int, float) with min and max values, etc.
Validation for more exotic types, like:URL.
Email.
UUID.
...and others.
All the validation is handled by the well-established and robust Pydantic.Security and authentication¶
Security and authentication integrated. Without any compromise with databases or data models.All the security schemes defined in OpenAPI, including:HTTP Basic.
OAuth2 (also with JWT tokens). Check the tutorial on OAuth2 with JWT.
API keys in:
Headers.
Query parameters.
Cookies, etc.
Plus all the security features from Starlette (including session cookies).All built as reusable tools and components that are easy to integrate with your systems, data stores, relational and NoSQL databases, etc.Dependency Injection¶
FastAPI includes an extremely easy to use, but extremely powerful Dependency Injection system.Even dependencies can have dependencies, creating a hierarchy or "graph" of dependencies.
All automatically handled by the framework.
All the dependencies can require data from requests and augment the path operation constraints and automatic documentation.
Automatic validation even for path operation parameters defined in dependencies.
Support for complex user authentication systems, database connections, etc.
No compromise with databases, frontends, etc. But easy integration with all of them.
Unlimited "plug-ins"¶
Or in other way, no need for them, import and use the code you need.Any integration is designed to be so simple to use (with dependencies) that you can create a "plug-in" for your application in 2 lines of code using the same structure and syntax used for your path operations.Tested¶
100% test coverage.
100% type annotated code base.
Used in production applications.
Starlette features¶
FastAPI is fully compatible with (and based on) Starlette. So, any additional Starlette code you have, will also work.FastAPI is actually a sub-class of Starlette. So, if you already know or use Starlette, most of the functionality will work the same way.With FastAPI you get all of Starlette's features (as FastAPI is just Starlette on steroids):Seriously impressive performance. It is one of the fastest Python frameworks available, on par with NodeJS and Go.
WebSocket support.
In-process background tasks.
Startup and shutdown events.
Test client built on HTTPX.
CORS, GZip, Static Files, Streaming responses.
Session and Cookie support.
100% test coverage.
100% type annotated codebase.
Pydantic features¶
FastAPI is fully compatible with (and based on) Pydantic. So, any additional Pydantic code you have, will also work.Including external libraries also based on Pydantic, as ORMs, ODMs for databases.This also means that in many cases you can pass the same object you get from a request directly to the database, as everything is validated automatically.The same applies the other way around, in many cases you can just pass the object you get from the database directly to the client.With FastAPI you get all of Pydantic's features (as FastAPI is based on Pydantic for all the data handling):No brainfuck:
No new schema definition micro-language to learn.
If you know Python types you know how to use Pydantic.
Plays nicely with your IDE/linter/brain:
Because pydantic data structures are just instances of classes you define; auto-completion, linting, mypy and your intuition should all work properly with your validated data.
Validate complex structures:
Use of hierarchical Pydantic models, Python typing’s List and Dict, etc.
And validators allow complex data schemas to be clearly and easily defined, checked and documented as JSON Schema.
You can have deeply nested JSON objects and have them all validated and annotated.
Extensible:
Pydantic allows custom data types to be defined or you can extend validation with methods on a model decorated with the validator decorator.
100% test coverage.Python Types Intro 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Motivation
Edit it
Add types
More motivation
Declaring types
Simple types
Generic types with type parameters
Newer versions of Python
List
Tuple and Set
Dict
Union
Possibly None
Using Union or Optional
Generic types
Classes as types
Pydantic models
Type Hints with Metadata Annotations
Type hints in Python Types Intro¶
Python has support for optional "type hints" (also called "type annotations").These "type hints" or annotations are a special syntax that allow declaring the type of a variable.By declaring types for your variables, editors and tools can give you better support.This is just a quick tutorial / refresher about Python type hints. It covers only the minimum necessary to use them with FastAPI... which is actually very little.FastAPI is all based on these type hints, they give it many advantages and benefits.But even if you never use FastAPI, you would benefit from learning a bit about them.NoteIf you are a Python expert, and you already know everything about type hints, skip to the next chapter.Motivation¶
Let's start with a simple example:
def get_full_name(first_name, last_name):
    full_name = first_name.title() + " " + last_name.title()
    return full_name
print(get_full_name("john", "doe"))Calling this program outputs:
John Doe
The function does the following:Takes a first_name and last_name.
Converts the first letter of each one to upper case with title().
Concatenates them with a space in the middle.def get_full_name(first_name, last_name):
    full_name = first_name.title() + " " + last_name.title()
    return full_name
print(get_full_name("john", "doe"))Edit it¶
It's a very simple program.But now imagine that you were writing it from scratch.At some point you would have started the definition of the function, you had the parameters ready...But then you have to call "that method that converts the first letter to upper case".Was it upper Was it uppercase first_uppercase capitalizeThen, you try with the old programmer's friend, editor autocompletion.You type the first parameter of the function, first_name, then a dot (.) and then hit Ctrl+Space to trigger the completion.But, sadly, you get nothing useful:Add types¶
Let's modify a single line from the previous version.We will change exactly this fragment, the parameters of the function, from:
    first_name, last_name
to:
    first_name: str, last_name: str
That's it.Those are the "type hints":
def get_full_name(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title()
    return full_name
print(get_full_name("john", "doe"))That is not the same as declaring default values like would be with:
    first_name="john", last_name="doe"
It's a different thing.We are using colons (:), not equals (=).And adding type hints normally doesn't change what happens from what would happen without them.But now, imagine you are again in the middle of creating that function, but with type hints.At the same point, you try to trigger the autocomplete with Ctrl+Space and you see:With that, you can scroll, seeing the options, until you find the one that "rings a bell":More motivation¶
Check this function, it already has type hints:
def get_name_with_age(name: str, age: int):
    name_with_age = name + " is this old: " + age
    return name_with_ageBecause the editor knows the types of the variables, you don't only get completion, you also get error checks:Now you know that you have to fix it, convert age to a string with str(age):
def get_name_with_age(name: str, age: int):
    name_with_age = name + " is this old: " + str(age)
    return name_with_ageDeclaring types¶
You just saw the main place to declare type hints. As function parameters.This is also the main place you would use them with FastAPI.Simple types¶
You can declare all the standard Python types, not only str.You can use, for example:int
float
bool
bytesdef get_items(item_a: str, item_b: int, item_c: float, item_d: bool, item_e: bytes):
    return item_a, item_b, item_c, item_d, item_d, item_eGeneric types with type parameters¶
There are some data structures that can contain other values, like dict, list, set and tuple. And the internal values can have their own type too.These types that have internal types are called "generic" types. And it's possible to declare them, even with their internal types.To declare those types and the internal types, you can use the standard Python module typing. It exists specifically to support these type hints.Newer versions of Python¶
The syntax using typing is compatible with all versions, from Python 3.6 to the latest ones, including Python 3.9, Python 3.10, etc.As Python advances, newer versions come with improved support for these type annotations and in many cases you won't even need to import and use the typing module to declare the type annotations.If you can choose a more recent version of Python for your project, you will be able to take advantage of that extra simplicity.In all the docs there are examples compatible with each version of Python (when there's a difference).For example "Python 3.6+" means it's compatible with Python 3.6 or above (including 3.7, 3.8, 3.9, 3.10, etc). And "" means it's compatible with Python 3.9 or above (including 3.10, etc).If you can use the latest versions of Python, use the examples for the latest version, those will have the best and simplest syntax, for example, "".List¶
For example, let's define a variable to be a list of str.
Declare the variable, with the same colon (:) syntax.As the type, put list.As the list is a type that contains some internal types, you put them in square brackets:
def process_items(items: list[str]):
    for item in items:
        print(item)InfoThose internal types in the square brackets are called "type parameters".In this case, str is the type parameter passed to List (or list in Python 3.9 and above).That means: "the variable items is a list, and each of the items in this list is a str".TipIf you use Python 3.9 or above, you don't have to import List from typing, you can use the same regular list type instead.By doing that, your editor can provide support even while processing items from the list:Without types, that's almost impossible to achieve.Notice that the variable item is one of the elements in the list items.And still, the editor knows it is a str, and provides support for that.Tuple and Set¶
You would do the same to declare tuples and sets:def process_items(items_t: tuple[int, int, str], items_s: set[bytes]):
    return items_t, items_sThis means:The variable items_t is a tuple with 3 items, an int, another int, and a str.
The variable items_s is a set, and each of its items is of type bytes.
Dict¶
To define a dict, you pass 2 type parameters, separated by commas.The first type parameter is for the keys of the dict.The second type parameter is for the values of the dict:def process_items(prices: dict[str, float]):
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)This means:The variable prices is a dict:
The keys of this dict are of type str (let's say, the name of each item).
The values of this dict are of type float (let's say, the price of each item).
Union¶
You can declare that a variable can be any of several types, for example, an int or a str.In Python 3.6 and above (including Python 3.10) you can use the Union type from typing and put inside the square brackets the possible types to accept.In Python 3.10 there's also a new syntax where you can put the possible types separated by a vertical bar (|).def process_item(item: int | str):
    print(item)In both cases this means that item could be an int or a str.Possibly None¶
You can declare that a value could have a type, like str, but that it could also be None.In Python 3.6 and above (including Python 3.10) you can declare it by importing and using Optional from the typing module.
from typing import Optional
def say_hi(name: Optional[str] = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")
Using Optional[str] instead of just str will let the editor help you detect errors where you could be assuming that a value is always a str, when it could actually be None too.Optional[Something] is actually a shortcut for Union[Something, None], they are equivalent.This also means that in Python 3.10, you can use Something | None:
 alternativedef say_hi(name: str | None = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")Using Union or Optional¶
If you are using a Python version below 3.10, here's a tip from my very subjective point of view:🚨 Avoid using Optional[SomeType]
Instead ✨ use Union[SomeType, None] ✨.
Both are equivalent and underneath they are the same, but I would recommend Union instead of Optional because the word "optional" would seem to imply that the value is optional, and it actually means "it can be None", even if it's not optional and is still required.I think Union[SomeType, None] is more explicit about what it means.It's just about the words and names. But those words can affect how you and your teammates think about the code.As an example, let's take this function:
from typing import Optional
def say_hi(name: Optional[str]):
    print(f"Hey {name}!")🤓 Other versions and variants
The parameter name is defined as Optional[str], but it is not optional, you cannot call the function without the parameter:
say_hi()  # Oh, no, this throws an error! 😱
The name parameter is still required (not optional) because it doesn't have a default value. Still, name accepts None as the value:
say_hi(name=None)  # This works, None is valid 🎉
The good news is, once you are on Python 3.10 you won't have to worry about that, as you will be able to simply use | to define unions of types:
def say_hi(name: str | None):
    print(f"Hey {name}!")🤓 Other versions and variants
And then you won't have to worry about names like Optional and Union. 😎Generic types¶
These types that take type parameters in square brackets are called Generic types or Generics, for example:You can use the same builtin types as generics (with square brackets and types inside):list
tuple
set
dict
And the same as with Python 3.8, from the typing module:Union
Optional (the same as with Python 3.8)
...and others.
In Python 3.10, as an alternative to using the generics Union and Optional, you can use the vertical bar (|) to declare unions of types, that's a lot better and simpler.
Classes as types¶
You can also declare a class as the type of a variable.Let's say you have a class Person, with a name:
class Person:
    def __init__(self, name: str):
        self.name = name
def get_person_name(one_person: Person):
    return one_person.nameThen you can declare a variable to be of type Person:
class Person:
    def __init__(self, name: str):
        self.name = name
def get_person_name(one_person: Person):
    return one_person.nameAnd then, again, you get all the editor support:Notice that this means "one_person is an instance of the class Person".It doesn't mean "one_person is the class called Person".Pydantic models¶
Pydantic is a Python library to perform data validation.You declare the "shape" of the data as classes with attributes.And each attribute has a type.Then you create an instance of that class with some values and it will validate the values, convert them to the appropriate type (if that's the case) and give you an object with all the data.And you get all the editor support with that resulting object.An example from the official Pydantic docs:
from datetime import datetimefrom pydantic import BaseModel
class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: datetime | None = None
    friends: list[int] = []
external_data = {
    "id": "123",
    "signup_ts": "2017-06-01 12:22",
    "friends": [1, "2", b"3"],
}
user = User(**external_data)
print(user)
# > User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]
print(user.id)
# > 123InfoTo learn more about Pydantic, check its docs.FastAPI is all based on Pydantic.You will see a lot more of all this in practice in the Tutorial - User Guide.TipPydantic has a special behavior when you use Optional or Union[Something, None] without a default value, you can read more about it in the Pydantic docs about Required Optional fields.Type Hints with Metadata Annotations¶
Python also has a feature that allows putting additional metadata in these type hints using Annotated.
In Python 3.9, Annotated is part of the standard library, so you can import it from typing.
from typing import Annotated
def say_hello(name: Annotated[str, "this is just metadata"]) -> str:
    return f"Hello {name}"Python itself doesn't do anything with this Annotated. And for editors and other tools, the type is still str.But you can use this space in Annotated to provide FastAPI with additional metadata about how you want your application to behave.The important thing to remember is that the first type parameter you pass to Annotated is the actual type. The rest, is just metadata for other tools.For now, you just need to know that Annotated exists, and that it's standard Python. 😎Later you will see how powerful it can be.TipThe fact that this is standard Python means that you will still get the best possible developer experience in your editor, with the tools you use to analyze and refactor your code, etc. ✨And also that your code will be very compatible with many other Python tools and libraries. 🚀Type hints in FastAPI¶
FastAPI takes advantage of these type hints to do several things.With FastAPI you declare parameters with type hints and you get:Editor support.
Type checks.
...and FastAPI uses the same declarations to:Define requirements: from request path parameters, query parameters, headers, bodies, dependencies, etc.
Convert data: from the request to the required type.
Validate data: coming from each request:
Generating automatic errors returned to the client when the data is invalid.
Document the API using OpenAPI:
which is then used by the automatic interactive documentation user interfaces.
This might all sound abstract. Don't worry. You'll see all this in action in the Tutorial - User Guide.The important thing is that by using standard Python types, in a single place (instead of adding more classes, decorators, etc), FastAPI will do a lot of the work for you.InfoIf you already went through all the tutorial and came back to see more about types, a good resource is the "cheat sheet" from mypy.
Concurrency and async / await
Concurrency and async / await 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Technical Details
Asynchronous Code
Concurrency and Burgers
Concurrent Burgers
Parallel Burgers
Burger Conclusion
Is concurrency better than parallelism
Concurrency + Parallelism: Web + Machine Learning
async and await
More technical details
Write your own async code
Other forms of asynchronous code
Coroutines
Conclusion
Very Technical Details
Path operation functions
Dependencies
Sub-dependencies
Other utility functions
Concurrency and async / await¶
Details about the async def syntax for path operation functions and some background about asynchronous code, concurrency, and parallelism.In a hurry¶
TL;DR:If you are using third party libraries that tell you to call them with await, like:
results = await some_library()
Then, declare your path operation functions with async def like:
@app.get('/')
async def read_results():
    results = await some_library()
    return results
NoteYou can only use await inside of functions created with async def.If you are using a third party library that communicates with something (a database, an API, the file system, etc.) and doesn't have support for using await, (this is currently the case for most database libraries), then declare your path operation functions as normally, with just def, like:
@app.get('/')
def results():
    results = some_library()
    return results
If your application (somehow) doesn't have to communicate with anything else and wait for it to respond, use async def.If you just don't know, use normal def.Note: You can mix def and async def in your path operation functions as much as you need and define each one using the best option for you. FastAPI will do the right thing with them.Anyway, in any of the cases above, FastAPI will still work asynchronously and be extremely fast.But by following the steps above, it will be able to do some performance optimizations.Technical Details¶
Modern versions of Python have support for "asynchronous code" using something called "coroutines", with async and await syntax.Let's see that phrase by parts in the sections below:Asynchronous Code
async and await
Coroutines
Asynchronous Code¶
Asynchronous code just means that the language 💬 has a way to tell the computer / program 🤖 that at some point in the code, it 🤖 will have to wait for something else to finish somewhere else. Let's say that something else is called "slow-file" 📝.So, during that time, the computer can go and do some other work, while "slow-file" 📝 finishes.Then the computer / program 🤖 will come back every time it has a chance because it's waiting again, or whenever it 🤖 finished all the work it had at that point. And it 🤖 will see if any of the tasks it was waiting for have already finished, doing whatever it had to do.Next, it 🤖 takes the first task to finish (let's say, our "slow-file" 📝) and continues whatever it had to do with it.That "wait for something else" normally refers to I/O operations that are relatively "slow" (compared to the speed of the processor and the RAM memory), like waiting for:the data from the client to be sent through the network
the data sent by your program to be received by the client through the network
the contents of a file in the disk to be read by the system and given to your program
the contents your program gave to the system to be written to disk
a remote API operation
a database operation to finish
a database query to return the results
etc.
As the execution time is consumed mostly by waiting for I/O operations, they call them "I/O bound" operations.It's called "asynchronous" because the computer / program doesn't have to be "synchronized" with the slow task, waiting for the exact moment that the task finishes, while doing nothing, to be able to take the task result and continue the work.Instead of that, by being an "asynchronous" system, once finished, the task can wait in line a little bit (some microseconds) for the computer / program to finish whatever it went to do, and then come back to take the results and continue working with them.For "synchronous" (contrary to "asynchronous") they commonly also use the term "sequential", because the computer / program follows all the steps in sequence before switching to a different task, even if those steps involve waiting.Concurrency and Burgers¶
This idea of asynchronous code described above is also sometimes called "concurrency". It is different from "parallelism".Concurrency and parallelism both relate to "different things happening more or less at the same time".But the details between concurrency and parallelism are quite different.To see the difference, imagine the following story about burgers:Concurrent Burgers¶
You go with your crush to get fast food, you stand in line while the cashier takes the orders from the people in front of you. 😍Then it's your turn, you place your order of 2 very fancy burgers for your crush and you. 🍔🍔The cashier says something to the cook in the kitchen so they know they have to prepare your burgers (even though they are currently preparing the ones for the previous clients).You pay. 💸The cashier gives you the number of your turn.While you are waiting, you go with your crush and pick a table, you sit and talk with your crush for a long time (as your burgers are very fancy and take some time to prepare).As you are sitting at the table with your crush, while you wait for the burgers, you can spend that time admiring how awesome, cute and smart your crush is ✨😍✨.While waiting and talking to your crush, from time to time, you check the number displayed on the counter to see if it's your turn already.Then at some point, it finally is your turn. You go to the counter, get your burgers and come back to the table.You and your crush eat the burgers and have a nice time. ✨InfoBeautiful illustrations by Ketrina Thompson. 🎨Imagine you are the computer / program 🤖 in that story.While you are at the line, you are just idle 😴, waiting for your turn, not doing anything very "productive". But the line is fast because the cashier is only taking the orders (not preparing them), so that's fine.Then, when it's your turn, you do actual "productive" work, you process the menu, decide what you want, get your crush's choice, pay, check that you give the correct bill or card, check that you are charged correctly, check that the order has the correct items, etc.But then, even though you still don't have your burgers, your work with the cashier is "on pause" ⏸, because you have to wait 🕙 for your burgers to be ready.But as you go away from the counter and sit at the table with a number for your turn, you can switch 🔀 your attention to your crush, and "work" ⏯ 🤓 on that. Then you are again doing something very "productive" as is flirting with your crush 😍.Then the cashier 💁 says "I'm finished with doing the burgers" by putting your number on the counter's display, but you don't jump like crazy immediately when the displayed number changes to your turn number. You know no one will steal your burgers because you have the number of your turn, and they have theirs.So you wait for your crush to finish the story (finish the current work ⏯ / task being processed 🤓), smile gently and say that you are going for the burgers ⏸.Then you go to the counter 🔀, to the initial task that is now finished ⏯, pick the burgers, say thanks and take them to the table. That finishes that step / task of interaction with the counter ⏹. That in turn, creates a new task, of "eating burgers" 🔀 ⏯, but the previous one of "getting burgers" is finished ⏹.Parallel Burgers¶
Now let's imagine these aren't "Concurrent Burgers", but "Parallel Burgers".You go with your crush to get parallel fast food.You stand in line while several (let's say 8) cashiers that at the same time are cooks take the orders from the people in front of you.Everyone before you is waiting for their burgers to be ready before leaving the counter because each of the 8 cashiers goes and prepares the burger right away before getting the next order.Then it's finally your turn, you place your order of 2 very fancy burgers for your crush and you.You pay 💸.The cashier goes to the kitchen.You wait, standing in front of the counter 🕙, so that no one else takes your burgers before you do, as there are no numbers for turns.As you and your crush are busy not letting anyone get in front of you and take your burgers whenever they arrive, you cannot pay attention to your crush. 😞This is "synchronous" work, you are "synchronized" with the cashier/cook 👨‍🍳. You have to wait 🕙 and be there at the exact moment that the cashier/cook 👨‍🍳 finishes the burgers and gives them to you, or otherwise, someone else might take them.Then your cashier/cook 👨‍🍳 finally comes back with your burgers, after a long time waiting 🕙 there in front of the counter.You take your burgers and go to the table with your crush.You just eat them, and you are done. ⏹There was not much talk or flirting as most of the time was spent waiting 🕙 in front of the counter. 😞InfoBeautiful illustrations by Ketrina Thompson. 🎨In this scenario of the parallel burgers, you are a computer / program 🤖 with two processors (you and your crush), both waiting 🕙 and dedicating their attention ⏯ to be "waiting on the counter" 🕙 for a long time.The fast food store has 8 processors (cashiers/cooks). While the concurrent burgers store might have had only 2 (one cashier and one cook).But still, the final experience is not the best. 😞This would be the parallel equivalent story for burgers. 🍔For a more "real life" example of this, imagine a bank.Up to recently, most of the banks had multiple cashiers 👨‍💼👨‍💼👨‍💼👨‍💼 and a big line 🕙🕙🕙🕙🕙🕙🕙🕙.All of the cashiers doing all the work with one client after the other 👨‍💼⏯.And you have to wait 🕙 in the line for a long time or you lose your turn.You probably wouldn't want to take your crush 😍 with you to run errands at the bank 🏦.Burger Conclusion¶
In this scenario of "fast food burgers with your crush", as there is a lot of waiting 🕙, it makes a lot more sense to have a concurrent system ⏸🔀⏯.This is the case for most of the web applications.Many, many users, but your server is waiting 🕙 for their not-so-good connection to send their requests.And then waiting 🕙 again for the responses to come back.This "waiting" 🕙 is measured in microseconds, but still, summing it all, it's a lot of waiting in the end.That's why it makes a lot of sense to use asynchronous ⏸🔀⏯ code for web APIs.This kind of asynchronicity is what made NodeJS popular (even though NodeJS is not parallel) and that's the strength of Go as a programming language.And that's the same level of performance you get with FastAPI.And as you can have parallelism and asynchronicity at the same time, you get higher performance than most of the tested NodeJS frameworks and on par with Go, which is a compiled language closer to C (all thanks to Starlette).Is concurrency better than parallelism¶
Nope! That's not the moral of the story.Concurrency is different than parallelism. And it is better on specific scenarios that involve a lot of waiting. Because of that, it generally is a lot better than parallelism for web application development. But not for everything.So, to balance that out, imagine the following short story:You have to clean a big, dirty house.Yep, that's the whole story.There's no waiting 🕙 anywhere, just a lot of work to be done, on multiple places of the house.You could have turns as in the burgers example, first the living room, then the kitchen, but as you are not waiting 🕙 for anything, just cleaning and cleaning, the turns wouldn't affect anything.It would take the same amount of time to finish with or without turns (concurrency) and you would have done the same amount of work.But in this case, if you could bring the 8 ex-cashier/cooks/now-cleaners, and each one of them (plus you) could take a zone of the house to clean it, you could do all the work in parallel, with the extra help, and finish much sooner.In this scenario, each one of the cleaners (including you) would be a processor, doing their part of the job.And as most of the execution time is taken by actual work (instead of waiting), and the work in a computer is done by a CPU, they call these problems "CPU bound".Common examples of CPU bound operations are things that require complex math processing.For example:Audio or image processing.
Computer vision: an image is composed of millions of pixels, each pixel has 3 values / colors, processing that normally requires computing something on those pixels, all at the same time.
Machine Learning: it normally requires lots of "matrix" and "vector" multiplications. Think of a huge spreadsheet with numbers and multiplying all of them together at the same time.
Deep Learning: this is a sub-field of Machine Learning, so, the same applies. It's just that there is not a single spreadsheet of numbers to multiply, but a huge set of them, and in many cases, you use a special processor to build and / or use those models.
Concurrency + Parallelism: Web + Machine Learning¶
With FastAPI you can take advantage of concurrency that is very common for web development (the same main attraction of NodeJS).But you can also exploit the benefits of parallelism and multiprocessing (having multiple processes running in parallel) for CPU bound workloads like those in Machine Learning systems.That, plus the simple fact that Python is the main language for Data Science, Machine Learning and especially Deep Learning, make FastAPI a very good match for Data Science / Machine Learning web APIs and applications (among many others).To see how to achieve this parallelism in production see the section about Deployment.async and await¶
Modern versions of Python have a very intuitive way to define asynchronous code. This makes it look just like normal "sequential" code and do the "awaiting" for you at the right moments.When there is an operation that will require waiting before giving the results and has support for these new Python features, you can code it like:
burgers = await get_burgers(2)
The key here is the await. It tells Python that it has to wait ⏸ for get_burgers(2) to finish doing its thing 🕙 before storing the results in burgers. With that, Python will know that it can go and do something else 🔀 ⏯ in the meanwhile (like receiving another request).For await to work, it has to be inside a function that supports this asynchronicity. To do that, you just declare it with async def:
async def get_burgers(number: int):
    # Do some asynchronous stuff to create the burgers
    return burgers
...instead of def:
# This is not asynchronous
def get_sequential_burgers(number: int):
    # Do some sequential stuff to create the burgers
    return burgers
With async def, Python knows that, inside that function, it has to be aware of await expressions, and that it can "pause" ⏸ the execution of that function and go do something else 🔀 before coming back.When you want to call an async def function, you have to "await" it. So, this won't work:
# This won't work, because get_burgers was defined with: async def
burgers = get_burgers(2)
So, if you are using a library that tells you that you can call it with await, you need to create the path operation functions that uses it with async def, like in:
@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
More technical details¶
You might have noticed that await can only be used inside of functions defined with async def.But at the same time, functions defined with async def have to be "awaited". So, functions with async def can only be called inside of functions defined with async def too.So, about the egg and the chicken, how do you call the first async functionIf you are working with FastAPI you don't have to worry about that, because that "first" function will be your path operation function, and FastAPI will know how to do the right thing.But if you want to use async / await without FastAPI, you can do it as well.Write your own async code¶
Starlette (and FastAPI) are based on AnyIO, which makes it compatible with both Python's standard library asyncio and Trio.In particular, you can directly use AnyIO for your advanced concurrency use cases that require more advanced patterns in your own code.And even if you were not using FastAPI, you could also write your own async applications with AnyIO to be highly compatible and get its benefits (e.g. structured concurrency).I created another library on top of AnyIO, as a thin layer on top, to improve a bit the type annotations and get better autocompletion, inline errors, etc. It also has a friendly introduction and tutorial to help you understand and write your own async code: Asyncer. It would be particularly useful if you need to combine async code with regular (blocking/synchronous) code.Other forms of asynchronous code¶
This style of using async and await is relatively new in the language.But it makes working with asynchronous code a lot easier.This same syntax (or almost identical) was also included recently in modern versions of JavaScript (in Browser and NodeJS).But before that, handling asynchronous code was quite more complex and difficult.In previous versions of Python, you could have used threads or Gevent. But the code is way more complex to understand, debug, and think about.In previous versions of NodeJS / Browser JavaScript, you would have used "callbacks". Which leads to callback hell.Coroutines¶
Coroutine is just the very fancy term for the thing returned by an async def function. Python knows that it is something like a function, that it can start and that it will end at some point, but that it might be paused ⏸ internally too, whenever there is an await inside of it.But all this functionality of using asynchronous code with async and await is many times summarized as using "coroutines". It is comparable to the main key feature of Go, the "Goroutines".Conclusion¶
Let's see the same phrase from above:Modern versions of Python have support for "asynchronous code" using something called "coroutines", with async and await syntax.That should make more sense now. ✨All that is what powers FastAPI (through Starlette) and what makes it have such an impressive performance.Very Technical Details¶
WarningYou can probably skip this.These are very technical details of how FastAPI works underneath.If you have quite some technical knowledge (coroutines, threads, blocking, etc.) and are curious about how FastAPI handles async def vs normal def, go ahead.Path operation functions¶
When you declare a path operation function with normal def instead of async def, it is run in an external threadpool that is then awaited, instead of being called directly (as it would block the server).If you are coming from another async framework that does not work in the way described above and you are used to defining trivial compute-only path operation functions with plain def for a tiny performance gain (about 100 nanoseconds), please note that in FastAPI the effect would be quite opposite. In these cases, it's better to use async def unless your path operation functions use code that performs blocking I/O.Still, in both situations, chances are that FastAPI will still be faster than (or at least comparable to) your previous framework.Dependencies¶
The same applies for dependencies. If a dependency is a standard def function instead of async def, it is run in the external threadpool.Sub-dependencies¶
You can have multiple dependencies and sub-dependencies requiring each other (as parameters of the function definitions), some of them might be created with async def and some with normal def. It would still work, and the ones created with normal def would be called on an external thread (from the threadpool) instead of being "awaited".Other utility functions¶
Any other utility function that you call directly can be created with normal def or async def and FastAPI won't affect the way you call it.This is in contrast to the functions that FastAPI calls for you: path operation functions and dependencies.If your utility function is a normal function with def, it will be called directly (as you write it in your code), not in a threadpool, if the function is created with async def then you should await for that function when you call it in your code.Again, these are very technical details that would probably be useful if you came searching for them.Otherwise, you should be good with the guidelines from the section above: In a hurry.
Python Types Intro
Environment Variables
Environment Variables 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Create and Use Env Vars
Read env vars in Python
Types and Validation
PATH Environment Variable
Installing Python and Updating the PATH
Conclusion
Environment Variables¶
TipIf you already know what "environment variables" are and how to use them, feel free to skip this.An environment variable (also known as "env var") is a variable that lives outside of the Python code, in the operating system, and could be read by your Python code (or by other programs as well).Environment variables could be useful for handling application settings, as part of the installation of Python, etc.Create and Use Env Vars¶
You can create and use environment variables in the shell (terminal), without needing Python:
Linux, macOS, Windows Bash
Windows PowerShellfast →
💬 You could create an env var MY_NAME with
exporRead env vars in Python¶
You could also create environment variables outside of Python, in the terminal (or with any other method), and then read them in Python.For example you could have a file main.py with:
import osname = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
TipThe second argument to os.getenv() is the default value to return.If not provided, it's None by default, here we provide "World" as the default value to use.Then you could call that Python program:
Linux, macOS, Windows Bash
Windows PowerShellAs environment variables can be set outside of the code, but can be read by the code, and don't have to be stored (committed to git) with the rest of the files, it's common to use them for configurations or settings.You can also create an environment variable only for a specific program invocation, that is only available to that program, and only for its duration.To do that, create it right before the program itself, on the same line:TipYou can read more about it at The Twelve-Factor App: Config.Types and Validation¶
These environment variables can only handle text strings, as they are external to Python and have to be compatible with other programs and the rest of the system (and even with different operating systems, as Linux, Windows, macOS).That means that any value read in Python from an environment variable will be a str, and any conversion to a different type or any validation has to be done in code.You will learn more about using environment variables for handling application settings in the Advanced User Guide - Settings and Environment Variables.PATH Environment Variable¶
There is a special environment variable called PATH that is used by the operating systems (Linux, macOS, Windows) to find programs to run.The value of the variable PATH is a long string that is made of directories separated by a colon : on Linux and macOS, and by a semicolon ; on Windows.For example, the PATH environment variable could look like this:
Linux, macOS
Windows/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
This means that the system should look for programs in the directories:/usr/local/bin
/usr/bin
/bin
/usr/sbin
/sbinWhen you type a command in the terminal, the operating system looks for the program in each of those directories listed in the PATH environment variable.For example, when you type python in the terminal, the operating system looks for a program called python in the first directory in that list.If it finds it, then it will use it. Otherwise it keeps looking in the other directories.Installing Python and Updating the PATH¶
When you install Python, you might be asked if you want to update the PATH environment variable.
Linux, macOS
Windows
Let's say you install Python and it ends up in a directory /opt/custompython/bin.If you say yes to update the PATH environment variable, then the installer will add /opt/custompython/bin to the PATH environment variable.It could look like this:
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
This way, when you type python in the terminal, the system will find the Python program in /opt/custompython/bin (the last directory) and use that one.
So, if you type:
Linux, macOS
Windows
The system will find the python program in /opt/custompython/bin and run it.It would be roughly equivalent to typing:
This information will be useful when learning about Virtual Environments.Conclusion¶
With this you should have a basic understanding of what environment variables are and how to use them in Python.You can also read more about them in the Wikipedia for Environment Variable.In many cases it's not very obvious how environment variables would be useful and applicable right away. But they keep showing up in many different scenarios when you are developing, so it's good to know about them.For example, you will need this information in the next section, about Virtual Environments.
Concurrency and async / await
Virtual Environments
Virtual Environments 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Create a Project
Create a Virtual Environment
Activate the Virtual Environment
Check the Virtual Environment is Active
Upgrade pip
Add .gitignore
Install Packages
Install Packages Directly
Install from requirements.txt
Run Your Program
Configure Your Editor
Deactivate the Virtual Environment
Ready to Work
Why Virtual Environments
The Problem
Where are Packages Installed
What are Virtual Environments
What Does Activating a Virtual Environment Mean
Checking a Virtual Environment
Why Deactivate a Virtual Environment
Alternatives
Conclusion
Virtual Environments¶
When you work in Python projects you probably should use a virtual environment (or a similar mechanism) to isolate the packages you install for each project.InfoIf you already know about virtual environments, how to create them and use them, you might want to skip this section. 🤓TipA virtual environment is different than an environment variable.An environment variable is a variable in the system that can be used by programs.A virtual environment is a directory with some files in it.InfoThis page will teach you how to use virtual environments and how they work.If you are ready to adopt a tool that manages everything for you (including installing Python), try uv.Create a Project¶
First, create a directory for your project.What I normally do is that I create a directory named code inside my home/user directory.And inside of that I create one directory per project.Create a Virtual Environment¶
When you start working on a Python project for the first time, create a virtual environment inside your project.TipYou only need to do this once per project, not every time you work.
venv
uv
To create a virtual environment, you can use the venv module that comes with Python.What that command meansThat command creates a new virtual environment in a directory called .venv..venv or other name
Activate the Virtual Environment¶
Activate the new virtual environment so that any Python command you run or package you install uses it.TipDo this every time you start a new terminal session to work on the project.
Linux, macOS
Windows PowerShell
Windows BashTipEvery time you install a new package in that environment, activate the environment again.This makes sure that if you use a terminal (CLI) program installed by that package, you use the one from your virtual environment and not any other that could be installed globally, probably with a different version than what you need.Check the Virtual Environment is Active¶
Check that the virtual environment is active (the previous command worked).TipThis is optional, but it's a good way to check that everything is working as expected and you are using the virtual environment you intended.
Linux, macOS, Windows Bash
Windows PowerShell
If it shows the python binary at .venv/bin/python, inside of your project (in this case awesome-project), then it worked. 🎉
Upgrade pip¶
TipIf you use uv you would use it to install things instead of pip, so you don't need to upgrade pip. 😎If you are using pip to install packages (it comes by default with Python), you should upgrade it to the latest version.Many exotic errors while installing a package are solved by just upgrading pip first.TipYou would normally do this once, right after you create the virtual environment.Make sure the virtual environment is active (with the command above) and then run:
Add .gitignore¶
If you are using Git (you should), add a .gitignore file to exclude everything in your .venv from Git.TipIf you used uv to create the virtual environment, it already did this for you, you can skip this step. 😎TipDo this once, right after you create the virtual environment.What that command means
Install Packages¶
After activating the environment, you can install packages in it.TipDo this once when installing or upgrading the packages your project needs.If you need to upgrade a version or add a new package you would do this again.Install Packages Directly¶
If you're in a hurry and don't want to use a file to declare your project's package requirements, you can install them directly.TipIt's a (very) good idea to put the packages and versions your program needs in a file (for example requirements.txt or pyproject.toml).
pip
uv
Install from requirements.txt¶
If you have a requirements.txt, you can now use it to install its packages.
pip
uvrequirements.txt
Run Your Program¶
After you activated the virtual environment, you can run your program, and it will use the Python inside of your virtual environment with the packages you installed there.Configure Your Editor¶
You would probably use an editor, make sure you configure it to use the same virtual environment you created (it will probably autodetect it) so that you can get autocompletion and inline errors.For example:VS Code
PyCharm
TipYou normally have to do this only once, when you create the virtual environment.Deactivate the Virtual Environment¶
Once you are done working on your project you can deactivate the virtual environment.This way, when you run python it won't try to run it from that virtual environment with the packages installed there.Ready to Work¶
Now you're ready to start working on your project.TipDo you want to understand what's all that aboveContinue reading. 👇🤓Why Virtual Environments¶
To work with FastAPI you need to install Python.After that, you would need to install FastAPI and any other packages you want to use.To install packages you would normally use the pip command that comes with Python (or similar alternatives).Nevertheless, if you just use pip directly, the packages would be installed in your global Python environment (the global installation of Python).The Problem¶
So, what's the problem with installing packages in the global Python environmentAt some point, you will probably end up writing many different programs that depend on different packages. And some of these projects you work on will depend on different versions of the same package. 😱For example, you could create a project called philosophers-stone, this program depends on another package called harry, using the version 1. So, you need to install harry.requires
philosophers-stone
harry vThen, at some point later, you create another project called prisoner-of-azkaban, and this project also depends on harry, but this project needs harry version 3.requires
prisoner-of-azkaban
harry v3
But now the problem is, if you install the packages globally (in the global environment) instead of in a local virtual environment, you will have to choose which version of harry to install.If you want to run philosophers-stone you will need to first install harry version 1, for example with:And then you would end up with harry version 1 installed in your global Python environment.philosophers-stone project
global env
requires
philosophers-stone
harry vBut then if you want to run prisoner-of-azkaban, you will need to uninstall harry version 1 and install harry version 3 (or just installing version 3 would automatically uninstall version 1).And then you would end up with harry version 3 installed in your global Python environment.And if you try to run philosophers-stone again, there's a chance it would not work because it needs harry version 1.prisoner-of-azkaban project
philosophers-stone project
global env
⛔️
requires
prisoner-of-azkaban
philosophers-stone
harry vharry v3
TipIt's very common in Python packages to try the best to avoid breaking changes in new versions, but it's better to be safe, and install newer versions intentionally and when you can run the tests to check everything is working correctly.Now, imagine that with many other packages that all your projects depend on. That's very difficult to manage. And you would probably end up running some projects with some incompatible versions of the packages, and not knowing why something isn't working.Also, depending on your operating system (e.g. Linux, Windows, macOS), it could have come with Python already installed. And in that case it probably had some packages pre-installed with some specific versions needed by your system. If you install packages in the global Python environment, you could end up breaking some of the programs that came with your operating system.Where are Packages Installed¶
When you install Python, it creates some directories with some files in your computer.Some of these directories are the ones in charge of having all the packages you install.When you run:That will download a compressed file with the FastAPI code, normally from PyPI.It will also download files for other packages that FastAPI depends on.Then it will extract all those files and put them in a directory in your computer.By default, it will put those files downloaded and extracted in the directory that comes with your Python installation, that's the global environment.What are Virtual Environments¶
The solution to the problems of having all the packages in the global environment is to use a virtual environment for each project you work on.A virtual environment is a directory, very similar to the global one, where you can install the packages for a project.This way, each project will have its own virtual environment (.venv directory) with its own packages.prisoner-of-azkaban project
.venv
requires
prisoner-of-azkaban
harry v3
philosophers-stone project
.venv
requires
philosophers-stone
harry vWhat Does Activating a Virtual Environment Mean¶
When you activate a virtual environment, for example with:
Linux, macOS
Windows PowerShell
Windows BashThat command will create or modify some environment variables that will be available for the next commands.One of those variables is the PATH variable.TipYou can learn more about the PATH environment variable in the Environment Variables section.Activating a virtual environment adds its path .venv/bin (on Linux and macOS) or .venv\Scripts (on Windows) to the PATH environment variable.Let's say that before activating the environment, the PATH variable looked like this:
Linux, macOS
Windows/usr/bin:/bin:/usr/sbin:/sbin
That means that the system would look for programs in:/usr/bin
/bin
/usr/sbin
/sbinAfter activating the virtual environment, the PATH variable would look something like this:
Linux, macOS
Windows/home/user/code/awesome-project/.venv/bin:/usr/bin:/bin:/usr/sbin:/sbin
That means that the system will now start looking first look for programs in:
/home/user/code/awesome-project/.venv/bin
before looking in the other directories.So, when you type python in the terminal, the system will find the Python program in
/home/user/code/awesome-project/.venv/bin/python
and use that one.
An important detail is that it will put the virtual environment path at the beginning of the PATH variable. The system will find it before finding any other Python available. This way, when you run python, it will use the Python from the virtual environment instead of any other python (for example, a python from a global environment).Activating a virtual environment also changes a couple of other things, but this is one of the most important things it does.Checking a Virtual Environment¶
When you check if a virtual environment is active, for example with:
Linux, macOS, Windows Bash
Windows PowerShellThat means that the python program that will be used is the one in the virtual environment.you use which in Linux and macOS and Get-Command in Windows PowerShell.The way that command works is that it will go and check in the PATH environment variable, going through each path in order, looking for the program called python. Once it finds it, it will show you the path to that program.The most important part is that when you call python, that is the exact "python" that will be executed.So, you can confirm if you are in the correct virtual environment.TipIt's easy to activate one virtual environment, get one Python, and then go to another project.And the second project wouldn't work because you are using the incorrect Python, from a virtual environment for another project.It's useful being able to check what python is being used. 🤓Why Deactivate a Virtual Environment¶
For example, you could be working on a project philosophers-stone, activate that virtual environment, install packages and work with that environment.And then you want to work on another project prisoner-of-azkaban.You go to that project:If you don't deactivate the virtual environment for philosophers-stone, when you run python in the terminal, it will try to use the Python from philosophers-stone.
But if you deactivate the virtual environment and activate the new one for prisoner-of-askaban then when you run python it will use the Python from the virtual environment in prisoner-of-azkaban.
Alternatives¶
This is a simple guide to get you started and teach you how everything works underneath.There are many alternatives to managing virtual environments, package dependencies (requirements), projects.Once you are ready and want to use a tool to manage the entire project, packages dependencies, virtual environments, etc. I would suggest you try uv.uv can do a lot of things, it can:Install Python for you, including different versions
Manage the virtual environment for your projects
Install packages
Manage package dependencies and versions for your project
Make sure you have an exact set of packages and versions to install, including their dependencies, so that you can be sure that you can run your project in production exactly the same as in your computer while developing, this is called locking
And many other things
Conclusion¶
If you read and understood all this, now you know much more about virtual environments than many developers out there. 🤓Knowing these details will most probably be useful in a future time when you are debugging something that seems complex, but you will know how it all works underneath. 😎
Environment Variables 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Run the code
Install Advanced User Guide
Tutorial - User Guide¶
This tutorial shows you how to use FastAPI with most of its features, step by step.Each section gradually builds on the previous ones, but it's structured to separate topics, so that you can go directly to any specific one to solve your specific API needs.It is also built to work as a future reference so you can come back and see exactly what you need.Run the code¶
All the code blocks can be copied and used directly (they are actually tested Python files).To run any of the examples, copy the code to a file main.py, and start fastapi dev with:
fastapi dev main.py
INFO     Using path main.py
INFO     Resolved absolute path /home/user/code/awesomeapp/main.py
INFO     Searching for package file structure from directories with __init__.py files
INFO     Importing from /home/user/code/awesomeapp ╭─ Python module file ─╮
 │                      │
 │  🐍 main.py          │
 │                      │
 ╰──────────────────────╯INFO     Importing module main
INFO     Found importable FastAPI app ╭─ Importable FastAPI app ─╮
 │                          │
 │  from main import app    │
 │                          │
 ╰──────────────────────────╯INFO     Using import string main:app ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2265862] using WatchFiles
INFO:     Started server process [2265873]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
restart ↻
It is HIGHLY encouraged that you write or copy the code, edit it and run it locally.Using it in your editor is what really shows you the benefits of FastAPI, seeing how little code you have to write, all the type checks, autocompletion, etc.Install FastAPI¶
The first step is to install FastAPI.Make sure you create a virtual environment, activate it, and then install FastAPI:
NoteWhen you install with pip install "fastapi[standard]" it comes with some default optional standard dependencies.If you don't want to have those optional dependencies, you can instead install pip install fastapi.Advanced User Guide¶
There is also an Advanced User Guide that you can read later after this Tutorial - User guide.The Advanced User Guide builds on this one, uses the same concepts, and teaches you some extra features.But you should first read the Tutorial - User Guide (what you are reading right now).It's designed so that you can build a complete application with just the Tutorial - User Guide, and then extend it in different ways, depending on your needs, using some of the additional ideas from the Advanced User Guide.
Virtual Environments
First Steps
First Steps 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Check it
Interactive API docs
Alternative API docs
OpenAPI
"Schema"
API "schema"
Data "schema"
OpenAPI and JSON Schema
Check the openapi.json
What is OpenAPI for
Recap, step by step
Step 1: import Step 2: create a FastAPI "instance"
Step 3: create a path operation
Path
Operation
Define a path operation decorator
Step 4: define the path operation function
Step 5: return the content
Recap
First Steps¶
The simplest FastAPI file could look like this:
from fastapi import 
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}Copy that to a file main.py.Run the live server:
fast →
fast
In the output, there's a line with something like:
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
That line shows the URL where your app is being served, in your local machine.Check it¶
Open your browser at http://127.0.0.1:8000.You will see the JSON response as:
{"message": "Hello World"}
Interactive API docs¶
Now go to http://127.0.0.1:8000/docs.You will see the automatic interactive API documentation (provided by Swagger UI):Swagger UIAlternative API docs¶
And now, go to http://127.0.0.1:8000/redoc.You will see the alternative automatic documentation (provided by ReDoc):ReDocOpenAPI¶
FastAPI generates a "schema" with all your API using the OpenAPI standard for defining APIs."Schema"¶
A "schema" is a definition or description of something. Not the code that implements it, but just an abstract description.API "schema"¶
In this case, OpenAPI is a specification that dictates how to define a schema of your API.This schema definition includes your API paths, the possible parameters they take, etc.Data "schema"¶
The term "schema" might also refer to the shape of some data, like a JSON content.In that case, it would mean the JSON attributes, and data types they have, etc.OpenAPI and JSON Schema¶
OpenAPI defines an API schema for your API. And that schema includes definitions (or "schemas") of the data sent and received by your API using JSON Schema, the standard for JSON data schemas.Check the openapi.json¶
If you are curious about how the raw OpenAPI schema looks like, FastAPI automatically generates a JSON (schema) with the descriptions of all your API.You can see it directly at: http://127.0.0.1:8000/openapi.json.It will show a JSON starting with something like:
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {...
What is OpenAPI for¶
The OpenAPI schema is what powers the two interactive documentation systems included.And there are dozens of alternatives, all based on OpenAPI. You could easily add any of those alternatives to your application built with FastAPI.You could also use it to generate code automatically, for clients that communicate with your API. For example, frontend, mobile or IoT applications.Recap, step by step¶
Step 1: import FastAPI¶from fastapi import 
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}FastAPI is a Python class that provides all the functionality for your API.Technical DetailsFastAPI is a class that inherits directly from Starlette.You can use all the Starlette functionality with FastAPI too.Step 2: create a FastAPI "instance"¶from fastapi import 
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}Here the app variable will be an "instance" of the class FastAPI.This will be the main point of interaction to create all your API.Step 3: create a path operation¶
Path¶
"Path" here refers to the last part of the URL starting from the first /.So, in a URL like:
https://example.com/items/foo
...the path would be:
/items/foo
InfoA "path" is also commonly called an "endpoint" or a "route".While building an API, the "path" is the main way to separate "concerns" and "resources".Operation¶
"Operation" here refers to one of the HTTP "methods".One of:POST
GET
PUT
DELETE
...and the more exotic ones:OPTIONS
HEAD
PATCH
TRACE
In the HTTP protocol, you can communicate to each path using one (or more) of these "methods".When building APIs, you normally use these specific HTTP methods to perform a specific action.Normally you use:POST: to create data.
GET: to read data.
PUT: to update data.
DELETE: to delete data.
So, in OpenAPI, each of the HTTP methods is called an "operation".We are going to call them "operations" too.Define a path operation decorator¶from fastapi import 
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}The @app.get("/") tells FastAPI that the function right below is in charge of handling requests that go to:the path /
using a get operation
@decorator InfoThat @something syntax in Python is called a "decorator".You put it on top of a function. Like a pretty decorative hat (I guess that's where the term came from).A "decorator" takes the function below and does something with it.In our case, this decorator tells FastAPI that the function below corresponds to the path / with an operation get.It is the "path operation decorator".You can also use the other operations:@app.post()
@app.put()
@app.delete()
And the more exotic ones:@app.options()
@app.head()
@app.patch()
@app.trace()
TipYou are free to use each operation (HTTP method) as you wish.FastAPI doesn't enforce any specific meaning.The information here is presented as a guideline, not a requirement.For example, when using GraphQL you normally perform all the actions using only POST operations.Step 4: define the path operation function¶
This is our "path operation function":path: is /.
operation: is get.
function: is the function below the "decorator" (below @app.get("/")).from fastapi import 
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}This is a Python function.It will be called by FastAPI whenever it receives a request to the URL "/" using a GET operation.In this case, it is an async function.You could also define it as a normal function instead of async def:
from fastapi import 
app = FastAPI()
@app.get("/")
def root():
    return {"message": "Hello World"}NoteIf you don't know the difference, check the Async: "In a hurry".Step 5: return the content¶from fastapi import 
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}You can return a dict, list, singular values as str, int, etc.You can also return Pydantic models (you'll see more about that later).There are many other objects and models that will be automatically converted to JSON (including ORMs, etc). Try using your favorite ones, it's highly probable that they are already supported.Recap¶
Import FastAPI.
Create an app instance.
Write a path operation decorator using decorators like @app.get("/").
Define a path operation function; for example, def root(): ....
Run the development server using the command fastapi dev.Path Parameters
Path Parameters 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Path parameters with types
Data conversion
Data validation
Documentation
Standards-based benefits, alternative documentation
Pydantic
Order matters
Predefined values
Create an Enum class
Declare a path parameter
Check the docs
Working with Python enumerations
Compare enumeration members
Get the enumeration value
Return enumeration members
Path parameters containing paths
OpenAPI support
Path convertor
Recap
Path Parameters¶
You can declare path "parameters" or "variables" with the same syntax used by Python format strings:
from fastapi import 
app = FastAPI()
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}The value of the path parameter item_id will be passed to your function as the argument item_id.So, if you run this example and go to http://127.0.0.1:8000/items/foo, you will see a response of:
{"item_id":"foo"}
Path parameters with types¶
You can declare the type of a path parameter in the function, using standard Python type annotations:
from fastapi import 
app = FastAPI()
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}In this case, item_id is declared to be an int.CheckThis will give you editor support inside of your function, with error checks, completion, etc.Data conversion¶
If you run this example and open your browser at http://127.0.0.1:8000/items/3, you will see a response of:
{"item_id":3}
CheckNotice that the value your function received (and returned) is 3, as a Python int, not a string "3".So, with that type declaration, FastAPI gives you automatic request "parsing".Data validation¶
But if you go to the browser at http://127.0.0.1:8000/items/foo, you will see a nice HTTP error of:
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "item_id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "foo",
      "url": "https://errors.pydantic.dev/2.1/v/int_parsing"
    }
  ]
}
because the path parameter item_id had a value of "foo", which is not an int.The same error would appear if you provided a float instead of an int, as in: http://127.0.0.1:8000/items/4.2CheckSo, with the same Python type declaration, FastAPI gives you data validation.Notice that the error also clearly states exactly the point where the validation didn't pass.This is incredibly helpful while developing and debugging code that interacts with your API.Documentation¶
And when you open your browser at http://127.0.0.1:8000/docs, you will see an automatic, interactive, API documentation like:CheckAgain, just with that same Python type declaration, FastAPI gives you automatic, interactive documentation (integrating Swagger UI).Notice that the path parameter is declared to be an integer.Standards-based benefits, alternative documentation¶
And because the generated schema is from the OpenAPI standard, there are many compatible tools.Because of this, FastAPI itself provides an alternative API documentation (using ReDoc), which you can access at http://127.0.0.1:8000/redoc:The same way, there are many compatible tools. Including code generation tools for many languages.Pydantic¶
All the data validation is performed under the hood by Pydantic, so you get all the benefits from it. And you know you are in good hands.You can use the same type declarations with str, float, bool and many other complex data types.Several of these are explored in the next chapters of the tutorial.Order matters¶
When creating path operations, you can find situations where you have a fixed path.Like /users/me, let's say that it's to get data about the current user.And then you can also have a path /users/{user_id} to get data about a specific user by some user ID.Because path operations are evaluated in order, you need to make sure that the path for /users/me is declared before the one for /users/{user_id}:
from fastapi import 
app = FastAPI()
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}Otherwise, the path for /users/{user_id} would match also for /users/me, "thinking" that it's receiving a parameter user_id with a value of "me".Similarly, you cannot redefine a path operation:
from fastapi import 
app = FastAPI()
@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]
@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]The first one will always be used since the path matches first.Predefined values¶
If you have a path operation that receives a path parameter, but you want the possible valid path parameter values to be predefined, you can use a standard Python Enum.Create an Enum class¶
Import Enum and create a sub-class that inherits from str and from Enum.By inheriting from str the API docs will be able to know that the values must be of type string and will be able to render correctly.Then create class attributes with fixed values, which will be the available valid values:
from enum import Enumfrom fastapi import class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
app = FastAPI()
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}    return {"model_name": model_name, "message": "Have some residuals"}InfoEnumerations (or enums) are available in Python since version 3.4.TipIf you are wondering, "AlexNet", "ResNet", and "LeNet" are just names of Machine Learning models.Declare a path parameter¶
Then create a path parameter with a type annotation using the enum class you created (ModelName):
from enum import Enumfrom fastapi import class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
app = FastAPI()
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}    return {"model_name": model_name, "message": "Have some residuals"}Check the docs¶
Because the available values for the path parameter are predefined, the interactive docs can show them nicely:Working with Python enumerations¶
The value of the path parameter will be an enumeration member.Compare enumeration members¶
You can compare it with the enumeration member in your created enum ModelName:
from enum import Enumfrom fastapi import class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
app = FastAPI()
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}    return {"model_name": model_name, "message": "Have some residuals"}Get the enumeration value¶
You can get the actual value (a str in this case) using model_name.value, or in general, your_enum_member.value:
from enum import Enumfrom fastapi import class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
app = FastAPI()
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}    return {"model_name": model_name, "message": "Have some residuals"}TipYou could also access the value "lenet" with ModelName.lenet.value.Return enumeration members¶
You can return enum members from your path operation, even nested in a JSON body (e.g. a dict).They will be converted to their corresponding values (strings in this case) before returning them to the client:
from enum import Enumfrom fastapi import class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
app = FastAPI()
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}    return {"model_name": model_name, "message": "Have some residuals"}In your client you will get a JSON response like:
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
Path parameters containing paths¶
Let's say you have a path operation with a path /files/{file_path}.But you need file_path itself to contain a path, like home/johndoe/myfile.txt.So, the URL for that file would be something like: /files/home/johndoe/myfile.txt.OpenAPI support¶
OpenAPI doesn't support a way to declare a path parameter to contain a path inside, as that could lead to scenarios that are difficult to test and define.Nevertheless, you can still do it in FastAPI, using one of the internal tools from Starlette.And the docs would still work, although not adding any documentation telling that the parameter should contain a path.Path convertor¶
Using an option directly from Starlette you can declare a path parameter containing a path using a URL like:
/files/{file_path:path}
In this case, the name of the parameter is file_path, and the last part, :path, tells it that the parameter should match any path.So, you can use it with:
from fastapi import 
app = FastAPI()
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}TipYou could need the parameter to contain /home/johndoe/myfile.txt, with a leading slash (/).In that case, the URL would be: /files//home/johndoe/myfile.txt, with a double slash (//) between files and home.Recap¶
With FastAPI, by using short, intuitive and standard Python type declarations, you get:Editor support: error checks, autocompletion, etc.
Data "parsing"
Data validation
API annotation and automatic documentation
And you only have to declare them once.That's probably the main visible advantage of FastAPI compared to alternative frameworks (apart from the raw performance).
First Steps
Query Parameters
Query Parameters 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Defaults
Optional parameters
Query parameter type conversion
Multiple path and query parameters
Required query parameters
Query Parameters¶
When you declare other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters.
from fastapi import 
app = FastAPI()fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]The query is the set of key-value pairs that go after the  in a URL, separated by & characters.For example, in the URL:
http://127.0.0.1:8000/items/skip=0&limit=10
...the query parameters are:skip: with a value of 0
limit: with a value of 10
As they are part of the URL, they are "naturally" strings.But when you declare them with Python types (in the example above, as int), they are converted to that type and validated against it.All the same process that applied for path parameters also applies for query parameters:Editor support (obviously)
Data "parsing"
Data validation
Automatic documentation
Defaults¶
As query parameters are not a fixed part of a path, they can be optional and can have default values.In the example above they have default values of skip=0 and limit=10.So, going to the URL:
http://127.0.0.1:8000/items/
would be the same as going to:
http://127.0.0.1:8000/items/skip=0&limit=10
But if you go to, for example:
http://127.0.0.1:8000/items/skip=20
The parameter values in your function will be:skip=20: because you set it in the URL
limit=10: because that was the default value
Optional parameters¶
The same way, you can declare optional query parameters, by setting their default to None:
from fastapi import 
app = FastAPI()
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}🤓 Other versions and variants
In this case, the function parameter q will be optional, and will be None by default.CheckAlso notice that FastAPI is smart enough to notice that the path parameter item_id is a path parameter and q is not, so, it's a query parameter.Query parameter type conversion¶
You can also declare bool types, and they will be converted:
from fastapi import 
app = FastAPI()
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item🤓 Other versions and variants
In this case, if you go to:
http://127.0.0.1:8000/items/fooshort=or
http://127.0.0.1:8000/items/fooshort=True
or
http://127.0.0.1:8000/items/fooshort=true
or
http://127.0.0.1:8000/items/fooshort=on
or
http://127.0.0.1:8000/items/fooshort=yes
or any other case variation (uppercase, first letter in uppercase, etc), your function will see the parameter short with a bool value of True. Otherwise as False.Multiple path and query parameters¶
You can declare multiple path parameters and query parameters at the same time, FastAPI knows which is which.And you don't have to declare them in any specific order.They will be detected by name:
from fastapi import 
app = FastAPI()
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item🤓 Other versions and variants
Required query parameters¶
When you declare a default value for non-path parameters (for now, we have only seen query parameters), then it is not required.If you don't want to add a specific value but just make it optional, set the default as None.But when you want to make a query parameter required, you can just not declare any default value:
from fastapi import 
app = FastAPI()
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return itemHere the query parameter needy is a required query parameter of type str.If you open in your browser a URL like:
http://127.0.0.1:8000/items/foo-item
...without adding the required parameter needy, you will see an error like:
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "query",
        "needy"
      ],
      "msg": "Field required",
      "input": null,
      "url": "https://errors.pydantic.dev/2.1/v/missing"
    }
  ]
}
As needy is a required parameter, you would need to set it in the URL:
http://127.0.0.1:8000/items/foo-itemneedy=sooooneedy
...this would work:
{
    "item_id": "foo-item",
    "needy": "sooooneedy"
}
And of course, you can define some parameters as required, some as having a default value, and some entirely optional:
from fastapi import 
app = FastAPI()
@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item🤓 Other versions and variants
In this case, there are 3 query parameters:needy, a required str.
skip, an int with a default value of 0.
limit, an optional int.
TipYou could also use Enums the same way as with Path Parameters.
Path Parameters
Request Body
Request Body 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Import Pydantic's BaseModel
Create your data model
Declare it as a parameter
Results
Automatic docs
Editor support
Use the model
Request body + path parameters
Request body + path + query parameters
Without Pydantic
Request Body¶
When you need to send data from a client (let's say, a browser) to your API, you send it as a request body.A request body is data sent by the client to your API. A response body is the data your API sends to the client.Your API almost always has to send a response body. But clients don't necessarily need to send request bodies all the time, sometimes they only request a path, maybe with some query parameters, but don't send a body.To declare a request body, you use Pydantic models with all their power and benefits.InfoTo send data, you should use one of: POST (the more common), PUT, DELETE or PATCH.Sending a body with a GET request has an undefined behavior in the specifications, nevertheless, it is supported by FastAPI, only for very complex/extreme use cases.As it is discouraged, the interactive docs with Swagger UI won't show the documentation for the body when using GET, and proxies in the middle might not support it.Import Pydantic's BaseModel¶
First, you need to import BaseModel from pydantic:
from fastapi import from pydantic import BaseModel
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
app = FastAPI()
@app.post("/items/")
async def create_item(item: Item):
    return item🤓 Other versions and variants
Create your data model¶
Then you declare your data model as a class that inherits from BaseModel.Use standard Python types for all the attributes:
from fastapi import from pydantic import BaseModel
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
app = FastAPI()
@app.post("/items/")
async def create_item(item: Item):
    return item🤓 Other versions and variants
The same as when declaring query parameters, when a model attribute has a default value, it is not required. Otherwise, it is required. Use None to make it just optional.For example, this model above declares a JSON "object" (or Python dict) like:
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
...as description and tax are optional (with a default value of None), this JSON "object" would also be valid:
{
    "name": "Foo",
    "price": 45.2
}
Declare it as a parameter¶
To add it to your path operation, declare it the same way you declared path and query parameters:
from fastapi import from pydantic import BaseModel
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
app = FastAPI()
@app.post("/items/")
async def create_item(item: Item):
    return item🤓 Other versions and variants
...and declare its type as the model you created, Item.Results¶
With just that Python type declaration, FastAPI will:Read the body of the request as JSON.
Convert the corresponding types (if needed).
Validate the data.
If the data is invalid, it will return a nice and clear error, indicating exactly where and what was the incorrect data.
Give you the received data in the parameter item.
As you declared it in the function to be of type Item, you will also have all the editor support (completion, etc) for all of the attributes and their types.
Generate JSON Schema definitions for your model, you can also use them anywhere else you like if it makes sense for your project.
Those schemas will be part of the generated OpenAPI schema, and used by the automatic documentation UIs.
Automatic docs¶
The JSON Schemas of your models will be part of your OpenAPI generated schema, and will be shown in the interactive API docs:And will also be used in the API docs inside each path operation that needs them:Editor support¶
In your editor, inside your function you will get type hints and completion everywhere (this wouldn't happen if you received a dict instead of a Pydantic model):You also get error checks for incorrect type operations:This is not by chance, the whole framework was built around that design.And it was thoroughly tested at the design phase, before any implementation, to ensure it would work with all the editors.There were even some changes to Pydantic itself to support this.The previous screenshots were taken with Visual Studio Code.But you would get the same editor support with PyCharm and most of the other Python editors:TipIf you use PyCharm as your editor, you can use the Pydantic PyCharm Plugin.It improves editor support for Pydantic models, with:auto-completion
type checks
refactoring
searching
inspections
Use the model¶
Inside of the function, you can access all the attributes of the model object directly:
from fastapi import from pydantic import BaseModel
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
app = FastAPI()
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict🤓 Other versions and variants
Request body + path parameters¶
You can declare path parameters and request body at the same time.FastAPI will recognize that the function parameters that match path parameters should be taken from the path, and that function parameters that are declared to be Pydantic models should be taken from the request body.
from fastapi import from pydantic import BaseModel
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
app = FastAPI()
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}🤓 Other versions and variants
Request body + path + query parameters¶
You can also declare body, path and query parameters, all at the same time.FastAPI will recognize each of them and take the data from the correct place.
from fastapi import from pydantic import BaseModel
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
app = FastAPI()
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result🤓 Other versions and variants
The function parameters will be recognized as follows:If the parameter is also declared in the path, it will be used as a path parameter.
If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body.
NoteFastAPI will know that the value of q is not required because of the default value = None.The str | None () or Union in Union[str, None] () is not used by FastAPI to determine that the value is not required, it will know it's not required because it has a default value of = None.But adding the type annotations will allow your editor to give you better support and detect errors.Without Pydantic¶
If you don't want to use Pydantic models, you can also use Body parameters. See the docs for Body - Multiple Parameters: Singular values in body.
Query Parameters
Query Parameters and String Validations
Query Parameters and String Validations 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Additional validation
Import Query and Annotated
Use Annotated in the type for the q parameter
Add Query to Annotated in the q parameter
Alternative (old): Query as the default value
Query as the default value or in Annotated
Advantages of Annotated
Add more validations
Add regular expressions
Pydantic v1 regex instead of pattern
Default values
Required parameters
Required with Ellipsis (...)
Required, can be None
Query parameter list / multiple values
Query parameter list / multiple values with defaults
Using just list
Declare more metadata
Alias parameters
Deprecating parameters
Exclude parameters from OpenAPI
Recap
Query Parameters and String Validations¶
FastAPI allows you to declare additional information and validation for your parameters.Let's take this application as example:
from fastapi import 
app = FastAPI()
@app.get("/items/")
async def read_items(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
The query parameter q is of type Union[str, None] (or str | None in Python 3.10), that means that it's of type str but could also be None, and indeed, the default value is None, so FastAPI will know it's not required.NoteFastAPI will know that the value of q is not required because of the default value = None.The Union in Union[str, None] will allow your editor to give you better support and detect errors.Additional validation¶
We are going to enforce that even though q is optional, whenever it is provided, its length doesn't exceed 50 characters.Import Query and Annotated¶
To achieve that, first import:Query from Annotated from typing (or from typing_extensions in Python below 3.9)In Python 3.9 or above, Annotated is part of the standard library, so you can import it from typing.
from typing import Annotatedfrom fastapi import FastAPI, Queryapp = FastAPI()
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return resultsInfoFastAPI added support for Annotated (and started recommending it) in version 0.95.0.If you have an older version, you would get errors when trying to use Annotated.Make sure you Upgrade the FastAPI version to at least 0.95.1 before using Annotated.Use Annotated in the type for the q parameter¶
Remember I told you before that Annotated can be used to add metadata to your parameters in the Python Types IntroNow it's the time to use it with FastAPI. 🚀We had this type annotation:q: str | None = NoneWhat we will do is wrap that with Annotated, so it becomes:q: Annotated[str | None] = NoneBoth of those versions mean the same thing, q is a parameter that can be a str or None, and by default, it is None.Now let's jump to the fun stuff. 🎉Add Query to Annotated in the q parameter¶
Now that we have this Annotated where we can put more information (in this case some additional validation), add Query inside of Annotated, and set the parameter max_length to 50:
from typing import Annotatedfrom fastapi import FastAPI, Queryapp = FastAPI()
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
Notice that the default value is still None, so the parameter is still optional.But now, having Query(max_length=50) inside of Annotated, we are telling FastAPI that we want it to have additional validation for this value, we want it to have maximum 50 characters. 😎TipHere we are using Query() because this is a query parameter. Later we will see others like Path(), Body(), Header(), and Cookie(), that also accept the same arguments as Query().FastAPI will now:Validate the data making sure that the max length is 50 characters
Show a clear error for the client when the data is not valid
Document the parameter in the OpenAPI schema path operation (so it will show up in the automatic docs UI)
Alternative (old): Query as the default value¶
Previous versions of FastAPI (before 0.95.0) required you to use Query as the default value of your parameter, instead of putting it in Annotated, there's a high chance that you will see code using it around, so I'll explain it to you.TipFor new code and whenever possible, use Annotated as explained above. There are multiple advantages (explained below) and no disadvantages. 🍰This is how you would use Query() as the default value of your function parameter, setting the parameter max_length to 50:
 - non-Annotatedfrom fastapi import FastAPI, Queryapp = FastAPI()
@app.get("/items/")
async def read_items(q: str | None = Query(default=None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
As in this case (without using Annotated) we have to replace the default value None in the function with Query(), we now need to set the default value with the parameter Query(default=None), it serves the same purpose of defining that default value (at least for FastAPI).So:
q: Union[str, None] = Query(default=None)
...makes the parameter optional, with a default value of None, the same as:
q: Union[str, None] = None
And in Python 3.10 and above:
q: str | None = Query(default=None)
...makes the parameter optional, with a default value of None, the same as:
q: str | None = None
But the Query versions declare it explicitly as being a query parameter.InfoKeep in mind that the most important part to make a parameter optional is the part:
= None
or the:
= Query(default=None)
as it will use that None as the default value, and that way make the parameter not required.The Union[str, None] part allows your editor to provide better support, but it is not what tells FastAPI that this parameter is not required.Then, we can pass more parameters to Query. In this case, the max_length parameter that applies to strings:
q: Union[str, None] = Query(default=None, max_length=50)
This will validate the data, show a clear error when the data is not valid, and document the parameter in the OpenAPI schema path operation.Query as the default value or in Annotated¶
Keep in mind that when using Query inside of Annotated you cannot use the default parameter for Query.Instead use the actual default value of the function parameter. Otherwise, it would be inconsistent.For example, this is not allowed:
q: Annotated[str, Query(default="rick")] = "morty"
...because it's not clear if the default value should be "rick" or "morty".So, you would use (preferably):
q: Annotated[str, Query()] = "rick"
...or in older code bases you will find:
q: str = Query(default="rick")
Advantages of Annotated¶
Using Annotated is recommended instead of the default value in function parameters, it is better for multiple reasons. 🤓The default value of the function parameter is the actual default value, that's more intuitive with Python in general. 😌You could call that same function in other places without FastAPI, and it would work as expected. If there's a required parameter (without a default value), your editor will let you know with an error, Python will also complain if you run it without passing the required parameter.When you don't use Annotated and instead use the (old) default value style, if you call that function without FastAPI in other places, you have to remember to pass the arguments to the function for it to work correctly, otherwise the values will be different from what you expect (e.g. QueryInfo or something similar instead of str). And your editor won't complain, and Python won't complain running that function, only when the operations inside error out.Because Annotated can have more than one metadata annotation, you could now even use the same function with other tools, like Typer. 🚀Add more validations¶
You can also add a parameter min_length:
from typing import Annotatedfrom fastapi import FastAPI, Queryapp = FastAPI()
@app.get("/items/")
async def read_items(
    q: Annotated[str | None, Query(min_length=3, max_length=50)] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
Add regular expressions¶
You can define a regular expression pattern that the parameter should match:
from typing import Annotatedfrom fastapi import FastAPI, Queryapp = FastAPI()
@app.get("/items/")
async def read_items(
    q: Annotated[
        str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
This specific regular expression pattern checks that the received parameter value:^: starts with the following characters, doesn't have characters before.
fixedquery: has the exact value fixedquery.
$: ends there, doesn't have any more characters after fixedquery.
If you feel lost with all these "regular expression" ideas, don't worry. They are a hard topic for many people. You can still do a lot of stuff without needing regular expressions yet.But whenever you need them and go and learn them, know that you can already use them directly in FastAPI.Pydantic v1 regex instead of pattern¶
Before Pydantic version 2 and before FastAPI 0.100.0, the parameter was called regex instead of pattern, but it's now deprecated.You could still see some code using it:
Pydantic v
from typing import Annotatedfrom fastapi import FastAPI, Queryapp = FastAPI()
@app.get("/items/")
async def read_items(
    q: Annotated[
        str | None, Query(min_length=3, max_length=50, regex="^fixedquery$")
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
But know that this is deprecated and it should be updated to use the new parameter pattern. 🤓Default values¶
You can, of course, use default values other than None.Let's say that you want to declare the q query parameter to have a min_length of 3, and to have a default value of "fixedquery":
from typing import Annotatedfrom fastapi import FastAPI, Queryapp = FastAPI()
@app.get("/items/")
async def read_items(q: Annotated[str, Query(min_length=3)] = "fixedquery"):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
NoteHaving a default value of any type, including None, makes the parameter optional (not required).Required parameters¶
When we don't need to declare more validations or metadata, we can make the q query parameter required just by not declaring a default value, like:
q: str
instead of:
q: Union[str, None] = None
But we are now declaring it with Query, for example like:
Annotated
non-Annotatedq: Annotated[Union[str, None], Query(min_length=3)] = NoneSo, when you need to declare a value as required while using Query, you can simply not declare a default value:
from typing import Annotatedfrom fastapi import FastAPI, Queryapp = FastAPI()
@app.get("/items/")
async def read_items(q: Annotated[str, Query(min_length=3)]):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
Required with Ellipsis (...)¶
There's an alternative way to explicitly declare that a value is required. You can set the default to the literal value ...:
from typing import Annotatedfrom fastapi import FastAPI, Queryapp = FastAPI()
@app.get("/items/")
async def read_items(q: Annotated[str, Query(min_length=3)] = ...):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
InfoIf you hadn't seen that ... before: it is a special single value, it is part of Python and is called "Ellipsis".It is used by Pydantic and FastAPI to explicitly declare that a value is required.This will let FastAPI know that this parameter is required.Required, can be None¶
You can declare that a parameter can accept None, but that it's still required. This would force clients to send a value, even if the value is None.To do that, you can declare that None is a valid type but still use ... as the default:
from typing import Annotatedfrom fastapi import FastAPI, Queryapp = FastAPI()
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(min_length=3)] = ...):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
TipPydantic, which is what powers all the data validation and serialization in FastAPI, has a special behavior when you use Optional or Union[Something, None] without a default value, you can read more about it in the Pydantic docs about Required fields.TipRemember that in most of the cases, when something is required, you can simply omit the default, so you normally don't have to use ....Query parameter list / multiple values¶
When you define a query parameter explicitly with Query you can also declare it to receive a list of values, or said in another way, to receive multiple values.For example, to declare a query parameter q that can appear multiple times in the URL, you can write:
from typing import Annotatedfrom fastapi import FastAPI, Queryapp = FastAPI()
@app.get("/items/")
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items🤓 Other versions and variants
Then, with a URL like:
http://localhost:8000/items/q=foo&q=bar
you would receive the multiple q query parameters' values (foo and bar) in a Python list inside your path operation function, in the function parameter q.So, the response to that URL would be:
{
  "q": [
    "foo",
    "bar"
  ]
}
TipTo declare a query parameter with a type of list, like in the example above, you need to explicitly use Query, otherwise it would be interpreted as a request body.The interactive API docs will update accordingly, to allow multiple values:Query parameter list / multiple values with defaults¶
And you can also define a default list of values if none are provided:
from typing import Annotatedfrom fastapi import FastAPI, Queryapp = FastAPI()
@app.get("/items/")
async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items🤓 Other versions and variants
If you go to:
http://localhost:8000/items/
the default of q will be: ["foo", "bar"] and your response will be:
{
  "q": [
    "foo",
    "bar"
  ]
}
Using just list¶
You can also use list directly instead of List[str] (or list[str] in ):
from typing import Annotatedfrom fastapi import FastAPI, Queryapp = FastAPI()
@app.get("/items/")
async def read_items(q: Annotated[list, Query()] = []):
    query_items = {"q": q}
    return query_items🤓 Other versions and variants
NoteKeep in mind that in this case, FastAPI won't check the contents of the list.For example, List[int] would check (and document) that the contents of the list are integers. But list alone wouldn't.Declare more metadata¶
You can add more information about the parameter.That information will be included in the generated OpenAPI and used by the documentation user interfaces and external tools.NoteKeep in mind that different tools might have different levels of OpenAPI support.Some of them might not show all the extra information declared yet, although in most of the cases, the missing feature is already planned for development.You can add a title:
from typing import Annotatedfrom fastapi import FastAPI, Queryapp = FastAPI()
@app.get("/items/")
async def read_items(
    q: Annotated[str | None, Query(title="Query string", min_length=3)] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
And a description:
from typing import Annotatedfrom fastapi import FastAPI, Queryapp = FastAPI()
@app.get("/items/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
Alias parameters¶
Imagine that you want the parameter to be item-query.Like in:
http://127.0.0.1:8000/items/item-query=foobaritems
But item-query is not a valid Python variable name.The closest would be item_query.But you still need it to be exactly item-query...Then you can declare an alias, and that alias is what will be used to find the parameter value:
from typing import Annotatedfrom fastapi import FastAPI, Queryapp = FastAPI()
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(alias="item-query")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
Deprecating parameters¶
Now let's say you don't like this parameter anymore.You have to leave it there a while because there are clients using it, but you want the docs to clearly show it as deprecated.Then pass the parameter deprecated=True to Query:
from typing import Annotatedfrom fastapi import FastAPI, Queryapp = FastAPI()
@app.get("/items/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
The docs will show it like this:Exclude parameters from OpenAPI¶
To exclude a query parameter from the generated OpenAPI schema (and thus, from the automatic documentation systems), set the parameter include_in_schema of Query to False:
from typing import Annotatedfrom fastapi import FastAPI, Queryapp = FastAPI()
@app.get("/items/")
async def read_items(
    hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None,
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}🤓 Other versions and variants
Recap¶
You can declare additional validations and metadata for your parameters.Generic validations and metadata:alias
title
description
deprecated
Validations specific for strings:min_length
max_length
pattern
In these examples you saw how to declare validations for str values.See the next chapters to learn how to declare validations for other types, like numbers.
Request Body
Path Parameters and Numeric Validations
Path Parameters and Numeric Validations 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Import Path
Declare metadata
Order the parameters as you need
Order the parameters as you need, tricks
Better with Annotated
Number validations: greater than or equal
Number validations: greater than and less than or equal
Number validations: floats, greater than and less than
Recap
Path Parameters and Numeric Validations¶
In the same way that you can declare more validations and metadata for query parameters with Query, you can declare the same type of validations and metadata for path parameters with Path.Import Path¶
First, import Path from fastapi, and import Annotated:
from typing import Annotatedfrom fastapi import FastAPI, Path, Queryapp = FastAPI()
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
InfoFastAPI added support for Annotated (and started recommending it) in version 0.95.0.If you have an older version, you would get errors when trying to use Annotated.Make sure you Upgrade the FastAPI version to at least 0.95.1 before using Annotated.Declare metadata¶
You can declare all the same parameters as for Query.For example, to declare a title metadata value for the path parameter item_id you can type:
from typing import Annotatedfrom fastapi import FastAPI, Path, Queryapp = FastAPI()
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
NoteA path parameter is always required as it has to be part of the path. Even if you declared it with None or set a default value, it would not affect anything, it would still be always required.Order the parameters as you need¶
TipThis is probably not as important or necessary if you use Annotated.Let's say that you want to declare the query parameter q as a required str.And you don't need to declare anything else for that parameter, so you don't really need to use Query.But you still need to use Path for the item_id path parameter. And you don't want to use Annotated for some reason.Python will complain if you put a value with a "default" before a value that doesn't have a "default".But you can re-order them, and have the value without a default (the query parameter q) first.It doesn't matter for FastAPI. It will detect the parameters by their names, types and default declarations (Query, Path, etc), it doesn't care about the order.So, you can declare your function as:
Python 3.8 non-Annotated
TipPrefer to use the Annotated version if possible.
 - non-Annotatedfrom fastapi import FastAPI, Pathapp = FastAPI()
@app.get("/items/{item_id}")
async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
🤓 Other versions and variants
But keep in mind that if you use Annotated, you won't have this problem, it won't matter as you're not using the function parameter default values for Query() or Path().
from typing import Annotatedfrom fastapi import FastAPI, Pathapp = FastAPI()
@app.get("/items/{item_id}")
async def read_items(
    q: str, item_id: Annotated[int, Path(title="The ID of the item to get")]
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
Order the parameters as you need, tricks¶
TipThis is probably not as important or necessary if you use Annotated.Here's a small trick that can be handy, but you won't need it often.If you want to:declare the q query parameter without a Query nor any default value
declare the path parameter item_id using Path
have them in a different order
not use Annotated
...Python has a little special syntax for that.Pass *, as the first parameter of the function.Python won't do anything with that *, but it will know that all the following parameters should be called as keyword arguments (key-value pairs), also known as kwargs. Even if they don't have a default value.
 - non-Annotatedfrom fastapi import FastAPI, Pathapp = FastAPI()
@app.get("/items/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
Better with Annotated¶
Keep in mind that if you use Annotated, as you are not using function parameter default values, you won't have this problem, and you probably won't need to use *.
from typing import Annotatedfrom fastapi import FastAPI, Pathapp = FastAPI()
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")], q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
Number validations: greater than or equal¶
With Query and Path (and others you'll see later) you can declare number constraints.Here, with ge=1, item_id will need to be an integer number "greater than or equal" to 1.
from typing import Annotatedfrom fastapi import FastAPI, Pathapp = FastAPI()
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)], q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
Number validations: greater than and less than or equal¶
The same applies for:gt: greater than
le: less than or equalfrom typing import Annotatedfrom fastapi import FastAPI, Pathapp = FastAPI()
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
Number validations: floats, greater than and less than¶
Number validations also work for float values.Here's where it becomes important to be able to declare gt and not just ge. As with it you can require, for example, that a value must be greater than 0, even if it is less than 1.So, 0.5 would be a valid value. But 0.0 or 0 would not.And the same for lt.
from typing import Annotatedfrom fastapi import FastAPI, Path, Queryapp = FastAPI()
@app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str,
    size: Annotated[float, Query(gt=0, lt=10.5)],
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results🤓 Other versions and variants
Recap¶
With Query, Path (and others you haven't seen yet) you can declare metadata and string validations in the same ways as with Query Parameters and String Validations.And you can also declare numeric validations:gt: greater than
ge: greater than or equal
lt: less than
le: less than or equal
InfoQuery, Path, and other classes you will see later are subclasses of a common Param class.All of them share the same parameters for additional validation and metadata you have seen.Technical DetailsWhen you import Query, Path and others from fastapi, they are actually functions.That when called, return instances of classes of the same name.So, you import Query, which is a function. And when you call it, it returns an instance of a class also named Query.These functions are there (instead of just using the classes directly) so that your editor doesn't mark errors about their types.That way you can use your normal editor and coding tools without having to add custom configurations to disregard those errors.
Query Parameters and String Validations
Query Parameter Models
Query Parameter Models 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Query Parameters with a Pydantic Model
Check the Docs
Forbid Extra Query Parameters
Summary
Query Parameter Models¶
If you have a group of query parameters that are related, you can create a Pydantic model to declare them.This would allow you to re-use the model in multiple places and also to declare validations and metadata for all the parameters at once. 😎NoteThis is supported since FastAPI version 0.115.0. 🤓Query Parameters with a Pydantic Model¶
Declare the query parameters that you need in a Pydantic model, and then declare the parameter as Query:
from typing import Annotated, Literalfrom fastapi import FastAPI, Query
from pydantic import BaseModel, Fieldapp = FastAPI()
class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []
@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query🤓 Other versions and variants
FastAPI will extract the data for each field from the query parameters in the request and give you the Pydantic model you defined.Check the Docs¶
You can see the query parameters in the docs UI at /docs:
Forbid Extra Query Parameters¶
In some special use cases (probably not very common), you might want to restrict the query parameters that you want to receive.You can use Pydantic's model configuration to forbid any extra fields:
from typing import Annotated, Literalfrom fastapi import FastAPI, Query
from pydantic import BaseModel, Fieldapp = FastAPI()
class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []
@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query🤓 Other versions and variants
If a client tries to send some extra data in the query parameters, they will receive an error response.For example, if the client tries to send a tool query parameter with a value of plumbus, like:
https://example.com/items/limit=10&tool=plumbus
They will receive an error response telling them that the query parameter tool is not allowed:
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["query", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus"
        }
    ]
}
Summary¶
You can use Pydantic models to declare query parameters in FastAPI. 😎TipSpoiler alert: you can also use Pydantic models to declare cookies and headers, but you will read about that later in the tutorial. 🤫
Path Parameters and Numeric Validations
Body - Multiple Parameters
Body - Multiple Parameters 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Mix Path, Query and body parameters
Multiple body parameters
Multiple body parameters
Singular values in body
Multiple body params and query
Embed a single body parameter
Recap
Body - Multiple Parameters¶
Now that we have seen how to use Path and Query, let's see more advanced uses of request body declarations.Mix Path, Query and body parameters¶
First, of course, you can mix Path, Query and request body parameter declarations freely and FastAPI will know what to do.And you can also declare body parameters as optional, by setting the default to None:
from typing import Annotatedfrom fastapi import FastAPI, Path
from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results🤓 Other versions and variants
Multiple body parameters¶
NoteNotice that, in this case, the item that would be taken from the body is optional. As it has a None default value.Multiple body parameters¶
In the previous example, the path operations would expect a JSON body with the attributes of an Item, like:
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
But you can also declare multiple body parameters, e.g. item and user:
from fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
class User(BaseModel):
    username: str
    full_name: str | None = None
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results🤓 Other versions and variants
In this case, FastAPI will notice that there is more than one body parameter in the function (there are two parameters that are Pydantic models).So, it will then use the parameter names as keys (field names) in the body, and expect a body like:
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
NoteNotice that even though the item was declared the same way as before, it is now expected to be inside of the body with a key item.FastAPI will do the automatic conversion from the request, so that the parameter item receives its specific content and the same for user.It will perform the validation of the compound data, and will document it like that for the OpenAPI schema and automatic docs.Singular values in body¶
The same way there is a Query and Path to define extra data for query and path parameters, FastAPI provides an equivalent Body.For example, extending the previous model, you could decide that you want to have another key importance in the same body, besides the item and user.If you declare it as is, because it is a singular value, FastAPI will assume that it is a query parameter.But you can instruct FastAPI to treat it as another body key using Body:
from typing import Annotatedfrom fastapi import Body, from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
class User(BaseModel):
    username: str
    full_name: str | None = None
@app.put("/items/{item_id}")
async def update_item(
    item_id: int, item: Item, user: User, importance: Annotated[int, Body()]
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results🤓 Other versions and variants
In this case, FastAPI will expect a body like:
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
Again, it will convert the data types, validate, document, etc.Multiple body params and query¶
Of course, you can also declare additional query parameters whenever you need, additional to any body parameters.As, by default, singular values are interpreted as query parameters, you don't have to explicitly add a Query, you can just do:
q: Union[str, None] = None
Or in Python 3.10 and above:
q: str | None = None
For example:
from typing import Annotatedfrom fastapi import Body, from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
class User(BaseModel):
    username: str
    full_name: str | None = None
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)],
    q: str | None = None,
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results🤓 Other versions and variants
InfoBody also has all the same extra validation and metadata parameters as Query,Path and others you will see later.Embed a single body parameter¶
Let's say you only have a single item body parameter from a Pydantic model Item.By default, FastAPI will then expect its body directly.But if you want it to expect a JSON with a key item and inside of it the model contents, as it does when you declare extra body parameters, you can use the special Body parameter embed:
item: Item = Body(embed=True)
as in:
from typing import Annotatedfrom fastapi import Body, from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results🤓 Other versions and variants
In this case FastAPI will expect a body like:
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
instead of:
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
Recap¶
You can add multiple body parameters to your path operation function, even though a request can only have a single body.But FastAPI will handle it, give you the correct data in your function, and validate and document the correct schema in the path operation.You can also declare singular values to be received as part of the body.And you can instruct FastAPI to embed the body in a key even when there is only a single parameter declared.
Query Parameter Models
Body - Fields
Body - Fields 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Import Field
Declare model attributes
Add extra information
Recap
Body - Fields¶
The same way you can declare additional validation and metadata in path operation function parameters with Query, Path and Body, you can declare validation and metadata inside of Pydantic models using Pydantic's Field.Import Field¶
First, you have to import it:
from typing import Annotatedfrom fastapi import Body, from pydantic import BaseModel, Fieldapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results🤓 Other versions and variants
WarningNotice that Field is imported directly from pydantic, not from fastapi as are all the rest (Query, Path, Body, etc).Declare model attributes¶
You can then use Field with model attributes:
from typing import Annotatedfrom fastapi import Body, from pydantic import BaseModel, Fieldapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results🤓 Other versions and variants
Field works the same way as Query, Path and Body, it has all the same parameters, etc.Technical DetailsActually, Query, Path and others you'll see next create objects of subclasses of a common Param class, which is itself a subclass of Pydantic's FieldInfo class.And Pydantic's Field returns an instance of FieldInfo as well.Body also returns objects of a subclass of FieldInfo directly. And there are others you will see later that are subclasses of the Body class.Remember that when you import Query, Path, and others from fastapi, those are actually functions that return special classes.TipNotice how each model's attribute with a type, default value and Field has the same structure as a path operation function's parameter, with Field instead of Path, Query and Body.Add extra information¶
You can declare extra information in Field, Query, Body, etc. And it will be included in the generated JSON Schema.You will learn more about adding extra information later in the docs, when learning to declare examples.WarningExtra keys passed to Field will also be present in the resulting OpenAPI schema for your application. As these keys may not necessarily be part of the OpenAPI specification, some OpenAPI tools, for example the OpenAPI validator, may not work with your generated schema.Recap¶
You can use Pydantic's Field to declare extra validations and metadata for model attributes.You can also use the extra keyword arguments to pass additional JSON Schema metadata.
Body - Multiple Parameters
Body - Nested Models
Body - Nested Models 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
List fields
List fields with type parameter
Import typing's List
Declare a list with a type parameter
Set types
Nested Models
Define a submodel
Use the submodel as a type
Special types and validation
Attributes with lists of submodels
Deeply nested models
Bodies of pure lists
Editor support everywhere
Bodies of arbitrary dicts
Recap
Body - Nested Models¶
With FastAPI, you can define, validate, document, and use arbitrarily deeply nested models (thanks to Pydantic).List fields¶
You can define an attribute to be a subtype. For example, a Python list:
from fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list = []
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results🤓 Other versions and variants
This will make tags be a list, although it doesn't declare the type of the elements of the list.List fields with type parameter¶
But Python has a specific way to declare lists with internal types, or "type parameters":Import typing's List¶
In Python 3.9 and above you can use the standard list to declare these type annotations as we'll see below. 💡But in Python versions before 3.9 (3.6 and above), you first need to import List from standard Python's typing module:
from typing import List, Unionfrom fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results🤓 Other versions and variants
Declare a list with a type parameter¶
To declare types that have type parameters (internal types), like list, dict, tuple:If you are in a Python version lower than 3.9, import their equivalent version from the typing module
Pass the internal type(s) as "type parameters" using square brackets: [ and ]
In Python 3.9 it would be:
my_list: list[str]
In versions of Python before 3.9, it would be:
from typing import Listmy_list: List[str]
That's all standard Python syntax for type declarations.Use that same standard syntax for model attributes with internal types.So, in our example, we can make tags be specifically a "list of strings":
from fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results🤓 Other versions and variants
Set types¶
But then we think about it, and realize that tags shouldn't repeat, they would probably be unique strings.And Python has a special data type for sets of unique items, the set.Then we can declare tags as a set of strings:
from fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results🤓 Other versions and variants
With this, even if you receive a request with duplicate data, it will be converted to a set of unique items.And whenever you output that data, even if the source had duplicates, it will be output as a set of unique items.And it will be annotated / documented accordingly too.Nested Models¶
Each attribute of a Pydantic model has a type.But that type can itself be another Pydantic model.So, you can declare deeply nested JSON "objects" with specific attribute names, types and validations.All that, arbitrarily nested.Define a submodel¶
For example, we can define an Image model:
from fastapi import from pydantic import BaseModelapp = FastAPI()
class Image(BaseModel):
    url: str
    name: str
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results🤓 Other versions and variants
Use the submodel as a type¶
And then we can use it as the type of an attribute:
from fastapi import from pydantic import BaseModelapp = FastAPI()
class Image(BaseModel):
    url: str
    name: str
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results🤓 Other versions and variants
This would mean that FastAPI would expect a body similar to:
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
Again, doing just that declaration, with FastAPI you get:Editor support (completion, etc.), even for nested models
Data conversion
Data validation
Automatic documentation
Special types and validation¶
Apart from normal singular types like str, int, float, etc. you can use more complex singular types that inherit from str.To see all the options you have, checkout Pydantic's Type Overview. You will see some examples in the next chapter.For example, as in the Image model we have a url field, we can declare it to be an instance of Pydantic's HttpUrl instead of a str:
from fastapi import from pydantic import BaseModel, HttpUrlapp = FastAPI()
class Image(BaseModel):
    url: HttpUrl
    name: str
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results🤓 Other versions and variants
The string will be checked to be a valid URL, and documented in JSON Schema / OpenAPI as such.Attributes with lists of submodels¶
You can also use Pydantic models as subtypes of list, set, etc.:
from fastapi import from pydantic import BaseModel, HttpUrlapp = FastAPI()
class Image(BaseModel):
    url: HttpUrl
    name: str
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results🤓 Other versions and variants
This will expect (convert, validate, document, etc.) a JSON body like:
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": [
        "rock",
        "metal",
        "bar"
    ],
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}
InfoNotice how the images key now has a list of image objects.Deeply nested models¶
You can define arbitrarily deeply nested models:
from fastapi import from pydantic import BaseModel, HttpUrlapp = FastAPI()
class Image(BaseModel):
    url: HttpUrl
    name: str
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None
class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]
@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer🤓 Other versions and variants
InfoNotice how Offer has a list of Items, which in turn have an optional list of ImagesBodies of pure lists¶
If the top level value of the JSON body you expect is a JSON array (a Python list), you can declare the type in the parameter of the function, the same as in Pydantic models:
images: List[Image]
or in Python 3.9 and above:
images: list[Image]
as in:
from fastapi import from pydantic import BaseModel, HttpUrlapp = FastAPI()
class Image(BaseModel):
    url: HttpUrl
    name: str
@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images🤓 Other versions and variants
Editor support everywhere¶
And you get editor support everywhere.Even for items inside of lists:You couldn't get this kind of editor support if you were working directly with dict instead of Pydantic models.But you don't have to worry about them either, incoming dicts are converted automatically and your output is converted automatically to JSON too.Bodies of arbitrary dicts¶
You can also declare a body as a dict with keys of some type and values of some other type.This way, you don't have to know beforehand what the valid field/attribute names are (as would be the case with Pydantic models).This would be useful if you want to receive keys that you don't already know.Another useful case is when you want to have keys of another type (e.g., int).That's what we are going to see here.In this case, you would accept any dict as long as it has int keys with float values:
from fastapi import 
app = FastAPI()
@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights🤓 Other versions and variants
TipKeep in mind that JSON only supports str as keys.But Pydantic has automatic data conversion.This means that, even though your API clients can only send strings as keys, as long as those strings contain pure integers, Pydantic will convert them and validate them.And the dict you receive as weights will actually have int keys and float values.Recap¶
With FastAPI you have the maximum flexibility provided by Pydantic models, while keeping your code simple, short and elegant.But with all the benefits:Editor support (completion everywhere!)
Data conversion (a.k.a. parsing / serialization)
Data validation
Schema documentation
Automatic docsBody - Fields
Declare Request Example Data
Declare Request Example Data 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Extra JSON Schema data in Pydantic models
Field additional arguments
examples in JSON Schema - OpenAPI
Body with examples
Example in the docs UI
Body with multiple examples
OpenAPI-specific examples
Using the openapi_examples Parameter
OpenAPI Examples in the Docs UI
Technical Details
JSON Schema's examples field
Pydantic and FastAPI examples
Swagger UI and OpenAPI-specific examples
Summary
Declare Request Example Data¶
You can declare examples of the data your app can receive.Here are several ways to do it.Extra JSON Schema data in Pydantic models¶
You can declare examples for a Pydantic model that will be added to the generated JSON Schema.
Pydantic v2
Pydantic v
from fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
🤓 Other versions and variants
That extra info will be added as-is to the output JSON Schema for that model, and it will be used in the API docs.
Pydantic v2
Pydantic vIn Pydantic version 2, you would use the attribute model_config, that takes a dict as described in Pydantic's docs: Configuration.You can set "json_schema_extra" with a dict containing any additional data you would like to show up in the generated JSON Schema, including examples.
TipYou could use the same technique to extend the JSON Schema and add your own custom extra info.For example you could use it to add metadata for a frontend user interface, etc.InfoOpenAPI 3.1.0 (used since FastAPI 0.99.0) added support for examples, which is part of the JSON Schema standard.Before that, it only supported the keyword example with a single example. That is still supported by OpenAPI 3.1.0, but is deprecated and is not part of the JSON Schema standard. So you are encouraged to migrate example to examples. 🤓You can read more at the end of this page.Field additional arguments¶
When using Field() with Pydantic models, you can also declare additional examples:
from fastapi import from pydantic import BaseModel, Fieldapp = FastAPI()
class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results🤓 Other versions and variants
examples in JSON Schema - OpenAPI¶
When using any of:Path()
Query()
Header()
Cookie()
Body()
Form()
File()
you can also declare a group of examples with additional information that will be added to their JSON Schemas inside of OpenAPI.Body with examples¶
Here we pass examples containing one example of the data expected in Body():
from typing import Annotatedfrom fastapi import Body, from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ],
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results🤓 Other versions and variants
Example in the docs UI¶
With any of the methods above it would look like this in the /docs:Body with multiple examples¶
You can of course also pass multiple examples:
from typing import Annotatedfrom fastapi import Body, from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
                {
                    "name": "Bar",
                    "price": "35.4",
                },
                {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            ],
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results🤓 Other versions and variants
When you do this, the examples will be part of the internal JSON Schema for that body data.Nevertheless, at the time of writing this, Swagger UI, the tool in charge of showing the docs UI, doesn't support showing multiple examples for the data in JSON Schema. But read below for a workaround.OpenAPI-specific examples¶
Since before JSON Schema supported examples OpenAPI had support for a different field also called examples.This OpenAPI-specific examples goes in another section in the OpenAPI specification. It goes in the details for each path operation, not inside each JSON Schema.And Swagger UI has supported this particular examples field for a while. So, you can use it to show different examples in the docs UI.The shape of this OpenAPI-specific field examples is a dict with multiple examples (instead of a list), each with extra information that will be added to OpenAPI too.This doesn't go inside of each JSON Schema contained in OpenAPI, this goes outside, in the path operation directly.Using the openapi_examples Parameter¶
You can declare the OpenAPI-specific examples in FastAPI with the parameter openapi_examples for:Path()
Query()
Header()
Cookie()
Body()
Form()
File()
The keys of the dict identify each example, and each value is another dict.Each specific example dict in the examples can contain:summary: Short description for the example.
description: A long description that can contain Markdown text.
value: This is the actual example shown, e.g. a dict.
externalValue: alternative to value, a URL pointing to the example. Although this might not be supported by as many tools as value.
You can use it like this:
from typing import Annotatedfrom fastapi import Body, from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results🤓 Other versions and variants
OpenAPI Examples in the Docs UI¶
With openapi_examples added to Body() the /docs would look like:Technical Details¶
TipIf you are already using FastAPI version 0.99.0 or above, you can probably skip these details.They are more relevant for older versions, before OpenAPI 3.1.0 was available.You can consider this a brief OpenAPI and JSON Schema history lesson. 🤓WarningThese are very technical details about the standards JSON Schema and OpenAPI.If the ideas above already work for you, that might be enough, and you probably don't need these details, feel free to skip them.Before OpenAPI 3.1.0, OpenAPI used an older and modified version of JSON Schema.JSON Schema didn't have examples, so OpenAPI added its own example field to its own modified version.OpenAPI also added example and examples fields to other parts of the specification:Parameter Object (in the specification) that was used by FastAPI's:
Path()
Query()
Header()
Cookie()
Request Body Object, in the field content, on the Media Type Object (in the specification) that was used by FastAPI's:
Body()
File()
Form()
InfoThis old OpenAPI-specific examples parameter is now openapi_examples since FastAPI 0.103.0.JSON Schema's examples field¶
But then JSON Schema added an examples field to a new version of the specification.And then the new OpenAPI 3.1.0 was based on the latest version (JSON Schema 2020-12) that included this new field examples.And now this new examples field takes precedence over the old single (and custom) example field, that is now deprecated.This new examples field in JSON Schema is just a list of examples, not a dict with extra metadata as in the other places in OpenAPI (described above).InfoEven after OpenAPI 3.1.0 was released with this new simpler integration with JSON Schema, for a while, Swagger UI, the tool that provides the automatic docs, didn't support OpenAPI 3.1.0 (it does since version 5.0.0 🎉).Because of that, versions of FastAPI previous to 0.99.0 still used versions of OpenAPI lower than 3.1.0.Pydantic and FastAPI examples¶
When you add examples inside a Pydantic model, using schema_extra or Field(examples=["something"]) that example is added to the JSON Schema for that Pydantic model.And that JSON Schema of the Pydantic model is included in the OpenAPI of your API, and then it's used in the docs UI.In versions of FastAPI before 0.99.0 (0.99.0 and above use the newer OpenAPI 3.1.0) when you used example or examples with any of the other utilities (Query(), Body(), etc.) those examples were not added to the JSON Schema that describes that data (not even to OpenAPI's own version of JSON Schema), they were added directly to the path operation declaration in OpenAPI (outside the parts of OpenAPI that use JSON Schema).But now that FastAPI 0.99.0 and above uses OpenAPI 3.1.0, that uses JSON Schema 2020-12, and Swagger UI 5.0.0 and above, everything is more consistent and the examples are included in JSON Schema.Swagger UI and OpenAPI-specific examples¶
Now, as Swagger UI didn't support multiple JSON Schema examples (as of 2023-08-26), users didn't have a way to show multiple examples in the docs.To solve that, FastAPI 0.103.0 added support for declaring the same old OpenAPI-specific examples field with the new parameter openapi_examples. 🤓Summary¶
I used to say I didn't like history that much... and look at me now giving "tech history" lessons. 😅In short, upgrade to FastAPI 0.99.0 or above, and things are much simpler, consistent, and intuitive, and you don't have to know all these historic details. 😎
Body - Nested Models
Extra Data Types
Extra Data Types 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Other data types
Example
Extra Data Types¶
Up to now, you have been using common data types, like:int
float
str
bool
But you can also use more complex data types.And you will still have the same features as seen up to now:Great editor support.
Data conversion from incoming requests.
Data conversion for response data.
Data validation.
Automatic annotation and documentation.
Other data types¶
Here are some of the additional data types you can use:UUID:
A standard "Universally Unique Identifier", common as an ID in many databases and systems.
In requests and responses will be represented as a str.
datetime.datetime:
A Python datetime.datetime.
In requests and responses will be represented as a str in ISO 8601 format, like: 2008-09-15T15:53:00+05:00.
datetime.date:
Python datetime.date.
In requests and responses will be represented as a str in ISO 8601 format, like: 2008-09-15.
datetime.time:
A Python datetime.time.
In requests and responses will be represented as a str in ISO 8601 format, like: 14:23:55.003.
datetime.timedelta:
A Python datetime.timedelta.
In requests and responses will be represented as a float of total seconds.
Pydantic also allows representing it as a "ISO 8601 time diff encoding", see the docs for more info.
frozenset:
In requests and responses, treated the same as a set:
In requests, a list will be read, eliminating duplicates and converting it to a set.
In responses, the set will be converted to a list.
The generated schema will specify that the set values are unique (using JSON Schema's uniqueItems).
bytes:
Standard Python bytes.
In requests and responses will be treated as str.
The generated schema will specify that it's a str with binary "format".
Decimal:
Standard Python Decimal.
In requests and responses, handled the same as a float.
You can check all the valid Pydantic data types here: Pydantic data types.
Example¶
Here's an example path operation with parameters using some of the above types.
from datetime import datetime, time, timedelta
from typing import Annotated
from uuid import UUIDfrom fastapi import Body, 
app = FastAPI()
@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }🤓 Other versions and variants
Note that the parameters inside the function have their natural data type, and you can, for example, perform normal date manipulations, like:
from datetime import datetime, time, timedelta
from typing import Annotated
from uuid import UUIDfrom fastapi import Body, 
app = FastAPI()
@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }🤓 Other versions and variantsDeclare Request Example Data
Cookie Parameters
Cookie Parameters 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Import Cookie
Declare Cookie parameters
Recap
Cookie Parameters¶
You can define Cookie parameters the same way you define Query and Path parameters.Import Cookie¶
First import Cookie:
from typing import Annotatedfrom fastapi import Cookie, 
app = FastAPI()
@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}🤓 Other versions and variants
Declare Cookie parameters¶
Then declare the cookie parameters using the same structure as with Path and Query.You can define the default value as well as all the extra validation or annotation parameters:
from typing import Annotatedfrom fastapi import Cookie, 
app = FastAPI()
@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}🤓 Other versions and variants
Technical DetailsCookie is a "sister" class of Path and Query. It also inherits from the same common Param class.But remember that when you import Query, Path, Cookie and others from fastapi, those are actually functions that return special classes.InfoTo declare cookies, you need to use Cookie, because otherwise the parameters would be interpreted as query parameters.Recap¶
Declare cookies with Cookie, using the same common pattern as Query and Path.
Extra Data Types
Header Parameters
Header Parameters 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Import Header
Declare Header parameters
Automatic conversion
Duplicate headers
Recap
Header Parameters¶
You can define Header parameters the same way you define Query, Path and Cookie parameters.Import Header¶
First import Header:
from typing import Annotatedfrom fastapi import FastAPI, Headerapp = FastAPI()
@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}🤓 Other versions and variants
Declare Header parameters¶
Then declare the header parameters using the same structure as with Path, Query and Cookie.You can define the default value as well as all the extra validation or annotation parameters:
from typing import Annotatedfrom fastapi import FastAPI, Headerapp = FastAPI()
@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}🤓 Other versions and variants
Technical DetailsHeader is a "sister" class of Path, Query and Cookie. It also inherits from the same common Param class.But remember that when you import Query, Path, Header, and others from fastapi, those are actually functions that return special classes.InfoTo declare headers, you need to use Header, because otherwise the parameters would be interpreted as query parameters.Automatic conversion¶
Header has a little extra functionality on top of what Path, Query and Cookie provide.Most of the standard headers are separated by a "hyphen" character, also known as the "minus symbol" (-).But a variable like user-agent is invalid in Python.So, by default, Header will convert the parameter names characters from underscore (_) to hyphen (-) to extract and document the headers.Also, HTTP headers are case-insensitive, so, you can declare them with standard Python style (also known as "snake_case").So, you can use user_agent as you normally would in Python code, instead of needing to capitalize the first letters as User_Agent or something similar.If for some reason you need to disable automatic conversion of underscores to hyphens, set the parameter convert_underscores of Header to False:
from typing import Annotatedfrom fastapi import FastAPI, Headerapp = FastAPI()
@app.get("/items/")
async def read_items(
    strange_header: Annotated[str | None, Header(convert_underscores=False)] = None,
):
    return {"strange_header": strange_header}🤓 Other versions and variants
WarningBefore setting convert_underscores to False, bear in mind that some HTTP proxies and servers disallow the usage of headers with underscores.Duplicate headers¶
It is possible to receive duplicate headers. That means, the same header with multiple values.You can define those cases using a list in the type declaration.You will receive all the values from the duplicate header as a Python list.For example, to declare a header of X-Token that can appear more than once, you can write:
from typing import Annotatedfrom fastapi import FastAPI, Headerapp = FastAPI()
@app.get("/items/")
async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}🤓 Other versions and variants
If you communicate with that path operation sending two HTTP headers like:
X-Token: foo
X-Token: bar
The response would be like:
{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
Recap¶
Declare headers with Header, using the same common pattern as Query, Path and Cookie.And don't worry about underscores in your variables, FastAPI will take care of converting them.
Cookie Parameters
Cookie Parameter Models
Cookie Parameter Models 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Cookies with a Pydantic Model
Check the Docs
Forbid Extra Cookies
Summary
Cookie Parameter Models¶
If you have a group of cookies that are related, you can create a Pydantic model to declare them. 🍪This would allow you to re-use the model in multiple places and also to declare validations and metadata for all the parameters at once. 😎NoteThis is supported since FastAPI version 0.115.0. 🤓TipThis same technique applies to Query, Cookie, and Header. 😎Cookies with a Pydantic Model¶
Declare the cookie parameters that you need in a Pydantic model, and then declare the parameter as Cookie:
from typing import Annotatedfrom fastapi import Cookie, from pydantic import BaseModelapp = FastAPI()
class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None
@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies🤓 Other versions and variants
FastAPI will extract the data for each field from the cookies received in the request and give you the Pydantic model you defined.Check the Docs¶
You can see the defined cookies in the docs UI at /docs:
InfoHave in mind that, as browsers handle cookies in special ways and behind the scenes, they don't easily allow JavaScript to touch them.If you go to the API docs UI at /docs you will be able to see the documentation for cookies for your path operations.But even if you fill the data and click "Execute", because the docs UI works with JavaScript, the cookies won't be sent, and you will see an error message as if you didn't write any values.Forbid Extra Cookies¶
In some special use cases (probably not very common), you might want to restrict the cookies that you want to receive.Your API now has the power to control its own cookie consent. 🤪🍪You can use Pydantic's model configuration to forbid any extra fields:
from typing import Annotated, Unionfrom fastapi import Cookie, from pydantic import BaseModelapp = FastAPI()
class Cookies(BaseModel):
    model_config = {"extra": "forbid"}    session_id: str
    fatebook_tracker: Union[str, None] = None
    googall_tracker: Union[str, None] = None
@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies🤓 Other versions and variants
If a client tries to send some extra cookies, they will receive an error response.Poor cookie banners with all their effort to get your consent for the API to reject it. 🍪For example, if the client tries to send a santa_tracker cookie with a value of good-list-please, the client will receive an error response telling them that the santa_tracker cookie is not allowed:
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["cookie", "santa_tracker"],
            "msg": "Extra inputs are not permitted",
            "input": "good-list-please",
        }
    ]
}
Summary¶
You can use Pydantic models to declare cookies in FastAPI. 😎
Header Parameters
Header Parameter Models
Header Parameter Models 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Header Parameters with a Pydantic Model
Check the Docs
Forbid Extra Headers
Summary
Header Parameter Models¶
If you have a group of related header parameters, you can create a Pydantic model to declare them.This would allow you to re-use the model in multiple places and also to declare validations and metadata for all the parameters at once. 😎NoteThis is supported since FastAPI version 0.115.0. 🤓Header Parameters with a Pydantic Model¶
Declare the header parameters that you need in a Pydantic model, and then declare the parameter as Header:
from typing import Annotatedfrom fastapi import FastAPI, Header
from pydantic import BaseModelapp = FastAPI()
class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []
@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers🤓 Other versions and variants
FastAPI will extract the data for each field from the headers in the request and give you the Pydantic model you defined.Check the Docs¶
You can see the required headers in the docs UI at /docs:
Forbid Extra Headers¶
In some special use cases (probably not very common), you might want to restrict the headers that you want to receive.You can use Pydantic's model configuration to forbid any extra fields:
from typing import Annotatedfrom fastapi import FastAPI, Header
from pydantic import BaseModelapp = FastAPI()
class CommonHeaders(BaseModel):
    model_config = {"extra": "forbid"}    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []
@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers🤓 Other versions and variants
If a client tries to send some extra headers, they will receive an error response.For example, if the client tries to send a tool header with a value of plumbus, they will receive an error response telling them that the header parameter tool is not allowed:
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["header", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus",
        }
    ]
}
Summary¶
You can use Pydantic models to declare headers in FastAPI. 😎
Cookie Parameter Models
Response Model - Return Type
Response Model - Return Type 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
response_model Parameter
response_model Priority
Return the same input data
Add an output model
response_model or Return Type
Return Type and Data Filtering
Type Annotations and Tooling
FastAPI Data Filtering
See it in the docs
Other Return Type Annotations
Return a Response Directly
Annotate a Response Subclass
Invalid Return Type Annotations
Disable Response Model
Response Model encoding parameters
Use the response_model_exclude_unset parameter
Data with values for fields with defaults
Data with the same values as the defaults
response_model_include and response_model_exclude
Using lists instead of sets
Recap
Response Model - Return Type¶
You can declare the type used for the response by annotating the path operation function return type.You can use type annotations the same way you would for input data in function parameters, you can use Pydantic models, lists, dictionaries, scalar values like integers, booleans, etc.
from fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item
@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]🤓 Other versions and variants
FastAPI will use this return type to:Validate the returned data.
If the data is invalid (e.g. you are missing a field), it means that your app code is broken, not returning what it should, and it will return a server error instead of returning incorrect data. This way you and your clients can be certain that they will receive the data and the data shape expected.
Add a JSON Schema for the response, in the OpenAPI path operation.
This will be used by the automatic docs.
It will also be used by automatic client code generation tools.
But most importantly:It will limit and filter the output data to what is defined in the return type.
This is particularly important for security, we'll see more of that below.
response_model Parameter¶
There are some cases where you need or want to return some data that is not exactly what the type declares.For example, you could want to return a dictionary or a database object, but declare it as a Pydantic model. This way the Pydantic model would do all the data documentation, validation, etc. for the object that you returned (e.g. a dictionary or database object).If you added the return type annotation, tools and editors would complain with a (correct) error telling you that your function is returning a type (e.g. a dict) that is different from what you declared (e.g. a Pydantic model).In those cases, you can use the path operation decorator parameter response_model instead of the return type.You can use the response_model parameter in any of the path operations:@app.get()
@app.post()
@app.put()
@app.delete()
etc.from typing import Anyfrom fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item
@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]🤓 Other versions and variants
NoteNotice that response_model is a parameter of the "decorator" method (get, post, etc). Not of your path operation function, like all the parameters and body.response_model receives the same type you would declare for a Pydantic model field, so, it can be a Pydantic model, but it can also be, e.g. a list of Pydantic models, like List[Item].FastAPI will use this response_model to do all the data documentation, validation, etc. and also to convert and filter the output data to its type declaration.TipIf you have strict type checks in your editor, mypy, etc, you can declare the function return type as Any.That way you tell the editor that you are intentionally returning anything. But FastAPI will still do the data documentation, validation, filtering, etc. with the response_model.response_model Priority¶
If you declare both a return type and a response_model, the response_model will take priority and be used by FastAPI.This way you can add correct type annotations to your functions even when you are returning a type different than the response model, to be used by the editor and tools like mypy. And still you can have FastAPI do the data validation, documentation, etc. using the response_model.You can also use response_model=None to disable creating a response model for that path operation, you might need to do it if you are adding type annotations for things that are not valid Pydantic fields, you will see an example of that in one of the sections below.Return the same input data¶
Here we are declaring a UserIn model, it will contain a plaintext password:
from fastapi import from pydantic import BaseModel, EmailStrapp = FastAPI()
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None
# Don't do this in production!
@app.post("/user/")
async def create_user(user: UserIn) -> UserIn:
    return user🤓 Other versions and variants
InfoTo use EmailStr, first install email-validator.Make sure you create a virtual environment, activate it, and then install it, for example:
$ pip install email-validator
or with:
$ pip install "pydantic[email]"
And we are using this model to declare our input and the same model to declare our output:
from fastapi import from pydantic import BaseModel, EmailStrapp = FastAPI()
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None
# Don't do this in production!
@app.post("/user/")
async def create_user(user: UserIn) -> UserIn:
    return user🤓 Other versions and variants
Now, whenever a browser is creating a user with a password, the API will return the same password in the response.In this case, it might not be a problem, because it's the same user sending the password.But if we use the same model for another path operation, we could be sending our user's passwords to every client.DangerNever store the plain password of a user or send it in a response like this, unless you know all the caveats and you know what you are doing.Add an output model¶
We can instead create an input model with the plaintext password and an output model without it:
from typing import Anyfrom fastapi import from pydantic import BaseModel, EmailStrapp = FastAPI()
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user🤓 Other versions and variants
Here, even though our path operation function is returning the same input user that contains the password:
from typing import Anyfrom fastapi import from pydantic import BaseModel, EmailStrapp = FastAPI()
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user🤓 Other versions and variants
...we declared the response_model to be our model UserOut, that doesn't include the password:
from typing import Anyfrom fastapi import from pydantic import BaseModel, EmailStrapp = FastAPI()
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user🤓 Other versions and variants
So, FastAPI will take care of filtering out all the data that is not declared in the output model (using Pydantic).response_model or Return Type¶
In this case, because the two models are different, if we annotated the function return type as UserOut, the editor and tools would complain that we are returning an invalid type, as those are different classes.That's why in this example we have to declare it in the response_model parameter....but continue reading below to see how to overcome that.Return Type and Data Filtering¶
Let's continue from the previous example. We wanted to annotate the function with one type, but we wanted to be able to return from the function something that actually includes more data.We want FastAPI to keep filtering the data using the response model. So that even though the function returns more data, the response will only include the fields declared in the response model.In the previous example, because the classes were different, we had to use the response_model parameter. But that also means that we don't get the support from the editor and tools checking the function return type.But in most of the cases where we need to do something like this, we want the model just to filter/remove some of the data as in this example.And in those cases, we can use classes and inheritance to take advantage of function type annotations to get better support in the editor and tools, and still get the FastAPI data filtering.
from fastapi import from pydantic import BaseModel, EmailStrapp = FastAPI()
class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
class UserIn(BaseUser):
    password: str
@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user🤓 Other versions and variants
With this, we get tooling support, from editors and mypy as this code is correct in terms of types, but we also get the data filtering from FastAPI.How does this work Let's check that out. 🤓Type Annotations and Tooling¶
First let's see how editors, mypy and other tools would see this.BaseUser has the base fields. Then UserIn inherits from BaseUser and adds the password field, so, it will include all the fields from both models.We annotate the function return type as BaseUser, but we are actually returning a UserIn instance.The editor, mypy, and other tools won't complain about this because, in typing terms, UserIn is a subclass of BaseUser, which means it's a valid type when what is expected is anything that is a BaseUser.FastAPI Data Filtering¶
Now, for FastAPI, it will see the return type and make sure that what you return includes only the fields that are declared in the type.FastAPI does several things internally with Pydantic to make sure that those same rules of class inheritance are not used for the returned data filtering, otherwise you could end up returning much more data than what you expected.This way, you can get the best of both worlds: type annotations with tooling support and data filtering.See it in the docs¶
When you see the automatic docs, you can check that the input model and output model will both have their own JSON Schema:And both models will be used for the interactive API documentation:Other Return Type Annotations¶
There might be cases where you return something that is not a valid Pydantic field and you annotate it in the function, only to get the support provided by tooling (the editor, mypy, etc).Return a Response Directly¶
The most common case would be returning a Response directly as explained later in the advanced docs.
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponseapp = FastAPI()
@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watchv=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})This simple case is handled automatically by FastAPI because the return type annotation is the class (or a subclass of) Response.And tools will also be happy because both RedirectResponse and JSONResponse are subclasses of Response, so the type annotation is correct.Annotate a Response Subclass¶
You can also use a subclass of Response in the type annotation:
from fastapi import from fastapi.responses import RedirectResponseapp = FastAPI()
@app.get("/teleport")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watchv=dQw4w9WgXcQ")This will also work because RedirectResponse is a subclass of Response, and FastAPI will automatically handle this simple case.Invalid Return Type Annotations¶
But when you return some other arbitrary object that is not a valid Pydantic type (e.g. a database object) and you annotate it like that in the function, FastAPI will try to create a Pydantic response model from that type annotation, and will fail.The same would happen if you had something like a union between different types where one or more of them are not valid Pydantic types, for example this would fail 💥:
from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponseapp = FastAPI()
@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watchv=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}🤓 Other versions and variants
...this fails because the type annotation is not a Pydantic type and is not just a single Response class or subclass, it's a union (any of the two) between a Response and a dict.Disable Response Model¶
Continuing from the example above, you might not want to have the default data validation, documentation, filtering, etc. that is performed by FastAPI.But you might want to still keep the return type annotation in the function to get the support from tools like editors and type checkers (e.g. mypy).In this case, you can disable the response model generation by setting response_model=None:
from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponseapp = FastAPI()
@app.get("/portal", response_model=None)
async def get_portal(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watchv=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}🤓 Other versions and variants
This will make FastAPI skip the response model generation and that way you can have any return type annotations you need without it affecting your FastAPI application. 🤓Response Model encoding parameters¶
Your response model could have default values, like:
from fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}
@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]🤓 Other versions and variants
description: Union[str, None] = None (or str | None = None in Python 3.10) has a default of None.
tax: float = 10.5 has a default of 10.5.
tags: List[str] = [] has a default of an empty list: [].
but you might want to omit them from the result if they were not actually stored.For example, if you have models with many optional attributes in a NoSQL database, but you don't want to send very long JSON responses full of default values.Use the response_model_exclude_unset parameter¶
You can set the path operation decorator parameter response_model_exclude_unset=True:
from fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}
@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]🤓 Other versions and variants
and those default values won't be included in the response, only the values actually set.So, if you send a request to that path operation for the item with ID foo, the response (not including default values) will be:
{
    "name": "Foo",
    "price": 50.2
}
InfoIn Pydantic v1 the method was called .dict(), it was deprecated (but still supported) in Pydantic v2, and renamed to .model_dump().The examples here use .dict() for compatibility with Pydantic v1, but you should use .model_dump() instead if you can use Pydantic v2.InfoFastAPI uses Pydantic model's .dict() with its exclude_unset parameter to achieve this.InfoYou can also use:response_model_exclude_defaults=True
response_model_exclude_none=True
as described in the Pydantic docs for exclude_defaults and exclude_none.Data with values for fields with defaults¶
But if your data has values for the model's fields with default values, like the item with ID bar:
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
they will be included in the response.Data with the same values as the defaults¶
If the data has the same values as the default ones, like the item with ID baz:
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
FastAPI is smart enough (actually, Pydantic is smart enough) to realize that, even though description, tax, and tags have the same values as the defaults, they were set explicitly (instead of taken from the defaults).So, they will be included in the JSON response.TipNotice that the default values can be anything, not only None.They can be a list ([]), a float of 10.5, etc.response_model_include and response_model_exclude¶
You can also use the path operation decorator parameters response_model_include and response_model_exclude.They take a set of str with the name of the attributes to include (omitting the rest) or to exclude (including the rest).This can be used as a quick shortcut if you have only one Pydantic model and want to remove some data from the output.TipBut it is still recommended to use the ideas above, using multiple classes, instead of these parameters.This is because the JSON Schema generated in your app's OpenAPI (and the docs) will still be the one for the complete model, even if you use response_model_include or response_model_exclude to omit some attributes.This also applies to response_model_by_alias that works similarly.
from fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}
@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]
@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]🤓 Other versions and variants
TipThe syntax {"name", "description"} creates a set with those two values.It is equivalent to set(["name", "description"]).Using lists instead of sets¶
If you forget to use a set and use a list or tuple instead, FastAPI will still convert it to a set and it will work correctly:
from fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}
@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include=["name", "description"],
)
async def read_item_name(item_id: str):
    return items[item_id]
@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude=["tax"])
async def read_item_public_data(item_id: str):
    return items[item_id]🤓 Other versions and variants
Recap¶
Use the path operation decorator's parameter response_model to define response models and especially to ensure private data is filtered out.Use response_model_exclude_unset to return only the values explicitly set.
Header Parameter Models
Extra Models
Extra Models 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Multiple models
About **user_in.dict()
Pydantic's .dict()
Unwrapping a dict
A Pydantic model from the contents of another
Unwrapping a dict and extra keywords
Reduce duplication
Union or anyOf
Union in Python 3.10
List of models
Response with arbitrary dict
Recap
Extra Models¶
Continuing with the previous example, it will be common to have more than one related model.This is especially the case for user models, because:The input model needs to be able to have a password.
The output model should not have a password.
The database model would probably need to have a hashed password.
DangerNever store user's plaintext passwords. Always store a "secure hash" that you can then verify.If you don't know, you will learn what a "password hash" is in the security chapters.Multiple models¶
Here's a general idea of how the models could look like with their password fields and the places where they are used:
from fastapi import from pydantic import BaseModel, EmailStrapp = FastAPI()
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None
def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password
def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db
@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved🤓 Other versions and variants
InfoIn Pydantic v1 the method was called .dict(), it was deprecated (but still supported) in Pydantic v2, and renamed to .model_dump().The examples here use .dict() for compatibility with Pydantic v1, but you should use .model_dump() instead if you can use Pydantic v2.About **user_in.dict()¶
Pydantic's .dict()¶
user_in is a Pydantic model of class UserIn.Pydantic models have a .dict() method that returns a dict with the model's data.So, if we create a Pydantic object user_in like:
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
and then we call:
user_dict = user_in.dict()
we now have a dict with the data in the variable user_dict (it's a dict instead of a Pydantic model object).And if we call:
print(user_dict)
we would get a Python dict with:
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
Unwrapping a dict¶
If we take a dict like user_dict and pass it to a function (or class) with **user_dict, Python will "unwrap" it. It will pass the keys and values of the user_dict directly as key-value arguments.So, continuing with the user_dict from above, writing:
UserInDB(**user_dict)
would result in something equivalent to:
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
Or more exactly, using user_dict directly, with whatever contents it might have in the future:
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
A Pydantic model from the contents of another¶
As in the example above we got user_dict from user_in.dict(), this code:
user_dict = user_in.dict()
UserInDB(**user_dict)
would be equivalent to:
UserInDB(**user_in.dict())
...because user_in.dict() is a dict, and then we make Python "unwrap" it by passing it to UserInDB prefixed with **.So, we get a Pydantic model from the data in another Pydantic model.Unwrapping a dict and extra keywords¶
And then adding the extra keyword argument hashed_password=hashed_password, like in:
UserInDB(**user_in.dict(), hashed_password=hashed_password)
...ends up being like:
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
WarningThe supporting additional functions fake_password_hasher and fake_save_user are just to demo a possible flow of the data, but they of course are not providing any real security.Reduce duplication¶
Reducing code duplication is one of the core ideas in FastAPI.As code duplication increments the chances of bugs, security issues, code desynchronization issues (when you update in one place but not in the others), etc.And these models are all sharing a lot of the data and duplicating attribute names and types.We could do better.We can declare a UserBase model that serves as a base for our other models. And then we can make subclasses of that model that inherit its attributes (type declarations, validation, etc).All the data conversion, validation, documentation, etc. will still work as normally.That way, we can declare just the differences between the models (with plaintext password, with hashed_password and without password):
from fastapi import from pydantic import BaseModel, EmailStrapp = FastAPI()
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
class UserIn(UserBase):
    password: str
class UserOut(UserBase):
    pass
class UserInDB(UserBase):
    hashed_password: str
def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password
def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db
@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved🤓 Other versions and variants
Union or anyOf¶
You can declare a response to be the Union of two or more types, that means, that the response would be any of them.It will be defined in OpenAPI with anyOf.To do that, use the standard Python type hint typing.Union:NoteWhen defining a Union, include the most specific type first, followed by the less specific type. In the example below, the more specific PlaneItem comes before CarItem in Union[PlaneItem, CarItem].
from typing import Unionfrom fastapi import from pydantic import BaseModelapp = FastAPI()
class BaseItem(BaseModel):
    description: str
    type: str
class CarItem(BaseItem):
    type: str = "car"
class PlaneItem(BaseItem):
    type: str = "plane"
    size: int
items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}
@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]🤓 Other versions and variants
Union in Python 3.10¶
In this example we pass Union[PlaneItem, CarItem] as the value of the argument response_model.Because we are passing it as a value to an argument instead of putting it in a type annotation, we have to use Union even in Python 3.10.If it was in a type annotation we could have used the vertical bar, as:
some_variable: PlaneItem | CarItem
But if we put that in the assignment response_model=PlaneItem | CarItem we would get an error, because Python would try to perform an invalid operation between PlaneItem and CarItem instead of interpreting that as a type annotation.List of models¶
The same way, you can declare responses of lists of objects.For that, use the standard Python typing.List (or just list in Python 3.9 and above):
from fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str
items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]
@app.get("/items/", response_model=list[Item])
async def read_items():
    return items🤓 Other versions and variants
Response with arbitrary dict¶
You can also declare a response using a plain arbitrary dict, declaring just the type of the keys and values, without using a Pydantic model.This is useful if you don't know the valid field/attribute names (that would be needed for a Pydantic model) beforehand.In this case, you can use typing.Dict (or just dict in Python 3.9 and above):
from fastapi import 
app = FastAPI()
@app.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}🤓 Other versions and variants
Recap¶
Use multiple Pydantic models and inherit freely for each case.You don't need to have a single data model per entity if that entity must be able to have different "states". As the case with the user "entity" with a state including password, password_hash and no password.
Response Model - Return Type
Response Status Code
Response Status Code 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
About HTTP status codes
Shortcut to remember the names
Changing the default
Response Status Code¶
The same way you can specify a response model, you can also declare the HTTP status code used for the response with the parameter status_code in any of the path operations:@app.get()
@app.post()
@app.put()
@app.delete()
etc.from fastapi import 
app = FastAPI()
@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}NoteNotice that status_code is a parameter of the "decorator" method (get, post, etc). Not of your path operation function, like all the parameters and body.The status_code parameter receives a number with the HTTP status code.Infostatus_code can alternatively also receive an IntEnum, such as Python's http.HTTPStatus.It will:Return that status code in the response.
Document it as such in the OpenAPI schema (and so, in the user interfaces):
NoteSome response codes (see the next section) indicate that the response does not have a body.FastAPI knows this, and will produce OpenAPI docs that state there is no response body.About HTTP status codes¶
NoteIf you already know what HTTP status codes are, skip to the next section.In HTTP, you send a numeric status code of 3 digits as part of the response.These status codes have a name associated to recognize them, but the important part is the number.In short:100 and above are for "Information". You rarely use them directly. Responses with these status codes cannot have a body.
200 and above are for "Successful" responses. These are the ones you would use the most.
200 is the default status code, which means everything was "OK".
Another example would be 201, "Created". It is commonly used after creating a new record in the database.
A special case is 204, "No Content". This response is used when there is no content to return to the client, and so the response must not have a body.
300 and above are for "Redirection". Responses with these status codes may or may not have a body, except for 304, "Not Modified", which must not have one.
400 and above are for "Client error" responses. These are the second type you would probably use the most.
An example is 404, for a "Not Found" response.
For generic errors from the client, you can just use 400.
500 and above are for server errors. You almost never use them directly. When something goes wrong at some part in your application code, or server, it will automatically return one of these status codes.
TipTo know more about each status code and which code is for what, check the MDN documentation about HTTP status codes.Shortcut to remember the names¶
Let's see the previous example again:
from fastapi import 
app = FastAPI()
@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}201 is the status code for "Created".But you don't have to memorize what each of these codes mean.You can use the convenience variables from fastapi.status.
from fastapi import FastAPI, statusapp = FastAPI()
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}They are just a convenience, they hold the same number, but that way you can use the editor's autocomplete to find them:Technical DetailsYou could also use from starlette import status.FastAPI provides the same starlette.status as fastapi.status just as a convenience for you, the developer. But it comes directly from Starlette.Changing the default¶
Later, in the Advanced User Guide, you will see how to return a different status code than the default you are declaring here.
Extra Models
Form Data
Form Data 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Import Form
Define Form parameters
About "Form Fields"
Recap
Form Data¶
When you need to receive form fields instead of JSON, you can use Form.InfoTo use forms, first install python-multipart.Make sure you create a virtual environment, activate it, and then install it, for example:
$ pip install python-multipart
Import Form¶
Import Form from fastapi:
from typing import Annotatedfrom fastapi import FastAPI, Formapp = FastAPI()
@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}🤓 Other versions and variants
Define Form parameters¶
Create form parameters the same way you would for Body or Query:
from typing import Annotatedfrom fastapi import FastAPI, Formapp = FastAPI()
@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}🤓 Other versions and variants
For example, in one of the ways the OAuth2 specification can be used (called "password flow") it is required to send a username and password as form fields.The spec requires the fields to be exactly named username and password, and to be sent as form fields, not JSON.With Form you can declare the same configurations as with Body (and Query, Path, Cookie), including validation, examples, an alias (e.g. user-name instead of username), etc.InfoForm is a class that inherits directly from Body.TipTo declare form bodies, you need to use Form explicitly, because without it the parameters would be interpreted as query parameters or body (JSON) parameters.About "Form Fields"¶
The way HTML forms (<form></form>) sends the data to the server normally uses a "special" encoding for that data, it's different from JSON.FastAPI will make sure to read that data from the right place instead of JSON.Technical DetailsData from forms is normally encoded using the "media type" application/x-www-form-urlencoded.But when the form includes files, it is encoded as multipart/form-data. You'll read about handling files in the next chapter.If you want to read more about these encodings and form fields, head to the MDN web docs for POST.WarningYou can declare multiple Form parameters in a path operation, but you can't also declare Body fields that you expect to receive as JSON, as the request will have the body encoded using application/x-www-form-urlencoded instead of application/json.This is not a limitation of FastAPI, it's part of the HTTP protocol.Recap¶
Use Form to declare form data input parameters.
Response Status Code
Form Models
Form Models 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Pydantic Models for Forms
Check the Docs
Forbid Extra Form Fields
Summary
Form Models¶
You can use Pydantic models to declare form fields in FastAPI.InfoTo use forms, first install python-multipart.Make sure you create a virtual environment, activate it, and then install it, for example:
$ pip install python-multipart
NoteThis is supported since FastAPI version 0.113.0. 🤓Pydantic Models for Forms¶
You just need to declare a Pydantic model with the fields you want to receive as form fields, and then declare the parameter as Form:
from typing import Annotatedfrom fastapi import FastAPI, Form
from pydantic import BaseModelapp = FastAPI()
class FormData(BaseModel):
    username: str
    password: str
@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data🤓 Other versions and variants
FastAPI will extract the data for each field from the form data in the request and give you the Pydantic model you defined.Check the Docs¶
You can verify it in the docs UI at /docs:
Forbid Extra Form Fields¶
In some special use cases (probably not very common), you might want to restrict the form fields to only those declared in the Pydantic model. And forbid any extra fields.NoteThis is supported since FastAPI version 0.114.0. 🤓You can use Pydantic's model configuration to forbid any extra fields:
from typing import Annotatedfrom fastapi import FastAPI, Form
from pydantic import BaseModelapp = FastAPI()
class FormData(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"}
@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data🤓 Other versions and variants
If a client tries to send some extra data, they will receive an error response.For example, if the client tries to send the form fields:username: Rick
password: Portal Gun
extra: Mr. Poopybutthole
They will receive an error response telling them that the field extra is not allowed:
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["body", "extra"],
            "msg": "Extra inputs are not permitted",
            "input": "Mr. Poopybutthole"
        }
    ]
}
Summary¶
You can use Pydantic models to declare form fields in FastAPI. 😎
Form Data
Request Files
Request Files 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Import File
Define File Parameters
File Parameters with UploadFile
UploadFile
What is "Form Data"
Optional File Upload
UploadFile with Additional Metadata
Multiple File Uploads
Multiple File Uploads with Additional Metadata
Recap
Request Files¶
You can define files to be uploaded by the client using File.InfoTo receive uploaded files, first install python-multipart.Make sure you create a virtual environment, activate it, and then install it, for example:
$ pip install python-multipart
This is because uploaded files are sent as "form data".Import File¶
Import File and UploadFile from fastapi:
from typing import Annotatedfrom fastapi import FastAPI, File, UploadFileapp = FastAPI()
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}🤓 Other versions and variants
Define File Parameters¶
Create file parameters the same way you would for Body or Form:
from typing import Annotatedfrom fastapi import FastAPI, File, UploadFileapp = FastAPI()
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}🤓 Other versions and variants
InfoFile is a class that inherits directly from Form.But remember that when you import Query, Path, File and others from fastapi, those are actually functions that return special classes.TipTo declare File bodies, you need to use File, because otherwise the parameters would be interpreted as query parameters or body (JSON) parameters.The files will be uploaded as "form data".If you declare the type of your path operation function parameter as bytes, FastAPI will read the file for you and you will receive the contents as bytes.Keep in mind that this means that the whole contents will be stored in memory. This will work well for small files.But there are several cases in which you might benefit from using UploadFile.File Parameters with UploadFile¶
Define a file parameter with a type of UploadFile:
from typing import Annotatedfrom fastapi import FastAPI, File, UploadFileapp = FastAPI()
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}🤓 Other versions and variants
Using UploadFile has several advantages over bytes:You don't have to use File() in the default value of the parameter.
It uses a "spooled" file:
A file stored in memory up to a maximum size limit, and after passing this limit it will be stored in disk.
This means that it will work well for large files like images, videos, large binaries, etc. without consuming all the memory.
You can get metadata from the uploaded file.
It has a file-like async interface.
It exposes an actual Python SpooledTemporaryFile object that you can pass directly to other libraries that expect a file-like object.
UploadFile¶
UploadFile has the following attributes:filename: A str with the original file name that was uploaded (e.g. myimage.jpg).
content_type: A str with the content type (MIME type / media type) (e.g. image/jpeg).
file: A SpooledTemporaryFile (a file-like object). This is the actual Python file object that you can pass directly to other functions or libraries that expect a "file-like" object.
UploadFile has the following async methods. They all call the corresponding file methods underneath (using the internal SpooledTemporaryFile).write(data): Writes data (str or bytes) to the file.
read(size): Reads size (int) bytes/characters of the file.
seek(offset): Goes to the byte position offset (int) in the file.
E.g., await myfile.seek(0) would go to the start of the file.
This is especially useful if you run await myfile.read() once and then need to read the contents again.
close(): Closes the file.
As all these methods are async methods, you need to "await" them.For example, inside of an async path operation function you can get the contents with:
contents = await myfile.read()
If you are inside of a normal def path operation function, you can access the UploadFile.file directly, for example:
contents = myfile.file.read()
async Technical DetailsWhen you use the async methods, FastAPI runs the file methods in a threadpool and awaits for them.Starlette Technical DetailsFastAPI's UploadFile inherits directly from Starlette's UploadFile, but adds some necessary parts to make it compatible with Pydantic and the other parts of FastAPI.What is "Form Data"¶
The way HTML forms (<form></form>) sends the data to the server normally uses a "special" encoding for that data, it's different from JSON.FastAPI will make sure to read that data from the right place instead of JSON.Technical DetailsData from forms is normally encoded using the "media type" application/x-www-form-urlencoded when it doesn't include files.But when the form includes files, it is encoded as multipart/form-data. If you use File, FastAPI will know it has to get the files from the correct part of the body.If you want to read more about these encodings and form fields, head to the MDN web docs for POST.WarningYou can declare multiple File and Form parameters in a path operation, but you can't also declare Body fields that you expect to receive as JSON, as the request will have the body encoded using multipart/form-data instead of application/json.This is not a limitation of FastAPI, it's part of the HTTP protocol.Optional File Upload¶
You can make a file optional by using standard type annotations and setting a default value of None:
from typing import Annotatedfrom fastapi import FastAPI, File, UploadFileapp = FastAPI()
@app.post("/files/")
async def create_file(file: Annotated[bytes | None, File()] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}🤓 Other versions and variants
UploadFile with Additional Metadata¶
You can also use File() with UploadFile, for example, to set additional metadata:
from typing import Annotatedfrom fastapi import FastAPI, File, UploadFileapp = FastAPI()
@app.post("/files/")
async def create_file(file: Annotated[bytes, File(description="A file read as bytes")]):
    return {"file_size": len(file)}
@app.post("/uploadfile/")
async def create_upload_file(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
):
    return {"filename": file.filename}🤓 Other versions and variants
Multiple File Uploads¶
It's possible to upload several files at the same time.They would be associated to the same "form field" sent using "form data".To use that, declare a list of bytes or UploadFile:
from typing import Annotatedfrom fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponseapp = FastAPI()
@app.post("/files/")
async def create_files(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}
@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}
@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)🤓 Other versions and variants
You will receive, as declared, a list of bytes or UploadFiles.Technical DetailsYou could also use from starlette.responses import HTMLResponse.FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette.Multiple File Uploads with Additional Metadata¶
And the same way as before, you can use File() to set additional parameters, even for UploadFile:
from typing import Annotatedfrom fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponseapp = FastAPI()
@app.post("/files/")
async def create_files(
    files: Annotated[list[bytes], File(description="Multiple files as bytes")],
):
    return {"file_sizes": [len(file) for file in files]}
@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    return {"filenames": [file.filename for file in files]}
@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)🤓 Other versions and variants
Recap¶
Use File, bytes, and UploadFile to declare files to be uploaded in the request, sent as form data.
Form Models
Request Forms and Files
Request Forms and Files 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Import File and Form
Define File and Form parameters
Recap
Request Forms and Files¶
You can define files and form fields at the same time using File and Form.InfoTo receive uploaded files and/or form data, first install python-multipart.Make sure you create a virtual environment, activate it, and then install it, for example:
$ pip install python-multipart
Import File and Form¶from typing import Annotatedfrom fastapi import FastAPI, File, Form, UploadFileapp = FastAPI()
@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }🤓 Other versions and variants
Define File and Form parameters¶
Create file and form parameters the same way you would for Body or Query:
from typing import Annotatedfrom fastapi import FastAPI, File, Form, UploadFileapp = FastAPI()
@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }🤓 Other versions and variants
The files and form fields will be uploaded as form data and you will receive the files and form fields.And you can declare some of the files as bytes and some as UploadFile.WarningYou can declare multiple File and Form parameters in a path operation, but you can't also declare Body fields that you expect to receive as JSON, as the request will have the body encoded using multipart/form-data instead of application/json.This is not a limitation of FastAPI, it's part of the HTTP protocol.Recap¶
Use File and Form together when you need to receive data and files in the same request.
Request Files
Handling Errors
Handling Errors 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Use HTTPException
Import HTTPException
Raise an HTTPException in your code
The resulting response
Add custom headers
Install custom exception handlers
Override the default exception handlers
Override request validation exceptions
RequestValidationError vs ValidationError
Override the HTTPException error handler
Use the RequestValidationError body
FastAPI's HTTPException vs Starlette's HTTPException
Reuse FastAPI's exception handlers
Handling Errors¶
There are many situations in which you need to notify an error to a client that is using your API.This client could be a browser with a frontend, a code from someone else, an IoT device, etc.You could need to tell the client that:The client doesn't have enough privileges for that operation.
The client doesn't have access to that resource.
The item the client was trying to access doesn't exist.
etc.
In these cases, you would normally return an HTTP status code in the range of 400 (from 400 to 499).This is similar to the 200 HTTP status codes (from 200 to 299). Those "200" status codes mean that somehow there was a "success" in the request.The status codes in the 400 range mean that there was an error from the client.Remember all those "404 Not Found" errors (and jokes)Use HTTPException¶
To return HTTP responses with errors to the client you use HTTPException.Import HTTPException¶from fastapi import FastAPI, HTTPExceptionapp = FastAPI()items = {"foo": "The Foo Wrestlers"}
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}Raise an HTTPException in your code¶
HTTPException is a normal Python exception with additional data relevant for APIs.Because it's a Python exception, you don't return it, you raise it.This also means that if you are inside a utility function that you are calling inside of your path operation function, and you raise the HTTPException from inside of that utility function, it won't run the rest of the code in the path operation function, it will terminate that request right away and send the HTTP error from the HTTPException to the client.The benefit of raising an exception over returning a value will be more evident in the section about Dependencies and Security.In this example, when the client requests an item by an ID that doesn't exist, raise an exception with a status code of 404:
from fastapi import FastAPI, HTTPExceptionapp = FastAPI()items = {"foo": "The Foo Wrestlers"}
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}The resulting response¶
If the client requests http://example.com/items/foo (an item_id "foo"), that client will receive an HTTP status code of 200, and a JSON response of:
{
  "item": "The Foo Wrestlers"
}
But if the client requests http://example.com/items/bar (a non-existent item_id "bar"), that client will receive an HTTP status code of 404 (the "not found" error), and a JSON response of:
{
  "detail": "Item not found"
}
TipWhen raising an HTTPException, you can pass any value that can be converted to JSON as the parameter detail, not only str.You could pass a dict, a list, etc.They are handled automatically by FastAPI and converted to JSON.Add custom headers¶
There are some situations in where it's useful to be able to add custom headers to the HTTP error. For example, for some types of security.You probably won't need to use it directly in your code.But in case you needed it for an advanced scenario, you can add custom headers:
from fastapi import FastAPI, HTTPExceptionapp = FastAPI()items = {"foo": "The Foo Wrestlers"}
@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}Install custom exception handlers¶
You can add custom exception handlers with the same exception utilities from Starlette.Let's say you have a custom exception UnicornException that you (or a library you use) might raise.And you want to handle this exception globally with FastAPI.You could add a custom exception handler with @app.exception_handler():
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name
app = FastAPI()
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )
@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}Here, if you request /unicorns/yolo, the path operation will raise a UnicornException.But it will be handled by the unicorn_exception_handler.So, you will receive a clean error, with an HTTP status code of 418 and a JSON content of:
{"message": "Oops! yolo did something. There goes a rainbow..."}
Technical DetailsYou could also use from starlette.requests import Request and from starlette.responses import JSONResponse.FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette. The same with Request.Override the default exception handlers¶
FastAPI has some default exception handlers.These handlers are in charge of returning the default JSON responses when you raise an HTTPException and when the request has invalid data.You can override these exception handlers with your own.Override request validation exceptions¶
When a request contains invalid data, FastAPI internally raises a RequestValidationError.And it also includes a default exception handler for it.To override it, import the RequestValidationError and use it with @app.exception_handler(RequestValidationError) to decorate the exception handler.The exception handler will receive a Request and the exception.
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPExceptionapp = FastAPI()
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}Now, if you go to /items/foo, instead of getting the default JSON error with:
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
you will get a text version, with:
1 validation error
path -> item_id
  value is not a valid integer (type=type_error.integer)
RequestValidationError vs ValidationError¶
WarningThese are technical details that you might skip if it's not important for you now.RequestValidationError is a sub-class of Pydantic's ValidationError.FastAPI uses it so that, if you use a Pydantic model in response_model, and your data has an error, you will see the error in your log.But the client/user will not see it. Instead, the client will receive an "Internal Server Error" with an HTTP status code 500.It should be this way because if you have a Pydantic ValidationError in your response or anywhere in your code (not in the client's request), it's actually a bug in your code.And while you fix it, your clients/users shouldn't have access to internal information about the error, as that could expose a security vulnerability.Override the HTTPException error handler¶
The same way, you can override the HTTPException handler.For example, you could want to return a plain text response instead of JSON for these errors:
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPExceptionapp = FastAPI()
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}Technical DetailsYou could also use from starlette.responses import PlainTextResponse.FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette.Use the RequestValidationError body¶
The RequestValidationError contains the body it received with invalid data.You could use it while developing your app to log the body and debug it, return it to the user, etc.
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModelapp = FastAPI()
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
class Item(BaseModel):
    title: str
    size: int
@app.post("/items/")
async def create_item(item: Item):
    return itemNow try sending an invalid item like:
{
  "title": "towel",
  "size": "XL"
}
You will receive a response telling you that the data is invalid containing the received body:
{
  "detail": [
    {
      "loc": [
        "body",
        "size"
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ],
  "body": {
    "title": "towel",
    "size": "XL"
  }
}
FastAPI's HTTPException vs Starlette's HTTPException¶
FastAPI has its own HTTPException.And FastAPI's HTTPException error class inherits from Starlette's HTTPException error class.The only difference is that FastAPI's HTTPException accepts any JSON-able data for the detail field, while Starlette's HTTPException only accepts strings for it.So, you can keep raising FastAPI's HTTPException as normally in your code.But when you register an exception handler, you should register it for Starlette's HTTPException.This way, if any part of Starlette's internal code, or a Starlette extension or plug-in, raises a Starlette HTTPException, your handler will be able to catch and handle it.In this example, to be able to have both HTTPExceptions in the same code, Starlette's exceptions is renamed to StarletteHTTPException:
from starlette.exceptions import HTTPException as StarletteHTTPException
Reuse FastAPI's exception handlers¶
If you want to use the exception along with the same default exception handlers from FastAPI, you can import and reuse the default exception handlers from fastapi.exception_handlers:
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPExceptionapp = FastAPI()
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}In this example you are just printing the error with a very expressive message, but you get the idea. You can use the exception and then just reuse the default exception handlers.
Request Forms and Files
Path Operation Configuration
Path Operation Configuration 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Response Status Code
Tags
Tags with Enums
Summary and description
Description from docstring
Response description
Deprecate a path operation
Recap
Path Operation Configuration¶
There are several parameters that you can pass to your path operation decorator to configure it.WarningNotice that these parameters are passed directly to the path operation decorator, not to your path operation function.Response Status Code¶
You can define the (HTTP) status_code to be used in the response of your path operation.You can pass directly the int code, like 404.But if you don't remember what each number code is for, you can use the shortcut constants in status:
from fastapi import FastAPI, status
from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item🤓 Other versions and variants
That status code will be used in the response and will be added to the OpenAPI schema.Technical DetailsYou could also use from starlette import status.FastAPI provides the same starlette.status as fastapi.status just as a convenience for you, the developer. But it comes directly from Starlette.Tags¶
You can add tags to your path operation, pass the parameter tags with a list of str (commonly just one str):
from fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
@app.post("/items/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item
@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]
@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]🤓 Other versions and variants
They will be added to the OpenAPI schema and used by the automatic documentation interfaces:Tags with Enums¶
If you have a big application, you might end up accumulating several tags, and you would want to make sure you always use the same tag for related path operations.In these cases, it could make sense to store the tags in an Enum.FastAPI supports that the same way as with plain strings:
from enum import Enumfrom fastapi import 
app = FastAPI()
class Tags(Enum):
    items = "items"
    users = "users"
@app.get("/items/", tags=[Tags.items])
async def get_items():
    return ["Portal gun", "Plumbus"]
@app.get("/users/", tags=[Tags.users])
async def read_users():
    return ["Rick", "Morty"]Summary and description¶
You can add a summary and description:
from fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    return item🤓 Other versions and variants
Description from docstring¶
As descriptions tend to be long and cover multiple lines, you can declare the path operation description in the function docstring and FastAPI will read it from there.You can write Markdown in the docstring, it will be interpreted and displayed correctly (taking into account docstring indentation).
from fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
@app.post("/items/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item🤓 Other versions and variants
It will be used in the interactive docs:Response description¶
You can specify the response description with the parameter response_description:
from fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item",
)
async def create_item(item: Item):
    """
    Create an item with all the information:    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item🤓 Other versions and variants
InfoNotice that response_description refers specifically to the response, the description refers to the path operation in general.CheckOpenAPI specifies that each path operation requires a response description.So, if you don't provide one, FastAPI will automatically generate one of "Successful response".Deprecate a path operation¶
If you need to mark a path operation as deprecated, but without removing it, pass the parameter deprecated:
from fastapi import 
app = FastAPI()
@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]
@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]
@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]It will be clearly marked as deprecated in the interactive docs:Check how deprecated and non-deprecated path operations look like:Recap¶
You can configure and add metadata for your path operations easily by passing parameters to the path operation decorators.
Handling Errors
JSON Compatible Encoder
JSON Compatible Encoder 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Using the jsonable_encoder
JSON Compatible Encoder¶
There are some cases where you might need to convert a data type (like a Pydantic model) to something compatible with JSON (like a dict, list, etc).For example, if you need to store it in a database.For that, FastAPI provides a jsonable_encoder() function.Using the jsonable_encoder¶
Let's imagine that you have a database fake_db that only receives JSON compatible data.For example, it doesn't receive datetime objects, as those are not compatible with JSON.So, a datetime object would have to be converted to a str containing the data in ISO format.The same way, this database wouldn't receive a Pydantic model (an object with attributes), only a dict.You can use jsonable_encoder for that.It receives an object, like a Pydantic model, and returns a JSON compatible version:
from datetime import datetimefrom fastapi import from fastapi.encoders import jsonable_encoder
from pydantic import BaseModelfake_db = {}
class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None
app = FastAPI()
@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data🤓 Other versions and variants
In this example, it would convert the Pydantic model to a dict, and the datetime to a str.The result of calling it is something that can be encoded with the Python standard json.dumps().It doesn't return a large str containing the data in JSON format (as a string). It returns a Python standard data structure (e.g. a dict) with values and sub-values that are all compatible with JSON.Notejsonable_encoder is actually used by FastAPI internally to convert data. But it is useful in many other scenarios.
Path Operation Configuration
Body - Updates
Body - Updates 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Update replacing with PUT
Warning about replacing
Partial updates with PATCH
Using Pydantic's exclude_unset parameter
Using Pydantic's update parameter
Partial updates recap
Body - Updates¶
Update replacing with PUT¶
To update an item you can use the HTTP PUT operation.You can use the jsonable_encoder to convert the input data to data that can be stored as JSON (e.g. with a NoSQL database). For example, converting datetime to str.
from fastapi import from fastapi.encoders import jsonable_encoder
from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded🤓 Other versions and variants
PUT is used to receive data that should replace the existing data.Warning about replacing¶
That means that if you want to update the item bar using PUT with a body containing:
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
because it doesn't include the already stored attribute "tax": 20.2, the input model would take the default value of "tax": 10.5.And the data would be saved with that "new" tax of 10.5.Partial updates with PATCH¶
You can also use the HTTP PATCH operation to partially update data.This means that you can send only the data that you want to update, leaving the rest intact.NotePATCH is less commonly used and known than PUT.And many teams use only PUT, even for partial updates.You are free to use them however you want, FastAPI doesn't impose any restrictions.But this guide shows you, more or less, how they are intended to be used.Using Pydantic's exclude_unset parameter¶
If you want to receive partial updates, it's very useful to use the parameter exclude_unset in Pydantic's model's .model_dump().Like item.model_dump(exclude_unset=True).InfoIn Pydantic v1 the method was called .dict(), it was deprecated (but still supported) in Pydantic v2, and renamed to .model_dump().The examples here use .dict() for compatibility with Pydantic v1, but you should use .model_dump() instead if you can use Pydantic v2.That would generate a dict with only the data that was set when creating the item model, excluding default values.Then you can use this to generate a dict with only the data that was set (sent in the request), omitting default values:
from fastapi import from fastapi.encoders import jsonable_encoder
from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]
@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item🤓 Other versions and variants
Using Pydantic's update parameter¶
Now, you can create a copy of the existing model using .model_copy(), and pass the update parameter with a dict containing the data to update.InfoIn Pydantic v1 the method was called .copy(), it was deprecated (but still supported) in Pydantic v2, and renamed to .model_copy().The examples here use .copy() for compatibility with Pydantic v1, but you should use .model_copy() instead if you can use Pydantic v2.Like stored_item_model.model_copy(update=update_data):
from fastapi import from fastapi.encoders import jsonable_encoder
from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]
@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item🤓 Other versions and variants
Partial updates recap¶
In summary, to apply partial updates you would:(Optionally) use PATCH instead of PUT.
Retrieve the stored data.
Put that data in a Pydantic model.
Generate a dict without default values from the input model (using exclude_unset).
This way you can update only the values actually set by the user, instead of overriding values already stored with default values in your model.
Create a copy of the stored model, updating its attributes with the received partial updates (using the update parameter).
Convert the copied model to something that can be stored in your DB (for example, using the jsonable_encoder).
This is comparable to using the model's .model_dump() method again, but it makes sure (and converts) the values to data types that can be converted to JSON, for example, datetime to str.
Save the data to your DB.
Return the updated model.from fastapi import from fastapi.encoders import jsonable_encoder
from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]
@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item🤓 Other versions and variants
TipYou can actually use this same technique with an HTTP PUT operation.But the example here uses PATCH because it was created for these use cases.NoteNotice that the input model is still validated.So, if you want to receive partial updates that can omit all the attributes, you need to have a model with all the attributes marked as optional (with default values or None).To distinguish from the models with all optional values for updates and models with required values for creation, you can use the ideas described in Extra Models.
JSON Compatible Encoder
Dependencies
Dependencies 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Classes as Dependencies
Sub-dependencies
Dependencies in path operation decorators
Global Dependencies
Dependencies with yield
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
What is "Dependency Injection"
First Steps
Create a dependency, or "dependable"
Import Depends
Declare the dependency, in the "dependant"
Share Annotated dependencies
To async or not to async
Integrated with OpenAPI
Simple usage
FastAPI plug-ins
FastAPI compatibility
Simple and Powerful
Integrated with OpenAPI
Dependencies
Dependencies¶
FastAPI has a very powerful but intuitive Dependency Injection system.It is designed to be very simple to use, and to make it very easy for any developer to integrate other components with FastAPI.What is "Dependency Injection"¶
"Dependency Injection" means, in programming, that there is a way for your code (in this case, your path operation functions) to declare things that it requires to work and use: "dependencies".And then, that system (in this case FastAPI) will take care of doing whatever is needed to provide your code with those needed dependencies ("inject" the dependencies).This is very useful when you need to:Have shared logic (the same code logic again and again).
Share database connections.
Enforce security, authentication, role requirements, etc.
And many other things...
All these, while minimizing code repetition.First Steps¶
Let's see a very simple example. It will be so simple that it is not very useful, for now.But this way we can focus on how the Dependency Injection system works.Create a dependency, or "dependable"¶
Let's first focus on the dependency.It is just a function that can take all the same parameters that a path operation function can take:
from typing import Annotatedfrom fastapi import Depends, 
app = FastAPI()
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}
@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons🤓 Other versions and variants
That's it.2 lines.And it has the same shape and structure that all your path operation functions have.You can think of it as a path operation function without the "decorator" (without the @app.get("/some-path")).And it can return anything you want.In this case, this dependency expects:An optional query parameter q that is a str.
An optional query parameter skip that is an int, and by default is 0.
An optional query parameter limit that is an int, and by default is 100.
And then it just returns a dict containing those values.InfoFastAPI added support for Annotated (and started recommending it) in version 0.95.0.If you have an older version, you would get errors when trying to use Annotated.Make sure you Upgrade the FastAPI version to at least 0.95.1 before using Annotated.Import Depends¶from typing import Annotatedfrom fastapi import Depends, 
app = FastAPI()
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}
@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons🤓 Other versions and variants
Declare the dependency, in the "dependant"¶
The same way you use Body, Query, etc. with your path operation function parameters, use Depends with a new parameter:
from typing import Annotatedfrom fastapi import Depends, 
app = FastAPI()
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}
@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons🤓 Other versions and variants
Although you use Depends in the parameters of your function the same way you use Body, Query, etc, Depends works a bit differently.You only give Depends a single parameter.This parameter must be something like a function.You don't call it directly (don't add the parenthesis at the end), you just pass it as a parameter to Depends().And that function takes parameters in the same way that path operation functions do.TipYou'll see what other "things", apart from functions, can be used as dependencies in the next chapter.Whenever a new request arrives, FastAPI will take care of:Calling your dependency ("dependable") function with the correct parameters.
Get the result from your function.
Assign that result to the parameter in your path operation function.
common_parameters
/items/
/users/
This way you write shared code once and FastAPI takes care of calling it for your path operations.CheckNotice that you don't have to create a special class and pass it somewhere to FastAPI to "register" it or anything similar.You just pass it to Depends and FastAPI knows how to do the rest.Share Annotated dependencies¶
In the examples above, you see that there's a tiny bit of code duplication.When you need to use the common_parameters() dependency, you have to write the whole parameter with the type annotation and Depends():
commons: Annotated[dict, Depends(common_parameters)]
But because we are using Annotated, we can store that Annotated value in a variable and use it in multiple places:
from typing import Annotatedfrom fastapi import Depends, 
app = FastAPI()
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}
CommonsDep = Annotated[dict, Depends(common_parameters)]
@app.get("/items/")
async def read_items(commons: CommonsDep):
    return commons
@app.get("/users/")
async def read_users(commons: CommonsDep):
    return commons🤓 Other versions and variants
TipThis is just standard Python, it's called a "type alias", it's actually not specific to FastAPI.But because FastAPI is based on the Python standards, including Annotated, you can use this trick in your code. 😎The dependencies will keep working as expected, and the best part is that the type information will be preserved, which means that your editor will be able to keep providing you with autocompletion, inline errors, etc. The same for other tools like mypy.This will be especially useful when you use it in a large code base where you use the same dependencies over and over again in many path operations.To async or not to async¶
As dependencies will also be called by FastAPI (the same as your path operation functions), the same rules apply while defining your functions.You can use async def or normal def.And you can declare dependencies with async def inside of normal def path operation functions, or def dependencies inside of async def path operation functions, etc.It doesn't matter. FastAPI will know what to do.NoteIf you don't know, check the Async: "In a hurry" section about async and await in the docs.Integrated with OpenAPI¶
All the request declarations, validations and requirements of your dependencies (and sub-dependencies) will be integrated in the same OpenAPI schema.So, the interactive docs will have all the information from these dependencies too:Simple usage¶
If you look at it, path operation functions are declared to be used whenever a path and operation matches, and then FastAPI takes care of calling the function with the correct parameters, extracting the data from the request.Actually, all (or most) of the web frameworks work in this same way.You never call those functions directly. They are called by your framework (in this case, FastAPI).With the Dependency Injection system, you can also tell FastAPI that your path operation function also "depends" on something else that should be executed before your path operation function, and FastAPI will take care of executing it and "injecting" the results.Other common terms for this same idea of "dependency injection" are:providers
services
injectables
components
FastAPI plug-ins¶
Integrations and "plug-ins" can be built using the Dependency Injection system. But in fact, there is actually no need to create "plug-ins", as by using dependencies it's possible to declare an infinite number of integrations and interactions that become available to your path operation functions.And dependencies can be created in a very simple and intuitive way that allows you to just import the Python packages you need, and integrate them with your API functions in a couple of lines of code, literally.You will see examples of this in the next chapters, about relational and NoSQL databases, security, etc.FastAPI compatibility¶
The simplicity of the dependency injection system makes FastAPI compatible with:all the relational databases
NoSQL databases
external packages
external APIs
authentication and authorization systems
API usage monitoring systems
response data injection systems
etc.
Simple and Powerful¶
Although the hierarchical dependency injection system is very simple to define and use, it's still very powerful.You can define dependencies that in turn can define dependencies themselves.In the end, a hierarchical tree of dependencies is built, and the Dependency Injection system takes care of solving all these dependencies for you (and their sub-dependencies) and providing (injecting) the results at each step.For example, let's say you have 4 API endpoints (path operations):/items/public/
/items/private/
/users/{user_id}/activate
/items/pro/
then you could add different permission requirements for each of them just with dependencies and sub-dependencies:current_user
active_user
admin_user
paying_user
/items/public/
/items/private/
/users/{user_id}/activate
/items/pro/
Integrated with OpenAPI¶
All these dependencies, while declaring their requirements, also add parameters, validations, etc. to your path operations.FastAPI will take care of adding it all to the OpenAPI schema, so that it is shown in the interactive documentation systems.
Body - Updates
Classes as Dependencies
Classes as Dependencies 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Classes as Dependencies
Sub-dependencies
Dependencies in path operation decorators
Global Dependencies
Dependencies with yield
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
A dict from the previous example
What makes a dependency
Classes as dependencies
Use it
Type annotation vs Depends
Shortcut
Dependencies
Classes as Dependencies¶
Before diving deeper into the Dependency Injection system, let's upgrade the previous example.A dict from the previous example¶
In the previous example, we were returning a dict from our dependency ("dependable"):
from typing import Annotatedfrom fastapi import Depends, 
app = FastAPI()
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}
@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons🤓 Other versions and variants
But then we get a dict in the parameter commons of the path operation function.And we know that editors can't provide a lot of support (like completion) for dicts, because they can't know their keys and value types.We can do better...What makes a dependency¶
Up to now you have seen dependencies declared as functions.But that's not the only way to declare dependencies (although it would probably be the more common).The key factor is that a dependency should be a "callable".A "callable" in Python is anything that Python can "call" like a function.So, if you have an object something (that might not be a function) and you can "call" it (execute it) like:
something()
or
something(some_argument, some_keyword_argument="foo")
then it is a "callable".Classes as dependencies¶
You might notice that to create an instance of a Python class, you use that same syntax.For example:
class Cat:
    def __init__(self, name: str):
        self.name = name
fluffy = Cat(name="Mr Fluffy")
In this case, fluffy is an instance of the class Cat.And to create fluffy, you are "calling" Cat.So, a Python class is also a callable.Then, in FastAPI, you could use a Python class as a dependency.What FastAPI actually checks is that it is a "callable" (function, class or anything else) and the parameters defined.If you pass a "callable" as a dependency in FastAPI, it will analyze the parameters for that "callable", and process them in the same way as the parameters for a path operation function. Including sub-dependencies.That also applies to callables with no parameters at all. The same as it would be for path operation functions with no parameters.Then, we can change the dependency "dependable" common_parameters from above to the class CommonQueryParams:
from typing import Annotatedfrom fastapi import Depends, 
app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit
@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response🤓 Other versions and variants
Pay attention to the __init__ method used to create the instance of the class:
from typing import Annotatedfrom fastapi import Depends, 
app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit
@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response🤓 Other versions and variants
...it has the same parameters as our previous common_parameters:
from typing import Annotatedfrom fastapi import Depends, 
app = FastAPI()
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}
@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons🤓 Other versions and variants
Those parameters are what FastAPI will use to "solve" the dependency.In both cases, it will have:An optional q query parameter that is a str.
A skip query parameter that is an int, with a default of 0.
A limit query parameter that is an int, with a default of 100.
In both cases the data will be converted, validated, documented on the OpenAPI schema, etc.Use it¶
Now you can declare your dependency using this class.
from typing import Annotatedfrom fastapi import Depends, 
app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit
@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response🤓 Other versions and variants
FastAPI calls the CommonQueryParams class. This creates an "instance" of that class and the instance will be passed as the parameter commons to your function.Type annotation vs Depends¶
Notice how we write CommonQueryParams twice in the above code: non-Annotatedcommons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]The last CommonQueryParams, in:
... Depends(CommonQueryParams)
...is what FastAPI will actually use to know what is the dependency.It is from this one that FastAPI will extract the declared parameters and that is what FastAPI will actually call.In this case, the first CommonQueryParams, in: non-Annotatedcommons: Annotated[CommonQueryParams, ......doesn't have any special meaning for FastAPI. FastAPI won't use it for data conversion, validation, etc. (as it is using the Depends(CommonQueryParams) for that).You could actually write just: non-Annotatedcommons: Annotated[Any, Depends(CommonQueryParams)]...as in:
from typing import Annotated, Anyfrom fastapi import Depends, 
app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit
@app.get("/items/")
async def read_items(commons: Annotated[Any, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response🤓 Other versions and variants
But declaring the type is encouraged as that way your editor will know what will be passed as the parameter commons, and then it can help you with code completion, type checks, etc:Shortcut¶
But you see that we are having some code repetition here, writing CommonQueryParams twice: non-Annotatedcommons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]FastAPI provides a shortcut for these cases, in where the dependency is specifically a class that FastAPI will "call" to create an instance of the class itself.For those specific cases, you can do the following:Instead of writing: non-Annotatedcommons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]...you write:Python 3.8 non-Annotatedcommons: Annotated[CommonQueryParams, Depends()]You declare the dependency as the type of the parameter, and you use Depends() without any parameter, instead of having to write the full class again inside of Depends(CommonQueryParams).The same example would then look like:
from typing import Annotatedfrom fastapi import Depends, 
app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit
@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends()]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response🤓 Other versions and variants
...and FastAPI will know what to do.TipIf that seems more confusing than helpful, disregard it, you don't need it.It is just a shortcut. Because FastAPI cares about helping you minimize code repetition.
Dependencies
Sub-dependencies
Sub-dependencies 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Classes as Dependencies
Sub-dependencies
Dependencies in path operation decorators
Global Dependencies
Dependencies with yield
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
First dependency "dependable"
Second dependency, "dependable" and "dependant"
Use the dependency
Using the same dependency multiple times
Recap
Dependencies
Sub-dependencies¶
You can create dependencies that have sub-dependencies.They can be as deep as you need them to be.FastAPI will take care of solving them.First dependency "dependable"¶
You could create a first dependency ("dependable") like:
from typing import Annotatedfrom fastapi import Cookie, Depends, 
app = FastAPI()
def query_extractor(q: str | None = None):
    return q
def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q
@app.get("/items/")
async def read_query(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
):
    return {"q_or_cookie": query_or_default}🤓 Other versions and variants
It declares an optional query parameter q as a str, and then it just returns it.This is quite simple (not very useful), but will help us focus on how the sub-dependencies work.Second dependency, "dependable" and "dependant"¶
Then you can create another dependency function (a "dependable") that at the same time declares a dependency of its own (so it is a "dependant" too):
from typing import Annotatedfrom fastapi import Cookie, Depends, 
app = FastAPI()
def query_extractor(q: str | None = None):
    return q
def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q
@app.get("/items/")
async def read_query(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
):
    return {"q_or_cookie": query_or_default}🤓 Other versions and variants
Let's focus on the parameters declared:Even though this function is a dependency ("dependable") itself, it also declares another dependency (it "depends" on something else).
It depends on the query_extractor, and assigns the value returned by it to the parameter q.
It also declares an optional last_query cookie, as a str.
If the user didn't provide any query q, we use the last query used, which we saved to a cookie before.
Use the dependency¶
Then we can use the dependency with:
from typing import Annotatedfrom fastapi import Cookie, Depends, 
app = FastAPI()
def query_extractor(q: str | None = None):
    return q
def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q
@app.get("/items/")
async def read_query(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
):
    return {"q_or_cookie": query_or_default}🤓 Other versions and variants
InfoNotice that we are only declaring one dependency in the path operation function, the query_or_cookie_extractor.But FastAPI will know that it has to solve query_extractor first, to pass the results of that to query_or_cookie_extractor while calling it.query_extractor
query_or_cookie_extractor
/items/
Using the same dependency multiple times¶
If one of your dependencies is declared multiple times for the same path operation, for example, multiple dependencies have a common sub-dependency, FastAPI will know to call that sub-dependency only once per request.And it will save the returned value in a "cache" and pass it to all the "dependants" that need it in that specific request, instead of calling the dependency multiple times for the same request.In an advanced scenario where you know you need the dependency to be called at every step (possibly multiple times) in the same request instead of using the "cached" value, you can set the parameter use_cache=False when using Depends: non-Annotatedasync def needy_dependency(fresh_value: Annotated[str, Depends(get_value, use_cache=False)]):
    return {"fresh_value": fresh_value}Recap¶
Apart from all the fancy words used here, the Dependency Injection system is quite simple.Just functions that look the same as the path operation functions.But still, it is very powerful, and allows you to declare arbitrarily deeply nested dependency "graphs" (trees).TipAll this might not seem as useful with these simple examples.But you will see how useful it is in the chapters about security.And you will also see the amounts of code it will save you.
Classes as Dependencies
Dependencies in path operation decorators
Dependencies in path operation decorators 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Classes as Dependencies
Sub-dependencies
Dependencies in path operation decorators
Global Dependencies
Dependencies with yield
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Add dependencies to the path operation decorator
Dependencies errors and return values
Dependency requirements
Raise exceptions
Return values
Dependencies for a group of path operations
Global Dependencies
Dependencies
Dependencies in path operation decorators¶
In some cases you don't really need the return value of a dependency inside your path operation function.Or the dependency doesn't return a value.But you still need it to be executed/solved.For those cases, instead of declaring a path operation function parameter with Depends, you can add a list of dependencies to the path operation decorator.Add dependencies to the path operation decorator¶
The path operation decorator receives an optional argument dependencies.It should be a list of Depends():
from typing import Annotatedfrom fastapi import Depends, FastAPI, Header, HTTPExceptionapp = FastAPI()
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key
@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]🤓 Other versions and variants
These dependencies will be executed/solved the same way as normal dependencies. But their value (if they return any) won't be passed to your path operation function.TipSome editors check for unused function parameters, and show them as errors.Using these dependencies in the path operation decorator you can make sure they are executed while avoiding editor/tooling errors.It might also help avoid confusion for new developers that see an unused parameter in your code and could think it's unnecessary.InfoIn this example we use invented custom headers X-Key and X-Token.But in real cases, when implementing security, you would get more benefits from using the integrated Security utilities (the next chapter).Dependencies errors and return values¶
You can use the same dependency functions you use normally.Dependency requirements¶
They can declare request requirements (like headers) or other sub-dependencies:
from typing import Annotatedfrom fastapi import Depends, FastAPI, Header, HTTPExceptionapp = FastAPI()
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key
@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]🤓 Other versions and variants
Raise exceptions¶
These dependencies can raise exceptions, the same as normal dependencies:
from typing import Annotatedfrom fastapi import Depends, FastAPI, Header, HTTPExceptionapp = FastAPI()
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key
@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]🤓 Other versions and variants
Return values¶
And they can return values or not, the values won't be used.So, you can reuse a normal dependency (that returns a value) you already use somewhere else, and even though the value won't be used, the dependency will be executed:
from typing import Annotatedfrom fastapi import Depends, FastAPI, Header, HTTPExceptionapp = FastAPI()
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key
@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]🤓 Other versions and variants
Dependencies for a group of path operations¶
Later, when reading about how to structure bigger applications (Bigger Applications - Multiple Files), possibly with multiple files, you will learn how to declare a single dependencies parameter for a group of path operations.Global Dependencies¶
Next we will see how to add dependencies to the whole FastAPI application, so that they apply to each path operation.
Sub-dependencies
Global Dependencies
Global Dependencies 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Classes as Dependencies
Sub-dependencies
Dependencies in path operation decorators
Global Dependencies
Dependencies with yield
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Dependencies for groups of path operations
Dependencies
Global Dependencies¶
For some types of applications you might want to add dependencies to the whole application.Similar to the way you can add dependencies to the path operation decorators, you can add them to the FastAPI application.In that case, they will be applied to all the path operations in the application:
from fastapi import Depends, FastAPI, Header, HTTPException
from typing_extensions import Annotated
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key
app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
@app.get("/items/")
async def read_items():
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]
@app.get("/users/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]🤓 Other versions and variants
And all the ideas in the section about adding dependencies to the path operation decorators still apply, but in this case, to all of the path operations in the app.Dependencies for groups of path operations¶
Later, when reading about how to structure bigger applications (Bigger Applications - Multiple Files), possibly with multiple files, you will learn how to declare a single dependencies parameter for a group of path operations.
Dependencies in path operation decorators
Dependencies with yield
Dependencies with yield 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Classes as Dependencies
Sub-dependencies
Dependencies in path operation decorators
Global Dependencies
Dependencies with yield
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
A database dependency with yield
A dependency with yield and try
Sub-dependencies with yield
Dependencies with yield and HTTPException
Dependencies with yield and except
Always raise in Dependencies with yield and except
Execution of dependencies with yield
Dependencies with yield, HTTPException, except and Background Tasks
Dependencies with yield and except, Technical Details
Background Tasks and Dependencies with yield, Technical Details
Context Managers
What are "Context Managers"
Using context managers in dependencies with yield
Dependencies
Dependencies with yield¶
FastAPI supports dependencies that do some extra steps after finishing.To do this, use yield instead of return, and write the extra steps (code) after.TipMake sure to use yield one single time per dependency.Technical DetailsAny function that is valid to use with:@contextlib.contextmanager or
@contextlib.asynccontextmanager
would be valid to use as a FastAPI dependency.In fact, FastAPI uses those two decorators internally.A database dependency with yield¶
For example, you could use this to create a database session and close it after finishing.Only the code prior to and including the yield statement is executed before creating a response:
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()The yielded value is what is injected into path operations and other dependencies:
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()The code following the yield statement is executed after creating the response but before sending it:
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()TipYou can use async or regular functions.FastAPI will do the right thing with each, the same as with normal dependencies.A dependency with yield and try¶
If you use a try block in a dependency with yield, you'll receive any exception that was thrown when using the dependency.For example, if some code at some point in the middle, in another dependency or in a path operation, made a database transaction "rollback" or create any other error, you will receive the exception in your dependency.So, you can look for that specific exception inside the dependency with except SomeException.In the same way, you can use finally to make sure the exit steps are executed, no matter if there was an exception or not.
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()Sub-dependencies with yield¶
You can have sub-dependencies and "trees" of sub-dependencies of any size and shape, and any or all of them can use yield.FastAPI will make sure that the "exit code" in each dependency with yield is run in the correct order.For example, dependency_c can have a dependency on dependency_b, and dependency_b on dependency_a:
from typing import Annotatedfrom fastapi import Depends
async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()
async def dependency_b(dep_a: Annotated[DepA, Depends(dependency_a)]):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)
async def dependency_c(dep_b: Annotated[DepB, Depends(dependency_b)]):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)🤓 Other versions and variants
And all of them can use yield.In this case dependency_c, to execute its exit code, needs the value from dependency_b (here named dep_b) to still be available.And, in turn, dependency_b needs the value from dependency_a (here named dep_a) to be available for its exit code.
from typing import Annotatedfrom fastapi import Depends
async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()
async def dependency_b(dep_a: Annotated[DepA, Depends(dependency_a)]):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)
async def dependency_c(dep_b: Annotated[DepB, Depends(dependency_b)]):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)🤓 Other versions and variants
The same way, you could have some dependencies with yield and some other dependencies with return, and have some of those depend on some of the others.And you could have a single dependency that requires several other dependencies with yield, etc.You can have any combinations of dependencies that you want.FastAPI will make sure everything is run in the correct order.Technical DetailsThis works thanks to Python's Context Managers.FastAPI uses them internally to achieve this.Dependencies with yield and HTTPException¶
You saw that you can use dependencies with yield and have try blocks that catch exceptions.The same way, you could raise an HTTPException or similar in the exit code, after the yield.TipThis is a somewhat advanced technique, and in most of the cases you won't really need it, as you can raise exceptions (including HTTPException) from inside of the rest of your application code, for example, in the path operation function.But it's there for you if you need it. 🤓
from typing import Annotatedfrom fastapi import Depends, FastAPI, HTTPExceptionapp = FastAPI()
data = {
    "plumbus": {"description": "Freshly pickled plumbus", "owner": "Morty"},
    "portal-gun": {"description": "Gun to create portals", "owner": "Rick"},
}
class OwnerError(Exception):
    pass
def get_username():
    try:
        yield "Rick"
    except OwnerError as e:
        raise HTTPException(status_code=400, detail=f"Owner error: {e}")
@app.get("/items/{item_id}")
def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    item = data[item_id]
    if item["owner"] != username:
        raise OwnerError(username)
    return item🤓 Other versions and variants
An alternative you could use to catch exceptions (and possibly also raise another HTTPException) is to create a Custom Exception Handler.Dependencies with yield and except¶
If you catch an exception using except in a dependency with yield and you don't raise it again (or raise a new exception), FastAPI won't be able to notice there was an exception, the same way that would happen with regular Python:
from typing import Annotatedfrom fastapi import Depends, FastAPI, HTTPExceptionapp = FastAPI()
class InternalError(Exception):
    pass
def get_username():
    try:
        yield "Rick"
    except InternalError:
        print("Oops, we didn't raise again, Britney 😱")
@app.get("/items/{item_id}")
def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id == "portal-gun":
        raise InternalError(
            f"The portal gun is too dangerous to be owned by {username}"
        )
    if item_id != "plumbus":
        raise HTTPException(
            status_code=404, detail="Item not found, there's only a plumbus here"
        )
    return item_id🤓 Other versions and variants
In this case, the client will see an HTTP 500 Internal Server Error response as it should, given that we are not raising an HTTPException or similar, but the server will not have any logs or any other indication of what was the error. 😱Always raise in Dependencies with yield and except¶
If you catch an exception in a dependency with yield, unless you are raising another HTTPException or similar, you should re-raise the original exception.You can re-raise the same exception using raise:
from typing import Annotatedfrom fastapi import Depends, FastAPI, HTTPExceptionapp = FastAPI()
class InternalError(Exception):
    pass
def get_username():
    try:
        yield "Rick"
    except InternalError:
        print("We don't swallow the internal error here, we raise again 😎")
        raise
@app.get("/items/{item_id}")
def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id == "portal-gun":
        raise InternalError(
            f"The portal gun is too dangerous to be owned by {username}"
        )
    if item_id != "plumbus":
        raise HTTPException(
            status_code=404, detail="Item not found, there's only a plumbus here"
        )
    return item_id🤓 Other versions and variants
Now the client will get the same HTTP 500 Internal Server Error response, but the server will have our custom InternalError in the logs. 😎Execution of dependencies with yield¶
The sequence of execution is more or less like this diagram. Time flows from top to bottom. And each column is one of the parts interacting or executing code.Background tasks
Path Operation
Dep with yield
Exception handler
Client
Background tasks
Path Operation
Dep with yield
Exception handler
Client
Can raise exceptions, including HTTPException
Run code up to yield
opt
[raise Exception]
opt
[handle]
opt
[raise]
Response is already sent, can't change it anymore
opt
[Tasks]
opt
[Raise other exception]
Start request
Raise Exception
HTTP error response
Run dependency, e.g. DB session
Raise Exception (e.g. HTTPException)
Can catch exception, raise a new HTTPException, raise other exception
HTTP error response
Return response to client
Send background tasks
Handle exceptions in the background task code
InfoOnly one response will be sent to the client. It might be one of the error responses or it will be the response from the path operation.After one of those responses is sent, no other response can be sent.TipThis diagram shows HTTPException, but you could also raise any other exception that you catch in a dependency with yield or with a Custom Exception Handler.If you raise any exception, it will be passed to the dependencies with yield, including HTTPException. In most cases you will want to re-raise that same exception or a new one from the dependency with yield to make sure it's properly handled.Dependencies with yield, HTTPException, except and Background Tasks¶
WarningYou most probably don't need these technical details, you can skip this section and continue below.These details are useful mainly if you were using a version of FastAPI prior to 0.106.0 and used resources from dependencies with yield in background tasks.Dependencies with yield and except, Technical Details¶
Before FastAPI 0.110.0, if you used a dependency with yield, and then you captured an exception with except in that dependency, and you didn't raise the exception again, the exception would be automatically raised/forwarded to any exception handlers or the internal server error handler.This was changed in version 0.110.0 to fix unhandled memory consumption from forwarded exceptions without a handler (internal server errors), and to make it consistent with the behavior of regular Python code.Background Tasks and Dependencies with yield, Technical Details¶
Before FastAPI 0.106.0, raising exceptions after yield was not possible, the exit code in dependencies with yield was executed after the response was sent, so Exception Handlers would have already run.This was designed this way mainly to allow using the same objects "yielded" by dependencies inside of background tasks, because the exit code would be executed after the background tasks were finished.Nevertheless, as this would mean waiting for the response to travel through the network while unnecessarily holding a resource in a dependency with yield (for example a database connection), this was changed in FastAPI 0.106.0.TipAdditionally, a background task is normally an independent set of logic that should be handled separately, with its own resources (e.g. its own database connection).So, this way you will probably have cleaner code.If you used to rely on this behavior, now you should create the resources for background tasks inside the background task itself, and use internally only data that doesn't depend on the resources of dependencies with yield.For example, instead of using the same database session, you would create a new database session inside of the background task, and you would obtain the objects from the database using this new session. And then instead of passing the object from the database as a parameter to the background task function, you would pass the ID of that object and then obtain the object again inside the background task function.Context Managers¶
What are "Context Managers"¶
"Context Managers" are any of those Python objects that you can use in a with statement.For example, you can use with to read a file:
with open("./somefile.txt") as f:
    contents = f.read()
    print(contents)
Underneath, the open("./somefile.txt") creates an object that is called a "Context Manager".When the with block finishes, it makes sure to close the file, even if there were exceptions.When you create a dependency with yield, FastAPI will internally create a context manager for it, and combine it with some other related tools.Using context managers in dependencies with yield¶
WarningThis is, more or less, an "advanced" idea.If you are just starting with FastAPI you might want to skip it for now.In Python, you can create Context Managers by creating a class with two methods: __enter__() and __exit__().You can also use them inside of FastAPI dependencies with yield by using with or async with statements inside of the dependency function:
class MySuperContextManager:
    def __init__(self):
        self.db = DBSession()    def __enter__(self):
        return self.db    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()
async def get_db():
    with MySuperContextManager() as db:
        yield dbTipAnother way to create a context manager is with:@contextlib.contextmanager or
@contextlib.asynccontextmanager
using them to decorate a function with a single yield.That's what FastAPI uses internally for dependencies with yield.But you don't have to use the decorators for FastAPI dependencies (and you shouldn't).FastAPI will do it for you internally.
Global Dependencies
Security
Security 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Security - First Steps
Get Current User
Simple OAuth2 with Password and Bearer
OAuth2 with Password (and hashing), Bearer with JWT tokens
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
OAuth2
OAuth OpenID Connect
OpenID (not "OpenID Connect")
OpenAPI
FastAPI utilities
Security
Security¶
There are many ways to handle security, authentication and authorization.And it normally is a complex and "difficult" topic.In many frameworks and systems just handling security and authentication takes a big amount of effort and code (in many cases it can be 50% or more of all the code written).FastAPI provides several tools to help you deal with Security easily, rapidly, in a standard way, without having to study and learn all the security specifications.But first, let's check some small concepts.In a hurry¶
If you don't care about any of these terms and you just need to add security with authentication based on username and password right now, skip to the next chapters.OAuth2¶
OAuth2 is a specification that defines several ways to handle authentication and authorization.It is quite an extensive specification and covers several complex use cases.It includes ways to authenticate using a "third party".That's what all the systems with "login with Facebook, Google, Twitter, GitHub" use underneath.OAuth 1¶
There was an OAuth 1, which is very different from OAuth2, and more complex, as it included direct specifications on how to encrypt the communication.It is not very popular or used nowadays.OAuth2 doesn't specify how to encrypt the communication, it expects you to have your application served with HTTPS.TipIn the section about deployment you will see how to set up HTTPS for free, using Traefik and Let's Encrypt.OpenID Connect¶
OpenID Connect is another specification, based on OAuth2.It just extends OAuth2 specifying some things that are relatively ambiguous in OAuth2, to try to make it more interoperable.For example, Google login uses OpenID Connect (which underneath uses OAuth2).But Facebook login doesn't support OpenID Connect. It has its own flavor of OAuth2.OpenID (not "OpenID Connect")¶
There was also an "OpenID" specification. That tried to solve the same thing as OpenID Connect, but was not based on OAuth2.So, it was a complete additional system.It is not very popular or used nowadays.OpenAPI¶
OpenAPI (previously known as Swagger) is the open specification for building APIs (now part of the Linux Foundation).FastAPI is based on OpenAPI.That's what makes it possible to have multiple automatic interactive documentation interfaces, code generation, etc.OpenAPI has a way to define multiple security "schemes".By using them, you can take advantage of all these standard-based tools, including these interactive documentation systems.OpenAPI defines the following security schemes:apiKey: an application specific key that can come from:
A query parameter.
A header.
A cookie.
http: standard HTTP authentication systems, including:
bearer: a header Authorization with a value of Bearer plus a token. This is inherited from OAuth2.
HTTP Basic authentication.
HTTP Digest, etc.
oauth2: all the OAuth2 ways to handle security (called "flows").
Several of these flows are appropriate for building an OAuth 2.0 authentication provider (like Google, Facebook, Twitter, GitHub, etc):
implicit
clientCredentials
authorizationCode
But there is one specific "flow" that can be perfectly used for handling authentication in the same application directly:
password: some next chapters will cover examples of this.
openIdConnect: has a way to define how to discover OAuth2 authentication data automatically.
This automatic discovery is what is defined in the OpenID Connect specification.
TipIntegrating other authentication/authorization providers like Google, Facebook, Twitter, GitHub, etc. is also possible and relatively easy.The most complex problem is building an authentication/authorization provider like those, but FastAPI gives you the tools to do it easily, while doing the heavy lifting for you.FastAPI utilities¶
FastAPI provides several tools for each of these security schemes in the fastapi.security module that simplify using these security mechanisms.In the next chapters you will see how to add security to your API using those tools provided by FastAPI.And you will also see how it gets automatically integrated into the interactive documentation system.
Dependencies with yield
Security - First Steps
Security - First Steps 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Security - First Steps
Get Current User
Simple OAuth2 with Password and Bearer
OAuth2 with Password (and hashing), Bearer with JWT tokens
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
How it looks
Create main.py
Run it
Check it
The password flow
FastAPI's OAuth2PasswordBearer
Use it
What it does
Recap
Security
Security - First Steps¶
Let's imagine that you have your backend API in some domain.And you have a frontend in another domain or in a different path of the same domain (or in a mobile application).And you want to have a way for the frontend to authenticate with the backend, using a username and password.We can use OAuth2 to build that with FastAPI.But let's save you the time of reading the full long specification just to find those little pieces of information you need.Let's use the tools provided by FastAPI to handle security.How it looks¶
Let's first just use the code and see how it works, and then we'll come back to understand what's happening.Create main.py¶
Copy the example in a file main.py:
from typing import Annotatedfrom fastapi import Depends, from fastapi.security import OAuth2PasswordBearerapp = FastAPI()oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}🤓 Other versions and variants
Run it¶
InfoThe python-multipart package is automatically installed with FastAPI when you run the pip install "fastapi[standard]" command.However, if you use the pip install fastapi command, the python-multipart package is not included by default.To install it manually, make sure you create a virtual environment, activate it, and then install it with:
$ pip install python-multipart
This is because OAuth2 uses "form data" for sending the username and password.Run the example with:Check it¶
Go to the interactive docs at: http://127.0.0.1:8000/docs.You will see something like this:Authorize button!You already have a shiny new "Authorize" button.And your path operation has a little lock in the top-right corner that you can click.And if you click it, you have a little authorization form to type a username and password (and other optional fields):NoteIt doesn't matter what you type in the form, it won't work yet. But we'll get there.This is of course not the frontend for the final users, but it's a great automatic tool to document interactively all your API.It can be used by the frontend team (that can also be yourself).It can be used by third party applications and systems.And it can also be used by yourself, to debug, check and test the same application.The password flow¶
Now let's go back a bit and understand what is all that.The password "flow" is one of the ways ("flows") defined in OAuth2, to handle security and authentication.OAuth2 was designed so that the backend or API could be independent of the server that authenticates the user.But in this case, the same FastAPI application will handle the API and the authentication.So, let's review it from that simplified point of view:The user types the username and password in the frontend, and hits Enter.
The frontend (running in the user's browser) sends that username and password to a specific URL in our API (declared with tokenUrl="token").
The API checks that username and password, and responds with a "token" (we haven't implemented any of this yet).
A "token" is just a string with some content that we can use later to verify this user.
Normally, a token is set to expire after some time.
So, the user will have to log in again at some point later.
And if the token is stolen, the risk is less. It is not like a permanent key that will work forever (in most of the cases).
The frontend stores that token temporarily somewhere.
The user clicks in the frontend to go to another section of the frontend web app.
The frontend needs to fetch some more data from the API.
But it needs authentication for that specific endpoint.
So, to authenticate with our API, it sends a header Authorization with a value of Bearer plus the token.
If the token contains foobar, the content of the Authorization header would be: Bearer foobar.
FastAPI's OAuth2PasswordBearer¶
FastAPI provides several tools, at different levels of abstraction, to implement these security features.In this example we are going to use OAuth2, with the Password flow, using a Bearer token. We do that using the OAuth2PasswordBearer class.InfoA "bearer" token is not the only option.But it's the best one for our use case.And it might be the best for most use cases, unless you are an OAuth2 expert and know exactly why there's another option that better suits your needs.In that case, FastAPI also provides you with the tools to build it.When we create an instance of the OAuth2PasswordBearer class we pass in the tokenUrl parameter. This parameter contains the URL that the client (the frontend running in the user's browser) will use to send the username and password in order to get a token.
from typing import Annotatedfrom fastapi import Depends, from fastapi.security import OAuth2PasswordBearerapp = FastAPI()oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}🤓 Other versions and variants
TipHere tokenUrl="token" refers to a relative URL token that we haven't created yet. As it's a relative URL, it's equivalent to ./token.Because we are using a relative URL, if your API was located at https://example.com/, then it would refer to https://example.com/token. But if your API was located at https://example.com/api/v1/, then it would refer to https://example.com/api/v1/token.Using a relative URL is important to make sure your application keeps working even in an advanced use case like Behind a Proxy.This parameter doesn't create that endpoint / path operation, but declares that the URL /token will be the one that the client should use to get the token. That information is used in OpenAPI, and then in the interactive API documentation systems.We will soon also create the actual path operation.InfoIf you are a very strict "Pythonista" you might dislike the style of the parameter name tokenUrl instead of token_url.That's because it is using the same name as in the OpenAPI spec. So that if you need to investigate more about any of these security schemes you can just copy and paste it to find more information about it.The oauth2_scheme variable is an instance of OAuth2PasswordBearer, but it is also a "callable".It could be called as:
oauth2_scheme(some, parameters)
So, it can be used with Depends.Use it¶
Now you can pass that oauth2_scheme in a dependency with Depends.
from typing import Annotatedfrom fastapi import Depends, from fastapi.security import OAuth2PasswordBearerapp = FastAPI()oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}🤓 Other versions and variants
This dependency will provide a str that is assigned to the parameter token of the path operation function.FastAPI will know that it can use this dependency to define a "security scheme" in the OpenAPI schema (and the automatic API docs).Technical DetailsFastAPI will know that it can use the class OAuth2PasswordBearer (declared in a dependency) to define the security scheme in OpenAPI because it inherits from fastapi.security.oauth2.OAuth2, which in turn inherits from fastapi.security.base.SecurityBase.All the security utilities that integrate with OpenAPI (and the automatic API docs) inherit from SecurityBase, that's how FastAPI can know how to integrate them in OpenAPI.What it does¶
It will go and look in the request for that Authorization header, check if the value is Bearer plus some token, and will return the token as a str.If it doesn't see an Authorization header, or the value doesn't have a Bearer token, it will respond with a 401 status code error (UNAUTHORIZED) directly.You don't even have to check if the token exists to return an error. You can be sure that if your function is executed, it will have a str in that token.You can try it already in the interactive docs:We are not verifying the validity of the token yet, but that's a start already.Recap¶
So, in just 3 or 4 extra lines, you already have some primitive form of security.
Security
Get Current User
Get Current User 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Security - First Steps
Get Current User
Simple OAuth2 with Password and Bearer
OAuth2 with Password (and hashing), Bearer with JWT tokens
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Create a user model
Create a get_current_user dependency
Get the user
Inject the current user
Other models
Code size
Recap
Security
Get Current User¶
In the previous chapter the security system (which is based on the dependency injection system) was giving the path operation function a token as a str:
from typing import Annotatedfrom fastapi import Depends, from fastapi.security import OAuth2PasswordBearerapp = FastAPI()oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}🤓 Other versions and variants
But that is still not that useful.Let's make it give us the current user.Create a user model¶
First, let's create a Pydantic user model.The same way we use Pydantic to declare bodies, we can use it anywhere else:
from typing import Annotatedfrom fastapi import Depends, from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModelapp = FastAPI()oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user
@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user🤓 Other versions and variants
Create a get_current_user dependency¶
Let's create a dependency get_current_user.Remember that dependencies can have sub-dependenciesget_current_user will have a dependency with the same oauth2_scheme we created before.The same as we were doing before in the path operation directly, our new dependency get_current_user will receive a token as a str from the sub-dependency oauth2_scheme:
from typing import Annotatedfrom fastapi import Depends, from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModelapp = FastAPI()oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user
@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user🤓 Other versions and variants
Get the user¶
get_current_user will use a (fake) utility function we created, that takes a token as a str and returns our Pydantic User model:
from typing import Annotatedfrom fastapi import Depends, from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModelapp = FastAPI()oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user
@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user🤓 Other versions and variants
Inject the current user¶
So now we can use the same Depends with our get_current_user in the path operation:
from typing import Annotatedfrom fastapi import Depends, from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModelapp = FastAPI()oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user
@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user🤓 Other versions and variants
Notice that we declare the type of current_user as the Pydantic model User.This will help us inside of the function with all the completion and type checks.TipYou might remember that request bodies are also declared with Pydantic models.Here FastAPI won't get confused because you are using Depends.CheckThe way this dependency system is designed allows us to have different dependencies (different "dependables") that all return a User model.We are not restricted to having only one dependency that can return that type of data.Other models¶
You can now get the current user directly in the path operation functions and deal with the security mechanisms at the Dependency Injection level, using Depends.And you can use any model or data for the security requirements (in this case, a Pydantic model User).But you are not restricted to using some specific data model, class or type.Do you want to have an id and email and not have any username in your model Sure. You can use these same tools.Do you want to just have a str Or just a dict Or a database class model instance directly It all works the same way.You actually don't have users that log in to your application but robots, bots, or other systems, that have just an access token Again, it all works the same.Just use any kind of model, any kind of class, any kind of database that you need for your application. FastAPI has you covered with the dependency injection system.Code size¶
This example might seem verbose. Keep in mind that we are mixing security, data models, utility functions and path operations in the same file.But here's the key point.The security and dependency injection stuff is written once.And you can make it as complex as you want. And still, have it written only once, in a single place. With all the flexibility.But you can have thousands of endpoints (path operations) using the same security system.And all of them (or any portion of them that you want) can take advantage of re-using these dependencies or any other dependencies you create.And all these thousands of path operations can be as small as 3 lines:
from typing import Annotatedfrom fastapi import Depends, from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModelapp = FastAPI()oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user
@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user🤓 Other versions and variants
Recap¶
You can now get the current user directly in your path operation function.We are already halfway there.We just need to add a path operation for the user/client to actually send the username and password.That comes next.
Security - First Steps
Simple OAuth2 with Password and Bearer
Simple OAuth2 with Password and Bearer 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Security - First Steps
Get Current User
Simple OAuth2 with Password and Bearer
OAuth2 with Password (and hashing), Bearer with JWT tokens
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Get the username and password
scope
Code to get the username and password
OAuth2PasswordRequestForm
Use the form data
Check the password
Password hashing
Why use password hashing
About **user_dict
Return the token
Update the dependencies
See it in action
Authenticate
Get your own user data
Inactive user
Recap
Security
Simple OAuth2 with Password and Bearer¶
Now let's build from the previous chapter and add the missing parts to have a complete security flow.Get the username and password¶
We are going to use FastAPI security utilities to get the username and password.OAuth2 specifies that when using the "password flow" (that we are using) the client/user must send a username and password fields as form data.And the spec says that the fields have to be named like that. So user-name or email wouldn't work.But don't worry, you can show it as you wish to your final users in the frontend.And your database models can use any other names you want.But for the login path operation, we need to use these names to be compatible with the spec (and be able to, for example, use the integrated API documentation system).The spec also states that the username and password must be sent as form data (so, no JSON here).scope¶
The spec also says that the client can send another form field "scope".The form field name is scope (in singular), but it is actually a long string with "scopes" separated by spaces.Each "scope" is just a string (without spaces).They are normally used to declare specific security permissions, for example:users:read or users:write are common examples.
instagram_basic is used by Facebook / Instagram.
https://www.googleapis.com/auth/drive is used by Google.
InfoIn OAuth2 a "scope" is just a string that declares a specific permission required.It doesn't matter if it has other characters like : or if it is a URL.Those details are implementation specific.For OAuth2 they are just strings.Code to get the username and password¶
Now let's use the utilities provided by FastAPI to handle this.OAuth2PasswordRequestForm¶
First, import OAuth2PasswordRequestForm, and use it as a dependency with Depends in the path operation for /token:
from typing import Annotatedfrom fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModelfake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}app = FastAPI()
def fake_hash_password(password: str):
    return "fakehashed" + password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
class UserInDB(User):
    hashed_password: str
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")    return {"access_token": user.username, "token_type": "bearer"}
@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user🤓 Other versions and variants
OAuth2PasswordRequestForm is a class dependency that declares a form body with:The username.
The password.
An optional scope field as a big string, composed of strings separated by spaces.
An optional grant_type.
TipThe OAuth2 spec actually requires a field grant_type with a fixed value of password, but OAuth2PasswordRequestForm doesn't enforce it.If you need to enforce it, use OAuth2PasswordRequestFormStrict instead of OAuth2PasswordRequestForm.An optional client_id (we don't need it for our example).
An optional client_secret (we don't need it for our example).
InfoThe OAuth2PasswordRequestForm is not a special class for FastAPI as is OAuth2PasswordBearer.OAuth2PasswordBearer makes FastAPI know that it is a security scheme. So it is added that way to OpenAPI.But OAuth2PasswordRequestForm is just a class dependency that you could have written yourself, or you could have declared Form parameters directly.But as it's a common use case, it is provided by FastAPI directly, just to make it easier.Use the form data¶
TipThe instance of the dependency class OAuth2PasswordRequestForm won't have an attribute scope with the long string separated by spaces, instead, it will have a scopes attribute with the actual list of strings for each scope sent.We are not using scopes in this example, but the functionality is there if you need it.Now, get the user data from the (fake) database, using the username from the form field.If there is no such user, we return an error saying "Incorrect username or password".For the error, we use the exception HTTPException:
from typing import Annotatedfrom fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModelfake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}app = FastAPI()
def fake_hash_password(password: str):
    return "fakehashed" + password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
class UserInDB(User):
    hashed_password: str
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")    return {"access_token": user.username, "token_type": "bearer"}
@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user🤓 Other versions and variants
Check the password¶
At this point we have the user data from our database, but we haven't checked the password.Let's put that data in the Pydantic UserInDB model first.You should never save plaintext passwords, so, we'll use the (fake) password hashing system.If the passwords don't match, we return the same error.Password hashing¶
"Hashing" means: converting some content (a password in this case) into a sequence of bytes (just a string) that looks like gibberish.Whenever you pass exactly the same content (exactly the same password) you get exactly the same gibberish.But you cannot convert from the gibberish back to the password.Why use password hashing¶
If your database is stolen, the thief won't have your users' plaintext passwords, only the hashes.So, the thief won't be able to try to use those same passwords in another system (as many users use the same password everywhere, this would be dangerous).
from typing import Annotatedfrom fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModelfake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}app = FastAPI()
def fake_hash_password(password: str):
    return "fakehashed" + password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
class UserInDB(User):
    hashed_password: str
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")    return {"access_token": user.username, "token_type": "bearer"}
@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user🤓 Other versions and variants
About **user_dict¶
UserInDB(**user_dict) means:Pass the keys and values of the user_dict directly as key-value arguments, equivalent to:
UserInDB(
    username = user_dict["username"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    disabled = user_dict["disabled"],
    hashed_password = user_dict["hashed_password"],
)
InfoFor a more complete explanation of **user_dict check back in the documentation for Extra Models.Return the token¶
The response of the token endpoint must be a JSON object.It should have a token_type. In our case, as we are using "Bearer" tokens, the token type should be "bearer".And it should have an access_token, with a string containing our access token.For this simple example, we are going to just be completely insecure and return the same username as the token.TipIn the next chapter, you will see a real secure implementation, with password hashing and JWT tokens.But for now, let's focus on the specific details we need.
from typing import Annotatedfrom fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModelfake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}app = FastAPI()
def fake_hash_password(password: str):
    return "fakehashed" + password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
class UserInDB(User):
    hashed_password: str
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")    return {"access_token": user.username, "token_type": "bearer"}
@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user🤓 Other versions and variants
TipBy the spec, you should return a JSON with an access_token and a token_type, the same as in this example.This is something that you have to do yourself in your code, and make sure you use those JSON keys.It's almost the only thing that you have to remember to do correctly yourself, to be compliant with the specifications.For the rest, FastAPI handles it for you.Update the dependencies¶
Now we are going to update our dependencies.We want to get the current_user only if this user is active.So, we create an additional dependency get_current_active_user that in turn uses get_current_user as a dependency.Both of these dependencies will just return an HTTP error if the user doesn't exist, or if is inactive.So, in our endpoint, we will only get a user if the user exists, was correctly authenticated, and is active:
from typing import Annotatedfrom fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModelfake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}app = FastAPI()
def fake_hash_password(password: str):
    return "fakehashed" + password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
class UserInDB(User):
    hashed_password: str
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")    return {"access_token": user.username, "token_type": "bearer"}
@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user🤓 Other versions and variants
InfoThe additional header WWW-Authenticate with value Bearer we are returning here is also part of the spec.Any HTTP (error) status code 401 "UNAUTHORIZED" is supposed to also return a WWW-Authenticate header.In the case of bearer tokens (our case), the value of that header should be Bearer.You can actually skip that extra header and it would still work.But it's provided here to be compliant with the specifications.Also, there might be tools that expect and use it (now or in the future) and that might be useful for you or your users, now or in the future.That's the benefit of standards...See it in action¶
Open the interactive docs: http://127.0.0.1:8000/docs.Authenticate¶
Click the "Authorize" button.Use the credentials:User: johndoePassword: secretAfter authenticating in the system, you will see it like:Get your own user data¶
Now use the operation GET with the path /users/me.You will get your user's data, like:
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false,
  "hashed_password": "fakehashedsecret"
}
If you click the lock icon and logout, and then try the same operation again, you will get an HTTP 401 error of:
{
  "detail": "Not authenticated"
}
Inactive user¶
Now try with an inactive user, authenticate with:User: alicePassword: secret2And try to use the operation GET with the path /users/me.You will get an "Inactive user" error, like:
{
  "detail": "Inactive user"
}
Recap¶
You now have the tools to implement a complete security system based on username and password for your API.Using these tools, you can make the security system compatible with any database and with any user or data model.The only detail missing is that it is not actually "secure" yet.In the next chapter you'll see how to use a secure password hashing library and JWT tokens.
Get Current User
OAuth2 with Password (and hashing), Bearer with JWT tokens
OAuth2 with Password (and hashing), Bearer with JWT tokens 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Security - First Steps
Get Current User
Simple OAuth2 with Password and Bearer
OAuth2 with Password (and hashing), Bearer with JWT tokens
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
About JWT
Install PyJWT
Password hashing
Why use password hashing
Install passlib
Hash and verify the passwords
Handle JWT tokens
Update the dependencies
Update the /token path operation
Technical details about the JWT "subject" sub
Check it
Advanced usage with scopes
Recap
Security
OAuth2 with Password (and hashing), Bearer with JWT tokens¶
Now that we have all the security flow, let's make the application actually secure, using JWT tokens and secure password hashing.This code is something you can actually use in your application, save the password hashes in your database, etc.We are going to start from where we left in the previous chapter and increment it.About JWT¶
JWT means "JSON Web Tokens".It's a standard to codify a JSON object in a long dense string without spaces. It looks like this:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
It is not encrypted, so, anyone could recover the information from the contents.But it's signed. So, when you receive a token that you emitted, you can verify that you actually emitted it.That way, you can create a token with an expiration of, let's say, 1 week. And then when the user comes back the next day with the token, you know that user is still logged in to your system.After a week, the token will be expired and the user will not be authorized and will have to sign in again to get a new token. And if the user (or a third party) tried to modify the token to change the expiration, you would be able to discover it, because the signatures would not match.If you want to play with JWT tokens and see how they work, check https://jwt.io.Install PyJWT¶
We need to install PyJWT to generate and verify the JWT tokens in Python.Make sure you create a virtual environment, activate it, and then install pyjwt:
InfoIf you are planning to use digital signature algorithms like RSA or ECDSA, you should install the cryptography library dependency pyjwt[crypto].You can read more about it in the PyJWT Installation docs.Password hashing¶
"Hashing" means converting some content (a password in this case) into a sequence of bytes (just a string) that looks like gibberish.Whenever you pass exactly the same content (exactly the same password) you get exactly the same gibberish.But you cannot convert from the gibberish back to the password.Why use password hashing¶
If your database is stolen, the thief won't have your users' plaintext passwords, only the hashes.So, the thief won't be able to try to use that password in another system (as many users use the same password everywhere, this would be dangerous).Install passlib¶
PassLib is a great Python package to handle password hashes.It supports many secure hashing algorithms and utilities to work with them.The recommended algorithm is "Bcrypt".Make sure you create a virtual environment, activate it, and then install PassLib with Bcrypt:
TipWith passlib, you could even configure it to be able to read passwords created by Django, a Flask security plug-in or many others.So, you would be able to, for example, share the same data from a Django application in a database with a FastAPI application. Or gradually migrate a Django application using the same database.And your users would be able to login from your Django app or from your FastAPI app, at the same time.Hash and verify the passwords¶
Import the tools we need from passlib.Create a PassLib "context". This is what will be used to hash and verify passwords.TipThe PassLib context also has functionality to use different hashing algorithms, including deprecated old ones only to allow verifying them, etc.For example, you could use it to read and verify passwords generated by another system (like Django) but hash any new passwords with a different algorithm like Bcrypt.And be compatible with all of them at the same time.Create a utility function to hash a password coming from the user.And another utility to verify if a received password matches the hash stored.And another one to authenticate and return a user.
from datetime import datetime, timedelta, timezone
from typing import Annotatedimport jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: str | None = None
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
class UserInDB(User):
    hashed_password: str
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")app = FastAPI()
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]🤓 Other versions and variants
NoteIf you check the new (fake) database fake_users_db, you will see how the hashed password looks like now: "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW".Handle JWT tokens¶
Import the modules installed.Create a random secret key that will be used to sign the JWT tokens.To generate a secure random secret key use the command:And copy the output to the variable SECRET_KEY (don't use the one in the example).Create a variable ALGORITHM with the algorithm used to sign the JWT token and set it to "HS256".Create a variable for the expiration of the token.Define a Pydantic Model that will be used in the token endpoint for the response.Create a utility function to generate a new access token.
from datetime import datetime, timedelta, timezone
from typing import Annotatedimport jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: str | None = None
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
class UserInDB(User):
    hashed_password: str
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")app = FastAPI()
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]🤓 Other versions and variants
Update the dependencies¶
Update get_current_user to receive the same token as before, but this time, using JWT tokens.Decode the received token, verify it, and return the current user.If the token is invalid, return an HTTP error right away.
from datetime import datetime, timedelta, timezone
from typing import Annotatedimport jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: str | None = None
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
class UserInDB(User):
    hashed_password: str
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")app = FastAPI()
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]🤓 Other versions and variants
Update the /token path operation¶
Create a timedelta with the expiration time of the token.Create a real JWT access token and return it.
from datetime import datetime, timedelta, timezone
from typing import Annotatedimport jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: str | None = None
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
class UserInDB(User):
    hashed_password: str
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")app = FastAPI()
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]🤓 Other versions and variants
Technical details about the JWT "subject" sub¶
The JWT specification says that there's a key sub, with the subject of the token.It's optional to use it, but that's where you would put the user's identification, so we are using it here.JWT might be used for other things apart from identifying a user and allowing them to perform operations directly on your API.For example, you could identify a "car" or a "blog post".Then you could add permissions about that entity, like "drive" (for the car) or "edit" (for the blog).And then, you could give that JWT token to a user (or bot), and they could use it to perform those actions (drive the car, or edit the blog post) without even needing to have an account, just with the JWT token your API generated for that.Using these ideas, JWT can be used for way more sophisticated scenarios.In those cases, several of those entities could have the same ID, let's say foo (a user foo, a car foo, and a blog post foo).So, to avoid ID collisions, when creating the JWT token for the user, you could prefix the value of the sub key, e.g. with username:. So, in this example, the value of sub could have been: username:johndoe.The important thing to keep in mind is that the sub key should have a unique identifier across the entire application, and it should be a string.Check it¶
Run the server and go to the docs: http://127.0.0.1:8000/docs.You'll see the user interface like:Authorize the application the same way as before.Using the credentials:Username: johndoe Password: secretCheckNotice that nowhere in the code is the plaintext password "secret", we only have the hashed version.Call the endpoint /users/me/, you will get the response as:
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false
}
If you open the developer tools, you could see how the data sent only includes the token, the password is only sent in the first request to authenticate the user and get that access token, but not afterwards:NoteNotice the header Authorization, with a value that starts with Bearer.Advanced usage with scopes¶
OAuth2 has the notion of "scopes".You can use them to add a specific set of permissions to a JWT token.Then you can give this token to a user directly or a third party, to interact with your API with a set of restrictions.You can learn how to use them and how they are integrated into FastAPI later in the Advanced User Guide.Recap¶
With what you have seen up to now, you can set up a secure FastAPI application using standards like OAuth2 and JWT.In almost any framework handling the security becomes a rather complex subject quite quickly.Many packages that simplify it a lot have to make many compromises with the data model, database, and available features. And some of these packages that simplify things too much actually have security flaws underneath.FastAPI doesn't make any compromise with any database, data model or tool.It gives you all the flexibility to choose the ones that fit your project the best.And you can use directly many well maintained and widely used packages like passlib and PyJWT, because FastAPI doesn't require any complex mechanisms to integrate external packages.But it provides you the tools to simplify the process as much as possible without compromising flexibility, robustness, or security.And you can use and implement secure, standard protocols, like OAuth2 in a relatively simple way.You can learn more in the Advanced User Guide about how to use OAuth2 "scopes", for a more fine-grained permission system, following these same standards. OAuth2 with scopes is the mechanism used by many big authentication providers, like Facebook, Google, GitHub, Microsoft, Twitter, etc. to authorize third party applications to interact with their APIs on behalf of their users.
Simple OAuth2 with Password and Bearer
Middleware
Middleware 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Create a middleware
Before and after the response
Other middlewares
Middleware¶
You can add middleware to FastAPI applications.A "middleware" is a function that works with every request before it is processed by any specific path operation. And also with every response before returning it.It takes each request that comes to your application.
It can then do something to that request or run any needed code.
Then it passes the request to be processed by the rest of the application (by some path operation).
It then takes the response generated by the application (by some path operation).
It can do something to that response or run any needed code.
Then it returns the response.
Technical DetailsIf you have dependencies with yield, the exit code will run after the middleware.If there were any background tasks (documented later), they will run after all the middleware.Create a middleware¶
To create a middleware you use the decorator @app.middleware("http") on top of a function.The middleware function receives:The request.
A function call_next that will receive the request as a parameter.
This function will pass the request to the corresponding path operation.
Then it returns the response generated by the corresponding path operation.
You can then further modify the response before returning it.import timefrom fastapi import FastAPI, Requestapp = FastAPI()
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return responseTipKeep in mind that custom proprietary headers can be added using the 'X-' prefix.But if you have custom headers that you want a client in a browser to be able to see, you need to add them to your CORS configurations (CORS (Cross-Origin Resource Sharing)) using the parameter expose_headers documented in Starlette's CORS docs.Technical DetailsYou could also use from starlette.requests import Request.FastAPI provides it as a convenience for you, the developer. But it comes directly from Starlette.Before and after the response¶
You can add code to be run with the request, before any path operation receives it.And also after the response is generated, before returning it.For example, you could add a custom header X-Process-Time containing the time in seconds that it took to process the request and generate a response:
import timefrom fastapi import FastAPI, Requestapp = FastAPI()
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return responseTipHere we use time.perf_counter() instead of time.time() because it can be more precise for these use cases. 🤓Other middlewares¶
You can later read more about other middlewares in the Advanced User Guide: Advanced Middleware.You will read about how to handle CORS with a middleware in the next section.
OAuth2 with Password (and hashing), Bearer with JWT tokens
CORS (Cross-Origin Resource Sharing)
CORS (Cross-Origin Resource Sharing) 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Origin
Steps
Wildcards
Use CORSMiddleware
CORS preflight requests
Simple requests
More info
CORS (Cross-Origin Resource Sharing)¶
CORS or "Cross-Origin Resource Sharing" refers to the situations when a frontend running in a browser has JavaScript code that communicates with a backend, and the backend is in a different "origin" than the frontend.Origin¶
An origin is the combination of protocol (http, https), domain (myapp.com, localhost, localhost.tiangolo.com), and port (80, 443, 8080).So, all these are different origins:http://localhost
https://localhost
http://localhost:8080
Even if they are all in localhost, they use different protocols or ports, so, they are different "origins".Steps¶
So, let's say you have a frontend running in your browser at http://localhost:8080, and its JavaScript is trying to communicate with a backend running at http://localhost (because we don't specify a port, the browser will assume the default port 80).Then, the browser will send an HTTP OPTIONS request to the :80-backend, and if the backend sends the appropriate headers authorizing the communication from this different origin (http://localhost:8080) then the :8080-browser will let the JavaScript in the frontend send its request to the :80-backend.To achieve this, the :80-backend must have a list of "allowed origins".In this case, the list would have to include http://localhost:8080 for the :8080-frontend to work correctly.Wildcards¶
It's also possible to declare the list as "*" (a "wildcard") to say that all are allowed.But that will only allow certain types of communication, excluding everything that involves credentials: Cookies, Authorization headers like those used with Bearer Tokens, etc.So, for everything to work correctly, it's better to specify explicitly the allowed origins.Use CORSMiddleware¶
You can configure it in your FastAPI application using the CORSMiddleware.Import CORSMiddleware.
Create a list of allowed origins (as strings).
Add it as a "middleware" to your FastAPI application.
You can also specify whether your backend allows:Credentials (Authorization headers, Cookies, etc).
Specific HTTP methods (POST, PUT) or all of them with the wildcard "*".
Specific HTTP headers or all of them with the wildcard "*".from fastapi import from fastapi.middleware.cors import CORSMiddlewareapp = FastAPI()origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def main():
    return {"message": "Hello World"}The default parameters used by the CORSMiddleware implementation are restrictive by default, so you'll need to explicitly enable particular origins, methods, or headers, in order for browsers to be permitted to use them in a Cross-Domain context.The following arguments are supported:allow_origins - A list of origins that should be permitted to make cross-origin requests. E.g. ['https://example.org', 'https://www.example.org']. You can use ['*'] to allow any origin.
allow_origin_regex - A regex string to match against origins that should be permitted to make cross-origin requests. e.g. 'https://.*\.example\.org'.
allow_methods - A list of HTTP methods that should be allowed for cross-origin requests. Defaults to ['GET']. You can use ['*'] to allow all standard methods.
allow_headers - A list of HTTP request headers that should be supported for cross-origin requests. Defaults to []. You can use ['*'] to allow all headers. The Accept, Accept-Language, Content-Language and Content-Type headers are always allowed for simple CORS requests.
allow_credentials - Indicate that cookies should be supported for cross-origin requests. Defaults to False. Also, allow_origins cannot be set to ['*'] for credentials to be allowed, origins must be specified.
expose_headers - Indicate any response headers that should be made accessible to the browser. Defaults to [].
max_age - Sets a maximum time in seconds for browsers to cache CORS responses. Defaults to 600.
The middleware responds to two particular types of HTTP request...CORS preflight requests¶
These are any OPTIONS request with Origin and Access-Control-Request-Method headers.In this case the middleware will intercept the incoming request and respond with appropriate CORS headers, and either a 200 or 400 response for informational purposes.Simple requests¶
Any request with an Origin header. In this case the middleware will pass the request through as normal, but will include appropriate CORS headers on the response.More info¶
For more info about CORS, check the Mozilla CORS documentation.Technical DetailsYou could also use from starlette.middleware.cors import CORSMiddleware.FastAPI provides several middlewares in fastapi.middleware just as a convenience for you, the developer. But most of the available middlewares come directly from Starlette.
Middleware
SQL (Relational) Databases
SQL (Relational) Databases 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Install SQLModel
Create the App with a Single Model
Create Models
Create an Engine
Create the Tables
Create a Session Dependency
Create Database Tables on Startup
Create a Hero
Read Heroes
Read One Hero
Delete a Hero
Run the App
Update the App with Multiple Models
Create Multiple Models
HeroBase - the base class
Hero - the table model
HeroPublic - the public data model
HeroCreate - the data model to create a hero
HeroUpdate - the data model to update a hero
Create with HeroCreate and return a HeroPublic
Read Heroes with HeroPublic
Read One Hero with HeroPublic
Update a Hero with HeroUpdate
Delete a Hero Again
Run the App Again
Recap
SQL (Relational) Databases¶
FastAPI doesn't require you to use a SQL (relational) database. But you can use any database that you want.Here we'll see an example using SQLModel.SQLModel is built on top of SQLAlchemy and Pydantic. It was made by the same author of FastAPI to be the perfect match for FastAPI applications that need to use SQL databases.TipYou could use any other SQL or NoSQL database library you want (in some cases called "ORMs"), FastAPI doesn't force you to use anything. 😎As SQLModel is based on SQLAlchemy, you can easily use any database supported by SQLAlchemy (which makes them also supported by SQLModel), like:PostgreSQL
MySQL
SQLite
Oracle
Microsoft SQL Server, etc.
In this example, we'll use SQLite, because it uses a single file and Python has integrated support. So, you can copy this example and run it as is.Later, for your production application, you might want to use a database server like PostgreSQL.TipThere is an official project generator with FastAPI and PostgreSQL including a frontend and more tools: https://github.com/fastapi/full-stack-fastapi-templateThis is a very simple and short tutorial, if you want to learn about databases in general, about SQL, or more advanced features, go to the SQLModel docs.Install SQLModel¶
First, make sure you create your virtual environment, activate it, and then install sqlmodel:Create the App with a Single Model¶
We'll create the simplest first version of the app with a single SQLModel model first.Later we'll improve it increasing security and versatility with multiple models below. 🤓Create Models¶
Import SQLModel and create a database model:
from typing import Annotatedfrom fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str# Code below omitted 👇👀 Full file preview
🤓 Other versions and variants
The Hero class is very similar to a Pydantic model (in fact, underneath, it actually is a Pydantic model).There are a few differences:table=True tells SQLModel that this is a table model, it should represent a table in the SQL database, it's not just a data model (as would be any other regular Pydantic class).Field(primary_key=True) tells SQLModel that the id is the primary key in the SQL database (you can learn more about SQL primary keys in the SQLModel docs).By having the type as int | None, SQLModel will know that this column should be an INTEGER in the SQL database and that it should be NULLABLE.Field(index=True) tells SQLModel that it should create a SQL index for this column, that would allow faster lookups in the database when reading data filtered by this column.SQLModel will know that something declared as str will be a SQL column of type TEXT (or VARCHAR, depending on the database).Create an Engine¶
A SQLModel engine (underneath it's actually a SQLAlchemy engine) is what holds the connections to the database.You would have one single engine object for all your code to connect to the same database.
# Code above omitted 👆sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)# Code below omitted 👇👀 Full file preview
🤓 Other versions and variants
Using check_same_thread=False allows FastAPI to use the same SQLite database in different threads. This is necessary as one single request could use more than one thread (for example in dependencies).Don't worry, with the way the code is structured, we'll make sure we use a single SQLModel session per request later, this is actually what the check_same_thread is trying to achieve.Create the Tables¶
We then add a function that uses SQLModel.metadata.create_all(engine) to create the tables for all the table models.
# Code above omitted 👆def create_db_and_tables():
    SQLModel.metadata.create_all(engine)# Code below omitted 👇👀 Full file preview
🤓 Other versions and variants
Create a Session Dependency¶
A Session is what stores the objects in memory and keeps track of any changes needed in the data, then it uses the engine to communicate with the database.We will create a FastAPI dependency with yield that will provide a new Session for each request. This is what ensures that we use a single session per request. 🤓Then we create an Annotated dependency SessionDep to simplify the rest of the code that will use this dependency.
# Code above omitted 👆def get_session():
    with Session(engine) as session:
        yield session
SessionDep = Annotated[Session, Depends(get_session)]# Code below omitted 👇👀 Full file preview
🤓 Other versions and variants
Create Database Tables on Startup¶
We will create the database tables when the application starts.
# Code above omitted 👆app = FastAPI()
@app.on_event("startup")
def on_startup():
    create_db_and_tables()# Code below omitted 👇👀 Full file preview
🤓 Other versions and variants
Here we create the tables on an application startup event.For production you would probably use a migration script that runs before you start your app. 🤓TipSQLModel will have migration utilities wrapping Alembic, but for now, you can use Alembic directly.Create a Hero¶
Because each SQLModel model is also a Pydantic model, you can use it in the same type annotations that you could use Pydantic models.For example, if you declare a parameter of type Hero, it will be read from the JSON body.The same way, you can declare it as the function's return type, and then the shape of the data will show up in the automatic API docs UI.
# Code above omitted 👆@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero# Code below omitted 👇👀 Full file preview
🤓 Other versions and variants
Here we use the SessionDep dependency (a Session) to add the new Hero to the Session instance, commit the changes to the database, refresh the data in the hero, and then return it.Read Heroes¶
We can read Heros from the database using a select(). We can include a limit and offset to paginate the results.
# Code above omitted 👆@app.get("/heroes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes# Code below omitted 👇👀 Full file preview
🤓 Other versions and variants
Read One Hero¶
We can read a single Hero.
# Code above omitted 👆@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero# Code below omitted 👇👀 Full file preview
🤓 Other versions and variants
Delete a Hero¶
We can also delete a Hero.
# Code above omitted 👆@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}👀 Full file preview
🤓 Other versions and variants
Run the App¶
You can run the app:Then go to the /docs UI, you will see that FastAPI is using these models to document the API, and it will use them to serialize and validate the data too.
Update the App with Multiple Models¶
Now let's refactor this app a bit to increase security and versatility.If you check the previous app, in the UI you can see that, up to now, it lets the client decide the id of the Hero to create. 😱We shouldn't let that happen, they could overwrite an id we already have assigned in the DB. Deciding the id should be done by the backend or the database, not by the client.Additionally, we create a secret_name for the hero, but so far, we are returning it everywhere, that's not very secret... 😅We'll fix these things by adding a few extra models. Here's where SQLModel will shine. ✨Create Multiple Models¶
In SQLModel, any model class that has table=True is a table model.And any model class that doesn't have table=True is a data model, these ones are actually just Pydantic models (with a couple of small extra features). 🤓With SQLModel, we can use inheritance to avoid duplicating all the fields in all the cases.HeroBase - the base class¶
Let's start with a HeroBase model that has all the fields that are shared by all the models:name
age# Code above omitted 👆class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)# Code below omitted 👇👀 Full file preview
🤓 Other versions and variants
Hero - the table model¶
Then let's create Hero, the actual table model, with the extra fields that are not always in the other models:id
secret_name
Because Hero inherits form HeroBase, it also has the fields declared in HeroBase, so all the fields for Hero are:id
name
age
secret_name# Code above omitted 👆class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str# Code below omitted 👇👀 Full file preview
🤓 Other versions and variants
HeroPublic - the public data model¶
Next, we create a HeroPublic model, this is the one that will be returned to the clients of the API.It has the same fields as HeroBase, so it won't include secret_name.Finally, the identity of our heroes is protected! 🥷It also re-declares id: int. By doing this, we are making a contract with the API clients, so that they can always expect the id to be there and to be an int (it will never be None).TipHaving the return model ensure that a value is always available and always int (not None) is very useful for the API clients, they can write much simpler code having this certainty.Also, automatically generated clients will have simpler interfaces, so that the developers communicating with your API can have a much better time working with your API. 😎All the fields in HeroPublic are the same as in HeroBase, with id declared as int (not None):id
name
age
secret_name# Code above omitted 👆class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str
class HeroPublic(HeroBase):
    id: int# Code below omitted 👇👀 Full file preview
🤓 Other versions and variants
HeroCreate - the data model to create a hero¶
Now we create a HeroCreate model, this is the one that will validate the data from the clients.It has the same fields as HeroBase, and it also has secret_name.Now, when the clients create a new hero, they will send the secret_name, it will be stored in the database, but those secret names won't be returned in the API to the clients.TipThis is how you would handle passwords. Receive them, but don't return them in the API.You would also hash the values of the passwords before storing them, never store them in plain text.The fields of HeroCreate are:name
age
secret_name# Code above omitted 👆class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str
class HeroPublic(HeroBase):
    id: int
class HeroCreate(HeroBase):
    secret_name: str# Code below omitted 👇👀 Full file preview
🤓 Other versions and variants
HeroUpdate - the data model to update a hero¶
We didn't have a way to update a hero in the previous version of the app, but now with multiple models, we can do it. 🎉The HeroUpdate data model is somewhat special, it has all the same fields that would be needed to create a new hero, but all the fields are optional (they all have a default value). This way, when you update a hero, you can send just the fields that you want to update.Because all the fields actually change (the type now includes None and they now have a default value of None), we need to re-declare them.We don't really need to inherit from HeroBase because we are re-declaring all the fields. I'll leave it inheriting just for consistency, but this is not necessary. It's more a matter of personal taste. 🤷The fields of HeroUpdate are:name
age
secret_name# Code above omitted 👆class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str
class HeroPublic(HeroBase):
    id: int
class HeroCreate(HeroBase):
    secret_name: str
class HeroUpdate(HeroBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None# Code below omitted 👇👀 Full file preview
🤓 Other versions and variants
Create with HeroCreate and return a HeroPublic¶
Now that we have multiple models, we can update the parts of the app that use them.We receive in the request a HeroCreate data model, and from it, we create a Hero table model.This new table model Hero will have the fields sent by the client, and will also have an id generated by the database.Then we return the same table model Hero as is from the function. But as we declare the response_model with the HeroPublic data model, FastAPI will use HeroPublic to validate and serialize the data.
# Code above omitted 👆@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero# Code below omitted 👇👀 Full file preview
🤓 Other versions and variants
TipNow we use response_model=HeroPublic instead of the return type annotation -> HeroPublic because the value that we are returning is actually not a HeroPublic.If we had declared -> HeroPublic, your editor and linter would complain (rightfully so) that you are returning a Hero instead of a HeroPublic.By declaring it in response_model we are telling FastAPI to do its thing, without interfering with the type annotations and the help from your editor and other tools.Read Heroes with HeroPublic¶
We can do the same as before to read Heros, again, we use response_model=list[HeroPublic] to ensure that the data is validated and serialized correctly.
# Code above omitted 👆@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes# Code below omitted 👇👀 Full file preview
🤓 Other versions and variants
Read One Hero with HeroPublic¶
We can read a single hero:
# Code above omitted 👆@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero# Code below omitted 👇👀 Full file preview
🤓 Other versions and variants
Update a Hero with HeroUpdate¶
We can update a hero. For this we use an HTTP PATCH operation.And in the code, we get a dict with all the data sent by the client, only the data sent by the client, excluding any values that would be there just for being the default values. To do it we use exclude_unset=True. This is the main trick. 🪄Then we use hero_db.sqlmodel_update(hero_data) to update the hero_db with the data from hero_data.
# Code above omitted 👆@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db# Code below omitted 👇👀 Full file preview
🤓 Other versions and variants
Delete a Hero Again¶
Deleting a hero stays pretty much the same.We won't satisfy the desire to refactor everything in this one. 😅
# Code above omitted 👆@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}👀 Full file preview
🤓 Other versions and variants
Run the App Again¶
You can run the app again:If you go to the /docs API UI, you will see that it is now updated, and it won't expect to receive the id from the client when creating a hero, etc.
Recap¶
You can use SQLModel to interact with a SQL database and simplify the code with data models and table models.You can learn a lot more at the SQLModel docs, there's a longer mini tutorial on using SQLModel with FastAPI. 🚀
CORS (Cross-Origin Resource Sharing)
Bigger Applications - Multiple Files
Bigger Applications - Multiple Files 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
An example file structure
APIRouter
Import APIRouter
Path operations with APIRouter
Dependencies
Another module with APIRouter
Import the dependencies
How relative imports work
Add some custom tags, responses, and dependencies
The main Import Import the APIRouter
How the importing works
Avoid name collisions
Include the APIRouters for users and items
Include an APIRouter with a custom prefix, tags, responses, and dependencies
Include a path operation
Check the automatic API docs
Include the same router multiple times with different prefix
Include an APIRouter in another
Bigger Applications - Multiple Files¶
If you are building an application or a web API, it's rarely the case that you can put everything in a single file.FastAPI provides a convenience tool to structure your application while keeping all the flexibility.InfoIf you come from Flask, this would be the equivalent of Flask's Blueprints.An example file structure¶
Let's say you have a file structure like this:
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
TipThere are several __init__.py files: one in each directory or subdirectory.This is what allows importing code from one file into another.For example, in app/main.py you could have a line like:
from app.routers import items
The app directory contains everything. And it has an empty file app/__init__.py, so it is a "Python package" (a collection of "Python modules"): app.
It contains an app/main.py file. As it is inside a Python package (a directory with a file __init__.py), it is a "module" of that package: app.main.
There's also an app/dependencies.py file, just like app/main.py, it is a "module": app.dependencies.
There's a subdirectory app/routers/ with another file __init__.py, so it's a "Python subpackage": app.routers.
The file app/routers/items.py is inside a package, app/routers/, so, it's a submodule: app.routers.items.
The same with app/routers/users.py, it's another submodule: app.routers.users.
There's also a subdirectory app/internal/ with another file __init__.py, so it's another "Python subpackage": app.internal.
And the file app/internal/admin.py is another submodule: app.internal.admin.
The same file structure with comments:
.
├── app                  # "app" is a Python package
│   ├── __init__.py      # this file makes "app" a "Python package"
│   ├── main.py          # "main" module, e.g. import app.main
│   ├── dependencies.py  # "dependencies" module, e.g. import app.dependencies
│   └── routers          # "routers" is a "Python subpackage"
│   │   ├── __init__.py  # makes "routers" a "Python subpackage"
│   │   ├── items.py     # "items" submodule, e.g. import app.routers.items
│   │   └── users.py     # "users" submodule, e.g. import app.routers.users
│   └── internal         # "internal" is a "Python subpackage"
│       ├── __init__.py  # makes "internal" a "Python subpackage"
│       └── admin.py     # "admin" submodule, e.g. import app.internal.admin
APIRouter¶
Let's say the file dedicated to handling just users is the submodule at /app/routers/users.py.You want to have the path operations related to your users separated from the rest of the code, to keep it organized.But it's still part of the same FastAPI application/web API (it's part of the same "Python Package").You can create the path operations for that module using APIRouter.Import APIRouter¶
You import it and create an "instance" the same way you would with the class FastAPI:app/routers/users.pyfrom fastapi import APIRouterrouter = APIRouter()
@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]
@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}
@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
Path operations with APIRouter¶
And then you use it to declare your path operations.Use it the same way you would use the FastAPI class:app/routers/users.pyfrom fastapi import APIRouterrouter = APIRouter()
@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]
@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}
@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
You can think of APIRouter as a "mini FastAPI" class.All the same options are supported.All the same parameters, responses, dependencies, tags, etc.TipIn this example, the variable is called router, but you can name it however you want.We are going to include this APIRouter in the main FastAPI app, but first, let's check the dependencies and another APIRouter.Dependencies¶
We see that we are going to need some dependencies used in several places of the application.So we put them in their own dependencies module (app/dependencies.py).We will now use a simple dependency to read a custom X-Token header:
 non-Annotated
app/dependencies.pyfrom typing import Annotatedfrom fastapi import Header, HTTPException
async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")TipWe are using an invented header to simplify this example.But in real cases you will get better results using the integrated Security utilities.Another module with APIRouter¶
Let's say you also have the endpoints dedicated to handling "items" from your application in the module at app/routers/items.py.You have path operations for:/items/
/items/{item_id}
It's all the same structure as with app/routers/users.py.But we want to be smarter and simplify the code a bit.We know all the path operations in this module have the same:Path prefix: /items.
tags: (just one tag: items).
Extra responses.
dependencies: they all need that X-Token dependency we created.
So, instead of adding all that to each path operation, we can add it to the APIRouter.app/routers/items.pyfrom fastapi import APIRouter, Depends, HTTPExceptionfrom ..dependencies import get_token_headerrouter = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}
@router.get("/")
async def read_items():
    return fake_items_db
@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}
@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
As the path of each path operation has to start with /, like in:
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
...the prefix must not include a final /.So, the prefix in this case is /items.We can also add a list of tags and extra responses that will be applied to all the path operations included in this router.And we can add a list of dependencies that will be added to all the path operations in the router and will be executed/solved for each request made to them.TipNote that, much like dependencies in path operation decorators, no value will be passed to your path operation function.The end result is that the item paths are now:/items/
/items/{item_id}
...as we intended.They will be marked with a list of tags that contain a single string "items".
These "tags" are especially useful for the automatic interactive documentation systems (using OpenAPI).
All of them will include the predefined responses.
All these path operations will have the list of dependencies evaluated/executed before them.
If you also declare dependencies in a specific path operation, they will be executed too.
The router dependencies are executed first, then the dependencies in the decorator, and then the normal parameter dependencies.
You can also add Security dependencies with scopes.
TipHaving dependencies in the APIRouter can be used, for example, to require authentication for a whole group of path operations. Even if the dependencies are not added individually to each one of them.CheckThe prefix, tags, responses, and dependencies parameters are (as in many other cases) just a feature from FastAPI to help you avoid code duplication.Import the dependencies¶
This code lives in the module app.routers.items, the file app/routers/items.py.And we need to get the dependency function from the module app.dependencies, the file app/dependencies.py.So we use a relative import with .. for the dependencies:app/routers/items.pyfrom fastapi import APIRouter, Depends, HTTPExceptionfrom ..dependencies import get_token_headerrouter = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}
@router.get("/")
async def read_items():
    return fake_items_db
@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}
@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
How relative imports work¶
TipIf you know perfectly how imports work, continue to the next section below.A single dot ., like in:
from .dependencies import get_token_header
would mean:Starting in the same package that this module (the file app/routers/items.py) lives in (the directory app/routers/)...
find the module dependencies (an imaginary file at app/routers/dependencies.py)...
and from it, import the function get_token_header.
But that file doesn't exist, our dependencies are in a file at app/dependencies.py.Remember how our app/file structure looks like:The two dots .., like in:
from ..dependencies import get_token_header
mean:Starting in the same package that this module (the file app/routers/items.py) lives in (the directory app/routers/)...
go to the parent package (the directory app/)...
and in there, find the module dependencies (the file at app/dependencies.py)...
and from it, import the function get_token_header.
That works correctly! 🎉The same way, if we had used three dots ..., like in:
from ...dependencies import get_token_header
that would mean:Starting in the same package that this module (the file app/routers/items.py) lives in (the directory app/routers/)...
go to the parent package (the directory app/)...
then go to the parent of that package (there's no parent package, app is the top level 😱)...
and in there, find the module dependencies (the file at app/dependencies.py)...
and from it, import the function get_token_header.
That would refer to some package above app/, with its own file __init__.py, etc. But we don't have that. So, that would throw an error in our example. 🚨But now you know how it works, so you can use relative imports in your own apps no matter how complex they are. 🤓Add some custom tags, responses, and dependencies¶
We are not adding the prefix /items nor the tags=["items"] to each path operation because we added them to the APIRouter.But we can still add more tags that will be applied to a specific path operation, and also some extra responses specific to that path operation:app/routers/items.pyfrom fastapi import APIRouter, Depends, HTTPExceptionfrom ..dependencies import get_token_headerrouter = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}
@router.get("/")
async def read_items():
    return fake_items_db
@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}
@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
TipThis last path operation will have the combination of tags: ["items", "custom"].And it will also have both responses in the documentation, one for 404 and one for 403.The main FastAPI¶
Now, let's see the module at app/main.py.Here's where you import and use the class FastAPI.This will be the main file in your application that ties everything together.And as most of your logic will now live in its own specific module, the main file will be quite simple.Import FastAPI¶
You import and create a FastAPI class as normally.And we can even declare global dependencies that will be combined with the dependencies for each APIRouter:app/main.pyfrom fastapi import Depends, 
from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, usersapp = FastAPI(dependencies=[Depends(get_query_token)])
app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
Import the APIRouter¶
Now we import the other submodules that have APIRouters:app/main.pyfrom fastapi import Depends, 
from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, usersapp = FastAPI(dependencies=[Depends(get_query_token)])
app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
As the files app/routers/users.py and app/routers/items.py are submodules that are part of the same Python package app, we can use a single dot . to import them using "relative imports".How the importing works¶
The section:
from .routers import items, users
means:Starting in the same package that this module (the file app/main.py) lives in (the directory app/)...
look for the subpackage routers (the directory at app/routers/)...
and from it, import the submodule items (the file at app/routers/items.py) and users (the file at app/routers/users.py)...
The module items will have a variable router (items.router). This is the same one we created in the file app/routers/items.py, it's an APIRouter object.And then we do the same for the module users.We could also import them like:
from app.routers import items, users
InfoThe first version is a "relative import":
from .routers import items, users
The second version is an "absolute import":
from app.routers import items, users
To learn more about Python Packages and Modules, read the official Python documentation about Modules.Avoid name collisions¶
We are importing the submodule items directly, instead of importing just its variable router.This is because we also have another variable named router in the submodule users.If we had imported one after the other, like:
from .routers.items import router
from .routers.users import router
the router from users would overwrite the one from items and we wouldn't be able to use them at the same time.So, to be able to use both of them in the same file, we import the submodules directly:app/main.pyfrom fastapi import Depends, 
from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, usersapp = FastAPI(dependencies=[Depends(get_query_token)])
app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
Include the APIRouters for users and items¶
Now, let's include the routers from the submodules users and items:app/main.pyfrom fastapi import Depends, 
from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, usersapp = FastAPI(dependencies=[Depends(get_query_token)])
app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
Infousers.router contains the APIRouter inside of the file app/routers/users.py.And items.router contains the APIRouter inside of the file app/routers/items.py.With app.include_router() we can add each APIRouter to the main FastAPI application.It will include all the routes from that router as part of it.Technical DetailsIt will actually internally create a path operation for each path operation that was declared in the APIRouter.So, behind the scenes, it will actually work as if everything was the same single app.CheckYou don't have to worry about performance when including routers.This will take microseconds and will only happen at startup.So it won't affect performance. ⚡Include an APIRouter with a custom prefix, tags, responses, and dependencies¶
Now, let's imagine your organization gave you the app/internal/admin.py file.It contains an APIRouter with some admin path operations that your organization shares between several projects.For this example it will be super simple. But let's say that because it is shared with other projects in the organization, we cannot modify it and add a prefix, dependencies, tags, etc. directly to the APIRouter:app/internal/admin.pyfrom fastapi import APIRouterrouter = APIRouter()
@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}
But we still want to set a custom prefix when including the APIRouter so that all its path operations start with /admin, we want to secure it with the dependencies we already have for this project, and we want to include tags and responses.We can declare all that without having to modify the original APIRouter by passing those parameters to app.include_router():app/main.pyfrom fastapi import Depends, 
from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, usersapp = FastAPI(dependencies=[Depends(get_query_token)])
app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
That way, the original APIRouter will stay unmodified, so we can still share that same app/internal/admin.py file with other projects in the organization.The result is that in our app, each of the path operations from the admin module will have:The prefix /admin.
The tag admin.
The dependency get_token_header.
The response 418. 🍵
But that will only affect that APIRouter in our app, not in any other code that uses it.So, for example, other projects could use the same APIRouter with a different authentication method.Include a path operation¶
We can also add path operations directly to the FastAPI app.Here we do it... just to show that we can 🤷:app/main.pyfrom fastapi import Depends, 
from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, usersapp = FastAPI(dependencies=[Depends(get_query_token)])
app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
and it will work correctly, together with all the other path operations added with app.include_router().Very Technical DetailsNote: this is a very technical detail that you probably can just skip.The APIRouters are not "mounted", they are not isolated from the rest of the application.This is because we want to include their path operations in the OpenAPI schema and the user interfaces.As we cannot just isolate them and "mount" them independently of the rest, the path operations are "cloned" (re-created), not included directly.Check the automatic API docs¶
Now, run your app:And open the docs at http://127.0.0.1:8000/docs.You will see the automatic API docs, including the paths from all the submodules, using the correct paths (and prefixes) and the correct tags:Include the same router multiple times with different prefix¶
You can also use .include_router() multiple times with the same router using different prefixes.This could be useful, for example, to expose the same API under different prefixes, e.g. /api/v1 and /api/latest.This is an advanced usage that you might not really need, but it's there in case you do.Include an APIRouter in another¶
The same way you can include an APIRouter in a FastAPI application, you can include an APIRouter in another APIRouter using:
router.include_router(other_router)
Make sure you do it before including router in the FastAPI app, so that the path operations from other_router are also included.
SQL (Relational) Databases
Background Tasks
Background Tasks 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Using BackgroundTasks
Create a task function
Add the background task
Dependency Injection
Technical Details
Caveat
Recap
Background Tasks¶
You can define background tasks to be run after returning a response.This is useful for operations that need to happen after a request, but that the client doesn't really have to be waiting for the operation to complete before receiving the response.This includes, for example:Email notifications sent after performing an action:
As connecting to an email server and sending an email tends to be "slow" (several seconds), you can return the response right away and send the email notification in the background.
Processing data:
For example, let's say you receive a file that must go through a slow process, you can return a response of "Accepted" (HTTP 202) and process the file in the background.
Using BackgroundTasks¶
First, import BackgroundTasks and define a parameter in your path operation function with a type declaration of BackgroundTasks:
from fastapi import BackgroundTasks, 
app = FastAPI()
def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)
@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}FastAPI will create the object of type BackgroundTasks for you and pass it as that parameter.Create a task function¶
Create a function to be run as the background task.It is just a standard function that can receive parameters.It can be an async def or normal def function, FastAPI will know how to handle it correctly.In this case, the task function will write to a file (simulating sending an email).And as the write operation doesn't use async and await, we define the function with normal def:
from fastapi import BackgroundTasks, 
app = FastAPI()
def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)
@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}Add the background task¶
Inside of your path operation function, pass your task function to the background tasks object with the method .add_task():
from fastapi import BackgroundTasks, 
app = FastAPI()
def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)
@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}.add_task() receives as arguments:A task function to be run in the background (write_notification).
Any sequence of arguments that should be passed to the task function in order (email).
Any keyword arguments that should be passed to the task function (message="some notification").
Dependency Injection¶
Using BackgroundTasks also works with the dependency injection system, you can declare a parameter of type BackgroundTasks at multiple levels: in a path operation function, in a dependency (dependable), in a sub-dependency, etc.FastAPI knows what to do in each case and how to reuse the same object, so that all the background tasks are merged together and are run in the background afterwards:
from typing import Annotatedfrom fastapi import BackgroundTasks, Depends, 
app = FastAPI()
def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)
def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q
@app.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}🤓 Other versions and variants
In this example, the messages will be written to the log.txt file after the response is sent.If there was a query in the request, it will be written to the log in a background task.And then another background task generated at the path operation function will write a message using the email path parameter.Technical Details¶
The class BackgroundTasks comes directly from starlette.background.It is imported/included directly into FastAPI so that you can import it from fastapi and avoid accidentally importing the alternative BackgroundTask (without the s at the end) from starlette.background.By only using BackgroundTasks (and not BackgroundTask), it's then possible to use it as a path operation function parameter and have FastAPI handle the rest for you, just like when using the Request object directly.It's still possible to use BackgroundTask alone in FastAPI, but you have to create the object in your code and return a Starlette Response including it.You can see more details in Starlette's official docs for Background Tasks.Caveat¶
If you need to perform heavy background computation and you don't necessarily need it to be run by the same process (for example, you don't need to share memory, variables, etc), you might benefit from using other bigger tools like Celery.They tend to require more complex configurations, a message/job queue manager, like RabbitMQ or Redis, but they allow you to run background tasks in multiple processes, and especially, in multiple servers.But if you need to access variables and objects from the same FastAPI app, or you need to perform small background tasks (like sending an email notification), you can simply just use BackgroundTasks.Recap¶
Import and use BackgroundTasks with parameters in path operation functions and dependencies to add background tasks.
Bigger Applications - Multiple Files
Metadata and Docs URLs
Metadata and Docs URLs 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Metadata for API
License identifier
Metadata for tags
Create metadata for tags
Use your tags
Check the docs
Order of tags
OpenAPI URL
Docs URLs
Metadata and Docs URLs¶
You can customize several metadata configurations in your FastAPI application.Metadata for API¶
You can set the following fields that are used in the OpenAPI specification and the automatic API docs UIs:Parameter	Type	Description
title	str	The title of the API.
summary	str	A short summary of the API. Available since OpenAPI 3.1.0, FastAPI 0.99.0.
description	str	A short description of the API. It can use Markdown.
version	string	The version of the API. This is the version of your own application, not of OpenAPI. For example 2.5.0.
terms_of_service	str	A URL to the Terms of Service for the API. If provided, this has to be a URL.
contact	dict	The contact information for the exposed API. It can contain several fields.
contact fields
license_info	dict	The license information for the exposed API. It can contain several fields.
license_info fields
You can set them as follows:
from fastapi import 
description = """
ChimichangApp API helps you do awesome stuff. 🚀## ItemsYou can **read items**.## UsersYou will be able to:* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""app = FastAPI(
    title="ChimichangApp",
    description=description,
    summary="Deadpool's favorite app. Nuff said.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
@app.get("/items/")
async def read_items():
    return [{"name": "Katana"}]TipYou can write Markdown in the description field and it will be rendered in the output.With this configuration, the automatic API docs would look like:License identifier¶
Since OpenAPI 3.1.0 and FastAPI 0.99.0, you can also set the license_info with an identifier instead of a url.For example:
from fastapi import 
description = """
ChimichangApp API helps you do awesome stuff. 🚀## ItemsYou can **read items**.## UsersYou will be able to:* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""app = FastAPI(
    title="ChimichangApp",
    description=description,
    summary="Deadpool's favorite app. Nuff said.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT",
    },
)
@app.get("/items/")
async def read_items():
    return [{"name": "Katana"}]Metadata for tags¶
You can also add additional metadata for the different tags used to group your path operations with the parameter openapi_tags.It takes a list containing one dictionary for each tag.Each dictionary can contain:name (required): a str with the same tag name you use in the tags parameter in your path operations and APIRouters.
description: a str with a short description for the tag. It can have Markdown and will be shown in the docs UI.
externalDocs: a dict describing external documentation with:
description: a str with a short description for the external docs.
url (required): a str with the URL for the external documentation.
Create metadata for tags¶
Let's try that in an example with tags for users and items.Create metadata for your tags and pass it to the openapi_tags parameter:
from fastapi import 
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]app = FastAPI(openapi_tags=tags_metadata)
@app.get("/users/", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]
@app.get("/items/", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]Notice that you can use Markdown inside of the descriptions, for example "login" will be shown in bold (login) and "fancy" will be shown in italics (fancy).TipYou don't have to add metadata for all the tags that you use.Use your tags¶
Use the tags parameter with your path operations (and APIRouters) to assign them to different tags:
from fastapi import 
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]app = FastAPI(openapi_tags=tags_metadata)
@app.get("/users/", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]
@app.get("/items/", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]InfoRead more about tags in Path Operation Configuration.Check the docs¶
Now, if you check the docs, they will show all the additional metadata:Order of tags¶
The order of each tag metadata dictionary also defines the order shown in the docs UI.For example, even though users would go after items in alphabetical order, it is shown before them, because we added their metadata as the first dictionary in the list.OpenAPI URL¶
By default, the OpenAPI schema is served at /openapi.json.But you can configure it with the parameter openapi_url.For example, to set it to be served at /api/v1/openapi.json:
from fastapi import 
app = FastAPI(openapi_url="/api/v1/openapi.json")
@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]If you want to disable the OpenAPI schema completely you can set openapi_url=None, that will also disable the documentation user interfaces that use it.Docs URLs¶
You can configure the two documentation user interfaces included:Swagger UI: served at /docs.
You can set its URL with the parameter docs_url.
You can disable it by setting docs_url=None.
ReDoc: served at /redoc.
You can set its URL with the parameter redoc_url.
You can disable it by setting redoc_url=None.
For example, to set Swagger UI to be served at /documentation and disable ReDoc:
from fastapi import 
app = FastAPI(docs_url="/documentation", redoc_url=None)
@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
Background Tasks
Static Files
Static Files 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Use StaticFiles
What is "Mounting"
Details
More info
Static Files¶
You can serve static files automatically from a directory using StaticFiles.Use StaticFiles¶
Import StaticFiles.
"Mount" a StaticFiles() instance in a specific path.from fastapi import from fastapi.staticfiles import StaticFilesapp = FastAPI()app.mount("/static", StaticFiles(directory="static"), name="static")Technical DetailsYou could also use from starlette.staticfiles import StaticFiles.FastAPI provides the same starlette.staticfiles as fastapi.staticfiles just as a convenience for you, the developer. But it actually comes directly from Starlette.What is "Mounting"¶
"Mounting" means adding a complete "independent" application in a specific path, that then takes care of handling all the sub-paths.This is different from using an APIRouter as a mounted application is completely independent. The OpenAPI and docs from your main application won't include anything from the mounted application, etc.You can read more about this in the Advanced User Guide.Details¶
The first "/static" refers to the sub-path this "sub-application" will be "mounted" on. So, any path that starts with "/static" will be handled by it.The directory="static" refers to the name of the directory that contains your static files.The name="static" gives it a name that can be used internally by FastAPI.All these parameters can be different than "static", adjust them with the needs and specific details of your own application.More info¶
For more details and options check Starlette's docs about Static Files.
Metadata and Docs URLs
Testing
Testing 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Using TestClient
Separating tests
FastAPI app file
Testing file
Testing: extended example
Extended FastAPI app file
Extended testing file
Run it
Testing¶
Thanks to Starlette, testing FastAPI applications is easy and enjoyable.It is based on HTTPX, which in turn is designed based on Requests, so it's very familiar and intuitive.With it, you can use pytest directly with FastAPI.Using TestClient¶
InfoTo use TestClient, first install httpx.Make sure you create a virtual environment, activate it, and then install it, for example:
$ pip install httpx
Import TestClient.Create a TestClient by passing your FastAPI application to it.Create functions with a name that starts with test_ (this is standard pytest conventions).Use the TestClient object the same way as you do with httpx.Write simple assert statements with the standard Python expressions that you need to check (again, standard pytest).
from fastapi import from fastapi.testclient import TestClientapp = FastAPI()
@app.get("/")
async def read_main():
    return {"msg": "Hello World"}
client = TestClient(app)
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}TipNotice that the testing functions are normal def, not async def.And the calls to the client are also normal calls, not using await.This allows you to use pytest directly without complications.Technical DetailsYou could also use from starlette.testclient import TestClient.FastAPI provides the same starlette.testclient as fastapi.testclient just as a convenience for you, the developer. But it comes directly from Starlette.TipIf you want to call async functions in your tests apart from sending requests to your FastAPI application (e.g. asynchronous database functions), have a look at the Async Tests in the advanced tutorial.Separating tests¶
In a real application, you probably would have your tests in a different file.And your FastAPI application might also be composed of several files/modules, etc.FastAPI app file¶
Let's say you have a file structure as described in Bigger Applications:
.
├── app
│   ├── __init__.py
│   └── main.py
In the file main.py you have your FastAPI app:
from fastapi import 
app = FastAPI()
@app.get("/")
async def read_main():
    return {"msg": "Hello World"}Testing file¶
Then you could have a file test_main.py with your tests. It could live on the same Python package (the same directory with a __init__.py file):
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
Because this file is in the same package, you can use relative imports to import the object app from the main module (main.py):
from fastapi.testclient import TestClientfrom .main import appclient = TestClient(app)
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}...and have the code for the tests just like before.Testing: extended example¶
Now let's extend this example and add more details to see how to test different parts.Extended FastAPI app file¶
Let's continue with the same file structure as before:
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
Let's say that now the file main.py with your FastAPI app has some other path operations.It has a GET operation that could return an error.It has a POST operation that could return several errors.Both path operations require an X-Token header. non-Annotated
 non-Annotatedfrom typing import Annotatedfrom fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModelfake_secret_token = "coneofsilence"fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}app = FastAPI()
class Item(BaseModel):
    id: str
    title: str
    description: str | None = None
@app.get("/items/{item_id}", response_model=Item)
async def read_main(item_id: str, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]
@app.post("/items/", response_model=Item)
async def create_item(item: Item, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item.id in fake_db:
        raise HTTPException(status_code=409, detail="Item already exists")
    fake_db[item.id] = item
    return itemExtended testing file¶
You could then update test_main.py with the extended tests:
from fastapi.testclient import TestClientfrom .main import appclient = TestClient(app)
def test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }
def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}
def test_read_nonexistent_item():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }
def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "hailhydra"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}
def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "foo",
            "title": "The Foo ID Stealers",
            "description": "There goes my stealer",
        },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Item already exists"}Whenever you need the client to pass information in the request and you don't know how to, you can search (Google) how to do it in httpx, or even how to do it with requests, as HTTPX's design is based on Requests' design.Then you just do the same in your tests.E.g.:To pass a path or query parameter, add it to the URL itself.
To pass a JSON body, pass a Python object (e.g. a dict) to the parameter json.
If you need to send Form Data instead of JSON, use the data parameter instead.
To pass headers, use a dict in the headers parameter.
For cookies, a dict in the cookies parameter.
For more information about how to pass data to the backend (using httpx or the TestClient) check the HTTPX documentation.InfoNote that the TestClient receives data that can be converted to JSON, not Pydantic models.If you have a Pydantic model in your test and you want to send its data to the application during testing, you can use the jsonable_encoder described in JSON Compatible Encoder.Run it¶
After that, you just need to install pytest.Make sure you create a virtual environment, activate it, and then install it, for example:
It will detect the files and tests automatically, execute them, and report the results back to you.Run the tests with:Static Files
Debugging
Debugging 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
First Steps
Path Parameters
Query Parameters
Request Body
Query Parameters and String Validations
Path Parameters and Numeric Validations
Query Parameter Models
Body - Multiple Parameters
Body - Fields
Body - Nested Models
Declare Request Example Data
Extra Data Types
Cookie Parameters
Header Parameters
Cookie Parameter Models
Header Parameter Models
Response Model - Return Type
Extra Models
Response Status Code
Form Data
Form Models
Request Files
Request Forms and Files
Handling Errors
Path Operation Configuration
JSON Compatible Encoder
Body - Updates
Dependencies
Security
Middleware
CORS (Cross-Origin Resource Sharing)
SQL (Relational) Databases
Bigger Applications - Multiple Files
Background Tasks
Metadata and Docs URLs
Static Files
Testing
Debugging
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Call uvicorn
About __name__ == "__main__"
More details
Run your code with your debugger
Debugging¶
You can connect the debugger in your editor, for example with Visual Studio Code or PyCharm.Call uvicorn¶
In your FastAPI application, import and run uvicorn directly:
import uvicorn
from fastapi import 
app = FastAPI()
@app.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)About __name__ == "__main__"¶
The main purpose of the __name__ == "__main__" is to have some code that is executed when your file is called with:
fast →
pyth
but is not called when another file imports it, like in:
from myapp import app
More details¶
Let's say your file is named myapp.py.If you run it with:then the internal variable __name__ in your file, created automatically by Python, will have as value the string "__main__".So, the section:
    uvicorn.run(app, host="0.0.0.0", port=8000)
will run.This won't happen if you import that module (file).So, if you have another file importer.py with:
from myapp import app# Some more code
in that case, the automatically created variable inside of myapp.py will not have the variable __name__ with a value of "__main__".So, the line:
    uvicorn.run(app, host="0.0.0.0", port=8000)
will not be executed.InfoFor more information, check the official Python docs.Run your code with your debugger¶
Because you are running the Uvicorn server directly from your code, you can call your Python program (your FastAPI application) directly from the debugger.For example, in Visual Studio Code, you can:Go to the "Debug" panel.
"Add configuration...".
Select "Python"
Run the debugger with the option "Python: Current File (Integrated Terminal)".
It will then start the server with your FastAPI code, stop at your breakpoints, etc.Here's how it might look:If you use Pycharm, you can:Open the "Run" menu.
Select the option "Debug...".
Then a context menu shows up.
Select the file to debug (in this case, main.py).
It will then start the server with your FastAPI code, stop at your breakpoints, etc.Here's how it might look:
Testing
Advanced User Guide
Advanced User Guide 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Additional Read the Tutorial first
External Courses
Advanced User Guide
Advanced User Guide¶
Additional Features¶
The main Tutorial - User Guide should be enough to give you a tour through all the main features of FastAPI.In the next sections you will see other options, configurations, and additional features.TipThe next sections are not necessarily "advanced".And it's possible that for your use case, the solution is in one of them.Read the Tutorial first¶
You could still use most of the features in FastAPI with the knowledge from the main Tutorial - User Guide.And the next sections assume you already read it, and assume that you know those main ideas.External Courses¶
Although the Tutorial - User Guide and this Advanced User Guide are written as a guided tutorial (like a book) and should be enough for you to learn FastAPI, you might want to complement it with additional courses.Or it might be the case that you just prefer to take other courses because they adapt better to your learning style.Some course providers ✨ sponsor FastAPI ✨, this ensures the continued and healthy development of FastAPI and its ecosystem.And it shows their true commitment to FastAPI and its community (you), as they not only want to provide you a good learning experience but also want to make sure you have a good and healthy framework, FastAPI. 🙇You might want to try their courses:Talk Python Training
Test-Driven DevelopmentDebugging
Path Operation Advanced Configuration
Path Operation Advanced Configuration 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
OpenAPI operationId
Using the path operation function name as the operationId
Exclude from OpenAPI
Advanced description from docstring
Additional Responses
OpenAPI Extra
OpenAPI Extensions
Custom OpenAPI path operation schema
Custom OpenAPI content type
Advanced User Guide
Path Operation Advanced Configuration¶
OpenAPI operationId¶
WarningIf you are not an "expert" in OpenAPI, you probably don't need this.You can set the OpenAPI operationId to be used in your path operation with the parameter operation_id.You would have to make sure that it is unique for each operation.
from fastapi import 
app = FastAPI()
@app.get("/items/", operation_id="some_specific_id_you_define")
async def read_items():
    return [{"item_id": "Foo"}]Using the path operation function name as the operationId¶
If you want to use your APIs' function names as operationIds, you can iterate over all of them and override each path operation's operation_id using their APIRoute.name.You should do it after adding all your path operations.
from fastapi import from fastapi.routing import APIRouteapp = FastAPI()
@app.get("/items/")
async def read_items():
    return [{"item_id": "Foo"}]
def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'
use_route_names_as_operation_ids(app)TipIf you manually call app.openapi(), you should update the operationIds before that.WarningIf you do this, you have to make sure each one of your path operation functions has a unique name.Even if they are in different modules (Python files).Exclude from OpenAPI¶
To exclude a path operation from the generated OpenAPI schema (and thus, from the automatic documentation systems), use the parameter include_in_schema and set it to False:
from fastapi import 
app = FastAPI()
@app.get("/items/", include_in_schema=False)
async def read_items():
    return [{"item_id": "Foo"}]Advanced description from docstring¶
You can limit the lines used from the docstring of a path operation function for OpenAPI.Adding an \f (an escaped "form feed" character) causes FastAPI to truncate the output used for OpenAPI at this point.It won't show up in the documentation, but other tools (such as Sphinx) will be able to use the rest.
from typing import Set, Unionfrom fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
@app.post("/items/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    \f
    :param item: User input.
    """
    return itemAdditional Responses¶
You probably have seen how to declare the response_model and status_code for a path operation.That defines the metadata about the main response of a path operation.You can also declare additional responses with their models, status codes, etc.There's a whole chapter here in the documentation about it, you can read it at Additional Responses in OpenAPI.OpenAPI Extra¶
When you declare a path operation in your application, FastAPI automatically generates the relevant metadata about that path operation to be included in the OpenAPI schema.Technical detailsIn the OpenAPI specification it is called the Operation Object.It has all the information about the path operation and is used to generate the automatic documentation.It includes the tags, parameters, requestBody, responses, etc.This path operation-specific OpenAPI schema is normally generated automatically by FastAPI, but you can also extend it.TipThis is a low level extension point.If you only need to declare additional responses, a more convenient way to do it is with Additional Responses in OpenAPI.You can extend the OpenAPI schema for a path operation using the parameter openapi_extra.OpenAPI Extensions¶
This openapi_extra can be helpful, for example, to declare OpenAPI Extensions:
from fastapi import 
app = FastAPI()
@app.get("/items/", openapi_extra={"x-aperture-labs-portal": "blue"})
async def read_items():
    return [{"item_id": "portal-gun"}]If you open the automatic API docs, your extension will show up at the bottom of the specific path operation.And if you see the resulting OpenAPI (at /openapi.json in your API), you will see your extension as part of the specific path operation too:
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                },
                "x-aperture-labs-portal": "blue"
            }
        }
    }
}
Custom OpenAPI path operation schema¶
The dictionary in openapi_extra will be deeply merged with the automatically generated OpenAPI schema for the path operation.So, you could add additional data to the automatically generated schema.For example, you could decide to read and validate the request with your own code, without using the automatic features of FastAPI with Pydantic, but you could still want to define the request in the OpenAPI schema.You could do that with openapi_extra:
from fastapi import FastAPI, Requestapp = FastAPI()
def magic_data_reader(raw_body: bytes):
    return {
        "size": len(raw_body),
        "content": {
            "name": "Maaaagic",
            "price": 42,
            "description": "Just kiddin', no magic here. ✨",
        },
    }
@app.post(
    "/items/",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "required": ["name", "price"],
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "price": {"type": "number"},
                            "description": {"type": "string"},
                        },
                    }
                }
            },
            "required": True,
        },
    },
)
async def create_item(request: Request):
    raw_body = await request.body()
    data = magic_data_reader(raw_body)
    return dataIn this example, we didn't declare any Pydantic model. In fact, the request body is not even parsed as JSON, it is read directly as bytes, and the function magic_data_reader() would be in charge of parsing it in some way.Nevertheless, we can declare the expected schema for the request body.Custom OpenAPI content type¶
Using this same trick, you could use a Pydantic model to define the JSON Schema that is then included in the custom OpenAPI schema section for the path operation.And you could do this even if the data type in the request is not JSON.For example, in this application we don't use FastAPI's integrated functionality to extract the JSON Schema from Pydantic models nor the automatic validation for JSON. In fact, we are declaring the request content type as YAML, not JSON:
Pydantic v2
Pydantic v
from typing import Listimport yaml
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ValidationErrorapp = FastAPI()
class Item(BaseModel):
    name: str
    tags: List[str]
@app.post(
    "/items/",
    openapi_extra={
        "requestBody": {
            "content": {"application/x-yaml": {"schema": Item.model_json_schema()}},
            "required": True,
        },
    },
)
async def create_item(request: Request):
    raw_body = await request.body()
    try:
        data = yaml.safe_load(raw_body)
    except yaml.YAMLError:
        raise HTTPException(status_code=422, detail="Invalid YAML")
    try:
        item = Item.model_validate(data)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors(include_url=False))
    return item
InfoIn Pydantic version 1 the method to get the JSON Schema for a model was called Item.schema(), in Pydantic version 2, the method is called Item.model_json_schema().Nevertheless, although we are not using the default integrated functionality, we are still using a Pydantic model to manually generate the JSON Schema for the data that we want to receive in YAML.Then we use the request directly, and extract the body as bytes. This means that FastAPI won't even try to parse the request payload as JSON.And then in our code, we parse that YAML content directly, and then we are again using the same Pydantic model to validate the YAML content:
Pydantic v2
Pydantic v
from typing import Listimport yaml
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ValidationErrorapp = FastAPI()
class Item(BaseModel):
    name: str
    tags: List[str]
@app.post(
    "/items/",
    openapi_extra={
        "requestBody": {
            "content": {"application/x-yaml": {"schema": Item.model_json_schema()}},
            "required": True,
        },
    },
)
async def create_item(request: Request):
    raw_body = await request.body()
    try:
        data = yaml.safe_load(raw_body)
    except yaml.YAMLError:
        raise HTTPException(status_code=422, detail="Invalid YAML")
    try:
        item = Item.model_validate(data)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors(include_url=False))
    return item
InfoIn Pydantic version 1 the method to parse and validate an object was Item.parse_obj(), in Pydantic version 2, the method is called Item.model_validate().TipHere we reuse the same Pydantic model.But the same way, we could have validated it in some other way.Advanced User Guide
Additional Status Codes
Additional Status Codes 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Additional status codes
OpenAPI and API docs
Advanced User Guide
Additional Status Codes¶
By default, FastAPI will return the responses using a JSONResponse, putting the content you return from your path operation inside of that JSONResponse.It will use the default status code or the one you set in your path operation.Additional status codes¶
If you want to return additional status codes apart from the main one, you can do that by returning a Response directly, like a JSONResponse, and set the additional status code directly.For example, let's say that you want to have a path operation that allows to update items, and returns HTTP status codes of 200 "OK" when successful.But you also want it to accept new items. And when the items didn't exist before, it creates them, and returns an HTTP status code of 201 "Created".To achieve that, import JSONResponse, and return your content there directly, setting the status_code that you want:
from typing import Annotatedfrom fastapi import Body, FastAPI, status
from fastapi.responses import JSONResponseapp = FastAPI()items = {"foo": {"name": "Fighters", "size": 6}, "bar": {"name": "Tenders", "size": 3}}
@app.put("/items/{item_id}")
async def upsert_item(
    item_id: str,
    name: Annotated[str | None, Body()] = None,
    size: Annotated[int | None, Body()] = None,
):
    if item_id in items:
        item = items[item_id]
        item["name"] = name
        item["size"] = size
        return item
    else:
        item = {"name": name, "size": size}
        items[item_id] = item
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)🤓 Other versions and variants
WarningWhen you return a Response directly, like in the example above, it will be returned directly.It won't be serialized with a model, etc.Make sure it has the data you want it to have, and that the values are valid JSON (if you are using JSONResponse).Technical DetailsYou could also use from starlette.responses import JSONResponse.FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette. The same with status.OpenAPI and API docs¶
If you return additional status codes and responses directly, they won't be included in the OpenAPI schema (the API docs), because FastAPI doesn't have a way to know beforehand what you are going to return.But you can document that in your code, using: Additional Responses.
Path Operation Advanced Configuration
Return a Response Directly
Return a Response Directly 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Return a Response
Using the jsonable_encoder in a Response
Returning a custom Response
Notes
Advanced User Guide
Return a Response Directly¶
When you create a FastAPI path operation you can normally return any data from it: a dict, a list, a Pydantic model, a database model, etc.By default, FastAPI would automatically convert that return value to JSON using the jsonable_encoder explained in JSON Compatible Encoder.Then, behind the scenes, it would put that JSON-compatible data (e.g. a dict) inside of a JSONResponse that would be used to send the response to the client.But you can return a JSONResponse directly from your path operations.It might be useful, for example, to return custom headers or cookies.Return a Response¶
In fact, you can return any Response or any sub-class of it.TipJSONResponse itself is a sub-class of Response.And when you return a Response, FastAPI will pass it directly.It won't do any data conversion with Pydantic models, it won't convert the contents to any type, etc.This gives you a lot of flexibility. You can return any data type, override any data declaration or validation, etc.Using the jsonable_encoder in a Response¶
Because FastAPI doesn't make any changes to a Response you return, you have to make sure its contents are ready for it.For example, you cannot put a Pydantic model in a JSONResponse without first converting it to a dict with all the data types (like datetime, UUID, etc) converted to JSON-compatible types.For those cases, you can use the jsonable_encoder to convert your data before passing it to a response:
from datetime import datetime
from typing import Unionfrom fastapi import from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Union[str, None] = None
app = FastAPI()
@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    return JSONResponse(content=json_compatible_item_data)Technical DetailsYou could also use from starlette.responses import JSONResponse.FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette.Returning a custom Response¶
The example above shows all the parts you need, but it's not very useful yet, as you could have just returned the item directly, and FastAPI would put it in a JSONResponse for you, converting it to a dict, etc. All that by default.Now, let's see how you could use that to return a custom response.Let's say that you want to return an XML response.You could put your XML content in a string, put that in a Response, and return it:
from fastapi import FastAPI, Responseapp = FastAPI()
@app.get("/legacy/")
def get_legacy_data():
    data = """<xml version="1.0">
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")Notes¶
When you return a Response directly its data is not validated, converted (serialized), nor documented automatically.But you can still document it as described in Additional Responses in OpenAPI.You can see in later sections how to use/declare these custom Responses while still having automatic data conversion, documentation, etc.
Additional Status Codes
Custom Response - HTML, Stream, File, others
Custom Response - HTML, Stream, File, others 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Use ORJSONResponse
HTML Response
Return a Response
Document in OpenAPI and override Response
Return an HTMLResponse directly
Available responses
Response
HTMLResponse
PlainTextResponse
JSONResponse
ORJSONResponse
UJSONResponse
RedirectResponse
StreamingResponse
Using StreamingResponse with file-like objects
FileResponse
Custom response class
Default response class
Additional documentation
Advanced User Guide
Custom Response - HTML, Stream, File, others¶
By default, FastAPI will return the responses using JSONResponse.You can override it by returning a Response directly as seen in Return a Response directly.But if you return a Response directly (or any subclass, like JSONResponse), the data won't be automatically converted (even if you declare a response_model), and the documentation won't be automatically generated (for example, including the specific "media type", in the HTTP header Content-Type as part of the generated OpenAPI).But you can also declare the Response that you want to be used (e.g. any Response subclass), in the path operation decorator using the response_class parameter.The contents that you return from your path operation function will be put inside of that Response.And if that Response has a JSON media type (application/json), like is the case with the JSONResponse and UJSONResponse, the data you return will be automatically converted (and filtered) with any Pydantic response_model that you declared in the path operation decorator.NoteIf you use a response class with no media type, FastAPI will expect your response to have no content, so it will not document the response format in its generated OpenAPI docs.Use ORJSONResponse¶
For example, if you are squeezing performance, you can install and use orjson and set the response to be ORJSONResponse.Import the Response class (sub-class) you want to use and declare it in the path operation decorator.For large responses, returning a Response directly is much faster than returning a dictionary.This is because by default, FastAPI will inspect every item inside and make sure it is serializable as JSON, using the same JSON Compatible Encoder explained in the tutorial. This is what allows you to return arbitrary objects, for example database models.But if you are certain that the content that you are returning is serializable with JSON, you can pass it directly to the response class and avoid the extra overhead that FastAPI would have by passing your return content through the jsonable_encoder before passing it to the response class.
from fastapi import from fastapi.responses import ORJSONResponseapp = FastAPI()
@app.get("/items/", response_class=ORJSONResponse)
async def read_items():
    return ORJSONResponse([{"item_id": "Foo"}])InfoThe parameter response_class will also be used to define the "media type" of the response.In this case, the HTTP header Content-Type will be set to application/json.And it will be documented as such in OpenAPI.TipThe ORJSONResponse is only available in FastAPI, not in Starlette.HTML Response¶
To return a response with HTML directly from FastAPI, use HTMLResponse.Import HTMLResponse.
Pass HTMLResponse as the parameter response_class of your path operation decorator.from fastapi import from fastapi.responses import HTMLResponseapp = FastAPI()
@app.get("/items/", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """InfoThe parameter response_class will also be used to define the "media type" of the response.In this case, the HTTP header Content-Type will be set to text/html.And it will be documented as such in OpenAPI.Return a Response¶
As seen in Return a Response directly, you can also override the response directly in your path operation, by returning it.The same example from above, returning an HTMLResponse, could look like:
from fastapi import from fastapi.responses import HTMLResponseapp = FastAPI()
@app.get("/items/")
async def read_items():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)WarningA Response returned directly by your path operation function won't be documented in OpenAPI (for example, the Content-Type won't be documented) and won't be visible in the automatic interactive docs.InfoOf course, the actual Content-Type header, status code, etc, will come from the Response object you returned.Document in OpenAPI and override Response¶
If you want to override the response from inside of the function but at the same time document the "media type" in OpenAPI, you can use the response_class parameter AND return a Response object.The response_class will then be used only to document the OpenAPI path operation, but your Response will be used as is.Return an HTMLResponse directly¶
For example, it could be something like:
from fastapi import from fastapi.responses import HTMLResponseapp = FastAPI()
def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
@app.get("/items/", response_class=HTMLResponse)
async def read_items():
    return generate_html_response()In this example, the function generate_html_response() already generates and returns a Response instead of returning the HTML in a str.By returning the result of calling generate_html_response(), you are already returning a Response that will override the default FastAPI behavior.But as you passed the HTMLResponse in the response_class too, FastAPI will know how to document it in OpenAPI and the interactive docs as HTML with text/html:Available responses¶
Here are some of the available responses.Keep in mind that you can use Response to return anything else, or even create a custom sub-class.Technical DetailsYou could also use from starlette.responses import HTMLResponse.FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette.Response¶
The main Response class, all the other responses inherit from it.You can return it directly.It accepts the following parameters:content - A str or bytes.
status_code - An int HTTP status code.
headers - A dict of strings.
media_type - A str giving the media type. E.g. "text/html".
FastAPI (actually Starlette) will automatically include a Content-Length header. It will also include a Content-Type header, based on the media_type and appending a charset for text types.
from fastapi import FastAPI, Responseapp = FastAPI()
@app.get("/legacy/")
def get_legacy_data():
    data = """<xml version="1.0">
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")HTMLResponse¶
Takes some text or bytes and returns an HTML response, as you read above.PlainTextResponse¶
Takes some text or bytes and returns a plain text response.
from fastapi import from fastapi.responses import PlainTextResponseapp = FastAPI()
@app.get("/", response_class=PlainTextResponse)
async def main():
    return "Hello World"JSONResponse¶
Takes some data and returns an application/json encoded response.This is the default response used in FastAPI, as you read above.ORJSONResponse¶
A fast alternative JSON response using orjson, as you read above.InfoThis requires installing orjson for example with pip install orjson.UJSONResponse¶
An alternative JSON response using ujson.InfoThis requires installing ujson for example with pip install ujson.Warningujson is less careful than Python's built-in implementation in how it handles some edge-cases.
from fastapi import from fastapi.responses import UJSONResponseapp = FastAPI()
@app.get("/items/", response_class=UJSONResponse)
async def read_items():
    return [{"item_id": "Foo"}]TipIt's possible that ORJSONResponse might be a faster alternative.RedirectResponse¶
Returns an HTTP redirect. Uses a 307 status code (Temporary Redirect) by default.You can return a RedirectResponse directly:
from fastapi import from fastapi.responses import RedirectResponseapp = FastAPI()
@app.get("/typer")
async def redirect_typer():
    return RedirectResponse("https://typer.tiangolo.com")Or you can use it in the response_class parameter:
from fastapi import from fastapi.responses import RedirectResponseapp = FastAPI()
@app.get("/fastapi", response_class=RedirectResponse)
async def redirect_fastapi():
    return "https://fastapi.tiangolo.com"If you do that, then you can return the URL directly from your path operation function.In this case, the status_code used will be the default one for the RedirectResponse, which is 307.You can also use the status_code parameter combined with the response_class parameter:
from fastapi import from fastapi.responses import RedirectResponseapp = FastAPI()
@app.get("/pydantic", response_class=RedirectResponse, status_code=302)
async def redirect_pydantic():
    return "https://docs.pydantic.dev/"StreamingResponse¶
Takes an async generator or a normal generator/iterator and streams the response body.
from fastapi import from fastapi.responses import StreamingResponseapp = FastAPI()
async def fake_video_streamer():
    for i in range(10):
        yield b"some fake video bytes"
@app.get("/")
async def main():
    return StreamingResponse(fake_video_streamer())Using StreamingResponse with file-like objects¶
If you have a file-like object (e.g. the object returned by open()), you can create a generator function to iterate over that file-like object.That way, you don't have to read it all first in memory, and you can pass that generator function to the StreamingResponse, and return it.This includes many libraries to interact with cloud storage, video processing, and others.
from fastapi import from fastapi.responses import StreamingResponsesome_file_path = "large-video-file.mp4"
app = FastAPI()
@app.get("/")
def main():
    def iterfile():  # (1)
        with open(some_file_path, mode="rb") as file_like:  # (2)
            yield from file_like  # (3)    return StreamingResponse(iterfile(), media_type="video/mp4")This is the generator function. It's a "generator function" because it contains yield statements inside.
By using a with block, we make sure that the file-like object is closed after the generator function is done. So, after it finishes sending the response.
This yield from tells the function to iterate over that thing named file_like. And then, for each part iterated, yield that part as coming from this generator function (iterfile).So, it is a generator function that transfers the "generating" work to something else internally.By doing it this way, we can put it in a with block, and that way, ensure that the file-like object is closed after finishing.TipNotice that here as we are using standard open() that doesn't support async and await, we declare the path operation with normal def.FileResponse¶
Asynchronously streams a file as the response.Takes a different set of arguments to instantiate than the other response types:path - The file path to the file to stream.
headers - Any custom headers to include, as a dictionary.
media_type - A string giving the media type. If unset, the filename or path will be used to infer a media type.
filename - If set, this will be included in the response Content-Disposition.
File responses will include appropriate Content-Length, Last-Modified and ETag headers.
from fastapi import from fastapi.responses import FileResponsesome_file_path = "large-video-file.mp4"
app = FastAPI()
@app.get("/")
async def main():
    return FileResponse(some_file_path)You can also use the response_class parameter:
from fastapi import from fastapi.responses import FileResponsesome_file_path = "large-video-file.mp4"
app = FastAPI()
@app.get("/", response_class=FileResponse)
async def main():
    return some_file_pathIn this case, you can return the file path directly from your path operation function.Custom response class¶
You can create your own custom response class, inheriting from Response and using it.For example, let's say that you want to use orjson, but with some custom settings not used in the included ORJSONResponse class.Let's say you want it to return indented and formatted JSON, so you want to use the orjson option orjson.OPT_INDENT_2.You could create a CustomORJSONResponse. The main thing you have to do is create a Response.render(content) method that returns the content as bytes:
from typing import Anyimport orjson
from fastapi import FastAPI, Responseapp = FastAPI()
class CustomORJSONResponse(Response):
    media_type = "application/json"    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)
@app.get("/", response_class=CustomORJSONResponse)
async def main():
    return {"message": "Hello World"}Now instead of returning:
{"message": "Hello World"}
...this response will return:
{
  "message": "Hello World"
}
Of course, you will probably find much better ways to take advantage of this than formatting JSON. 😉Default response class¶
When creating a FastAPI class instance or an APIRouter you can specify which response class to use by default.The parameter that defines this is default_response_class.In the example below, FastAPI will use ORJSONResponse by default, in all path operations, instead of JSONResponse.
from fastapi import from fastapi.responses import ORJSONResponseapp = FastAPI(default_response_class=ORJSONResponse)
@app.get("/items/")
async def read_items():
    return [{"item_id": "Foo"}]TipYou can still override response_class in path operations as before.Additional documentation¶
You can also declare the media type and many other details in OpenAPI using responses: Additional Responses in OpenAPI.
Return a Response Directly
Additional Responses in OpenAPI
Custom Response - HTML, Stream, File, others 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Use ORJSONResponse
HTML Response
Return a Response
Document in OpenAPI and override Response
Return an HTMLResponse directly
Available responses
Response
HTMLResponse
PlainTextResponse
JSONResponse
ORJSONResponse
UJSONResponse
RedirectResponse
StreamingResponse
Using StreamingResponse with file-like objects
FileResponse
Custom response class
Default response class
Additional documentation
Advanced User Guide
Custom Response - HTML, Stream, File, others¶
By default, FastAPI will return the responses using JSONResponse.You can override it by returning a Response directly as seen in Return a Response directly.But if you return a Response directly (or any subclass, like JSONResponse), the data won't be automatically converted (even if you declare a response_model), and the documentation won't be automatically generated (for example, including the specific "media type", in the HTTP header Content-Type as part of the generated OpenAPI).But you can also declare the Response that you want to be used (e.g. any Response subclass), in the path operation decorator using the response_class parameter.The contents that you return from your path operation function will be put inside of that Response.And if that Response has a JSON media type (application/json), like is the case with the JSONResponse and UJSONResponse, the data you return will be automatically converted (and filtered) with any Pydantic response_model that you declared in the path operation decorator.NoteIf you use a response class with no media type, FastAPI will expect your response to have no content, so it will not document the response format in its generated OpenAPI docs.Use ORJSONResponse¶
For example, if you are squeezing performance, you can install and use orjson and set the response to be ORJSONResponse.Import the Response class (sub-class) you want to use and declare it in the path operation decorator.For large responses, returning a Response directly is much faster than returning a dictionary.This is because by default, FastAPI will inspect every item inside and make sure it is serializable as JSON, using the same JSON Compatible Encoder explained in the tutorial. This is what allows you to return arbitrary objects, for example database models.But if you are certain that the content that you are returning is serializable with JSON, you can pass it directly to the response class and avoid the extra overhead that FastAPI would have by passing your return content through the jsonable_encoder before passing it to the response class.
from fastapi import from fastapi.responses import ORJSONResponseapp = FastAPI()
@app.get("/items/", response_class=ORJSONResponse)
async def read_items():
    return ORJSONResponse([{"item_id": "Foo"}])InfoThe parameter response_class will also be used to define the "media type" of the response.In this case, the HTTP header Content-Type will be set to application/json.And it will be documented as such in OpenAPI.TipThe ORJSONResponse is only available in FastAPI, not in Starlette.HTML Response¶
To return a response with HTML directly from FastAPI, use HTMLResponse.Import HTMLResponse.
Pass HTMLResponse as the parameter response_class of your path operation decorator.from fastapi import from fastapi.responses import HTMLResponseapp = FastAPI()
@app.get("/items/", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """InfoThe parameter response_class will also be used to define the "media type" of the response.In this case, the HTTP header Content-Type will be set to text/html.And it will be documented as such in OpenAPI.Return a Response¶
As seen in Return a Response directly, you can also override the response directly in your path operation, by returning it.The same example from above, returning an HTMLResponse, could look like:
from fastapi import from fastapi.responses import HTMLResponseapp = FastAPI()
@app.get("/items/")
async def read_items():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)WarningA Response returned directly by your path operation function won't be documented in OpenAPI (for example, the Content-Type won't be documented) and won't be visible in the automatic interactive docs.InfoOf course, the actual Content-Type header, status code, etc, will come from the Response object you returned.Document in OpenAPI and override Response¶
If you want to override the response from inside of the function but at the same time document the "media type" in OpenAPI, you can use the response_class parameter AND return a Response object.The response_class will then be used only to document the OpenAPI path operation, but your Response will be used as is.Return an HTMLResponse directly¶
For example, it could be something like:
from fastapi import from fastapi.responses import HTMLResponseapp = FastAPI()
def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
@app.get("/items/", response_class=HTMLResponse)
async def read_items():
    return generate_html_response()In this example, the function generate_html_response() already generates and returns a Response instead of returning the HTML in a str.By returning the result of calling generate_html_response(), you are already returning a Response that will override the default FastAPI behavior.But as you passed the HTMLResponse in the response_class too, FastAPI will know how to document it in OpenAPI and the interactive docs as HTML with text/html:Available responses¶
Here are some of the available responses.Keep in mind that you can use Response to return anything else, or even create a custom sub-class.Technical DetailsYou could also use from starlette.responses import HTMLResponse.FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette.Response¶
The main Response class, all the other responses inherit from it.You can return it directly.It accepts the following parameters:content - A str or bytes.
status_code - An int HTTP status code.
headers - A dict of strings.
media_type - A str giving the media type. E.g. "text/html".
FastAPI (actually Starlette) will automatically include a Content-Length header. It will also include a Content-Type header, based on the media_type and appending a charset for text types.
from fastapi import FastAPI, Responseapp = FastAPI()
@app.get("/legacy/")
def get_legacy_data():
    data = """<xml version="1.0">
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")HTMLResponse¶
Takes some text or bytes and returns an HTML response, as you read above.PlainTextResponse¶
Takes some text or bytes and returns a plain text response.
from fastapi import from fastapi.responses import PlainTextResponseapp = FastAPI()
@app.get("/", response_class=PlainTextResponse)
async def main():
    return "Hello World"JSONResponse¶
Takes some data and returns an application/json encoded response.This is the default response used in FastAPI, as you read above.ORJSONResponse¶
A fast alternative JSON response using orjson, as you read above.InfoThis requires installing orjson for example with pip install orjson.UJSONResponse¶
An alternative JSON response using ujson.InfoThis requires installing ujson for example with pip install ujson.Warningujson is less careful than Python's built-in implementation in how it handles some edge-cases.
from fastapi import from fastapi.responses import UJSONResponseapp = FastAPI()
@app.get("/items/", response_class=UJSONResponse)
async def read_items():
    return [{"item_id": "Foo"}]TipIt's possible that ORJSONResponse might be a faster alternative.RedirectResponse¶
Returns an HTTP redirect. Uses a 307 status code (Temporary Redirect) by default.You can return a RedirectResponse directly:
from fastapi import from fastapi.responses import RedirectResponseapp = FastAPI()
@app.get("/typer")
async def redirect_typer():
    return RedirectResponse("https://typer.tiangolo.com")Or you can use it in the response_class parameter:
from fastapi import from fastapi.responses import RedirectResponseapp = FastAPI()
@app.get("/fastapi", response_class=RedirectResponse)
async def redirect_fastapi():
    return "https://fastapi.tiangolo.com"If you do that, then you can return the URL directly from your path operation function.In this case, the status_code used will be the default one for the RedirectResponse, which is 307.You can also use the status_code parameter combined with the response_class parameter:
from fastapi import from fastapi.responses import RedirectResponseapp = FastAPI()
@app.get("/pydantic", response_class=RedirectResponse, status_code=302)
async def redirect_pydantic():
    return "https://docs.pydantic.dev/"StreamingResponse¶
Takes an async generator or a normal generator/iterator and streams the response body.
from fastapi import from fastapi.responses import StreamingResponseapp = FastAPI()
async def fake_video_streamer():
    for i in range(10):
        yield b"some fake video bytes"
@app.get("/")
async def main():
    return StreamingResponse(fake_video_streamer())Using StreamingResponse with file-like objects¶
If you have a file-like object (e.g. the object returned by open()), you can create a generator function to iterate over that file-like object.That way, you don't have to read it all first in memory, and you can pass that generator function to the StreamingResponse, and return it.This includes many libraries to interact with cloud storage, video processing, and others.
from fastapi import from fastapi.responses import StreamingResponsesome_file_path = "large-video-file.mp4"
app = FastAPI()
@app.get("/")
def main():
    def iterfile():  # (1)
        with open(some_file_path, mode="rb") as file_like:  # (2)
            yield from file_like  # (3)    return StreamingResponse(iterfile(), media_type="video/mp4")This is the generator function. It's a "generator function" because it contains yield statements inside.
By using a with block, we make sure that the file-like object is closed after the generator function is done. So, after it finishes sending the response.
This yield from tells the function to iterate over that thing named file_like. And then, for each part iterated, yield that part as coming from this generator function (iterfile).So, it is a generator function that transfers the "generating" work to something else internally.By doing it this way, we can put it in a with block, and that way, ensure that the file-like object is closed after finishing.TipNotice that here as we are using standard open() that doesn't support async and await, we declare the path operation with normal def.FileResponse¶
Asynchronously streams a file as the response.Takes a different set of arguments to instantiate than the other response types:path - The file path to the file to stream.
headers - Any custom headers to include, as a dictionary.
media_type - A string giving the media type. If unset, the filename or path will be used to infer a media type.
filename - If set, this will be included in the response Content-Disposition.
File responses will include appropriate Content-Length, Last-Modified and ETag headers.
from fastapi import from fastapi.responses import FileResponsesome_file_path = "large-video-file.mp4"
app = FastAPI()
@app.get("/")
async def main():
    return FileResponse(some_file_path)You can also use the response_class parameter:
from fastapi import from fastapi.responses import FileResponsesome_file_path = "large-video-file.mp4"
app = FastAPI()
@app.get("/", response_class=FileResponse)
async def main():
    return some_file_pathIn this case, you can return the file path directly from your path operation function.Custom response class¶
You can create your own custom response class, inheriting from Response and using it.For example, let's say that you want to use orjson, but with some custom settings not used in the included ORJSONResponse class.Let's say you want it to return indented and formatted JSON, so you want to use the orjson option orjson.OPT_INDENT_2.You could create a CustomORJSONResponse. The main thing you have to do is create a Response.render(content) method that returns the content as bytes:
from typing import Anyimport orjson
from fastapi import FastAPI, Responseapp = FastAPI()
class CustomORJSONResponse(Response):
    media_type = "application/json"    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)
@app.get("/", response_class=CustomORJSONResponse)
async def main():
    return {"message": "Hello World"}Now instead of returning:
{"message": "Hello World"}
...this response will return:
{
  "message": "Hello World"
}
Of course, you will probably find much better ways to take advantage of this than formatting JSON. 😉Default response class¶
When creating a FastAPI class instance or an APIRouter you can specify which response class to use by default.The parameter that defines this is default_response_class.In the example below, FastAPI will use ORJSONResponse by default, in all path operations, instead of JSONResponse.
from fastapi import from fastapi.responses import ORJSONResponseapp = FastAPI(default_response_class=ORJSONResponse)
@app.get("/items/")
async def read_items():
    return [{"item_id": "Foo"}]TipYou can still override response_class in path operations as before.Additional documentation¶
You can also declare the media type and many other details in OpenAPI using responses: Additional Responses in OpenAPI.
Return a Response Directly
Additional Responses in OpenAPI
Additional Responses in OpenAPI 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Additional Response with model
Additional media types for the main response
Combining information
Combine predefined responses and custom ones
More information about OpenAPI responses
Advanced User Guide
Additional Responses in OpenAPI¶
WarningThis is a rather advanced topic.If you are starting with FastAPI, you might not need this.You can declare additional responses, with additional status codes, media types, descriptions, etc.Those additional responses will be included in the OpenAPI schema, so they will also appear in the API docs.But for those additional responses you have to make sure you return a Response like JSONResponse directly, with your status code and content.Additional Response with model¶
You can pass to your path operation decorators a parameter responses.It receives a dict: the keys are status codes for each response (like 200), and the values are other dicts with the information for each of them.Each of those response dicts can have a key model, containing a Pydantic model, just like response_model.FastAPI will take that model, generate its JSON Schema and include it in the correct place in OpenAPI.For example, to declare another response with a status code 404 and a Pydantic model Message, you can write:
from fastapi import from fastapi.responses import JSONResponse
from pydantic import BaseModel
class Item(BaseModel):
    id: str
    value: str
class Message(BaseModel):
    message: str
app = FastAPI()
@app.get("/items/{item_id}", response_model=Item, responses={404: {"model": Message}})
async def read_item(item_id: str):
    if item_id == "foo":
        return {"id": "foo", "value": "there goes my hero"}
    return JSONResponse(status_code=404, content={"message": "Item not found"})NoteKeep in mind that you have to return the JSONResponse directly.InfoThe model key is not part of OpenAPI.FastAPI will take the Pydantic model from there, generate the JSON Schema, and put it in the correct place.The correct place is:In the key content, that has as value another JSON object (dict) that contains:
A key with the media type, e.g. application/json, that contains as value another JSON object, that contains:
A key schema, that has as the value the JSON Schema from the model, here's the correct place.
FastAPI adds a reference here to the global JSON Schemas in another place in your OpenAPI instead of including it directly. This way, other applications and clients can use those JSON Schemas directly, provide better code generation tools, etc.
The generated responses in the OpenAPI for this path operation will be:
{
    "responses": {
        "404": {
            "description": "Additional Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Message"
                    }
                }
            }
        },
        "200": {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Item"
                    }
                }
            }
        },
        "422": {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/HTTPValidationError"
                    }
                }
            }
        }
    }
}
The schemas are referenced to another place inside the OpenAPI schema:
{
    "components": {
        "schemas": {
            "Message": {
                "title": "Message",
                "required": [
                    "message"
                ],
                "type": "object",
                "properties": {
                    "message": {
                        "title": "Message",
                        "type": "string"
                    }
                }
            },
            "Item": {
                "title": "Item",
                "required": [
                    "id",
                    "value"
                ],
                "type": "object",
                "properties": {
                    "id": {
                        "title": "Id",
                        "type": "string"
                    },
                    "value": {
                        "title": "Value",
                        "type": "string"
                    }
                }
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": [
                    "loc",
                    "msg",
                    "type"
                ],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "msg": {
                        "title": "Message",
                        "type": "string"
                    },
                    "type": {
                        "title": "Error Type",
                        "type": "string"
                    }
                }
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/ValidationError"
                        }
                    }
                }
            }
        }
    }
}
Additional media types for the main response¶
You can use this same responses parameter to add different media types for the same main response.For example, you can add an additional media type of image/png, declaring that your path operation can return a JSON object (with media type application/json) or a PNG image:
from typing import Unionfrom fastapi import from fastapi.responses import FileResponse
from pydantic import BaseModel
class Item(BaseModel):
    id: str
    value: str
app = FastAPI()
@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Return the JSON item or an image.",
        }
    },
)
async def read_item(item_id: str, img: Union[bool, None] = None):
    if img:
        return FileResponse("image.png", media_type="image/png")
    else:
        return {"id": "foo", "value": "there goes my hero"}NoteNotice that you have to return the image using a FileResponse directly.InfoUnless you specify a different media type explicitly in your responses parameter, FastAPI will assume the response has the same media type as the main response class (default application/json).But if you have specified a custom response class with None as its media type, FastAPI will use application/json for any additional response that has an associated model.Combining information¶
You can also combine response information from multiple places, including the response_model, status_code, and responses parameters.You can declare a response_model, using the default status code 200 (or a custom one if you need), and then declare additional information for that same response in responses, directly in the OpenAPI schema.FastAPI will keep the additional information from responses, and combine it with the JSON Schema from your model.For example, you can declare a response with a status code 404 that uses a Pydantic model and has a custom description.And a response with a status code 200 that uses your response_model, but includes a custom example:
from fastapi import from fastapi.responses import JSONResponse
from pydantic import BaseModel
class Item(BaseModel):
    id: str
    value: str
class Message(BaseModel):
    message: str
app = FastAPI()
@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {"id": "bar", "value": "The bar tenders"}
                }
            },
        },
    },
)
async def read_item(item_id: str):
    if item_id == "foo":
        return {"id": "foo", "value": "there goes my hero"}
    else:
        return JSONResponse(status_code=404, content={"message": "Item not found"})It will all be combined and included in your OpenAPI, and shown in the API docs:Combine predefined responses and custom ones¶
You might want to have some predefined responses that apply to many path operations, but you want to combine them with custom responses needed by each path operation.For those cases, you can use the Python technique of "unpacking" a dict with **dict_to_unpack:
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
Here, new_dict will contain all the key-value pairs from old_dict plus the new key-value pair:
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
You can use that technique to reuse some predefined responses in your path operations and combine them with additional custom ones.For example:
from typing import Unionfrom fastapi import from fastapi.responses import FileResponse
from pydantic import BaseModel
class Item(BaseModel):
    id: str
    value: str
responses = {
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}
app = FastAPI()
@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={**responses, 200: {"content": {"image/png": {}}}},
)
async def read_item(item_id: str, img: Union[bool, None] = None):
    if img:
        return FileResponse("image.png", media_type="image/png")
    else:
        return {"id": "foo", "value": "there goes my hero"}More information about OpenAPI responses¶
To see what exactly you can include in the responses, you can check these sections in the OpenAPI specification:OpenAPI Responses Object, it includes the Response Object.
OpenAPI Response Object, you can include anything from this directly in each response inside your responses parameter. Including description, headers, content (inside of this is that you declare different media types and JSON Schemas), and links.Custom Response - HTML, Stream, File, others
Response CookiesResponse Cookies 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Use a Response parameter
Return a Response directly
More info
Advanced User Guide
Response Cookies¶
Use a Response parameter¶
You can declare a parameter of type Response in your path operation function.And then you can set cookies in that temporal response object.
from fastapi import FastAPI, Responseapp = FastAPI()
@app.post("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}And then you can return any object you need, as you normally would (a dict, a database model, etc).And if you declared a response_model, it will still be used to filter and convert the object you returned.FastAPI will use that temporal response to extract the cookies (also headers and status code), and will put them in the final response that contains the value you returned, filtered by any response_model.You can also declare the Response parameter in dependencies, and set cookies (and headers) in them.Return a Response directly¶
You can also create cookies when returning a Response directly in your code.To do that, you can create a response as described in Return a Response Directly.Then set Cookies in it, and then return it:
from fastapi import from fastapi.responses import JSONResponseapp = FastAPI()
@app.post("/cookie/")
def create_cookie():
    content = {"message": "Come to the dark side, we have cookies"}
    response = JSONResponse(content=content)
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return responseTipKeep in mind that if you return a response directly instead of using the Response parameter, FastAPI will return it directly.So, you will have to make sure your data is of the correct type. E.g. it is compatible with JSON, if you are returning a JSONResponse.And also that you are not sending any data that should have been filtered by a response_model.More info¶
Technical DetailsYou could also use from starlette.responses import Response or from starlette.responses import JSONResponse.FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette.And as the Response can be used frequently to set headers and cookies, FastAPI also provides it at fastapi.Response.To see all the available parameters and options, check the documentation in Starlette.
Additional Responses in OpenAPI
Response Headers
Response Headers 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Use a Response parameter
Return a Response directly
Custom Headers
Advanced User Guide
Response Headers¶
Use a Response parameter¶
You can declare a parameter of type Response in your path operation function (as you can do for cookies).And then you can set headers in that temporal response object.
from fastapi import FastAPI, Responseapp = FastAPI()
@app.get("/headers-and-object/")
def get_headers(response: Response):
    response.headers["X-Cat-Dog"] = "alone in the world"
    return {"message": "Hello World"}And then you can return any object you need, as you normally would (a dict, a database model, etc).And if you declared a response_model, it will still be used to filter and convert the object you returned.FastAPI will use that temporal response to extract the headers (also cookies and status code), and will put them in the final response that contains the value you returned, filtered by any response_model.You can also declare the Response parameter in dependencies, and set headers (and cookies) in them.Return a Response directly¶
You can also add headers when you return a Response directly.Create a response as described in Return a Response Directly and pass the headers as an additional parameter:
from fastapi import from fastapi.responses import JSONResponseapp = FastAPI()
@app.get("/headers/")
def get_headers():
    content = {"message": "Hello World"}
    headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)Technical DetailsYou could also use from starlette.responses import Response or from starlette.responses import JSONResponse.FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette.And as the Response can be used frequently to set headers and cookies, FastAPI also provides it at fastapi.Response.Custom Headers¶
Keep in mind that custom proprietary headers can be added using the 'X-' prefix.But if you have custom headers that you want a client in a browser to be able to see, you need to add them to your CORS configurations (read more in CORS (Cross-Origin Resource Sharing)), using the parameter expose_headers documented in Starlette's CORS docs.
Response Cookies
Response - Change Status Code
Response - Change Status Code 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Use case
Use a Response parameter
Advanced User Guide
Response - Change Status Code¶
You probably read before that you can set a default Response Status Code.But in some cases you need to return a different status code than the default.Use case¶
For example, imagine that you want to return an HTTP status code of "OK" 200 by default.But if the data didn't exist, you want to create it, and return an HTTP status code of "CREATED" 201.But you still want to be able to filter and convert the data you return with a response_model.For those cases, you can use a Response parameter.Use a Response parameter¶
You can declare a parameter of type Response in your path operation function (as you can do for cookies and headers).And then you can set the status_code in that temporal response object.
from fastapi import FastAPI, Response, statusapp = FastAPI()tasks = {"foo": "Listen to the Bar Fighters"}
@app.put("/get-or-create-task/{task_id}", status_code=200)
def get_or_create_task(task_id: str, response: Response):
    if task_id not in tasks:
        tasks[task_id] = "This didn't exist before"
        response.status_code = status.HTTP_201_CREATED
    return tasks[task_id]And then you can return any object you need, as you normally would (a dict, a database model, etc).And if you declared a response_model, it will still be used to filter and convert the object you returned.FastAPI will use that temporal response to extract the status code (also cookies and headers), and will put them in the final response that contains the value you returned, filtered by any response_model.You can also declare the Response parameter in dependencies, and set the status code in them. But keep in mind that the last one to be set will win.
Response Headers
Advanced Dependencies
Advanced Dependencies 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Parameterized dependencies
A "callable" instance
Parameterize the instance
Create an instance
Use the instance as a dependency
Advanced User Guide
Advanced Dependencies¶
Parameterized dependencies¶
All the dependencies we have seen are a fixed function or class.But there could be cases where you want to be able to set parameters on the dependency, without having to declare many different functions or classes.Let's imagine that we want to have a dependency that checks if the query parameter q contains some fixed content.But we want to be able to parameterize that fixed content.A "callable" instance¶
In Python there's a way to make an instance of a class a "callable".Not the class itself (which is already a callable), but an instance of that class.To do that, we declare a method __call__:
from typing import Annotatedfrom fastapi import Depends, 
app = FastAPI()
class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False
checker = FixedContentQueryChecker("bar")
@app.get("/query-checker/")
async def read_query_check(fixed_content_included: Annotated[bool, Depends(checker)]):
    return {"fixed_content_in_query": fixed_content_included}🤓 Other versions and variants
In this case, this __call__ is what FastAPI will use to check for additional parameters and sub-dependencies, and this is what will be called to pass a value to the parameter in your path operation function later.Parameterize the instance¶
And now, we can use __init__ to declare the parameters of the instance that we can use to "parameterize" the dependency:
from typing import Annotatedfrom fastapi import Depends, 
app = FastAPI()
class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False
checker = FixedContentQueryChecker("bar")
@app.get("/query-checker/")
async def read_query_check(fixed_content_included: Annotated[bool, Depends(checker)]):
    return {"fixed_content_in_query": fixed_content_included}🤓 Other versions and variants
In this case, FastAPI won't ever touch or care about __init__, we will use it directly in our code.Create an instance¶
We could create an instance of this class with:
from typing import Annotatedfrom fastapi import Depends, 
app = FastAPI()
class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False
checker = FixedContentQueryChecker("bar")
@app.get("/query-checker/")
async def read_query_check(fixed_content_included: Annotated[bool, Depends(checker)]):
    return {"fixed_content_in_query": fixed_content_included}🤓 Other versions and variants
And that way we are able to "parameterize" our dependency, that now has "bar" inside of it, as the attribute checker.fixed_content.Use the instance as a dependency¶
Then, we could use this checker in a Depends(checker), instead of Depends(FixedContentQueryChecker), because the dependency is the instance, checker, not the class itself.And when solving the dependency, FastAPI will call this checker like:
checker(q="somequery")
...and pass whatever that returns as the value of the dependency in our path operation function as the parameter fixed_content_included:
from typing import Annotatedfrom fastapi import Depends, 
app = FastAPI()
class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False
checker = FixedContentQueryChecker("bar")
@app.get("/query-checker/")
async def read_query_check(fixed_content_included: Annotated[bool, Depends(checker)]):
    return {"fixed_content_in_query": fixed_content_included}🤓 Other versions and variants
TipAll this might seem contrived. And it might not be very clear how is it useful yet.These examples are intentionally simple, but show how it all works.In the chapters about security, there are utility functions that are implemented in this same way.If you understood all this, you already know how those utility tools for security work underneath.
Response - Change Status Code
Advanced Security
Advanced Security 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
OAuth2 scopes
HTTP Basic Auth
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Additional Read the Tutorial first
Advanced User Guide
Advanced Security
Advanced Security¶
Additional Features¶
There are some extra features to handle security apart from the ones covered in the Tutorial - User Guide: Security.TipThe next sections are not necessarily "advanced".And it's possible that for your use case, the solution is in one of them.Read the Tutorial first¶
The next sections assume you already read the main Tutorial - User Guide: Security.They are all based on the same concepts, but allow some extra functionalities.
Advanced Dependencies
OAuth2 scopes
OAuth2 scopes 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
OAuth2 scopes
HTTP Basic Auth
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
OAuth2 scopes and OpenAPI
Global view
OAuth2 Security scheme
JWT token with scopes
Declare scopes in path operations and dependencies
Use SecurityScopes
Use the scopes
Verify the username and data shape
Verify the scopes
Dependency tree and scopes
More details about SecurityScopes
Check it
About third party integrations
Security in decorator dependencies
Advanced User Guide
Advanced Security
OAuth2 scopes¶
You can use OAuth2 scopes directly with FastAPI, they are integrated to work seamlessly.This would allow you to have a more fine-grained permission system, following the OAuth2 standard, integrated into your OpenAPI application (and the API docs).OAuth2 with scopes is the mechanism used by many big authentication providers, like Facebook, Google, GitHub, Microsoft, Twitter, etc. They use it to provide specific permissions to users and applications.Every time you "log in with" Facebook, Google, GitHub, Microsoft, Twitter, that application is using OAuth2 with scopes.In this section you will see how to manage authentication and authorization with the same OAuth2 with scopes in your FastAPI application.WarningThis is a more or less advanced section. If you are just starting, you can skip it.You don't necessarily need OAuth2 scopes, and you can handle authentication and authorization however you want.But OAuth2 with scopes can be nicely integrated into your API (with OpenAPI) and your API docs.Nevertheless, you still enforce those scopes, or any other security/authorization requirement, however you need, in your code.In many cases, OAuth2 with scopes can be an overkill.But if you know you need it, or you are curious, keep reading.OAuth2 scopes and OpenAPI¶
The OAuth2 specification defines "scopes" as a list of strings separated by spaces.The content of each of these strings can have any format, but should not contain spaces.These scopes represent "permissions".In OpenAPI (e.g. the API docs), you can define "security schemes".When one of these security schemes uses OAuth2, you can also declare and use scopes.Each "scope" is just a string (without spaces).They are normally used to declare specific security permissions, for example:users:read or users:write are common examples.
instagram_basic is used by Facebook / Instagram.
https://www.googleapis.com/auth/drive is used by Google.
InfoIn OAuth2 a "scope" is just a string that declares a specific permission required.It doesn't matter if it has other characters like : or if it is a URL.Those details are implementation specific.For OAuth2 they are just strings.Global view¶
First, let's quickly see the parts that change from the examples in the main Tutorial - User Guide for OAuth2 with Password (and hashing), Bearer with JWT tokens. Now using OAuth2 scopes:
from datetime import datetime, timedelta, timezone
from typing import Annotatedimport jwt
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
        "disabled": True,
    },
}
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
class UserInDB(User):
    hashed_password: str
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)app = FastAPI()
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user
async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["items"])],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
@app.get("/status/")
async def read_system_status(current_user: Annotated[User, Depends(get_current_user)]):
    return {"status": "ok"}🤓 Other versions and variants
Now let's review those changes step by step.OAuth2 Security scheme¶
The first change is that now we are declaring the OAuth2 security scheme with two available scopes, me and items.The scopes parameter receives a dict with each scope as a key and the description as the value:
from datetime import datetime, timedelta, timezone
from typing import Annotatedimport jwt
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
        "disabled": True,
    },
}
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
class UserInDB(User):
    hashed_password: str
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)app = FastAPI()
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user
async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["items"])],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
@app.get("/status/")
async def read_system_status(current_user: Annotated[User, Depends(get_current_user)]):
    return {"status": "ok"}🤓 Other versions and variants
Because we are now declaring those scopes, they will show up in the API docs when you log-in/authorize.And you will be able to select which scopes you want to give access to: me and items.This is the same mechanism used when you give permissions while logging in with Facebook, Google, GitHub, etc:JWT token with scopes¶
Now, modify the token path operation to return the scopes requested.We are still using the same OAuth2PasswordRequestForm. It includes a property scopes with a list of str, with each scope it received in the request.And we return the scopes as part of the JWT token.DangerFor simplicity, here we are just adding the scopes received directly to the token.But in your application, for security, you should make sure you only add the scopes that the user is actually able to have, or the ones you have predefined.
from datetime import datetime, timedelta, timezone
from typing import Annotatedimport jwt
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
        "disabled": True,
    },
}
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
class UserInDB(User):
    hashed_password: str
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)app = FastAPI()
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user
async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["items"])],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
@app.get("/status/")
async def read_system_status(current_user: Annotated[User, Depends(get_current_user)]):
    return {"status": "ok"}🤓 Other versions and variants
Declare scopes in path operations and dependencies¶
Now we declare that the path operation for /users/me/items/ requires the scope items.For this, we import and use Security from fastapi.You can use Security to declare dependencies (just like Depends), but Security also receives a parameter scopes with a list of scopes (strings).In this case, we pass a dependency function get_current_active_user to Security (the same way we would do with Depends).But we also pass a list of scopes, in this case with just one scope: items (it could have more).And the dependency function get_current_active_user can also declare sub-dependencies, not only with Depends but also with Security. Declaring its own sub-dependency function (get_current_user), and more scope requirements.In this case, it requires the scope me (it could require more than one scope).NoteYou don't necessarily need to add different scopes in different places.We are doing it here to demonstrate how FastAPI handles scopes declared at different levels.
from datetime import datetime, timedelta, timezone
from typing import Annotatedimport jwt
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
        "disabled": True,
    },
}
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
class UserInDB(User):
    hashed_password: str
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)app = FastAPI()
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user
async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["items"])],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
@app.get("/status/")
async def read_system_status(current_user: Annotated[User, Depends(get_current_user)]):
    return {"status": "ok"}🤓 Other versions and variants
Technical DetailsSecurity is actually a subclass of Depends, and it has just one extra parameter that we'll see later.But by using Security instead of Depends, FastAPI will know that it can declare security scopes, use them internally, and document the API with OpenAPI.But when you import Query, Path, Depends, Security and others from fastapi, those are actually functions that return special classes.Use SecurityScopes¶
Now update the dependency get_current_user.This is the one used by the dependencies above.Here's where we are using the same OAuth2 scheme we created before, declaring it as a dependency: oauth2_scheme.Because this dependency function doesn't have any scope requirements itself, we can use Depends with oauth2_scheme, we don't have to use Security when we don't need to specify security scopes.We also declare a special parameter of type SecurityScopes, imported from fastapi.security.This SecurityScopes class is similar to Request (Request was used to get the request object directly).
from datetime import datetime, timedelta, timezone
from typing import Annotatedimport jwt
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
        "disabled": True,
    },
}
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
class UserInDB(User):
    hashed_password: str
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)app = FastAPI()
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user
async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["items"])],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
@app.get("/status/")
async def read_system_status(current_user: Annotated[User, Depends(get_current_user)]):
    return {"status": "ok"}🤓 Other versions and variants
Use the scopes¶
The parameter security_scopes will be of type SecurityScopes.It will have a property scopes with a list containing all the scopes required by itself and all the dependencies that use this as a sub-dependency. That means, all the "dependants"... this might sound confusing, it is explained again later below.The security_scopes object (of class SecurityScopes) also provides a scope_str attribute with a single string, containing those scopes separated by spaces (we are going to use it).We create an HTTPException that we can reuse (raise) later at several points.In this exception, we include the scopes required (if any) as a string separated by spaces (using scope_str). We put that string containing the scopes in the WWW-Authenticate header (this is part of the spec).
from datetime import datetime, timedelta, timezone
from typing import Annotatedimport jwt
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
        "disabled": True,
    },
}
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
class UserInDB(User):
    hashed_password: str
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)app = FastAPI()
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user
async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["items"])],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
@app.get("/status/")
async def read_system_status(current_user: Annotated[User, Depends(get_current_user)]):
    return {"status": "ok"}🤓 Other versions and variants
Verify the username and data shape¶
We verify that we get a username, and extract the scopes.And then we validate that data with the Pydantic model (catching the ValidationError exception), and if we get an error reading the JWT token or validating the data with Pydantic, we raise the HTTPException we created before.For that, we update the Pydantic model TokenData with a new property scopes.By validating the data with Pydantic we can make sure that we have, for example, exactly a list of str with the scopes and a str with the username.Instead of, for example, a dict, or something else, as it could break the application at some point later, making it a security risk.We also verify that we have a user with that username, and if not, we raise that same exception we created before.
from datetime import datetime, timedelta, timezone
from typing import Annotatedimport jwt
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
        "disabled": True,
    },
}
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
class UserInDB(User):
    hashed_password: str
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)app = FastAPI()
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user
async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["items"])],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
@app.get("/status/")
async def read_system_status(current_user: Annotated[User, Depends(get_current_user)]):
    return {"status": "ok"}🤓 Other versions and variants
Verify the scopes¶
We now verify that all the scopes required, by this dependency and all the dependants (including path operations), are included in the scopes provided in the token received, otherwise raise an HTTPException.For this, we use security_scopes.scopes, that contains a list with all these scopes as str.
from datetime import datetime, timedelta, timezone
from typing import Annotatedimport jwt
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
        "disabled": True,
    },
}
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
class UserInDB(User):
    hashed_password: str
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)app = FastAPI()
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user
async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["items"])],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
@app.get("/status/")
async def read_system_status(current_user: Annotated[User, Depends(get_current_user)]):
    return {"status": "ok"}🤓 Other versions and variants
Dependency tree and scopes¶
Let's review again this dependency tree and the scopes.As the get_current_active_user dependency has as a sub-dependency on get_current_user, the scope "me" declared at get_current_active_user will be included in the list of required scopes in the security_scopes.scopes passed to get_current_user.The path operation itself also declares a scope, "items", so this will also be in the list of security_scopes.scopes passed to get_current_user.Here's how the hierarchy of dependencies and scopes looks like:The path operation read_own_items has:
Required scopes ["items"] with the dependency:
get_current_active_user:
The dependency function get_current_active_user has:
Required scopes ["me"] with the dependency:
get_current_user:
The dependency function get_current_user has:
No scopes required by itself.
A dependency using oauth2_scheme.
A security_scopes parameter of type SecurityScopes:
This security_scopes parameter has a property scopes with a list containing all these scopes declared above, so:
security_scopes.scopes will contain ["me", "items"] for the path operation read_own_items.
security_scopes.scopes will contain ["me"] for the path operation read_users_me, because it is declared in the dependency get_current_active_user.
security_scopes.scopes will contain [] (nothing) for the path operation read_system_status, because it didn't declare any Security with scopes, and its dependency, get_current_user, doesn't declare any scopes either.
TipThe important and "magic" thing here is that get_current_user will have a different list of scopes to check for each path operation.All depending on the scopes declared in each path operation and each dependency in the dependency tree for that specific path operation.More details about SecurityScopes¶
You can use SecurityScopes at any point, and in multiple places, it doesn't have to be at the "root" dependency.It will always have the security scopes declared in the current Security dependencies and all the dependants for that specific path operation and that specific dependency tree.Because the SecurityScopes will have all the scopes declared by dependants, you can use it to verify that a token has the required scopes in a central dependency function, and then declare different scope requirements in different path operations.They will be checked independently for each path operation.Check it¶
If you open the API docs, you can authenticate and specify which scopes you want to authorize.If you don't select any scope, you will be "authenticated", but when you try to access /users/me/ or /users/me/items/ you will get an error saying that you don't have enough permissions. You will still be able to access /status/.And if you select the scope me but not the scope items, you will be able to access /users/me/ but not /users/me/items/.That's what would happen to a third party application that tried to access one of these path operations with a token provided by a user, depending on how many permissions the user gave the application.About third party integrations¶
In this example we are using the OAuth2 "password" flow.This is appropriate when we are logging in to our own application, probably with our own frontend.Because we can trust it to receive the username and password, as we control it.But if you are building an OAuth2 application that others would connect to (i.e., if you are building an authentication provider equivalent to Facebook, Google, GitHub, etc.) you should use one of the other flows.The most common is the implicit flow.The most secure is the code flow, but it's more complex to implement as it requires more steps. As it is more complex, many providers end up suggesting the implicit flow.NoteIt's common that each authentication provider names their flows in a different way, to make it part of their brand.But in the end, they are implementing the same OAuth2 standard.FastAPI includes utilities for all these OAuth2 authentication flows in fastapi.security.oauth2.Security in decorator dependencies¶
The same way you can define a list of Depends in the decorator's dependencies parameter (as explained in Dependencies in path operation decorators), you could also use Security with scopes there.
Advanced Security
HTTP Basic Auth
HTTP Basic Auth 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
OAuth2 scopes
HTTP Basic Auth
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Simple HTTP Basic Auth
Check the username
Timing Attacks
The time to answer helps the attackers
A "professional" attack
Fix it with secrets.compare_digest()
Return the error
Advanced User Guide
Advanced Security
HTTP Basic Auth¶
For the simplest cases, you can use HTTP Basic Auth.In HTTP Basic Auth, the application expects a header that contains a username and a password.If it doesn't receive it, it returns an HTTP 401 "Unauthorized" error.And returns a header WWW-Authenticate with a value of Basic, and an optional realm parameter.That tells the browser to show the integrated prompt for a username and password.Then, when you type that username and password, the browser sends them in the header automatically.Simple HTTP Basic Auth¶
Import HTTPBasic and HTTPBasicCredentials.
Create a "security scheme" using HTTPBasic.
Use that security with a dependency in your path operation.
It returns an object of type HTTPBasicCredentials:
It contains the username and password sent.from typing import Annotatedfrom fastapi import Depends, from fastapi.security import HTTPBasic, HTTPBasicCredentialsapp = FastAPI()security = HTTPBasic()
@app.get("/users/me")
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {"username": credentials.username, "password": credentials.password}🤓 Other versions and variants
When you try to open the URL for the first time (or click the "Execute" button in the docs) the browser will ask you for your username and password:Check the username¶
Here's a more complete example.Use a dependency to check if the username and password are correct.For this, use the Python standard module secrets to check the username and password.secrets.compare_digest() needs to take bytes or a str that only contains ASCII characters (the ones in English), this means it wouldn't work with characters like á, as in Sebastián.To handle that, we first convert the username and password to bytes encoding them with UTF-8.Then we can use secrets.compare_digest() to ensure that credentials.username is "stanleyjobson", and that credentials.password is "swordfish".
import secrets
from typing import Annotatedfrom fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentialsapp = FastAPI()security = HTTPBasic()
def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"stanleyjobson"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"swordfish"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
@app.get("/users/me")
def read_current_user(username: Annotated[str, Depends(get_current_username)]):
    return {"username": username}🤓 Other versions and variants
This would be similar to:
if not (credentials.username == "stanleyjobson") or not (credentials.password == "swordfish"):
    # Return some error
    ...
But by using the secrets.compare_digest() it will be secure against a type of attacks called "timing attacks".Timing Attacks¶
But what's a "timing attack"Let's imagine some attackers are trying to guess the username and password.And they send a request with a username johndoe and a password love123.Then the Python code in your application would be equivalent to something like:
if "johndoe" == "stanleyjobson" and "love123" == "swordfish":
    ...
But right at the moment Python compares the first j in johndoe to the first s in stanleyjobson, it will return False, because it already knows that those two strings are not the same, thinking that "there's no need to waste more computation comparing the rest of the letters". And your application will say "Incorrect username or password".But then the attackers try with username stanleyjobsox and password love123.And your application code does something like:
if "stanleyjobsox" == "stanleyjobson" and "love123" == "swordfish":
    ...
Python will have to compare the whole stanleyjobso in both stanleyjobsox and stanleyjobson before realizing that both strings are not the same. So it will take some extra microseconds to reply back "Incorrect username or password".The time to answer helps the attackers¶
At that point, by noticing that the server took some microseconds longer to send the "Incorrect username or password" response, the attackers will know that they got something right, some of the initial letters were right.And then they can try again knowing that it's probably something more similar to stanleyjobsox than to johndoe.A "professional" attack¶
Of course, the attackers would not try all this by hand, they would write a program to do it, possibly with thousands or millions of tests per second. And they would get just one extra correct letter at a time.But doing that, in some minutes or hours the attackers would have guessed the correct username and password, with the "help" of our application, just using the time taken to answer.Fix it with secrets.compare_digest()¶
But in our code we are actually using secrets.compare_digest().In short, it will take the same time to compare stanleyjobsox to stanleyjobson than it takes to compare johndoe to stanleyjobson. And the same for the password.That way, using secrets.compare_digest() in your application code, it will be safe against this whole range of security attacks.Return the error¶
After detecting that the credentials are incorrect, return an HTTPException with a status code 401 (the same returned when no credentials are provided) and add the header WWW-Authenticate to make the browser show the login prompt again:
import secrets
from typing import Annotatedfrom fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentialsapp = FastAPI()security = HTTPBasic()
def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"stanleyjobson"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"swordfish"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
@app.get("/users/me")
def read_current_user(username: Annotated[str, Depends(get_current_username)]):
    return {"username": username}🤓 Other versions and variantsOAuth2 scopes
Using the Request Directly
Using the Request Directly 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Details about the Request object
Use the Request object directly
Request documentation
Advanced User Guide
Using the Request Directly¶
Up to now, you have been declaring the parts of the request that you need with their types.Taking data from:The path as parameters.
Headers.
Cookies.
etc.
And by doing so, FastAPI is validating that data, converting it and generating documentation for your API automatically.But there are situations where you might need to access the Request object directly.Details about the Request object¶
As FastAPI is actually Starlette underneath, with a layer of several tools on top, you can use Starlette's Request object directly when you need to.It would also mean that if you get data from the Request object directly (for example, read the body) it won't be validated, converted or documented (with OpenAPI, for the automatic API user interface) by FastAPI.Although any other parameter declared normally (for example, the body with a Pydantic model) would still be validated, converted, annotated, etc.But there are specific cases where it's useful to get the Request object.Use the Request object directly¶
Let's imagine you want to get the client's IP address/host inside of your path operation function.For that you need to access the request directly.
from fastapi import FastAPI, Requestapp = FastAPI()
@app.get("/items/{item_id}")
def read_root(item_id: str, request: Request):
    client_host = request.client.host
    return {"client_host": client_host, "item_id": item_id}By declaring a path operation function parameter with the type being the Request FastAPI will know to pass the Request in that parameter.TipNote that in this case, we are declaring a path parameter beside the request parameter.So, the path parameter will be extracted, validated, converted to the specified type and annotated with OpenAPI.The same way, you can declare any other parameter as normally, and additionally, get the Request too.Request documentation¶
You can read more details about the Request object in the official Starlette documentation site.Technical DetailsYou could also use from starlette.requests import Request.FastAPI provides it directly just as a convenience for you, the developer. But it comes directly from Starlette.
HTTP Basic Auth
Using Dataclasses
Using Dataclasses 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Dataclasses in response_model
Dataclasses in Nested Data Structures
Learn More
Version
Advanced User Guide
Using Dataclasses¶
FastAPI is built on top of Pydantic, and I have been showing you how to use Pydantic models to declare requests and responses.But FastAPI also supports using dataclasses the same way:
from dataclasses import dataclass
from typing import Unionfrom fastapi import @dataclass
class Item:
    name: str
    price: float
    description: Union[str, None] = None
    tax: Union[float, None] = None
app = FastAPI()
@app.post("/items/")
async def create_item(item: Item):
    return itemThis is still supported thanks to Pydantic, as it has internal support for dataclasses.So, even with the code above that doesn't use Pydantic explicitly, FastAPI is using Pydantic to convert those standard dataclasses to Pydantic's own flavor of dataclasses.And of course, it supports the same:data validation
data serialization
data documentation, etc.
This works the same way as with Pydantic models. And it is actually achieved in the same way underneath, using Pydantic.InfoKeep in mind that dataclasses can't do everything Pydantic models can do.So, you might still need to use Pydantic models.But if you have a bunch of dataclasses laying around, this is a nice trick to use them to power a web API using FastAPI. 🤓Dataclasses in response_model¶
You can also use dataclasses in the response_model parameter:
from dataclasses import dataclass, field
from typing import List, Unionfrom fastapi import @dataclass
class Item:
    name: str
    price: float
    tags: List[str] = field(default_factory=list)
    description: Union[str, None] = None
    tax: Union[float, None] = None
app = FastAPI()
@app.get("/items/next", response_model=Item)
async def read_next_item():
    return {
        "name": "Island In The Moon",
        "price": 12.99,
        "description": "A place to be playin' and havin' fun",
        "tags": ["breater"],
    }The dataclass will be automatically converted to a Pydantic dataclass.This way, its schema will show up in the API docs user interface:Dataclasses in Nested Data Structures¶
You can also combine dataclasses with other type annotations to make nested data structures.In some cases, you might still have to use Pydantic's version of dataclasses. For example, if you have errors with the automatically generated API documentation.In that case, you can simply swap the standard dataclasses with pydantic.dataclasses, which is a drop-in replacement:
from dataclasses import field  # (1)
from typing import List, Unionfrom fastapi import from pydantic.dataclasses import dataclass  # (2)
@dataclass
class Item:
    name: str
    description: Union[str, None] = None
@dataclass
class Author:
    name: str
    items: List[Item] = field(default_factory=list)  # (3)
app = FastAPI()
@app.post("/authors/{author_id}/items/", response_model=Author)  # (4)
async def create_author_items(author_id: str, items: List[Item]):  # (5)
    return {"name": author_id, "items": items}  # (6)
@app.get("/authors/", response_model=List[Author])  # (7)
def get_authors():  # (8)
    return [  # (9)
        {
            "name": "Breaters",
            "items": [
                {
                    "name": "Island In The Moon",
                    "description": "A place to be playin' and havin' fun",
                },
                {"name": "Holy Buddies"},
            ],
        },
        {
            "name": "System of an Up",
            "items": [
                {
                    "name": "Salt",
                    "description": "The kombucha mushroom people's favorite",
                },
                {"name": "Pad Thai"},
                {
                    "name": "Lonely Night",
                    "description": "The mostests lonliest nightiest of allest",
                },
            ],
        },
    ]We still import field from standard dataclasses.pydantic.dataclasses is a drop-in replacement for dataclasses.The Author dataclass includes a list of Item dataclasses.The Author dataclass is used as the response_model parameter.You can use other standard type annotations with dataclasses as the request body.In this case, it's a list of Item dataclasses.Here we are returning a dictionary that contains items which is a list of dataclasses.FastAPI is still capable of serializing the data to JSON.Here the response_model is using a type annotation of a list of Author dataclasses.Again, you can combine dataclasses with standard type annotations.Notice that this path operation function uses regular def instead of async def.As always, in FastAPI you can combine def and async def as needed.If you need a refresher about when to use which, check out the section "In a hurry" in the docs about async and await.This path operation function is not returning dataclasses (although it could), but a list of dictionaries with internal data.FastAPI will use the response_model parameter (that includes dataclasses) to convert the response.You can combine dataclasses with other type annotations in many different combinations to form complex data structures.Check the in-code annotation tips above to see more specific details.Learn More¶
You can also combine dataclasses with other Pydantic models, inherit from them, include them in your own models, etc.To learn more, check the Pydantic docs about dataclasses.Version¶
This is available since FastAPI version 0.67.0. 🔖
Using the Request Directly
Advanced Middleware
Advanced Middleware 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Adding ASGI middlewares
Integrated middlewares
HTTPSRedirectMiddleware
TrustedHostMiddleware
GZipMiddleware
Other middlewares
Advanced User Guide
Advanced Middleware¶
In the main tutorial you read how to add Custom Middleware to your application.And then you also read how to handle CORS with the CORSMiddleware.In this section we'll see how to use other middlewares.Adding ASGI middlewares¶
As FastAPI is based on Starlette and implements the ASGI specification, you can use any ASGI middleware.A middleware doesn't have to be made for FastAPI or Starlette to work, as long as it follows the ASGI spec.In general, ASGI middlewares are classes that expect to receive an ASGI app as the first argument.So, in the documentation for third-party ASGI middlewares they will probably tell you to do something like:
from unicorn import UnicornMiddlewareapp = SomeASGIApp()new_app = UnicornMiddleware(app, some_config="rainbow")
But FastAPI (actually Starlette) provides a simpler way to do it that makes sure that the internal middlewares handle server errors and custom exception handlers work properly.For that, you use app.add_middleware() (as in the example for CORS).
from fastapi import from unicorn import UnicornMiddlewareapp = FastAPI()app.add_middleware(UnicornMiddleware, some_config="rainbow")
app.add_middleware() receives a middleware class as the first argument and any additional arguments to be passed to the middleware.Integrated middlewares¶
FastAPI includes several middlewares for common use cases, we'll see next how to use them.Technical DetailsFor the next examples, you could also use from starlette.middleware.something import SomethingMiddleware.FastAPI provides several middlewares in fastapi.middleware just as a convenience for you, the developer. But most of the available middlewares come directly from Starlette.HTTPSRedirectMiddleware¶
Enforces that all incoming requests must either be https or wss.Any incoming request to http or ws will be redirected to the secure scheme instead.
from fastapi import from fastapi.middleware.httpsredirect import HTTPSRedirectMiddlewareapp = FastAPI()app.add_middleware(HTTPSRedirectMiddleware)
@app.get("/")
async def main():
    return {"message": "Hello World"}TrustedHostMiddleware¶
Enforces that all incoming requests have a correctly set Host header, in order to guard against HTTP Host Header attacks.
from fastapi import from fastapi.middleware.trustedhost import TrustedHostMiddlewareapp = FastAPI()app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"]
)
@app.get("/")
async def main():
    return {"message": "Hello World"}The following arguments are supported:allowed_hosts - A list of domain names that should be allowed as hostnames. Wildcard domains such as *.example.com are supported for matching subdomains. To allow any hostname either use allowed_hosts=["*"] or omit the middleware.
If an incoming request does not validate correctly then a 400 response will be sent.GZipMiddleware¶
Handles GZip responses for any request that includes "gzip" in the Accept-Encoding header.The middleware will handle both standard and streaming responses.
from fastapi import from fastapi.middleware.gzip import GZipMiddlewareapp = FastAPI()app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)
@app.get("/")
async def main():
    return "somebigcontent"The following arguments are supported:minimum_size - Do not GZip responses that are smaller than this minimum size in bytes. Defaults to 500.
compresslevel - Used during GZip compression. It is an integer ranging from 1 to 9. Defaults to 9. Lower value results in faster compression but larger file sizes, while higher value results in slower compression but smaller file sizes.
Other middlewares¶
There are many other ASGI middlewares.For example:Uvicorn's ProxyHeadersMiddleware
MessagePack
To see other available middlewares check Starlette's Middleware docs and the ASGI Awesome List.
Using Dataclasses
Sub Applications - Mounts
Sub Applications - Mounts 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Mounting a FastAPI application
Top-level application
Sub-application
Mount the sub-application
Check the automatic API docs
Technical Details: root_path
Advanced User Guide
Sub Applications - Mounts¶
If you need to have two independent FastAPI applications, with their own independent OpenAPI and their own docs UIs, you can have a main app and "mount" one (or more) sub-application(s).Mounting a FastAPI application¶
"Mounting" means adding a completely "independent" application in a specific path, that then takes care of handling everything under that path, with the path operations declared in that sub-application.Top-level application¶
First, create the main, top-level, FastAPI application, and its path operations:
from fastapi import 
app = FastAPI()
@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}
subapi = FastAPI()
@subapi.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}
app.mount("/subapi", subapi)Sub-application¶
Then, create your sub-application, and its path operations.This sub-application is just another standard FastAPI application, but this is the one that will be "mounted":
from fastapi import 
app = FastAPI()
@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}
subapi = FastAPI()
@subapi.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}
app.mount("/subapi", subapi)Mount the sub-application¶
In your top-level application, app, mount the sub-application, subapi.In this case, it will be mounted at the path /subapi:
from fastapi import 
app = FastAPI()
@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}
subapi = FastAPI()
@subapi.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}
app.mount("/subapi", subapi)Check the automatic API docs¶
Now, run the fastapi command with your file:And open the docs at http://127.0.0.1:8000/docs.You will see the automatic API docs for the main app, including only its own path operations:And then, open the docs for the sub-application, at http://127.0.0.1:8000/subapi/docs.You will see the automatic API docs for the sub-application, including only its own path operations, all under the correct sub-path prefix /subapi:If you try interacting with any of the two user interfaces, they will work correctly, because the browser will be able to talk to each specific app or sub-app.Technical Details: root_path¶
When you mount a sub-application as described above, FastAPI will take care of communicating the mount path for the sub-application using a mechanism from the ASGI specification called a root_path.That way, the sub-application will know to use that path prefix for the docs UI.And the sub-application could also have its own mounted sub-applications and everything would work correctly, because FastAPI handles all these root_paths automatically.You will learn more about the root_path and how to use it explicitly in the section about Behind a Proxy.
Advanced Middleware
Behind a Proxy
Behind a Proxy 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Proxy with a stripped path prefix
Providing the root_path
Checking the current root_path
Setting the root_path in the FastAPI app
About root_path
About proxies with a stripped path prefix
Testing locally with Traefik
Check the responses
Check the docs UI
Additional servers
Disable automatic server from root_path
Mounting a sub-application
Advanced User Guide
Behind a Proxy¶
In some situations, you might need to use a proxy server like Traefik or Nginx with a configuration that adds an extra path prefix that is not seen by your application.In these cases you can use root_path to configure your application.The root_path is a mechanism provided by the ASGI specification (that FastAPI is built on, through Starlette).The root_path is used to handle these specific cases.And it's also used internally when mounting sub-applications.Proxy with a stripped path prefix¶
Having a proxy with a stripped path prefix, in this case, means that you could declare a path at /app in your code, but then, you add a layer on top (the proxy) that would put your FastAPI application under a path like /api/v1.In this case, the original path /app would actually be served at /api/v1/app.Even though all your code is written assuming there's just /app.
from fastapi import FastAPI, Requestapp = FastAPI()
@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}And the proxy would be "stripping" the path prefix on the fly before transmitting the request to the app server (probably Uvicorn via FastAPI CLI), keeping your application convinced that it is being served at /app, so that you don't have to update all your code to include the prefix /api/v1.Up to here, everything would work as normally.But then, when you open the integrated docs UI (the frontend), it would expect to get the OpenAPI schema at /openapi.json, instead of /api/v1/openapi.json.So, the frontend (that runs in the browser) would try to reach /openapi.json and wouldn't be able to get the OpenAPI schema.Because we have a proxy with a path prefix of /api/v1 for our app, the frontend needs to fetch the OpenAPI schema at /api/v1/openapi.json.Browser
Proxy on http://0.0.0.0:9999/api/v1/app
Server on http://127.0.0.1:8000/app
TipThe IP 0.0.0.0 is commonly used to mean that the program listens on all the IPs available in that machine/server.The docs UI would also need the OpenAPI schema to declare that this API server is located at /api/v1 (behind the proxy). For example:
{
    "openapi": "3.1.0",
    // More stuff here
    "servers": [
        {
            "url": "/api/v1"
        }
    ],
    "paths": {
            // More stuff here
    }
}
In this example, the "Proxy" could be something like Traefik. And the server would be something like FastAPI CLI with Uvicorn, running your FastAPI application.Providing the root_path¶
To achieve this, you can use the command line option --root-path like:If you use Hypercorn, it also has the option --root-path.Technical DetailsThe ASGI specification defines a root_path for this use case.And the --root-path command line option provides that root_path.Checking the current root_path¶
You can get the current root_path used by your application for each request, it is part of the scope dictionary (that's part of the ASGI spec).Here we are including it in the message just for demonstration purposes.
from fastapi import FastAPI, Requestapp = FastAPI()
@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}Then, if you start Uvicorn with:The response would be something like:
{
    "message": "Hello World",
    "root_path": "/api/v1"
}
Setting the root_path in the FastAPI app¶
Alternatively, if you don't have a way to provide a command line option like --root-path or equivalent, you can set the root_path parameter when creating your FastAPI app:
from fastapi import FastAPI, Requestapp = FastAPI(root_path="/api/v1")
@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}Passing the root_path to FastAPI would be the equivalent of passing the --root-path command line option to Uvicorn or Hypercorn.About root_path¶
Keep in mind that the server (Uvicorn) won't use that root_path for anything else than passing it to the app.But if you go with your browser to http://127.0.0.1:8000/app you will see the normal response:
{
    "message": "Hello World",
    "root_path": "/api/v1"
}
So, it won't expect to be accessed at http://127.0.0.1:8000/api/v1/app.Uvicorn will expect the proxy to access Uvicorn at http://127.0.0.1:8000/app, and then it would be the proxy's responsibility to add the extra /api/v1 prefix on top.About proxies with a stripped path prefix¶
Keep in mind that a proxy with stripped path prefix is only one of the ways to configure it.Probably in many cases the default will be that the proxy doesn't have a stripped path prefix.In a case like that (without a stripped path prefix), the proxy would listen on something like https://myawesomeapp.com, and then if the browser goes to https://myawesomeapp.com/api/v1/app and your server (e.g. Uvicorn) listens on http://127.0.0.1:8000 the proxy (without a stripped path prefix) would access Uvicorn at the same path: http://127.0.0.1:8000/api/v1/app.Testing locally with Traefik¶
You can easily run the experiment locally with a stripped path prefix using Traefik.Download Traefik, it's a single binary, you can extract the compressed file and run it directly from the terminal.Then create a file traefik.toml with:
[entryPoints]
  [entryPoints.http]
    address = ":9999"[providers]
  [providers.file]
    filename = "routes.toml"
This tells Traefik to listen on port 9999 and to use another file routes.toml.TipWe are using port 9999 instead of the standard HTTP port 80 so that you don't have to run it with admin (sudo) privileges.Now create that other file routes.toml:
[http]
  [http.middlewares]    [http.middlewares.api-stripprefix.stripPrefix]
      prefixes = ["/api/v1"]  [http.routers]    [http.routers.app-http]
      entryPoints = ["http"]
      service = "app"
      rule = "PathPrefix(`/api/v1`)"
      middlewares = ["api-stripprefix"]  [http.services]    [http.services.app]
      [http.services.app.loadBalancer]
        [[http.services.app.loadBalancer.servers]]
          url = "http://127.0.0.1:8000"
This file configures Traefik to use the path prefix /api/v1.And then Traefik will redirect its requests to your Uvicorn running on http://127.0.0.1:8000.Now start Traefik:And now start your app, using the --root-path option:Check the responses¶
Now, if you go to the URL with the port for Uvicorn: http://127.0.0.1:8000/app, you will see the normal response:
{
    "message": "Hello World",
    "root_path": "/api/v1"
}
TipNotice that even though you are accessing it at http://127.0.0.1:8000/app it shows the root_path of /api/v1, taken from the option --root-path.And now open the URL with the port for Traefik, including the path prefix: http://127.0.0.1:9999/api/v1/app.We get the same response:
{
    "message": "Hello World",
    "root_path": "/api/v1"
}
but this time at the URL with the prefix path provided by the proxy: /api/v1.Of course, the idea here is that everyone would access the app through the proxy, so the version with the path prefix /api/v1 is the "correct" one.And the version without the path prefix (http://127.0.0.1:8000/app), provided by Uvicorn directly, would be exclusively for the proxy (Traefik) to access it.That demonstrates how the Proxy (Traefik) uses the path prefix and how the server (Uvicorn) uses the root_path from the option --root-path.Check the docs UI¶
But here's the fun part. ✨The "official" way to access the app would be through the proxy with the path prefix that we defined. So, as we would expect, if you try the docs UI served by Uvicorn directly, without the path prefix in the URL, it won't work, because it expects to be accessed through the proxy.You can check it at http://127.0.0.1:8000/docs:But if we access the docs UI at the "official" URL using the proxy with port 9999, at /api/v1/docs, it works correctly! 🎉You can check it at http://127.0.0.1:9999/api/v1/docs:Right as we wanted it. ✔️This is because FastAPI uses this root_path to create the default server in OpenAPI with the URL provided by root_path.Additional servers¶
WarningThis is a more advanced use case. Feel free to skip it.By default, FastAPI will create a server in the OpenAPI schema with the URL for the root_path.But you can also provide other alternative servers, for example if you want the same docs UI to interact with both a staging and a production environment.If you pass a custom list of servers and there's a root_path (because your API lives behind a proxy), FastAPI will insert a "server" with this root_path at the beginning of the list.For example:
from fastapi import FastAPI, Requestapp = FastAPI(
    servers=[
        {"url": "https://stag.example.com", "description": "Staging environment"},
        {"url": "https://prod.example.com", "description": "Production environment"},
    ],
    root_path="/api/v1",
)
@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}Will generate an OpenAPI schema like:
{
    "openapi": "3.1.0",
    // More stuff here
    "servers": [
        {
            "url": "/api/v1"
        },
        {
            "url": "https://stag.example.com",
            "description": "Staging environment"
        },
        {
            "url": "https://prod.example.com",
            "description": "Production environment"
        }
    ],
    "paths": {
            // More stuff here
    }
}
TipNotice the auto-generated server with a url value of /api/v1, taken from the root_path.In the docs UI at http://127.0.0.1:9999/api/v1/docs it would look like:TipThe docs UI will interact with the server that you select.Disable automatic server from root_path¶
If you don't want FastAPI to include an automatic server using the root_path, you can use the parameter root_path_in_servers=False:
from fastapi import FastAPI, Requestapp = FastAPI(
    servers=[
        {"url": "https://stag.example.com", "description": "Staging environment"},
        {"url": "https://prod.example.com", "description": "Production environment"},
    ],
    root_path="/api/v1",
    root_path_in_servers=False,
)
@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}and then it won't include it in the OpenAPI schema.Mounting a sub-application¶
If you need to mount a sub-application (as described in Sub Applications - Mounts) while also using a proxy with root_path, you can do it normally, as you would expect.FastAPI will internally use the root_path smartly, so it will just work. ✨
Sub Applications - Mounts
Templates
Templates 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Install dependencies
Using Jinja2Templates
Writing templates
Template Context Values
Template url_for Arguments
Templates and static files
More details
Advanced User Guide
Templates¶
You can use any template engine you want with FastAPI.A common choice is Jinja2, the same one used by Flask and other tools.There are utilities to configure it easily that you can use directly in your FastAPI application (provided by Starlette).Install dependencies¶
Make sure you create a virtual environment, activate it, and install jinja2:
fast →
pip 
Using Jinja2Templates¶
Import Jinja2Templates.
Create a templates object that you can reuse later.
Declare a Request parameter in the path operation that will return a template.
Use the templates you created to render and return a TemplateResponse, pass the name of the template, the request object, and a "context" dictionary with key-value pairs to be used inside of the Jinja2 template.from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templatesapp = FastAPI()app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )NoteBefore FastAPI 0.108.0, Starlette 0.29.0, the name was the first parameter.Also, before that, in previous versions, the request object was passed as part of the key-value pairs in the context for Jinja2.TipBy declaring response_class=HTMLResponse the docs UI will be able to know that the response will be HTML.Technical DetailsYou could also use from starlette.templating import Jinja2Templates.FastAPI provides the same starlette.templating as fastapi.templating just as a convenience for you, the developer. But most of the available responses come directly from Starlette. The same with Request and StaticFiles.Writing templates¶
Then you can write a template at templates/item.html with, for example:
<html>
<head>
    <title>Item Details</title>
    <link href="{{ url_for('static', path='/styles.css') }}" rel="stylesheet">
</head>
<body>
    <h1><a href="{{ url_for('read_item', id=id) }}">Item ID: {{ id }}</a></h1>
</body>
</html>
Template Context Values¶
In the HTML that contains:
Item ID: {{ id }}
...it will show the id taken from the "context" dict you passed:
{"id": id}
For example, with an ID of 42, this would render:
Item ID: 42
Template url_for Arguments¶
You can also use url_for() inside of the template, it takes as arguments the same arguments that would be used by your path operation function.So, the section with:
<a href="{{ url_for('read_item', id=id) }}">
...will generate a link to the same URL that would be handled by the path operation function read_item(id=id).For example, with an ID of 42, this would render:
<a href="/items/42">
Templates and static files¶
You can also use url_for() inside of the template, and use it, for example, with the StaticFiles you mounted with the name="static".
<html>
<head>
    <title>Item Details</title>
    <link href="{{ url_for('static', path='/styles.css') }}" rel="stylesheet">
</head>
<body>
    <h1><a href="{{ url_for('read_item', id=id) }}">Item ID: {{ id }}</a></h1>
</body>
</html>
In this example, it would link to a CSS file at static/styles.css with:
h1 {
    color: green;
}
And because you are using StaticFiles, that CSS file would be served automatically by your FastAPI application at the URL /static/styles.css.More details¶
For more details, including how to test templates, check Starlette's docs on templates.
Behind a Proxy
WebSockets
WebSockets 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Install WebSockets
WebSockets client
In production
Create a websocket
Await for messages and send messages
Try it
Using Depends and others
Try the WebSockets with dependencies
Handling disconnections and multiple clients
More info
Advanced User Guide
WebSockets¶
You can use WebSockets with FastAPI.Install WebSockets¶
Make sure you create a virtual environment, activate it, and install websockets:
fast →
pip
WebSockets client¶
In production¶
In your production system, you probably have a frontend created with a modern framework like React, Vue.js or Angular.And to communicate using WebSockets with your backend you would probably use your frontend's utilities.Or you might have a native mobile application that communicates with your WebSocket backend directly, in native code.Or you might have any other way to communicate with the WebSocket endpoint.But for this example, we'll use a very simple HTML document with some JavaScript, all inside a long string.This, of course, is not optimal and you wouldn't use it for production.In production you would have one of the options above.But it's the simplest way to focus on the server-side of WebSockets and have a working example:
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponseapp = FastAPI()html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
@app.get("/")
async def get():
    return HTMLResponse(html)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")Create a websocket¶
In your FastAPI application, create a websocket:
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponseapp = FastAPI()html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
@app.get("/")
async def get():
    return HTMLResponse(html)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")Technical DetailsYou could also use from starlette.websockets import WebSocket.FastAPI provides the same WebSocket directly just as a convenience for you, the developer. But it comes directly from Starlette.Await for messages and send messages¶
In your WebSocket route you can await for messages and send messages.
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponseapp = FastAPI()html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
@app.get("/")
async def get():
    return HTMLResponse(html)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")You can receive and send binary, text, and JSON data.Try it¶
If your file is named main.py, run your application with:Open your browser at http://127.0.0.1:8000.You will see a simple page like:You can type messages in the input box, and send them:And your FastAPI application with WebSockets will respond back:You can send (and receive) many messages:And all of them will use the same WebSocket connection.Using Depends and others¶
In WebSocket endpoints you can import from fastapi and use:Depends
Security
Cookie
Header
Path
Query
They work the same way as for other FastAPI endpoints/path operations:
from typing import Annotatedfrom fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    WebSocketException,
    status,
)
from fastapi.responses import HTMLResponseapp = FastAPI()html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var itemId = document.getElementById("itemId")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://localhost:8000/items/" + itemId.value + "/wstoken=" + token.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
@app.get("/")
async def get():
    return HTMLResponse(html)
async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token
@app.websocket("/items/{item_id}/ws")
async def websocket_endpoint(
    *,
    websocket: WebSocket,
    item_id: str,
    q: int | None = None,
    cookie_or_token: Annotated[str, Depends(get_cookie_or_token)],
):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(
            f"Session cookie or query token value is: {cookie_or_token}"
        )
        if q is not None:
            await websocket.send_text(f"Query parameter q is: {q}")
        await websocket.send_text(f"Message text was: {data}, for item ID: {item_id}")🤓 Other versions and variants
InfoAs this is a WebSocket it doesn't really make sense to raise an HTTPException, instead we raise a WebSocketException.You can use a closing code from the valid codes defined in the specification.Try the WebSockets with dependencies¶
If your file is named main.py, run your application with:Open your browser at http://127.0.0.1:8000.There you can set:The "Item ID", used in the path.
The "Token" used as a query parameter.
TipNotice that the query token will be handled by a dependency.With that you can connect the WebSocket and then send and receive messages:Handling disconnections and multiple clients¶
When a WebSocket connection is closed, the await websocket.receive_text() will raise a WebSocketDisconnect exception, which you can then catch and handle like in this example.
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponseapp = FastAPI()html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
manager = ConnectionManager()
@app.get("/")
async def get():
    return HTMLResponse(html)
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")🤓 Other versions and variants
To try it out:Open the app with several browser tabs.
Write messages from them.
Then close one of the tabs.
That will raise the WebSocketDisconnect exception, and all the other clients will receive a message like:
Client #1596980209979 left the chat
TipThe app above is a minimal and simple example to demonstrate how to handle and broadcast messages to several WebSocket connections.But keep in mind that, as everything is handled in memory, in a single list, it will only work while the process is running, and will only work with a single process.If you need something easy to integrate with FastAPI but that is more robust, supported by Redis, PostgreSQL or others, check encode/broadcaster.More info¶
To learn more about the options, check Starlette's documentation for:The WebSocket class.
Class-based WebSocket handling.Templates
Lifespan Events
Lifespan Events 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Use Case
Lifespan
Lifespan function
Async Context Manager
Alternative Events (deprecated)
startup event
shutdown event
startup and shutdown together
Technical Details
Sub Applications
Advanced User Guide
Lifespan Events¶
You can define logic (code) that should be executed before the application starts up. This means that this code will be executed once, before the application starts receiving requests.The same way, you can define logic (code) that should be executed when the application is shutting down. In this case, this code will be executed once, after having handled possibly many requests.Because this code is executed before the application starts taking requests, and right after it finishes handling requests, it covers the whole application lifespan (the word "lifespan" will be important in a second 😉).This can be very useful for setting up resources that you need to use for the whole app, and that are shared among requests, and/or that you need to clean up afterwards. For example, a database connection pool, or loading a shared machine learning model.Use Case¶
Let's start with an example use case and then see how to solve it with this.Let's imagine that you have some machine learning models that you want to use to handle requests. 🤖The same models are shared among requests, so, it's not one model per request, or one per user or something similar.Let's imagine that loading the model can take quite some time, because it has to read a lot of data from disk. So you don't want to do it for every request.You could load it at the top level of the module/file, but that would also mean that it would load the model even if you are just running a simple automated test, then that test would be slow because it would have to wait for the model to load before being able to run an independent part of the code.That's what we'll solve, let's load the model before the requests are handled, but only right before the application starts receiving requests, not while the code is being loaded.Lifespan¶
You can define this startup and shutdown logic using the lifespan parameter of the FastAPI app, and a "context manager" (I'll show you what that is in a second).Let's start with an example and then see it in detail.We create an async function lifespan() with yield like this:
from contextlib import asynccontextmanagerfrom fastapi import def fake_answer_to_everything_ml_model(x: float):
    return x * 42
ml_models = {}
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the     ml_models.clear()
app = FastAPI(lifespan=lifespan)
@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}Here we are simulating the expensive startup operation of loading the model by putting the (fake) model function in the dictionary with machine learning models before the yield. This code will be executed before the application starts taking requests, during the startup.And then, right after the yield, we unload the model. This code will be executed after the application finishes handling requests, right before the shutdown. This could, for example, release resources like memory or a GPU.TipThe shutdown would happen when you are stopping the application.Maybe you need to start a new version, or you just got tired of running it. 🤷Lifespan function¶
The first thing to notice, is that we are defining an async function with yield. This is very similar to Dependencies with yield.
from contextlib import asynccontextmanagerfrom fastapi import def fake_answer_to_everything_ml_model(x: float):
    return x * 42
ml_models = {}
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the     ml_models.clear()
app = FastAPI(lifespan=lifespan)
@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}The first part of the function, before the yield, will be executed before the application starts.And the part after the yield will be executed after the application has finished.Async Context Manager¶
If you check, the function is decorated with an @asynccontextmanager.That converts the function into something called an "async context manager".
from contextlib import asynccontextmanagerfrom fastapi import def fake_answer_to_everything_ml_model(x: float):
    return x * 42
ml_models = {}
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the     ml_models.clear()
app = FastAPI(lifespan=lifespan)
@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}A context manager in Python is something that you can use in a with statement, for example, open() can be used as a context manager:
with open("file.txt") as file:
    file.read()
In recent versions of Python, there's also an async context manager. You would use it with async with:
async with lifespan(app):
    await do_stuff()
When you create a context manager or an async context manager like above, what it does is that, before entering the with block, it will execute the code before the yield, and after exiting the with block, it will execute the code after the yield.In our code example above, we don't use it directly, but we pass it to FastAPI for it to use it.The lifespan parameter of the FastAPI app takes an async context manager, so we can pass our new lifespan async context manager to it.
from contextlib import asynccontextmanagerfrom fastapi import def fake_answer_to_everything_ml_model(x: float):
    return x * 42
ml_models = {}
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the     ml_models.clear()
app = FastAPI(lifespan=lifespan)
@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}Alternative Events (deprecated)¶
WarningThe recommended way to handle the startup and shutdown is using the lifespan parameter of the FastAPI app as described above. If you provide a lifespan parameter, startup and shutdown event handlers will no longer be called. It's all lifespan or all events, not both.You can probably skip this part.There's an alternative way to define this logic to be executed during startup and during shutdown.You can define event handlers (functions) that need to be executed before the application starts up, or when the application is shutting down.These functions can be declared with async def or normal def.startup event¶
To add a function that should be run before the application starts, declare it with the event "startup":
from fastapi import 
app = FastAPI()items = {}
@app.on_event("startup")
async def startup_event():
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}
@app.get("/items/{item_id}")
async def read_items(item_id: str):
    return items[item_id]In this case, the startup event handler function will initialize the items "database" (just a dict) with some values.You can add more than one event handler function.And your application won't start receiving requests until all the startup event handlers have completed.shutdown event¶
To add a function that should be run when the application is shutting down, declare it with the event "shutdown":
from fastapi import 
app = FastAPI()
@app.on_event("shutdown")
def shutdown_event():
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")
@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]Here, the shutdown event handler function will write a text line "Application shutdown" to a file log.txt.InfoIn the open() function, the mode="a" means "append", so, the line will be added after whatever is on that file, without overwriting the previous contents.TipNotice that in this case we are using a standard Python open() function that interacts with a file.So, it involves I/O (input/output), that requires "waiting" for things to be written to disk.But open() doesn't use async and await.So, we declare the event handler function with standard def instead of async def.startup and shutdown together¶
There's a high chance that the logic for your startup and shutdown is connected, you might want to start something and then finish it, acquire a resource and then release it, etc.Doing that in separated functions that don't share logic or variables together is more difficult as you would need to store values in global variables or similar tricks.Because of that, it's now recommended to instead use the lifespan as explained above.Technical Details¶
Just a technical detail for the curious nerds. 🤓Underneath, in the ASGI technical specification, this is part of the Lifespan Protocol, and it defines events called startup and shutdown.InfoYou can read more about the Starlette lifespan handlers in Starlette's Lifespan' docs.Including how to handle lifespan state that can be used in other areas of your code.Sub Applications¶
🚨 Keep in mind that these lifespan events (startup and shutdown) will only be executed for the main application, not for Sub Applications - Mounts.
WebSockets
Testing WebSockets
Testing WebSockets 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Advanced User Guide
Testing WebSockets¶
You can use the same TestClient to test WebSockets.For this, you use the TestClient in a with statement, connecting to the WebSocket:
from fastapi import from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketapp = FastAPI()
@app.get("/")
async def read_main():
    return {"msg": "Hello World"}
@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"msg": "Hello WebSocket"})
    await websocket.close()
def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Hello WebSocket"}NoteFor more details, check Starlette's documentation for testing WebSockets.
Lifespan Events
Testing Events: startup - shutdown
Testing Events: startup - shutdown 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Advanced User Guide
Testing Events: startup - shutdown¶
When you need your event handlers (startup and shutdown) to run in your tests, you can use the TestClient with a with statement:
from fastapi import from fastapi.testclient import TestClientapp = FastAPI()items = {}
@app.on_event("startup")
async def startup_event():
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}
@app.get("/items/{item_id}")
async def read_items(item_id: str):
    return items[item_id]
def test_read_items():
    with TestClient(app) as client:
        response = client.get("/items/foo")
        assert response.status_code == 200
        assert response.json() == {"name": "Fighters"}
Testing WebSockets
Testing Dependencies with Overrides
Testing Dependencies with Overrides 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Overriding dependencies during testing
Use cases: external service
Use the app.dependency_overrides attribute
Advanced User Guide
Testing Dependencies with Overrides¶
Overriding dependencies during testing¶
There are some scenarios where you might want to override a dependency during testing.You don't want the original dependency to run (nor any of the sub-dependencies it might have).Instead, you want to provide a different dependency that will be used only during tests (possibly only some specific tests), and will provide a value that can be used where the value of the original dependency was used.Use cases: external service¶
An example could be that you have an external authentication provider that you need to call.You send it a token and it returns an authenticated user.This provider might be charging you per request, and calling it might take some extra time than if you had a fixed mock user for tests.You probably want to test the external provider once, but not necessarily call it for every test that runs.In this case, you can override the dependency that calls that provider, and use a custom dependency that returns a mock user, only for your tests.Use the app.dependency_overrides attribute¶
For these cases, your FastAPI application has an attribute app.dependency_overrides, it is a simple dict.To override a dependency for testing, you put as a key the original dependency (a function), and as the value, your dependency override (another function).And then FastAPI will call that override instead of the original dependency.
from typing import Annotatedfrom fastapi import Depends, from fastapi.testclient import TestClientapp = FastAPI()
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}
@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return {"message": "Hello Items!", "params": commons}
@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return {"message": "Hello Users!", "params": commons}
client = TestClient(app)
async def override_dependency(q: str | None = None):
    return {"q": q, "skip": 5, "limit": 10}
app.dependency_overrides[common_parameters] = override_dependency
def test_override_in_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": None, "skip": 5, "limit": 10},
    }
def test_override_in_items_with_q():
    response = client.get("/items/q=foo")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }
def test_override_in_items_with_params():
    response = client.get("/items/q=foo&skip=100&limit=200")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }🤓 Other versions and variants
TipYou can set a dependency override for a dependency used anywhere in your FastAPI application.The original dependency could be used in a path operation function, a path operation decorator (when you don't use the return value), a .include_router() call, etc.FastAPI will still be able to override it.Then you can reset your overrides (remove them) by setting app.dependency_overrides to be an empty dict:
app.dependency_overrides = {}
TipIf you want to override a dependency only during some tests, you can set the override at the beginning of the test (inside the test function) and reset it at the end (at the end of the test function).
Testing Events: startup - shutdown
Async Tests
Async Tests 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
pytest.mark.anyio
HTTPX
Example
Run it
In Detail
Other Asynchronous Function Calls
Advanced User Guide
Async Tests¶
You have already seen how to test your FastAPI applications using the provided TestClient. Up to now, you have only seen how to write synchronous tests, without using async functions.Being able to use asynchronous functions in your tests could be useful, for example, when you're querying your database asynchronously. Imagine you want to test sending requests to your FastAPI application and then verify that your backend successfully wrote the correct data in the database, while using an async database library.Let's look at how we can make that work.pytest.mark.anyio¶
If we want to call asynchronous functions in our tests, our test functions have to be asynchronous. AnyIO provides a neat plugin for this, that allows us to specify that some test functions are to be called asynchronously.HTTPX¶
Even if your FastAPI application uses normal def functions instead of async def, it is still an async application underneath.The TestClient does some magic inside to call the asynchronous FastAPI application in your normal def test functions, using standard pytest. But that magic doesn't work anymore when we're using it inside asynchronous functions. By running our tests asynchronously, we can no longer use the TestClient inside our test functions.The TestClient is based on HTTPX, and luckily, we can use it directly to test the API.Example¶
For a simple example, let's consider a file structure similar to the one described in Bigger Applications and Testing:
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
The file main.py would have:
from fastapi import 
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Tomato"}The file test_main.py would have the tests for main.py, it could look like this now:
import pytest
from httpx import ASGITransport, AsyncClientfrom .main import app
@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}Run it¶
You can run your tests as usual via:
In Detail¶
The marker @pytest.mark.anyio tells pytest that this test function should be called asynchronously:
import pytest
from httpx import ASGITransport, AsyncClientfrom .main import app
@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}TipNote that the test function is now async def instead of just def as before when using the TestClient.Then we can create an AsyncClient with the app, and send async requests to it, using await.
import pytest
from httpx import ASGITransport, AsyncClientfrom .main import app
@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}This is the equivalent to:
response = client.get('/')
...that we used to make our requests with the TestClient.TipNote that we're using async/await with the new AsyncClient - the request is asynchronous.WarningIf your application relies on lifespan events, the AsyncClient won't trigger these events. To ensure they are triggered, use LifespanManager from florimondmanca/asgi-lifespan.Other Asynchronous Function Calls¶
As the testing function is now asynchronous, you can now also call (and await) other async functions apart from sending requests to your FastAPI application in your tests, exactly as you would call them anywhere else in your code.TipIf you encounter a RuntimeError: Task attached to a different loop when integrating asynchronous function calls in your tests (e.g. when using MongoDB's MotorClient), remember to instantiate objects that need an event loop only within async functions, e.g. an '@app.on_event("startup") callback.
Testing Dependencies with Overrides
Settings and Environment Variables
Settings and Environment Variables 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Types and validation
Pydantic Settings
Install pydantic-settings
Create the Settings object
Use the settings
Run the server
Settings in another module
Settings in a dependency
The config file
The main app file
Settings and testing
Reading a .env file
The .env file
Read settings from .env
Creating the Settings only once with lru_cache
lru_cache Technical Details
Recap
Advanced User Guide
Settings and Environment Variables¶
In many cases your application could need some external settings or configurations, for example secret keys, database credentials, credentials for email services, etc.Most of these settings are variable (can change), like database URLs. And many could be sensitive, like secrets.For this reason it's common to provide them in environment variables that are read by the application.TipTo understand environment variables you can read Environment Variables.Types and validation¶
These environment variables can only handle text strings, as they are external to Python and have to be compatible with other programs and the rest of the system (and even with different operating systems, as Linux, Windows, macOS).That means that any value read in Python from an environment variable will be a str, and any conversion to a different type or any validation has to be done in code.Pydantic Settings¶
Fortunately, Pydantic provides a great utility to handle these settings coming from environment variables with Pydantic: Settings management.Install pydantic-settings¶
First, make sure you create your virtual environment, activate it, and then install the pydantic-settings package:
fast →
pip install p
It also comes included when you install the all extras with:
fast →
pip install "
InfoIn Pydantic v1 it came included with the main package. Now it is distributed as this independent package so that you can choose to install it or not if you don't need that functionality.Create the Settings object¶
Import BaseSettings from Pydantic and create a sub-class, very much like with a Pydantic model.The same way as with Pydantic models, you declare class attributes with type annotations, and possibly default values.You can use all the same validation features and tools you use for Pydantic models, like different data types and additional validations with Field().
Pydantic v2
Pydantic v
from fastapi import from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50
settings = Settings()
app = FastAPI()
@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
TipIf you want something quick to copy and paste, don't use this example, use the last one below.Then, when you create an instance of that Settings class (in this case, in the settings object), Pydantic will read the environment variables in a case-insensitive way, so, an upper-case variable APP_NAME will still be read for the attribute app_name.Next it will convert and validate the data. So, when you use that settings object, you will have data of the types you declared (e.g. items_per_user will be an int).Use the settings¶
Then you can use the new settings object in your application:
from fastapi import from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50
settings = Settings()
app = FastAPI()
@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }Run the server¶
Next, you would run the server passing the configurations as environment variables, for example you could set an ADMIN_EMAIL and APP_NAME with:TipTo set multiple env vars for a single command just separate them with a space, and put them all before the command.And then the admin_email setting would be set to "deadpool@example.com".The app_name would be "ChimichangApp".And the items_per_user would keep its default value of 50.Settings in another module¶
You could put those settings in another module file as you saw in Bigger Applications - Multiple Files.For example, you could have a file config.py with:
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50
settings = Settings()And then use it in a file main.py:
from fastapi import 
from .config import settingsapp = FastAPI()
@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }TipYou would also need a file __init__.py as you saw in Bigger Applications - Multiple Files.Settings in a dependency¶
In some occasions it might be useful to provide the settings from a dependency, instead of having a global object with settings that is used everywhere.This could be especially useful during testing, as it's very easy to override a dependency with your own custom settings.The config file¶
Coming from the previous example, your config.py file could look like:
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50Notice that now we don't create a default instance settings = Settings().The main app file¶
Now we create a dependency that returns a new config.Settings().
from functools import lru_cache
from typing import Annotatedfrom fastapi import Depends, 
from .config import Settingsapp = FastAPI()
@lru_cache
def get_settings():
    return Settings()
@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }TipWe'll discuss the @lru_cache in a bit.For now you can assume get_settings() is a normal function.And then we can require it from the path operation function as a dependency and use it anywhere we need it.
from functools import lru_cache
from typing import Annotatedfrom fastapi import Depends, 
from .config import Settingsapp = FastAPI()
@lru_cache
def get_settings():
    return Settings()
@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }Settings and testing¶
Then it would be very easy to provide a different settings object during testing by creating a dependency override for get_settings:
from fastapi.testclient import TestClientfrom .config import Settings
from .main import app, get_settingsclient = TestClient(app)
def get_settings_override():
    return Settings(admin_email="testing_admin@example.com")
app.dependency_overrides[get_settings] = get_settings_override
def test_app():
    response = client.get("/info")
    data = response.json()
    assert data == {
        "app_name": "Awesome API",
        "admin_email": "testing_admin@example.com",
        "items_per_user": 50,
    }In the dependency override we set a new value for the admin_email when creating the new Settings object, and then we return that new object.Then we can test that it is used.Reading a .env file¶
If you have many settings that possibly change a lot, maybe in different environments, it might be useful to put them on a file and then read them from it as if they were environment variables.This practice is common enough that it has a name, these environment variables are commonly placed in a file .env, and the file is called a "dotenv".TipA file starting with a dot (.) is a hidden file in Unix-like systems, like Linux and macOS.But a dotenv file doesn't really have to have that exact filename.Pydantic has support for reading from these types of files using an external library. You can read more at Pydantic Settings: Dotenv (.env) support.TipFor this to work, you need to pip install python-dotenv.The .env file¶
You could have a .env file with:
ADMIN_EMAIL="deadpool@example.com"
APP_NAME="ChimichangApp"
Read settings from .env¶
And then update your config.py with:
Pydantic v2
Pydantic v
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50    model_config = SettingsConfigDict(env_file=".env")
TipThe model_config attribute is used just for Pydantic configuration. You can read more at Pydantic: Concepts: Configuration.InfoIn Pydantic version 1 the configuration was done in an internal class Config, in Pydantic version 2 it's done in an attribute model_config. This attribute takes a dict, and to get autocompletion and inline errors you can import and use SettingsConfigDict to define that dict.Here we define the config env_file inside of your Pydantic Settings class, and set the value to the filename with the dotenv file we want to use.Creating the Settings only once with lru_cache¶
Reading a file from disk is normally a costly (slow) operation, so you probably want to do it only once and then reuse the same settings object, instead of reading it for each request.But every time we do:
Settings()
a new Settings object would be created, and at creation it would read the .env file again.If the dependency function was just like:
def get_settings():
    return Settings()
we would create that object for each request, and we would be reading the .env file for each request. ⚠️But as we are using the @lru_cache decorator on top, the Settings object will be created only once, the first time it's called. ✔️
from functools import lru_cachefrom fastapi import Depends, from typing_extensions import Annotatedfrom . import configapp = FastAPI()
@lru_cache
def get_settings():
    return config.Settings()
@app.get("/info")
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }Then for any subsequent call of get_settings() in the dependencies for the next requests, instead of executing the internal code of get_settings() and creating a new Settings object, it will return the same object that was returned on the first call, again and again.lru_cache Technical Details¶
@lru_cache modifies the function it decorates to return the same value that was returned the first time, instead of computing it again, executing the code of the function every time.So, the function below it will be executed once for each combination of arguments. And then the values returned by each of those combinations of arguments will be used again and again whenever the function is called with exactly the same combination of arguments.For example, if you have a function:
@lru_cache
def say_hi(name: str, salutation: str = "Ms."):
    return f"Hello {salutation} {name}"
your program could execute like this:Execute function
say_hi()
Code
Execute function
say_hi()
Code
say_hi(name="Camila")
execute function code
return the result
say_hi(name="Camila")
return stored result
say_hi(name="Rick")
execute function code
return the result
say_hi(name="Rick", salutation="Mr.")
execute function code
return the result
say_hi(name="Rick")
return stored result
say_hi(name="Camila")
return stored result
In the case of our dependency get_settings(), the function doesn't even take any arguments, so it always returns the same value.That way, it behaves almost as if it was just a global variable. But as it uses a dependency function, then we can override it easily for testing.@lru_cache is part of functools which is part of Python's standard library, you can read more about it in the Python docs for @lru_cache.Recap¶
You can use Pydantic Settings to handle the settings or configurations for your application, with all the power of Pydantic models.By using a dependency you can simplify testing.
You can use .env files with it.
Using @lru_cache lets you avoid reading the dotenv file again and again for each request, while allowing you to override it during testing.Async Tests
OpenAPI Callbacks
OpenAPI Callbacks 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
An app with callbacks
The normal FastAPI app
Documenting the callback
Write the callback documentation code
Create a callback APIRouter
Create the callback path operation
The callback path expression
Add the callback router
Check the docs
Advanced User Guide
OpenAPI Callbacks¶
You could create an API with a path operation that could trigger a request to an external API created by someone else (probably the same developer that would be using your API).The process that happens when your API app calls the external API is named a "callback". Because the software that the external developer wrote sends a request to your API and then your API calls back, sending a request to an external API (that was probably created by the same developer).In this case, you could want to document how that external API should look like. What path operation it should have, what body it should expect, what response it should return, etc.An app with callbacks¶
Let's see all this with an example.Imagine you develop an app that allows creating invoices.These invoices will have an id, title (optional), customer, and total.The user of your API (an external developer) will create an invoice in your API with a POST request.Then your API will (let's imagine):Send the invoice to some customer of the external developer.
Collect the money.
Send a notification back to the API user (the external developer).
This will be done by sending a POST request (from your API) to some external API provided by that external developer (this is the "callback").
The normal FastAPI app¶
Let's first see how the normal API app would look like before adding the callback.It will have a path operation that will receive an Invoice body, and a query parameter callback_url that will contain the URL for the callback.This part is pretty normal, most of the code is probably already familiar to you:
from typing import Unionfrom fastapi import APIRouter, from pydantic import BaseModel, HttpUrlapp = FastAPI()
class Invoice(BaseModel):
    id: str
    title: Union[str, None] = None
    customer: str
    total: float
class InvoiceEvent(BaseModel):
    description: str
    paid: bool
class InvoiceEventReceived(BaseModel):
    ok: bool
invoices_callback_router = APIRouter()
@invoices_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
)
def invoice_notification(body: InvoiceEvent):
    pass
@app.post("/invoices/", callbacks=invoices_callback_router.routes)
def create_invoice(invoice: Invoice, callback_url: Union[HttpUrl, None] = None):
    """
    Create an invoice.    This will (let's imagine) let the API user (some external developer) create an
    invoice.    And this path operation will:    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the
            external API with the notification of the invoice event
            (e.g. "payment successful").
    """
    # Send the invoice, collect the money, send the notification (the callback)
    return {"msg": "Invoice received"}TipThe callback_url query parameter uses a Pydantic Url type.The only new thing is the callbacks=invoices_callback_router.routes as an argument to the path operation decorator. We'll see what that is next.Documenting the callback¶
The actual callback code will depend heavily on your own API app.And it will probably vary a lot from one app to the next.It could be just one or two lines of code, like:
callback_url = "https://example.com/api/v1/invoices/events/"
httpx.post(callback_url, json={"description": "Invoice paid", "paid": True})
But possibly the most important part of the callback is making sure that your API user (the external developer) implements the external API correctly, according to the data that your API is going to send in the request body of the callback, etc.So, what we will do next is add the code to document how that external API should look like to receive the callback from your API.That documentation will show up in the Swagger UI at /docs in your API, and it will let external developers know how to build the external API.This example doesn't implement the callback itself (that could be just a line of code), only the documentation part.TipThe actual callback is just an HTTP request.When implementing the callback yourself, you could use something like HTTPX or Requests.Write the callback documentation code¶
This code won't be executed in your app, we only need it to document how that external API should look like.But, you already know how to easily create automatic documentation for an API with FastAPI.So we are going to use that same knowledge to document how the external API should look like... by creating the path operation(s) that the external API should implement (the ones your API will call).TipWhen writing the code to document a callback, it might be useful to imagine that you are that external developer. And that you are currently implementing the external API, not your API.Temporarily adopting this point of view (of the external developer) can help you feel like it's more obvious where to put the parameters, the Pydantic model for the body, for the response, etc. for that external API.Create a callback APIRouter¶
First create a new APIRouter that will contain one or more callbacks.
from typing import Unionfrom fastapi import APIRouter, from pydantic import BaseModel, HttpUrlapp = FastAPI()
class Invoice(BaseModel):
    id: str
    title: Union[str, None] = None
    customer: str
    total: float
class InvoiceEvent(BaseModel):
    description: str
    paid: bool
class InvoiceEventReceived(BaseModel):
    ok: bool
invoices_callback_router = APIRouter()
@invoices_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
)
def invoice_notification(body: InvoiceEvent):
    pass
@app.post("/invoices/", callbacks=invoices_callback_router.routes)
def create_invoice(invoice: Invoice, callback_url: Union[HttpUrl, None] = None):
    """
    Create an invoice.    This will (let's imagine) let the API user (some external developer) create an
    invoice.    And this path operation will:    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the
            external API with the notification of the invoice event
            (e.g. "payment successful").
    """
    # Send the invoice, collect the money, send the notification (the callback)
    return {"msg": "Invoice received"}Create the callback path operation¶
To create the callback path operation use the same APIRouter you created above.It should look just like a normal FastAPI path operation:It should probably have a declaration of the body it should receive, e.g. body: InvoiceEvent.
And it could also have a declaration of the response it should return, e.g. response_model=InvoiceEventReceived.from typing import Unionfrom fastapi import APIRouter, from pydantic import BaseModel, HttpUrlapp = FastAPI()
class Invoice(BaseModel):
    id: str
    title: Union[str, None] = None
    customer: str
    total: float
class InvoiceEvent(BaseModel):
    description: str
    paid: bool
class InvoiceEventReceived(BaseModel):
    ok: bool
invoices_callback_router = APIRouter()
@invoices_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
)
def invoice_notification(body: InvoiceEvent):
    pass
@app.post("/invoices/", callbacks=invoices_callback_router.routes)
def create_invoice(invoice: Invoice, callback_url: Union[HttpUrl, None] = None):
    """
    Create an invoice.    This will (let's imagine) let the API user (some external developer) create an
    invoice.    And this path operation will:    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the
            external API with the notification of the invoice event
            (e.g. "payment successful").
    """
    # Send the invoice, collect the money, send the notification (the callback)
    return {"msg": "Invoice received"}There are 2 main differences from a normal path operation:It doesn't need to have any actual code, because your app will never call this code. It's only used to document the external API. So, the function could just have pass.
The path can contain an OpenAPI 3 expression (see more below) where it can use variables with parameters and parts of the original request sent to your API.
The callback path expression¶
The callback path can have an OpenAPI 3 expression that can contain parts of the original request sent to your API.In this case, it's the str:
"{$callback_url}/invoices/{$request.body.id}"
So, if your API user (the external developer) sends a request to your API to:
https://yourapi.com/invoices/callback_url=https://www.external.org/events
with a JSON body of:
{
    "id": "2expen51ve",
    "customer": "Mr. Richie Rich",
    "total": "9999"
}
then your API will process the invoice, and at some point later, send a callback request to the callback_url (the external API):
https://www.external.org/events/invoices/2expen51ve
with a JSON body containing something like:
{
    "description": "Payment celebration",
    "paid": true
}
and it would expect a response from that external API with a JSON body like:
{
    "ok": true
}
TipNotice how the callback URL used contains the URL received as a query parameter in callback_url (https://www.external.org/events) and also the invoice id from inside of the JSON body (2expen51ve).Add the callback router¶
At this point you have the callback path operation(s) needed (the one(s) that the external developer should implement in the external API) in the callback router you created above.Now use the parameter callbacks in your API's path operation decorator to pass the attribute .routes (that's actually just a list of routes/path operations) from that callback router:
from typing import Unionfrom fastapi import APIRouter, from pydantic import BaseModel, HttpUrlapp = FastAPI()
class Invoice(BaseModel):
    id: str
    title: Union[str, None] = None
    customer: str
    total: float
class InvoiceEvent(BaseModel):
    description: str
    paid: bool
class InvoiceEventReceived(BaseModel):
    ok: bool
invoices_callback_router = APIRouter()
@invoices_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
)
def invoice_notification(body: InvoiceEvent):
    pass
@app.post("/invoices/", callbacks=invoices_callback_router.routes)
def create_invoice(invoice: Invoice, callback_url: Union[HttpUrl, None] = None):
    """
    Create an invoice.    This will (let's imagine) let the API user (some external developer) create an
    invoice.    And this path operation will:    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the
            external API with the notification of the invoice event
            (e.g. "payment successful").
    """
    # Send the invoice, collect the money, send the notification (the callback)
    return {"msg": "Invoice received"}TipNotice that you are not passing the router itself (invoices_callback_router) to callback=, but the attribute .routes, as in invoices_callback_router.routes.Check the docs¶
Now you can start your app and go to http://127.0.0.1:8000/docs.You will see your docs including a "Callbacks" section for your path operation that shows how the external API should look like:
Settings and Environment Variables
OpenAPI Webhooks
OpenAPI Webhooks 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Webhooks steps
Documenting webhooks with FastAPI and OpenAPI
An app with webhooks
Check the docs
Advanced User Guide
OpenAPI Webhooks¶
There are cases where you want to tell your API users that your app could call their app (sending a request) with some data, normally to notify of some type of event.This means that instead of the normal process of your users sending requests to your API, it's your API (or your app) that could send requests to their system (to their API, their app).This is normally called a webhook.Webhooks steps¶
The process normally is that you define in your code what is the message that you will send, the body of the request.You also define in some way at which moments your app will send those requests or events.And your users define in some way (for example in a web dashboard somewhere) the URL where your app should send those requests.All the logic about how to register the URLs for webhooks and the code to actually send those requests is up to you. You write it however you want to in your own code.Documenting webhooks with FastAPI and OpenAPI¶
With FastAPI, using OpenAPI, you can define the names of these webhooks, the types of HTTP operations that your app can send (e.g. POST, PUT, etc.) and the request bodies that your app would send.This can make it a lot easier for your users to implement their APIs to receive your webhook requests, they might even be able to autogenerate some of their own API code.InfoWebhooks are available in OpenAPI 3.1.0 and above, supported by FastAPI 0.99.0 and above.An app with webhooks¶
When you create a FastAPI application, there is a webhooks attribute that you can use to define webhooks, the same way you would define path operations, for example with @app.webhooks.post().
from datetime import datetimefrom fastapi import from pydantic import BaseModelapp = FastAPI()
class Subscription(BaseModel):
    username: str
    monthly_fee: float
    start_date: datetime
@app.webhooks.post("new-subscription")
def new_subscription(body: Subscription):
    """
    When a new user subscribes to your service we'll send you a POST request with this
    data to the URL that you register for the event `new-subscription` in the dashboard.
    """
@app.get("/users/")
def read_users():
    return ["Rick", "Morty"]The webhooks that you define will end up in the OpenAPI schema and the automatic docs UI.InfoThe app.webhooks object is actually just an APIRouter, the same type you would use when structuring your app with multiple files.Notice that with webhooks you are actually not declaring a path (like /items/), the text you pass there is just an identifier of the webhook (the name of the event), for example in @app.webhooks.post("new-subscription"), the webhook name is new-subscription.This is because it is expected that your users would define the actual URL path where they want to receive the webhook request in some other way (e.g. a web dashboard).Check the docs¶
Now you can start your app and go to http://127.0.0.1:8000/docs.You will see your docs have the normal path operations and now also some webhooks:
OpenAPI Callbacks
Including WSGI - Flask, Django, others
Including WSGI - Flask, Django, others 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
Using WSGIMiddleware
Check it
Advanced User Guide
Including WSGI - Flask, Django, others¶
You can mount WSGI applications as you saw with Sub Applications - Mounts, Behind a Proxy.For that, you can use the WSGIMiddleware and use it to wrap your WSGI application, for example, Flask, Django, etc.Using WSGIMiddleware¶
You need to import WSGIMiddleware.Then wrap the WSGI (e.g. Flask) app with the middleware.And then mount that under a path.
from fastapi import from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, request
from markupsafe import escapeflask_app = Flask(__name__)
@flask_app.route("/")
def flask_main():
    name = request.args.get("name", "World")
    return f"Hello, {escape(name)} from Flask!"
app = FastAPI()
@app.get("/v2")
def read_main():
    return {"message": "Hello World"}
app.mount("/v1", WSGIMiddleware(flask_app))Check it¶
Now, every request under the path /v1/ will be handled by the Flask application.And the rest will be handled by FastAPI.If you run it and go to http://localhost:8000/v1/ you will see the response from Flask:
Hello, World from Flask!
And if you go to http://localhost:8000/v2 you will see the response from FastAPI:
{
    "message": "Hello World"
}OpenAPI Webhooks
Generate Clients
Generate Clients 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
Path Operation Advanced Configuration
Additional Status Codes
Return a Response Directly
Custom Response - HTML, Stream, File, others
Additional Responses in OpenAPI
Response Cookies
Response Headers
Response - Change Status Code
Advanced Dependencies
Advanced Security
Using the Request Directly
Using Dataclasses
Advanced Middleware
Sub Applications - Mounts
Behind a Proxy
Templates
WebSockets
Lifespan Events
Testing WebSockets
Testing Events: startup - shutdown
Testing Dependencies with Overrides
Async Tests
Settings and Environment Variables
OpenAPI Callbacks
OpenAPI Webhooks
Including WSGI - Flask, Django, others
Generate Clients
FastAPI CLI
Deployment
How To - Recipes
Table of contents
OpenAPI Client Generators
Client and SDK Generators - Generate a TypeScript Frontend Client
API Docs
Generate a TypeScript Client
Install openapi-ts
Generate Client Code
Try Out the Client Code
FastAPI App with Tags
Generate a TypeScript Client with Tags
Client Method Names
Custom Operation IDs and Better Method Names
Custom Generate Unique ID Function
Generate a TypeScript Client with Custom Operation IDs
Preprocess the OpenAPI Specification for the Client Generator
Generate a TypeScript Client with the Preprocessed OpenAPI
Benefits
Advanced User Guide
Generate Clients¶
As FastAPI is based on the OpenAPI specification, you get automatic compatibility with many tools, including the automatic API docs (provided by Swagger UI).One particular advantage that is not necessarily obvious is that you can generate clients (sometimes called SDKs ) for your API, for many different programming languages.OpenAPI Client Generators¶
There are many tools to generate clients from OpenAPI.A common tool is OpenAPI Generator.If you are building a frontend, a very interesting alternative is openapi-ts.Client and SDK Generators - Sponsor¶
There are also some company-backed Client and SDK generators based on OpenAPI (FastAPI), in some cases they can offer you additional features on top of high-quality generated SDKs/clients.Some of them also ✨ sponsor FastAPI ✨, this ensures the continued and healthy development of FastAPI and its ecosystem.And it shows their true commitment to FastAPI and its community (you), as they not only want to provide you a good service but also want to make sure you have a good and healthy framework, FastAPI. 🙇For example, you might want to try:Speakeasy
Stainless
liblab
There are also several other companies offering similar services that you can search and find online. 🤓Generate a TypeScript Frontend Client¶
Let's start with a simple FastAPI application:
from fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    price: float
class ResponseMessage(BaseModel):
    message: str
@app.post("/items/", response_model=ResponseMessage)
async def create_item(item: Item):
    return {"message": "item received"}
@app.get("/items/", response_model=list[Item])
async def get_items():
    return [
        {"name": "Plumbus", "price": 3},
        {"name": "Portal Gun", "price": 9001},
    ]🤓 Other versions and variants
Notice that the path operations define the models they use for request payload and response payload, using the models Item and ResponseMessage.API Docs¶
If you go to the API docs, you will see that it has the schemas for the data to be sent in requests and received in responses:You can see those schemas because they were declared with the models in the app.That information is available in the app's OpenAPI schema, and then shown in the API docs (by Swagger UI).And that same information from the models that is included in OpenAPI is what can be used to generate the client code.Generate a TypeScript Client¶
Now that we have the app with the models, we can generate the client code for the frontend.Install openapi-ts¶
You can install openapi-ts in your frontend code with:
Generate Client Code¶
To generate the client code you can use the command line application openapi-ts that would now be installed.Because it is installed in the local project, you probably wouldn't be able to call that command directly, but you would put it on your package.json file.It could look like this:
{
  "name": "frontend-app",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "generate-client": "openapi-ts --input http://localhost:8000/openapi.json --output ./src/client --client axios"
  },
  "author": "",
  "license": "",
  "devDependencies": {
    "@hey-api/openapi-ts": "^0.27.38",
    "typescript": "^4.6.2"
  }
}
After having that NPM generate-client script there, you can run it with:
That command will generate code in ./src/client and will use axios (the frontend HTTP library) internally.Try Out the Client Code¶
Now you can import and use the client code, it could look like this, notice that you get autocompletion for the methods:You will also get autocompletion for the payload to send:TipNotice the autocompletion for name and price, that was defined in the FastAPI application, in the Item model.You will have inline errors for the data that you send:The response object will also have autocompletion:FastAPI App with Tags¶
In many cases your FastAPI app will be bigger, and you will probably use tags to separate different groups of path operations.For example, you could have a section for items and another section for users, and they could be separated by tags:
from fastapi import from pydantic import BaseModelapp = FastAPI()
class Item(BaseModel):
    name: str
    price: float
class ResponseMessage(BaseModel):
    message: str
class User(BaseModel):
    username: str
    email: str
@app.post("/items/", response_model=ResponseMessage, tags=["items"])
async def create_item(item: Item):
    return {"message": "Item received"}
@app.get("/items/", response_model=list[Item], tags=["items"])
async def get_items():
    return [
        {"name": "Plumbus", "price": 3},
        {"name": "Portal Gun", "price": 9001},
    ]
@app.post("/users/", response_model=ResponseMessage, tags=["users"])
async def create_user(user: User):
    return {"message": "User received"}🤓 Other versions and variants
Generate a TypeScript Client with Tags¶
If you generate a client for a FastAPI app using tags, it will normally also separate the client code based on the tags.This way you will be able to have things ordered and grouped correctly for the client code:In this case you have:ItemsService
UsersService
Client Method Names¶
Right now the generated method names like createItemItemsPost don't look very clean:
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
...that's because the client generator uses the OpenAPI internal operation ID for each path operation.OpenAPI requires that each operation ID is unique across all the path operations, so FastAPI uses the function name, the path, and the HTTP method/operation to generate that operation ID, because that way it can make sure that the operation IDs are unique.But I'll show you how to improve that next. 🤓Custom Operation IDs and Better Method Names¶
You can modify the way these operation IDs are generated to make them simpler and have simpler method names in the clients.In this case you will have to ensure that each operation ID is unique in some other way.For example, you could make sure that each path operation has a tag, and then generate the operation ID based on the tag and the path operation name (the function name).Custom Generate Unique ID Function¶
FastAPI uses a unique ID for each path operation, it is used for the operation ID and also for the names of any needed custom models, for requests or responses.You can customize that function. It takes an APIRoute and outputs a string.For example, here it is using the first tag (you will probably have only one tag) and the path operation name (the function name).You can then pass that custom function to FastAPI as the generate_unique_id_function parameter:
from fastapi import from fastapi.routing import APIRoute
from pydantic import BaseModel
def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"
app = FastAPI(generate_unique_id_function=custom_generate_unique_id)
class Item(BaseModel):
    name: str
    price: float
class ResponseMessage(BaseModel):
    message: str
class User(BaseModel):
    username: str
    email: str
@app.post("/items/", response_model=ResponseMessage, tags=["items"])
async def create_item(item: Item):
    return {"message": "Item received"}
@app.get("/items/", response_model=list[Item], tags=["items"])
async def get_items():
    return [
        {"name": "Plumbus", "price": 3},
        {"name": "Portal Gun", "price": 9001},
    ]
@app.post("/users/", response_model=ResponseMessage, tags=["users"])
async def create_user(user: User):
    return {"message": "User received"}🤓 Other versions and variants
Generate a TypeScript Client with Custom Operation IDs¶
Now if you generate the client again, you will see that it has the improved method names:As you see, the method names now have the tag and then the function name, now they don't include information from the URL path and the HTTP operation.Preprocess the OpenAPI Specification for the Client Generator¶
The generated code still has some duplicated information.We already know that this method is related to the items because that word is in the ItemsService (taken from the tag), but we still have the tag name prefixed in the method name too. 😕We will probably still want to keep it for OpenAPI in general, as that will ensure that the operation IDs are unique.But for the generated client we could modify the OpenAPI operation IDs right before generating the clients, just to make those method names nicer and cleaner.We could download the OpenAPI JSON to a file openapi.json and then we could remove that prefixed tag with a script like this:Node.jsimport json
from pathlib import Pathfile_path = Path("./openapi.json")
openapi_content = json.loads(file_path.read_text())for path_data in openapi_content["paths"].values():
    for operation in path_data.values():
        tag = operation["tags"][0]
        operation_id = operation["operationId"]
        to_remove = f"{tag}-"
        new_operation_id = operation_id[len(to_remove) :]
        operation["operationId"] = new_operation_idfile_path.write_text(json.dumps(openapi_content))With that, the operation IDs would be renamed from things like items-get_items to just get_items, that way the client generator can generate simpler method names.Generate a TypeScript Client with the Preprocessed OpenAPI¶
Now as the end result is in a file openapi.json, you would modify the package.json to use that local file, for example:
{
  "name": "frontend-app",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "generate-client": "openapi-ts --input ./openapi.json --output ./src/client --client axios"
  },
  "author": "",
  "license": "",
  "devDependencies": {
    "@hey-api/openapi-ts": "^0.27.38",
    "typescript": "^4.6.2"
  }
}
After generating the new client, you would now have clean method names, with all the autocompletion, inline errors, etc:Benefits¶
When using the automatically generated clients you would get autocompletion for:Methods.
Request payloads in the body, query parameters, etc.
Response payloads.
You would also have inline errors for everything.And whenever you update the backend code, and regenerate the frontend, it would have any new path operations available as methods, the old ones removed, and any other change would be reflected on the generated code. 🤓This also means that if something changed it will be reflected on the client code automatically. And if you build the client it will error out if you have any mismatch in the data used.So, you would detect many errors very early in the development cycle instead of having to wait for the errors to show up to your final users in production and then trying to debug where the problem is. ✨
Including WSGI - Flask, Django, others
FastAPI CLI
Deployment 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
About FastAPI versions
About HTTPS
Run a Server Manually
Deployments Concepts
Deploy FastAPI on Cloud Providers
Server Workers - Uvicorn with Workers
FastAPI in Containers - Docker
How To - Recipes
Table of contents
What Does Deployment Mean
Deployment Strategies
Deployment
Deployment¶
Deploying a FastAPI application is relatively easy.What Does Deployment Mean¶
To deploy an application means to perform the necessary steps to make it available to the users.For a web API, it normally involves putting it in a remote machine, with a server program that provides good performance, stability, etc, so that your users can access the application efficiently and without interruptions or problems.This is in contrast to the development stages, where you are constantly changing the code, breaking it and fixing it, stopping and restarting the development server, etc.Deployment Strategies¶
There are several ways to do it depending on your specific use case and the tools that you use.You could deploy a server yourself using a combination of tools, you could use a cloud service that does part of the work for you, or other possible options.I will show you some of the main concepts you should probably keep in mind when deploying a FastAPI application (although most of it applies to any other type of web application).You will see more details to keep in mind and some of the techniques to do it in the next sections. ✨
FastAPI CLI
About FastAPI versions
About FastAPI versions 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
About FastAPI versions
About HTTPS
Run a Server Manually
Deployments Concepts
Deploy FastAPI on Cloud Providers
Server Workers - Uvicorn with Workers
FastAPI in Containers - Docker
How To - Recipes
Table of contents
Pin your fastapi version
Available versions
About versions
Upgrading the FastAPI versions
About Starlette
About Pydantic
Deployment
About FastAPI versions¶
FastAPI is already being used in production in many applications and systems. And the test coverage is kept at 100%. But its development is still moving quickly.New features are added frequently, bugs are fixed regularly, and the code is still continuously improving.That's why the current versions are still 0.x.x, this reflects that each version could potentially have breaking changes. This follows the Semantic Versioning conventions.You can create production applications with FastAPI right now (and you have probably been doing it for some time), you just have to make sure that you use a version that works correctly with the rest of your code.Pin your fastapi version¶
The first thing you should do is to "pin" the version of FastAPI you are using to the specific latest version that you know works correctly for your application.For example, let's say you are using version 0.112.0 in your app.If you use a requirements.txt file you could specify the version with:
fastapi[standard]==0.112.0
that would mean that you would use exactly the version 0.112.0.Or you could also pin it with:
fastapi[standard]>=0.112.0,<0.113.0
that would mean that you would use the versions 0.112.0 or above, but less than 0.113.0, for example, a version 0.112.2 would still be accepted.If you use any other tool to manage your installations, like uv, Poetry, Pipenv, or others, they all have a way that you can use to define specific versions for your packages.Available versions¶
You can see the available versions (e.g. to check what is the current latest) in the Release Notes.About versions¶
Following the Semantic Versioning conventions, any version below 1.0.0 could potentially add breaking changes.FastAPI also follows the convention that any "PATCH" version change is for bug fixes and non-breaking changes.TipThe "PATCH" is the last number, for example, in 0.2.3, the PATCH version is 3.So, you should be able to pin to a version like:
fastapi>=0.45.0,<0.46.0
Breaking changes and new features are added in "MINOR" versions.TipThe "MINOR" is the number in the middle, for example, in 0.2.3, the MINOR version is 2.Upgrading the FastAPI versions¶
You should add tests for your app.With FastAPI it's very easy (thanks to Starlette), check the docs: TestingAfter you have tests, then you can upgrade the FastAPI version to a more recent one, and make sure that all your code is working correctly by running your tests.If everything is working, or after you make the necessary changes, and all your tests are passing, then you can pin your fastapi to that new recent version.About Starlette¶
You shouldn't pin the version of starlette.Different versions of FastAPI will use a specific newer version of Starlette.So, you can just let FastAPI use the correct Starlette version.About Pydantic¶
Pydantic includes the tests for FastAPI with its own tests, so new versions of Pydantic (above 1.0.0) are always compatible with FastAPI.You can pin Pydantic to any version above 1.0.0 that works for you.For example:
pydantic>=2.7.0,<3.0.0Deployment
About HTTPS
About HTTPS 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
About FastAPI versions
About HTTPS
Run a Server Manually
Deployments Concepts
Deploy FastAPI on Cloud Providers
Server Workers - Uvicorn with Workers
FastAPI in Containers - Docker
How To - Recipes
Table of contents
Let's Encrypt
HTTPS for Developers
Domain Name
DNS
TLS Handshake Start
TLS with SNI Extension
HTTPS Request
Decrypt the Request
HTTP Response
HTTPS Response
Multiple Applications
Certificate Renewal
Recap
Deployment
About HTTPS¶
It is easy to assume that HTTPS is something that is just "enabled" or not.But it is way more complex than that.TipIf you are in a hurry or don't care, continue with the next sections for step by step instructions to set everything up with different techniques.To learn the basics of HTTPS, from a consumer perspective, check https://howhttps.works/.Now, from a developer's perspective, here are several things to keep in mind while thinking about HTTPS:For HTTPS, the server needs to have "certificates" generated by a third party.
Those certificates are actually acquired from the third party, not "generated".
Certificates have a lifetime.
They expire.
And then they need to be renewed, acquired again from the third party.
The encryption of the connection happens at the TCP level.
That's one layer below HTTP.
So, the certificate and encryption handling is done before HTTP.
TCP doesn't know about "domains". Only about IP addresses.
The information about the specific domain requested goes in the HTTP data.
The HTTPS certificates "certify" a certain domain, but the protocol and encryption happen at the TCP level, before knowing which domain is being dealt with.
By default, that would mean that you can only have one HTTPS certificate per IP address.
No matter how big your server is or how small each application you have on it might be.
There is a solution to this, however.
There's an extension to the TLS protocol (the one handling the encryption at the TCP level, before HTTP) called SNI.
This SNI extension allows one single server (with a single IP address) to have several HTTPS certificates and serve multiple HTTPS domains/applications.
For this to work, a single component (program) running on the server, listening on the public IP address, must have all the HTTPS certificates in the server.
After obtaining a secure connection, the communication protocol is still HTTP.
The contents are encrypted, even though they are being sent with the HTTP protocol.
It is a common practice to have one program/HTTP server running on the server (the machine, host, etc.) and managing all the HTTPS parts: receiving the encrypted HTTPS requests, sending the decrypted HTTP requests to the actual HTTP application running in the same server (the FastAPI application, in this case), take the HTTP response from the application, encrypt it using the appropriate HTTPS certificate and sending it back to the client using HTTPS. This server is often called a TLS Termination Proxy.Some of the options you could use as a TLS Termination Proxy are:Traefik (that can also handle certificate renewals)
Caddy (that can also handle certificate renewals)
Nginx
HAProxy
Let's Encrypt¶
Before Let's Encrypt, these HTTPS certificates were sold by trusted third parties.The process to acquire one of these certificates used to be cumbersome, require quite some paperwork and the certificates were quite expensive.But then Let's Encrypt was created.It is a project from the Linux Foundation. It provides HTTPS certificates for free, in an automated way. These certificates use all the standard cryptographic security, and are short-lived (about 3 months), so the security is actually better because of their reduced lifespan.The domains are securely verified and the certificates are generated automatically. This also allows automating the renewal of these certificates.The idea is to automate the acquisition and renewal of these certificates so that you can have secure HTTPS, for free, forever.HTTPS for Developers¶
Here's an example of how an HTTPS API could look like, step by step, paying attention mainly to the ideas important for developers.Domain Name¶
It would probably all start by you acquiring some domain name. Then, you would configure it in a DNS server (possibly your same cloud provider).You would probably get a cloud server (a virtual machine) or something similar, and it would have a fixed public IP address.In the DNS server(s) you would configure a record (an "A record") to point your domain to the public IP address of your server.You would probably do this just once, the first time, when setting everything up.TipThis Domain Name part is way before HTTPS, but as everything depends on the domain and the IP address, it's worth mentioning it here.DNS¶
Now let's focus on all the actual HTTPS parts.First, the browser would check with the DNS servers what is the IP for the domain, in this case, someapp.example.com.The DNS servers would tell the browser to use some specific IP address. That would be the public IP address used by your server, that you configured in the DNS servers.TLS Handshake Start¶
The browser would then communicate with that IP address on port 443 (the HTTPS port).The first part of the communication is just to establish the connection between the client and the server and to decide the cryptographic keys they will use, etc.This interaction between the client and the server to establish the TLS connection is called the TLS handshake.TLS with SNI Extension¶
Only one process in the server can be listening on a specific port in a specific IP address. There could be other processes listening on other ports in the same IP address, but only one for each combination of IP address and port.TLS (HTTPS) uses the specific port 443 by default. So that's the port we would need.As only one process can be listening on this port, the process that would do it would be the TLS Termination Proxy.The TLS Termination Proxy would have access to one or more TLS certificates (HTTPS certificates).Using the SNI extension discussed above, the TLS Termination Proxy would check which of the TLS (HTTPS) certificates available it should use for this connection, using the one that matches the domain expected by the client.In this case, it would use the certificate for someapp.example.com.The client already trusts the entity that generated that TLS certificate (in this case Let's Encrypt, but we'll see about that later), so it can verify that the certificate is valid.Then, using the certificate, the client and the TLS Termination Proxy decide how to encrypt the rest of the TCP communication. This completes the TLS Handshake part.After this, the client and the server have an encrypted TCP connection, this is what TLS provides. And then they can use that connection to start the actual HTTP communication.And that's what HTTPS is, it's just plain HTTP inside a secure TLS connection instead of a pure (unencrypted) TCP connection.TipNotice that the encryption of the communication happens at the TCP level, not at the HTTP level.HTTPS Request¶
Now that the client and server (specifically the browser and the TLS Termination Proxy) have an encrypted TCP connection, they can start the HTTP communication.So, the client sends an HTTPS request. This is just an HTTP request through an encrypted TLS connection.Decrypt the Request¶
The TLS Termination Proxy would use the encryption agreed to decrypt the request, and would transmit the plain (decrypted) HTTP request to the process running the application (for example a process with Uvicorn running the FastAPI application).HTTP Response¶
The application would process the request and send a plain (unencrypted) HTTP response to the TLS Termination Proxy.HTTPS Response¶
The TLS Termination Proxy would then encrypt the response using the cryptography agreed before (that started with the certificate for someapp.example.com), and send it back to the browser.Next, the browser would verify that the response is valid and encrypted with the right cryptographic key, etc. It would then decrypt the response and process it.The client (browser) will know that the response comes from the correct server because it is using the cryptography they agreed using the HTTPS certificate before.Multiple Applications¶
In the same server (or servers), there could be multiple applications, for example, other API programs or a database.Only one process can be handling the specific IP and port (the TLS Termination Proxy in our example) but the other applications/processes can be running on the server(s) too, as long as they don't try to use the same combination of public IP and port.That way, the TLS Termination Proxy could handle HTTPS and certificates for multiple domains, for multiple applications, and then transmit the requests to the right application in each case.Certificate Renewal¶
At some point in the future, each certificate would expire (about 3 months after acquiring it).And then, there would be another program (in some cases it's another program, in some cases it could be the same TLS Termination Proxy) that would talk to Let's Encrypt, and renew the certificate(s).The TLS certificates are associated with a domain name, not with an IP address.So, to renew the certificates, the renewal program needs to prove to the authority (Let's Encrypt) that it indeed "owns" and controls that domain.To do that, and to accommodate different application needs, there are several ways it can do it. Some popular ways are:Modify some DNS records.
For this, the renewal program needs to support the APIs of the DNS provider, so, depending on the DNS provider you are using, this might or might not be an option.
Run as a server (at least during the certificate acquisition process) on the public IP address associated with the domain.
As we said above, only one process can be listening on a specific IP and port.
This is one of the reasons why it's very useful when the same TLS Termination Proxy also takes care of the certificate renewal process.
Otherwise, you might have to stop the TLS Termination Proxy momentarily, start the renewal program to acquire the certificates, then configure them with the TLS Termination Proxy, and then restart the TLS Termination Proxy. This is not ideal, as your app(s) will not be available during the time that the TLS Termination Proxy is off.
All this renewal process, while still serving the app, is one of the main reasons why you would want to have a separate system to handle HTTPS with a TLS Termination Proxy instead of just using the TLS certificates with the application server directly (e.g. Uvicorn).Recap¶
Having HTTPS is very important, and quite critical in most cases. Most of the effort you as a developer have to put around HTTPS is just about understanding these concepts and how they work.But once you know the basic information of HTTPS for developers you can easily combine and configure different tools to help you manage everything in a simple way.In some of the next chapters, I'll show you several concrete examples of how to set up HTTPS for FastAPI applications. 🔒
About FastAPI versions
Run a Server Manually
Run a Server Manually 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
About FastAPI versions
About HTTPS
Run a Server Manually
Deployments Concepts
Deploy FastAPI on Cloud Providers
Server Workers - Uvicorn with Workers
FastAPI in Containers - Docker
How To - Recipes
Table of contents
Use the fastapi run Command
ASGI Servers
Server Machine and Server Program
Install the Server Program
Run the Server Program
Deployment Concepts
Deployment
Run a Server Manually¶
Use the fastapi run Command¶
In short, use fastapi run to serve your FastAPI application:
fast →
fas
That would work for most of the cases. 😎You could use that command for example to start your FastAPI app in a container, in a server, etc.ASGI Servers¶
Let's go a little deeper into the details.FastAPI uses a standard for building Python web frameworks and servers called ASGI. FastAPI is an ASGI web framework.The main thing you need to run a FastAPI application (or any other ASGI application) in a remote server machine is an ASGI server program like Uvicorn, this is the one that comes by default in the fastapi command.There are several alternatives, including:Uvicorn: a high performance ASGI server.
Hypercorn: an ASGI server compatible with HTTP/2 and Trio among other features.
Daphne: the ASGI server built for Django Channels.
Granian: A Rust HTTP server for Python applications.
NGINX Unit: NGINX Unit is a lightweight and versatile web application runtime.
Server Machine and Server Program¶
There's a small detail about names to keep in mind. 💡The word "server" is commonly used to refer to both the remote/cloud computer (the physical or virtual machine) and also the program that is running on that machine (e.g. Uvicorn).Just keep in mind that when you read "server" in general, it could refer to one of those two things.When referring to the remote machine, it's common to call it server, but also machine, VM (virtual machine), node. Those all refer to some type of remote machine, normally running Linux, where you run programs.Install the Server Program¶
When you install FastAPI, it comes with a production server, Uvicorn, and you can start it with the fastapi run command.But you can also install an ASGI server manually.Make sure you create a virtual environment, activate it, and then you can install the server application.For example, to install Uvicorn:
A similar process would apply to any other ASGI server program.TipBy adding the standard, Uvicorn will install and use some recommended extra dependencies.That including uvloop, the high-performance drop-in replacement for asyncio, that provides the big concurrency performance boost.When you install FastAPI with something like pip install "fastapi[standard]" you already get uvicorn[standard] as well.Run the Server Program¶
If you installed an ASGI server manually, you would normally need to pass an import string in a special format for it to import your FastAPI application:NoteThe command uvicorn main:app refers to:main: the file main.py (the Python "module").
app: the object created inside of main.py with the line app = FastAPI().
It is equivalent to:
from main import app
Each alternative ASGI server program would have a similar command, you can read more in their respective documentation.WarningUvicorn and other servers support a --reload option that is useful during development.The --reload option consumes much more resources, is more unstable, etc.It helps a lot during development, but you shouldn't use it in production.Deployment Concepts¶
These examples run the server program (e.g Uvicorn), starting a single process, listening on all the IPs (0.0.0.0) on a predefined port (e.g. 80).This is the basic idea. But you will probably want to take care of some additional things, like:Security - HTTPS
Running on startup
Restarts
Replication (the number of processes running)
Memory
Previous steps before starting
I'll tell you more about each of these concepts, how to think about them, and some concrete examples with strategies to handle them in the next chapters. 🚀
About HTTPS
Deployments Concepts
Deployments Concepts 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
About FastAPI versions
About HTTPS
Run a Server Manually
Deployments Concepts
Deploy FastAPI on Cloud Providers
Server Workers - Uvicorn with Workers
FastAPI in Containers - Docker
How To - Recipes
Table of contents
Security - HTTPS
Example Tools for HTTPS
Program and Process
What is a Program
What is a Process
Running on Startup
In a Remote Server
Run Automatically on Startup
Separate Program
Example Tools to Run at Startup
Restarts
We Make Mistakes
Small Errors Automatically Handled
Bigger Errors - Crashes
Restart After Crash
Example Tools to Restart Automatically
Replication - Processes and Memory
Multiple Processes - Workers
Worker Processes and Ports
Memory per Process
Server Memory
Multiple Processes - An Example
Examples of Replication Tools and Strategies
Previous Steps Before Starting
Examples of Previous Steps Strategies
Resource Utilization
Recap
Deployment
Deployments Concepts¶
When deploying a FastAPI application, or actually, any type of web API, there are several concepts that you probably care about, and using them you can find the most appropriate way to deploy your application.Some of the important concepts are:Security - HTTPS
Running on startup
Restarts
Replication (the number of processes running)
Memory
Previous steps before starting
We'll see how they would affect deployments.In the end, the ultimate objective is to be able to serve your API clients in a way that is secure, to avoid disruptions, and to use the compute resources (for example remote servers/virtual machines) as efficiently as possible. 🚀I'll tell you a bit more about these concepts here, and that would hopefully give you the intuition you would need to decide how to deploy your API in very different environments, possibly even in future ones that don't exist yet.By considering these concepts, you will be able to evaluate and design the best way to deploy your own APIs.In the next chapters, I'll give you more concrete recipes to deploy FastAPI applications.But for now, let's check these important conceptual ideas. These concepts also apply to any other type of web API. 💡Security - HTTPS¶
In the previous chapter about HTTPS we learned about how HTTPS provides encryption for your API.We also saw that HTTPS is normally provided by a component external to your application server, a TLS Termination Proxy.And there has to be something in charge of renewing the HTTPS certificates, it could be the same component or it could be something different.Example Tools for HTTPS¶
Some of the tools you could use as a TLS Termination Proxy are:Traefik
Automatically handles certificates renewals ✨
Caddy
Automatically handles certificates renewals ✨
Nginx
With an external component like Certbot for certificate renewals
HAProxy
With an external component like Certbot for certificate renewals
Kubernetes with an Ingress Controller like Nginx
With an external component like cert-manager for certificate renewals
Handled internally by a cloud provider as part of their services (read below 👇)
Another option is that you could use a cloud service that does more of the work including setting up HTTPS. It could have some restrictions or charge you more, etc. But in that case, you wouldn't have to set up a TLS Termination Proxy yourself.I'll show you some concrete examples in the next chapters.Then the next concepts to consider are all about the program running your actual API (e.g. Uvicorn).Program and Process¶
We will talk a lot about the running "process", so it's useful to have clarity about what it means, and what's the difference with the word "program".What is a Program¶
The word program is commonly used to describe many things:The code that you write, the Python files.
The file that can be executed by the operating system, for example: python, python.exe or uvicorn.
A particular program while it is running on the operating system, using the CPU, and storing things on memory. This is also called a process.
What is a Process¶
The word process is normally used in a more specific way, only referring to the thing that is running in the operating system (like in the last point above):A particular program while it is running on the operating system.
This doesn't refer to the file, nor to the code, it refers specifically to the thing that is being executed and managed by the operating system.
Any program, any code, can only do things when it is being executed. So, when there's a process running.
The process can be terminated (or "killed") by you, or by the operating system. At that point, it stops running/being executed, and it can no longer do things.
Each application that you have running on your computer has some process behind it, each running program, each window, etc. And there are normally many processes running at the same time while a computer is on.
There can be multiple processes of the same program running at the same time.
If you check out the "task manager" or "system monitor" (or similar tools) in your operating system, you will be able to see many of those processes running.And, for example, you will probably see that there are multiple processes running the same browser program (Firefox, Chrome, Edge, etc). They normally run one process per tab, plus some other extra processes.Now that we know the difference between the terms process and program, let's continue talking about deployments.Running on Startup¶
In most cases, when you create a web API, you want it to be always running, uninterrupted, so that your clients can always access it. This is of course, unless you have a specific reason why you want it to run only in certain situations, but most of the time you want it constantly running and available.In a Remote Server¶
When you set up a remote server (a cloud server, a virtual machine, etc.) the simplest thing you can do is use fastapi run (which uses Uvicorn) or something similar, manually, the same way you do when developing locally.And it will work and will be useful during development.But if your connection to the server is lost, the running process will probably die.And if the server is restarted (for example after updates, or migrations from the cloud provider) you probably won't notice it. And because of that, you won't even know that you have to restart the process manually. So, your API will just stay dead. 😱Run Automatically on Startup¶
In general, you will probably want the server program (e.g. Uvicorn) to be started automatically on server startup, and without needing any human intervention, to have a process always running with your API (e.g. Uvicorn running your FastAPI app).Separate Program¶
To achieve this, you will normally have a separate program that would make sure your application is run on startup. And in many cases, it would also make sure other components or applications are also run, for example, a database.Example Tools to Run at Startup¶
Some examples of the tools that can do this job are:Docker
Kubernetes
Docker Compose
Docker in Swarm Mode
Systemd
Supervisor
Handled internally by a cloud provider as part of their services
Others...
I'll give you more concrete examples in the next chapters.Restarts¶
Similar to making sure your application is run on startup, you probably also want to make sure it is restarted after failures.We Make Mistakes¶
We, as humans, make mistakes, all the time. Software almost always has bugs hidden in different places. 🐛And we as developers keep improving the code as we find those bugs and as we implement new features (possibly adding new bugs too 😅).Small Errors Automatically Handled¶
When building web APIs with FastAPI, if there's an error in our code, FastAPI will normally contain it to the single request that triggered the error. 🛡The client will get a 500 Internal Server Error for that request, but the application will continue working for the next requests instead of just crashing completely.Bigger Errors - Crashes¶
Nevertheless, there might be cases where we write some code that crashes the entire application making Uvicorn and Python crash. 💥And still, you would probably not want the application to stay dead because there was an error in one place, you probably want it to continue running at least for the path operations that are not broken.Restart After Crash¶
But in those cases with really bad errors that crash the running process, you would want an external component that is in charge of restarting the process, at least a couple of times...Tip...Although if the whole application is just crashing immediately it probably doesn't make sense to keep restarting it forever. But in those cases, you will probably notice it during development, or at least right after deployment.So let's focus on the main cases, where it could crash entirely in some particular cases in the future, and it still makes sense to restart it.You would probably want to have the thing in charge of restarting your application as an external component, because by that point, the same application with Uvicorn and Python already crashed, so there's nothing in the same code of the same app that could do anything about it.Example Tools to Restart Automatically¶
In most cases, the same tool that is used to run the program on startup is also used to handle automatic restarts.For example, this could be handled by:Docker
Kubernetes
Docker Compose
Docker in Swarm Mode
Systemd
Supervisor
Handled internally by a cloud provider as part of their services
Others...
Replication - Processes and Memory¶
With a FastAPI application, using a server program like the fastapi command that runs Uvicorn, running it once in one process can serve multiple clients concurrently.But in many cases, you will want to run several worker processes at the same time.Multiple Processes - Workers¶
If you have more clients than what a single process can handle (for example if the virtual machine is not too big) and you have multiple cores in the server's CPU, then you could have multiple processes running with the same application at the same time, and distribute all the requests among them.When you run multiple processes of the same API program, they are commonly called workers.Worker Processes and Ports¶
Remember from the docs About HTTPS that only one process can be listening on one combination of port and IP address in a serverThis is still true.So, to be able to have multiple processes at the same time, there has to be a single process listening on a port that then transmits the communication to each worker process in some way.Memory per Process¶
Now, when the program loads things in memory, for example, a machine learning model in a variable, or the contents of a large file in a variable, all that consumes a bit of the memory (RAM) of the server.And multiple processes normally don't share any memory. This means that each running process has its own things, variables, and memory. And if you are consuming a large amount of memory in your code, each process will consume an equivalent amount of memory.Server Memory¶
For example, if your code loads a Machine Learning model with 1 GB in size, when you run one process with your API, it will consume at least 1 GB of RAM. And if you start 4 processes (4 workers), each will consume 1 GB of RAM. So in total, your API will consume 4 GB of RAM.And if your remote server or virtual machine only has 3 GB of RAM, trying to load more than 4 GB of RAM will cause problems. 🚨Multiple Processes - An Example¶
In this example, there's a Manager Process that starts and controls two Worker Processes.This Manager Process would probably be the one listening on the port in the IP. And it would transmit all the communication to the worker processes.Those worker processes would be the ones running your application, they would perform the main computations to receive a request and return a response, and they would load anything you put in variables in RAM.And of course, the same machine would probably have other processes running as well, apart from your application.An interesting detail is that the percentage of the CPU used by each process can vary a lot over time, but the memory (RAM) normally stays more or less stable.If you have an API that does a comparable amount of computations every time and you have a lot of clients, then the CPU utilization will probably also be stable (instead of constantly going up and down quickly).Examples of Replication Tools and Strategies¶
There can be several approaches to achieve this, and I'll tell you more about specific strategies in the next chapters, for example when talking about Docker and containers.The main constraint to consider is that there has to be a single component handling the port in the public IP. And then it has to have a way to transmit the communication to the replicated processes/workers.Here are some possible combinations and strategies:Uvicorn with --workers
One Uvicorn process manager would listen on the IP and port, and it would start multiple Uvicorn worker processes.
Kubernetes and other distributed container systems
Something in the Kubernetes layer would listen on the IP and port. The replication would be by having multiple containers, each with one Uvicorn process running.
Cloud services that handle this for you
The cloud service will probably handle replication for you. It would possibly let you define a process to run, or a container image to use, in any case, it would most probably be a single Uvicorn process, and the cloud service would be in charge of replicating it.
TipDon't worry if some of these items about containers, Docker, or Kubernetes don't make a lot of sense yet.I'll tell you more about container images, Docker, Kubernetes, etc. in a future chapter: FastAPI in Containers - Docker.Previous Steps Before Starting¶
There are many cases where you want to perform some steps before starting your application.For example, you might want to run database migrations.But in most cases, you will want to perform these steps only once.So, you will want to have a single process to perform those previous steps, before starting the application.And you will have to make sure that it's a single process running those previous steps even if afterwards, you start multiple processes (multiple workers) for the application itself. If those steps were run by multiple processes, they would duplicate the work by running it in parallel, and if the steps were something delicate like a database migration, they could cause conflicts with each other.Of course, there are some cases where there's no problem in running the previous steps multiple times, in that case, it's a lot easier to handle.TipAlso, keep in mind that depending on your setup, in some cases you might not even need any previous steps before starting your application.In that case, you wouldn't have to worry about any of this. 🤷Examples of Previous Steps Strategies¶
This will depend heavily on the way you deploy your system, and it would probably be connected to the way you start programs, handling restarts, etc.Here are some possible ideas:An "Init Container" in Kubernetes that runs before your app container
A bash script that runs the previous steps and then starts your application
You would still need a way to start/restart that bash script, detect errors, etc.
TipI'll give you more concrete examples for doing this with containers in a future chapter: FastAPI in Containers - Docker.Resource Utilization¶
Your server(s) is (are) a resource, you can consume or utilize, with your programs, the computation time on the CPUs, and the RAM memory available.How much of the system resources do you want to be consuming/utilizing It might be easy to think "not much", but in reality, you will probably want to consume as much as possible without crashing.If you are paying for 3 servers but you are using only a little bit of their RAM and CPU, you are probably wasting money 💸, and probably wasting server electric power 🌎, etc.In that case, it could be better to have only 2 servers and use a higher percentage of their resources (CPU, memory, disk, network bandwidth, etc).On the other hand, if you have 2 servers and you are using 100% of their CPU and RAM, at some point one process will ask for more memory, and the server will have to use the disk as "memory" (which can be thousands of times slower), or even crash. Or one process might need to do some computation and would have to wait until the CPU is free again.In this case, it would be better to get one extra server and run some processes on it so that they all have enough RAM and CPU time.There's also the chance that for some reason you have a spike of usage of your API. Maybe it went viral, or maybe some other services or bots start using it. And you might want to have extra resources to be safe in those cases.You could put an arbitrary number to target, for example, something between 50% to 90% of resource utilization. The point is that those are probably the main things you will want to measure and use to tweak your deployments.You can use simple tools like htop to see the CPU and RAM used in your server or the amount used by each process. Or you can use more complex monitoring tools, which may be distributed across servers, etc.Recap¶
You have been reading here some of the main concepts that you would probably need to keep in mind when deciding how to deploy your application:Security - HTTPS
Running on startup
Restarts
Replication (the number of processes running)
Memory
Previous steps before starting
Understanding these ideas and how to apply them should give you the intuition necessary to take any decisions when configuring and tweaking your deployments. 🤓In the next sections, I'll give you more concrete examples of possible strategies you can follow. 🚀
Run a Server Manually
Deploy FastAPI on Cloud Providers
Deploy FastAPI on Cloud Providers 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
About FastAPI versions
About HTTPS
Run a Server Manually
Deployments Concepts
Deploy FastAPI on Cloud Providers
Server Workers - Uvicorn with Workers
FastAPI in Containers - Docker
How To - Recipes
Table of contents
Cloud Providers - Deployment
Deploy FastAPI on Cloud Providers¶
You can use virtually any cloud provider to deploy your FastAPI application.In most of the cases, the main cloud providers have guides to deploy FastAPI with them.Cloud Providers - Sponsors¶
Some cloud providers ✨ sponsor FastAPI ✨, this ensures the continued and healthy development of FastAPI and its ecosystem.And it shows their true commitment to FastAPI and its community (you), as they not only want to provide you a good service but also want to make sure you have a good and healthy framework, FastAPI. 🙇You might want to try their services and follow their guides:Platform.sh
Porter
Coherence
RenderDeployments Concepts
Server Workers - Uvicorn with Workers
Server Workers - Uvicorn with Workers 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
About FastAPI versions
About HTTPS
Run a Server Manually
Deployments Concepts
Deploy FastAPI on Cloud Providers
Server Workers - Uvicorn with Workers
FastAPI in Containers - Docker
How To - Recipes
Table of contents
Multiple Workers
Deployment Concepts
Containers and Docker
Recap
Deployment
Server Workers - Uvicorn with Workers¶
Let's check back those deployment concepts from before:Security - HTTPS
Running on startup
Restarts
Replication (the number of processes running)
Memory
Previous steps before starting
Up to this point, with all the tutorials in the docs, you have probably been running a server program, for example, using the fastapi command, that runs Uvicorn, running a single process.When deploying applications you will probably want to have some replication of processes to take advantage of multiple cores and to be able to handle more requests.As you saw in the previous chapter about Deployment Concepts, there are multiple strategies you can use.Here I'll show you how to use Uvicorn with worker processes using the fastapi command or the uvicorn command directly.InfoIf you are using containers, for example with Docker or Kubernetes, I'll tell you more about that in the next chapter: FastAPI in Containers - Docker.In particular, when running on Kubernetes you will probably not want to use workers and instead run a single Uvicorn process per container, but I'll tell you about it later in that chapter.Multiple Workers¶
You can start multiple workers with the --workers command line option:
uvicorn
If you use the fastapi command:The only new option here is --workers telling Uvicorn to start 4 worker processes.You can also see that it shows the PID of each process, 27365 for the parent process (this is the process manager) and one for each worker process: 27368, 27369, 27370, and 27367.Deployment Concepts¶
Here you saw how to use multiple workers to parallelize the execution of the application, take advantage of multiple cores in the CPU, and be able to serve more requests.From the list of deployment concepts from above, using workers would mainly help with the replication part, and a little bit with the restarts, but you still need to take care of the others:Security - HTTPS
Running on startup
Restarts
Replication (the number of processes running)
Memory
Previous steps before starting
Containers and Docker¶
In the next chapter about FastAPI in Containers - Docker I'll explain some strategies you could use to handle the other deployment concepts.I'll show you how to build your own image from scratch to run a single Uvicorn process. It is a simple process and is probably what you would want to do when using a distributed container management system like Kubernetes.Recap¶
You can use multiple worker processes with the --workers CLI option with the fastapi or uvicorn commands to take advantage of multi-core CPUs, to run multiple processes in parallel.You could use these tools and ideas if you are setting up your own deployment system while taking care of the other deployment concepts yourself.Check out the next chapter to learn about FastAPI with containers (e.g. Docker and Kubernetes). You will see that those tools have simple ways to solve the other deployment concepts as well. ✨
Deploy FastAPI on Cloud Providers
FastAPI in Containers - Docker
FastAPI in Containers - Docker 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
About FastAPI versions
About HTTPS
Run a Server Manually
Deployments Concepts
Deploy FastAPI on Cloud Providers
Server Workers - Uvicorn with Workers
FastAPI in Containers - Docker
How To - Recipes
Table of contents
What is a Container
What is a Container Image
Container Images
Containers and Processes
Build a Docker Image for Package Requirements
Create the FastAPI Code
Dockerfile
Use CMD - Exec Form
Directory Structure
Behind a TLS Termination Proxy
Docker Cache
Build the Docker Image
Start the Docker Container
Check it
Interactive API docs
Alternative API docs
Build a Docker Image with a Single-File Deployment Concepts
HTTPS
Running on Startup and Restarts
Replication - Number of Processes
Load Balancer
One Load Balancer - Multiple Worker Containers
One Process per Container
Containers with Multiple Processes and Special Cases
A Simple App
Docker Compose
Memory
Previous Steps Before Starting and Containers
Multiple Containers
Single Container
Base Docker Image
Deploy the Container Image
Docker Image with uv
Recap
Deployment
FastAPI in Containers - Docker¶
When deploying FastAPI applications a common approach is to build a Linux container image. It's normally done using Docker. You can then deploy that container image in one of a few possible ways.Using Linux containers has several advantages including security, replicability, simplicity, and others.TipIn a hurry and already know this stuff Jump to the Dockerfile below 👇.Dockerfile Preview 👀
What is a Container¶
Containers (mainly Linux containers) are a very lightweight way to package applications including all their dependencies and necessary files while keeping them isolated from other containers (other applications or components) in the same system.Linux containers run using the same Linux kernel of the host (machine, virtual machine, cloud server, etc). This just means that they are very lightweight (compared to full virtual machines emulating an entire operating system).This way, containers consume little resources, an amount comparable to running the processes directly (a virtual machine would consume much more).Containers also have their own isolated running processes (commonly just one process), file system, and network, simplifying deployment, security, development, etc.What is a Container Image¶
A container is run from a container image.A container image is a static version of all the files, environment variables, and the default command/program that should be present in a container. Static here means that the container image is not running, it's not being executed, it's only the packaged files and metadata.In contrast to a "container image" that is the stored static contents, a "container" normally refers to the running instance, the thing that is being executed.When the container is started and running (started from a container image) it could create or change files, environment variables, etc. Those changes will exist only in that container, but would not persist in the underlying container image (would not be saved to disk).A container image is comparable to the program file and contents, e.g. python and some file main.py.And the container itself (in contrast to the container image) is the actual running instance of the image, comparable to a process. In fact, a container is running only when it has a process running (and normally it's only a single process). The container stops when there's no process running in it.Container Images¶
Docker has been one of the main tools to create and manage container images and containers.And there's a public Docker Hub with pre-made official container images for many tools, environments, databases, and applications.For example, there's an official Python Image.And there are many other images for different things like databases, for example for:PostgreSQL
MySQL
MongoDB
Redis, etc.
By using a pre-made container image it's very easy to combine and use different tools. For example, to try out a new database. In most cases, you can use the official images, and just configure them with environment variables.That way, in many cases you can learn about containers and Docker and reuse that knowledge with many different tools and components.So, you would run multiple containers with different things, like a database, a Python application, a web server with a React frontend application, and connect them together via their internal network.All the container management systems (like Docker or Kubernetes) have these networking features integrated into them.Containers and Processes¶
A container image normally includes in its metadata the default program or command that should be run when the container is started and the parameters to be passed to that program. Very similar to what would be if it was in the command line.When a container is started, it will run that command/program (although you can override it and make it run a different command/program).A container is running as long as the main process (command or program) is running.A container normally has a single process, but it's also possible to start subprocesses from the main process, and that way you will have multiple processes in the same container.But it's not possible to have a running container without at least one running process. If the main process stops, the container stops.Build a Docker Image for FastAPI¶
Okay, let's build something now! 🚀I'll show you how to build a Docker image for FastAPI from scratch, based on the official Python image.This is what you would want to do in most cases, for example:Using Kubernetes or similar tools
When running on a Raspberry Pi
Using a cloud service that would run a container image for you, etc.
Package Requirements¶
You would normally have the package requirements for your application in some file.It would depend mainly on the tool you use to install those requirements.The most common way to do it is to have a file requirements.txt with the package names and their versions, one per line.You would of course use the same ideas you read in About FastAPI versions to set the ranges of versions.For example, your requirements.txt could look like:
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
And you would normally install those package dependencies with pip, for example:
InfoThere are other formats and tools to define and install package dependencies.Create the FastAPI Code¶
Create an app directory and enter it.
Create an empty file __init__.py.
Create a main.py file with:from typing import Unionfrom fastapi import 
app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
Dockerfile¶
Now in the same project directory create a file Dockerfile with:FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
TipReview what each line does by clicking each number bubble in the code. 👆WarningMake sure to always use the exec form of the CMD instruction, as explained below.Use CMD - Exec Form¶
The CMD Docker instruction can be written using two forms:✅ Exec form:
# ✅ Do this
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
⛔️ Shell form:
# ⛔️ Don't do this
CMD fastapi run app/main.py --port 80
Make sure to always use the exec form to ensure that FastAPI can shutdown gracefully and lifespan events are triggered.You can read more about it in the Docker docs for shell and exec form.This can be quite noticeable when using docker compose. See this Docker Compose FAQ section for more technical details: Why do my services take 10 seconds to recreate or stop.Directory Structure¶
You should now have a directory structure like:
.
├── app
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt
Behind a TLS Termination Proxy¶
If you are running your container behind a TLS Termination Proxy (load balancer) like Nginx or Traefik, add the option --proxy-headers, this will tell Uvicorn (through the FastAPI CLI) to trust the headers sent by that proxy telling it that the application is running behind HTTPS, etc.
CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
Docker Cache¶
There's an important trick in this Dockerfile, we first copy the file with the dependencies alone, not the rest of the code. Let me tell you why is that.
COPY ./requirements.txt /code/requirements.txt
Docker and other tools build these container images incrementally, adding one layer on top of the other, starting from the top of the Dockerfile and adding any files created by each of the instructions of the Dockerfile.Docker and similar tools also use an internal cache when building the image, if a file hasn't changed since the last time building the container image, then it will reuse the same layer created the last time, instead of copying the file again and creating a new layer from scratch.Just avoiding the copy of files doesn't necessarily improve things too much, but because it used the cache for that step, it can use the cache for the next step. For example, it could use the cache for the instruction that installs dependencies with:
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
The file with the package requirements won't change frequently. So, by copying only that file, Docker will be able to use the cache for that step.And then, Docker will be able to use the cache for the next step that downloads and install those dependencies. And here's where we save a lot of time. ✨ ...and avoid boredom waiting. 😪😆Downloading and installing the package dependencies could take minutes, but using the cache would take seconds at most.And as you would be building the container image again and again during development to check that your code changes are working, there's a lot of accumulated time this would save.Then, near the end of the Dockerfile, we copy all the code. As this is what changes most frequently, we put it near the end, because almost always, anything after this step will not be able to use the cache.
COPY ./app /code/app
Build the Docker Image¶
Now that all the files are in place, let's build the container image.Go to the project directory (in where your Dockerfile is, containing your app directory).
Build your FastAPI image:TipNotice the . at the end, it's equivalent to ./, it tells Docker the directory to use to build the container image.In this case, it's the same current directory (.).Start the Docker Container¶
Run a container based on your image:
Check it¶
You should be able to check it in your Docker container's URL, for example: http://192.168.99.100/items/5q=somequery or http://127.0.0.1/items/5q=somequery (or equivalent, using your Docker host).You will see something like:
{"item_id": 5, "q": "somequery"}
Interactive API docs¶
Now you can go to http://192.168.99.100/docs or http://127.0.0.1/docs (or equivalent, using your Docker host).You will see the automatic interactive API documentation (provided by Swagger UI):Swagger UIAlternative API docs¶
And you can also go to http://192.168.99.100/redoc or http://127.0.0.1/redoc (or equivalent, using your Docker host).You will see the alternative automatic documentation (provided by ReDoc):ReDocBuild a Docker Image with a Single-File FastAPI¶
If your FastAPI is a single file, for example, main.py without an ./app directory, your file structure could look like this:
.
├── Dockerfile
├── main.py
└── requirements.txt
Then you would just have to change the corresponding paths to copy the file inside the Dockerfile:
FROM python:3.9WORKDIR /codeCOPY ./requirements.txt /code/requirements.txtRUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./main.py /code/
CMD ["fastapi", "run", "main.py", "--port", "80"]
When you pass the file to fastapi run it will detect automatically that it is a single file and not part of a package and will know how to import it and serve your FastAPI app. 😎Deployment Concepts¶
Let's talk again about some of the same Deployment Concepts in terms of containers.Containers are mainly a tool to simplify the process of building and deploying an application, but they don't enforce a particular approach to handle these deployment concepts, and there are several possible strategies.The good news is that with each different strategy there's a way to cover all of the deployment concepts. 🎉Let's review these deployment concepts in terms of containers:HTTPS
Running on startup
Restarts
Replication (the number of processes running)
Memory
Previous steps before starting
HTTPS¶
If we focus just on the container image for a FastAPI application (and later the running container), HTTPS normally would be handled externally by another tool.It could be another container, for example with Traefik, handling HTTPS and automatic acquisition of certificates.TipTraefik has integrations with Docker, Kubernetes, and others, so it's very easy to set up and configure HTTPS for your containers with it.Alternatively, HTTPS could be handled by a cloud provider as one of their services (while still running the application in a container).Running on Startup and Restarts¶
There is normally another tool in charge of starting and running your container.It could be Docker directly, Docker Compose, Kubernetes, a cloud service, etc.In most (or all) cases, there's a simple option to enable running the container on startup and enabling restarts on failures. For example, in Docker, it's the command line option --restart.Without using containers, making applications run on startup and with restarts can be cumbersome and difficult. But when working with containers in most cases that functionality is included by default. ✨Replication - Number of Processes¶
If you have a cluster of machines with Kubernetes, Docker Swarm Mode, Nomad, or another similar complex system to manage distributed containers on multiple machines, then you will probably want to handle replication at the cluster level instead of using a process manager (like Uvicorn with workers) in each container.One of those distributed container management systems like Kubernetes normally has some integrated way of handling replication of containers while still supporting load balancing for the incoming requests. All at the cluster level.In those cases, you would probably want to build a Docker image from scratch as explained above, installing your dependencies, and running a single Uvicorn process instead of using multiple Uvicorn workers.Load Balancer¶
When using containers, you would normally have some component listening on the main port. It could possibly be another container that is also a TLS Termination Proxy to handle HTTPS or some similar tool.As this component would take the load of requests and distribute that among the workers in a (hopefully) balanced way, it is also commonly called a Load Balancer.TipThe same TLS Termination Proxy component used for HTTPS would probably also be a Load Balancer.And when working with containers, the same system you use to start and manage them would already have internal tools to transmit the network communication (e.g. HTTP requests) from that load balancer (that could also be a TLS Termination Proxy) to the container(s) with your app.One Load Balancer - Multiple Worker Containers¶
When working with Kubernetes or similar distributed container management systems, using their internal networking mechanisms would allow the single load balancer that is listening on the main port to transmit communication (requests) to possibly multiple containers running your app.Each of these containers running your app would normally have just one process (e.g. a Uvicorn process running your FastAPI application). They would all be identical containers, running the same thing, but each with its own process, memory, etc. That way you would take advantage of parallelization in different cores of the CPU, or even in different machines.And the distributed container system with the load balancer would distribute the requests to each one of the containers with your app in turns. So, each request could be handled by one of the multiple replicated containers running your app.And normally this load balancer would be able to handle requests that go to other apps in your cluster (e.g. to a different domain, or under a different URL path prefix), and would transmit that communication to the right containers for that other application running in your cluster.One Process per Container¶
In this type of scenario, you probably would want to have a single (Uvicorn) process per container, as you would already be handling replication at the cluster level.So, in this case, you would not want to have a multiple workers in the container, for example with the --workers command line option.You would want to have just a single Uvicorn process per container (but probably multiple containers).Having another process manager inside the container (as would be with multiple workers) would only add unnecessary complexity that you are most probably already taking care of with your cluster system.Containers with Multiple Processes and Special Cases¶
Of course, there are special cases where you could want to have a container with several Uvicorn worker processes inside.In those cases, you can use the --workers command line option to set the number of workers that you want to run:
FROM python:3.9WORKDIR /codeCOPY ./requirements.txt /code/requirements.txtRUN pip install --no-cache-dir --upgrade -r /code/requirements.txtCOPY ./app /code/app
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]
Here are some examples of when that could make sense:A Simple App¶
You could want a process manager in the container if your application is simple enough that can run it on a single server, not a cluster.Docker Compose¶
You could be deploying to a single server (not a cluster) with Docker Compose, so you wouldn't have an easy way to manage replication of containers (with Docker Compose) while preserving the shared network and load balancing.Then you could want to have a single container with a process manager starting several worker processes inside.The main point is, none of these are rules written in stone that you have to blindly follow. You can use these ideas to evaluate your own use case and decide what is the best approach for your system, checking out how to manage the concepts of:Security - HTTPS
Running on startup
Restarts
Replication (the number of processes running)
Memory
Previous steps before starting
Memory¶
If you run a single process per container you will have a more or less well-defined, stable, and limited amount of memory consumed by each of those containers (more than one if they are replicated).And then you can set those same memory limits and requirements in your configurations for your container management system (for example in Kubernetes). That way it will be able to replicate the containers in the available machines taking into account the amount of memory needed by them, and the amount available in the machines in the cluster.If your application is simple, this will probably not be a problem, and you might not need to specify hard memory limits. But if you are using a lot of memory (for example with machine learning models), you should check how much memory you are consuming and adjust the number of containers that runs in each machine (and maybe add more machines to your cluster).If you run multiple processes per container you will have to make sure that the number of processes started doesn't consume more memory than what is available.Previous Steps Before Starting and Containers¶
If you are using containers (e.g. Docker, Kubernetes), then there are two main approaches you can use.Multiple Containers¶
If you have multiple containers, probably each one running a single process (for example, in a Kubernetes cluster), then you would probably want to have a separate container doing the work of the previous steps in a single container, running a single process, before running the replicated worker containers.InfoIf you are using Kubernetes, this would probably be an Init Container.If in your use case there's no problem in running those previous steps multiple times in parallel (for example if you are not running database migrations, but just checking if the database is ready yet), then you could also just put them in each container right before starting the main process.Single Container¶
If you have a simple setup, with a single container that then starts multiple worker processes (or also just one process), then you could run those previous steps in the same container, right before starting the process with the app.Base Docker Image¶
There used to be an official FastAPI Docker image: tiangolo/uvicorn-gunicorn-fastapi. But it is now deprecated. ⛔️You should probably not use this base Docker image (or any other similar one).If you are using Kubernetes (or others) and you are already setting replication at the cluster level, with multiple containers. In those cases, you are better off building an image from scratch as described above: Build a Docker Image for FastAPI.And if you need to have multiple workers, you can simply use the --workers command line option.Technical DetailsThe Docker image was created when Uvicorn didn't support managing and restarting dead workers, so it was needed to use Gunicorn with Uvicorn, which added quite some complexity, just to have Gunicorn manage and restart the Uvicorn worker processes.But now that Uvicorn (and the fastapi command) support using --workers, there's no reason to use a base Docker image instead of building your own (it's pretty much the same amount of code 😅).Deploy the Container Image¶
After having a Container (Docker) Image there are several ways to deploy it.For example:With Docker Compose in a single server
With a Kubernetes cluster
With a Docker Swarm Mode cluster
With another tool like Nomad
With a cloud service that takes your container image and deploys it
Docker Image with uv¶
If you are using uv to install and manage your project, you can follow their uv Docker guide.Recap¶
Using container systems (e.g. with Docker and Kubernetes) it becomes fairly straightforward to handle all the deployment concepts:HTTPS
Running on startup
Restarts
Replication (the number of processes running)
Memory
Previous steps before starting
In most cases, you probably won't want to use any base image, and instead build a container image from scratch based on the official Python Docker image.Taking care of the order of instructions in the Dockerfile and the Docker cache you can minimize build times, to maximize your productivity (and avoid boredom). 😎
Server Workers - Uvicorn with Workers
How To - Recipes
How To - Recipes 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
General - How To - Recipes
GraphQL
Custom Request and APIRoute class
Conditional OpenAPI
Extending OpenAPI
Separate OpenAPI Schemas for Input and Output or Not
Custom Docs UI Static Assets (Self-Hosting)
Configure Swagger UI
Testing a Database
How To - Recipes
How To - Recipes¶
Here you will see different recipes or "how to" guides for several topics.Most of these ideas would be more or less independent, and in most cases you should only need to study them if they apply directly to your project.If something seems interesting and useful to your project, go ahead and check it, but otherwise, you might probably just skip them.TipIf you want to learn FastAPI in a structured way (recommended), go and read the Tutorial - User Guide chapter by chapter instead.
FastAPI in Containers - Docker
General - How To - Recipes
General - How To - Recipes 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
General - How To - Recipes
GraphQL
Custom Request and APIRoute class
Conditional OpenAPI
Extending OpenAPI
Separate OpenAPI Schemas for Input and Output or Not
Custom Docs UI Static Assets (Self-Hosting)
Configure Swagger UI
Testing a Database
Table of contents
Filter Data - Security
Documentation Tags - OpenAPI
Documentation Summary and Description - OpenAPI
Documentation Response description - OpenAPI
Documentation Deprecate a Path Operation - OpenAPI
Convert any Data to JSON-compatible
OpenAPI Metadata - Docs
OpenAPI Custom URL
OpenAPI Docs URLs
How To - Recipes
General - How To - Recipes¶
Here are several pointers to other places in the docs, for general or frequent questions.Filter Data - Security¶
To ensure that you don't return more data than you should, read the docs for Tutorial - Response Model - Return Type.Documentation Tags - OpenAPI¶
To add tags to your path operations, and group them in the docs UI, read the docs for Tutorial - Path Operation Configurations - Tags.Documentation Summary and Description - OpenAPI¶
To add a summary and description to your path operations, and show them in the docs UI, read the docs for Tutorial - Path Operation Configurations - Summary and Description.Documentation Response description - OpenAPI¶
To define the description of the response, shown in the docs UI, read the docs for Tutorial - Path Operation Configurations - Response description.Documentation Deprecate a Path Operation - OpenAPI¶
To deprecate a path operation, and show it in the docs UI, read the docs for Tutorial - Path Operation Configurations - Deprecation.Convert any Data to JSON-compatible¶
To convert any data to JSON-compatible, read the docs for Tutorial - JSON Compatible Encoder.OpenAPI Metadata - Docs¶
To add metadata to your OpenAPI schema, including a license, version, contact, etc, read the docs for Tutorial - Metadata and Docs URLs.OpenAPI Custom URL¶
To customize the OpenAPI URL (or remove it), read the docs for Tutorial - Metadata and Docs URLs.OpenAPI Docs URLs¶
To update the URLs used for the automatically generated docs user interfaces, read the docs for Tutorial - Metadata and Docs URLs.
How To - Recipes
GraphQL
GraphQL 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
General - How To - Recipes
GraphQL
Custom Request and APIRoute class
Conditional OpenAPI
Extending OpenAPI
Separate OpenAPI Schemas for Input and Output or Not
Custom Docs UI Static Assets (Self-Hosting)
Configure Swagger UI
Testing a Database
Table of contents
GraphQL Libraries
GraphQL with Strawberry
Older GraphQLApp from Starlette
Learn More
How To - Recipes
GraphQL¶
As FastAPI is based on the ASGI standard, it's very easy to integrate any GraphQL library also compatible with ASGI.You can combine normal FastAPI path operations with GraphQL on the same application.TipGraphQL solves some very specific use cases.It has advantages and disadvantages when compared to common web APIs.Make sure you evaluate if the benefits for your use case compensate the drawbacks. 🤓GraphQL Libraries¶
Here are some of the GraphQL libraries that have ASGI support. You could use them with FastAPI:Strawberry 🍓
With docs for Ariadne
With docs for Tartiflette
With Tartiflette ASGI to provide ASGI integration
Graphene
With starlette-graphene3
GraphQL with Strawberry¶
If you need or want to work with GraphQL, Strawberry is the recommended library as it has the design closest to FastAPI's design, it's all based on type annotations.Depending on your use case, you might prefer to use a different library, but if you asked me, I would probably suggest you try Strawberry.Here's a small preview of how you could integrate Strawberry with FastAPI:
import strawberry
from fastapi import from strawberry.asgi import GraphQL
@strawberry.type
class User:
    name: str
    age: int
@strawberry.type
class Query:
    @strawberry.field
    def user(self) -> User:
        return User(name="Patrick", age=100)
schema = strawberry.Schema(query=Query)
graphql_app = GraphQL(schema)app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)You can learn more about Strawberry in the Strawberry documentation.And also the docs about Strawberry with FastAPI.Older GraphQLApp from Starlette¶
Previous versions of Starlette included a GraphQLApp class to integrate with Graphene.It was deprecated from Starlette, but if you have code that used it, you can easily migrate to starlette-graphene3, that covers the same use case and has an almost identical interface.TipIf you need GraphQL, I still would recommend you check out Strawberry, as it's based on type annotations instead of custom classes and types.Learn More¶
You can learn more about GraphQL in the official GraphQL documentation.You can also read more about each those libraries described above in their links.
General - How To - Recipes
Custom Request and APIRoute class
Custom Request and APIRoute class 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
General - How To - Recipes
GraphQL
Custom Request and APIRoute class
Conditional OpenAPI
Extending OpenAPI
Separate OpenAPI Schemas for Input and Output or Not
Custom Docs UI Static Assets (Self-Hosting)
Configure Swagger UI
Testing a Database
Table of contents
Use cases
Handling custom request body encodings
Create a custom GzipRequest class
Create a custom GzipRoute class
Accessing the request body in an exception handler
Custom APIRoute class in a router
How To - Recipes
Custom Request and APIRoute class¶
In some cases, you may want to override the logic used by the Request and APIRoute classes.In particular, this may be a good alternative to logic in a middleware.For example, if you want to read or manipulate the request body before it is processed by your application.DangerThis is an "advanced" feature.If you are just starting with FastAPI you might want to skip this section.Use cases¶
Some use cases include:Converting non-JSON request bodies to JSON (e.g. msgpack).
Decompressing gzip-compressed request bodies.
Automatically logging all request bodies.
Handling custom request body encodings¶
Let's see how to make use of a custom Request subclass to decompress gzip requests.And an APIRoute subclass to use that custom request class.Create a custom GzipRequest class¶
TipThis is a toy example to demonstrate how it works, if you need Gzip support, you can use the provided GzipMiddleware.First, we create a GzipRequest class, which will overwrite the Request.body() method to decompress the body in the presence of an appropriate header.If there's no gzip in the header, it will not try to decompress the body.That way, the same route class can handle gzip compressed or uncompressed requests.
import gzip
from typing import Callable, Listfrom fastapi import Body, FastAPI, Request, Response
from fastapi.routing import APIRoute
class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body
class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)        return custom_route_handler
app = FastAPI()
app.router.route_class = GzipRoute
@app.post("/sum")
async def sum_numbers(numbers: List[int] = Body()):
    return {"sum": sum(numbers)}Create a custom GzipRoute class¶
Next, we create a custom subclass of fastapi.routing.APIRoute that will make use of the GzipRequest.This time, it will overwrite the method APIRoute.get_route_handler().This method returns a function. And that function is what will receive a request and return a response.Here we use it to create a GzipRequest from the original request.
import gzip
from typing import Callable, Listfrom fastapi import Body, FastAPI, Request, Response
from fastapi.routing import APIRoute
class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body
class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)        return custom_route_handler
app = FastAPI()
app.router.route_class = GzipRoute
@app.post("/sum")
async def sum_numbers(numbers: List[int] = Body()):
    return {"sum": sum(numbers)}Technical DetailsA Request has a request.scope attribute, that's just a Python dict containing the metadata related to the request.A Request also has a request.receive, that's a function to "receive" the body of the request.The scope dict and receive function are both part of the ASGI specification.And those two things, scope and receive, are what is needed to create a new Request instance.To learn more about the Request check Starlette's docs about Requests.The only thing the function returned by GzipRequest.get_route_handler does differently is convert the Request to a GzipRequest.Doing this, our GzipRequest will take care of decompressing the data (if necessary) before passing it to our path operations.After that, all of the processing logic is the same.But because of our changes in GzipRequest.body, the request body will be automatically decompressed when it is loaded by FastAPI when needed.Accessing the request body in an exception handler¶
TipTo solve this same problem, it's probably a lot easier to use the body in a custom handler for RequestValidationError (Handling Errors).But this example is still valid and it shows how to interact with the internal components.We can also use this same approach to access the request body in an exception handler.All we need to do is handle the request inside a try/except block:
from typing import Callable, Listfrom fastapi import Body, FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)        return custom_route_handler
app = FastAPI()
app.router.route_class = ValidationErrorLoggingRoute
@app.post("/")
async def sum_numbers(numbers: List[int] = Body()):
    return sum(numbers)If an exception occurs, theRequest instance will still be in scope, so we can read and make use of the request body when handling the error:
from typing import Callable, Listfrom fastapi import Body, FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)        return custom_route_handler
app = FastAPI()
app.router.route_class = ValidationErrorLoggingRoute
@app.post("/")
async def sum_numbers(numbers: List[int] = Body()):
    return sum(numbers)Custom APIRoute class in a router¶
You can also set the route_class parameter of an APIRouter:
import time
from typing import Callablefrom fastapi import APIRouter, FastAPI, Request, Response
from fastapi.routing import APIRoute
class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            return response        return custom_route_handler
app = FastAPI()
router = APIRouter(route_class=TimedRoute)
@app.get("/")
async def not_timed():
    return {"message": "Not timed"}
@router.get("/timed")
async def timed():
    return {"message": "It's the time of my life"}
app.include_router(router)In this example, the path operations under the router will use the custom TimedRoute class, and will have an extra X-Response-Time header in the response with the time it took to generate the response:
import time
from typing import Callablefrom fastapi import APIRouter, FastAPI, Request, Response
from fastapi.routing import APIRoute
class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            return response        return custom_route_handler
app = FastAPI()
router = APIRouter(route_class=TimedRoute)
@app.get("/")
async def not_timed():
    return {"message": "Not timed"}
@router.get("/timed")
async def timed():
    return {"message": "It's the time of my life"}
app.include_router(router)
GraphQL
Conditional OpenAPI
Conditional OpenAPI 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
General - How To - Recipes
GraphQL
Custom Request and APIRoute class
Conditional OpenAPI
Extending OpenAPI
Separate OpenAPI Schemas for Input and Output or Not
Custom Docs UI Static Assets (Self-Hosting)
Configure Swagger UI
Testing a Database
Table of contents
About security, APIs, and docs
Conditional OpenAPI from settings and env vars
How To - Recipes
Conditional OpenAPI¶
If you needed to, you could use settings and environment variables to configure OpenAPI conditionally depending on the environment, and even disable it entirely.About security, APIs, and docs¶
Hiding your documentation user interfaces in production shouldn't be the way to protect your API.That doesn't add any extra security to your API, the path operations will still be available where they are.If there's a security flaw in your code, it will still exist.Hiding the documentation just makes it more difficult to understand how to interact with your API, and could make it more difficult for you to debug it in production. It could be considered simply a form of Security through obscurity.If you want to secure your API, there are several better things you can do, for example:Make sure you have well defined Pydantic models for your request bodies and responses.
Configure any required permissions and roles using dependencies.
Never store plaintext passwords, only password hashes.
Implement and use well-known cryptographic tools, like Passlib and JWT tokens, etc.
Add more granular permission controls with OAuth2 scopes where needed.
...etc.
Nevertheless, you might have a very specific use case where you really need to disable the API docs for some environment (e.g. for production) or depending on configurations from environment variables.Conditional OpenAPI from settings and env vars¶
You can easily use the same Pydantic settings to configure your generated OpenAPI and the docs UIs.For example:
from fastapi import from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    openapi_url: str = "/openapi.json"
settings = Settings()app = FastAPI(openapi_url=settings.openapi_url)
@app.get("/")
def root():
    return {"message": "Hello World"}Here we declare the setting openapi_url with the same default of "/openapi.json".And then we use it when creating the FastAPI app.Then you could disable OpenAPI (including the UI docs) by setting the environment variable OPENAPI_URL to the empty string, like:Then if you go to the URLs at /openapi.json, /docs, or /redoc you will just get a 404 Not Found error like:
{
    "detail": "Not Found"
}Custom Request and APIRoute class
Extending OpenAPI
Extending OpenAPI 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
General - How To - Recipes
GraphQL
Custom Request and APIRoute class
Conditional OpenAPI
Extending OpenAPI
Separate OpenAPI Schemas for Input and Output or Not
Custom Docs UI Static Assets (Self-Hosting)
Configure Swagger UI
Testing a Database
Table of contents
The normal process
Overriding the defaults
Normal Generate the OpenAPI schema
Modify the OpenAPI schema
Cache the OpenAPI schema
Override the method
Check it
How To - Recipes
Extending OpenAPI¶
There are some cases where you might need to modify the generated OpenAPI schema.In this section you will see how.The normal process¶
The normal (default) process, is as follows.A FastAPI application (instance) has an .openapi() method that is expected to return the OpenAPI schema.As part of the application object creation, a path operation for /openapi.json (or for whatever you set your openapi_url) is registered.It just returns a JSON response with the result of the application's .openapi() method.By default, what the method .openapi() does is check the property .openapi_schema to see if it has contents and return them.If it doesn't, it generates them using the utility function at fastapi.openapi.utils.get_openapi.And that function get_openapi() receives as parameters:title: The OpenAPI title, shown in the docs.
version: The version of your API, e.g. 2.5.0.
openapi_version: The version of the OpenAPI specification used. By default, the latest: 3.1.0.
summary: A short summary of the API.
description: The description of your API, this can include markdown and will be shown in the docs.
routes: A list of routes, these are each of the registered path operations. They are taken from app.routes.
InfoThe parameter summary is available in OpenAPI 3.1.0 and above, supported by FastAPI 0.99.0 and above.Overriding the defaults¶
Using the information above, you can use the same utility function to generate the OpenAPI schema and override each part that you need.For example, let's add ReDoc's OpenAPI extension to include a custom logo.Normal FastAPI¶
First, write all your FastAPI application as normally:
from fastapi import from fastapi.openapi.utils import get_openapiapp = FastAPI()
@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapiGenerate the OpenAPI schema¶
Then, use the same utility function to generate the OpenAPI schema, inside a custom_openapi() function:
from fastapi import from fastapi.openapi.utils import get_openapiapp = FastAPI()
@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapiModify the OpenAPI schema¶
Now you can add the ReDoc extension, adding a custom x-logo to the info "object" in the OpenAPI schema:
from fastapi import from fastapi.openapi.utils import get_openapiapp = FastAPI()
@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapiCache the OpenAPI schema¶
You can use the property .openapi_schema as a "cache", to store your generated schema.That way, your application won't have to generate the schema every time a user opens your API docs.It will be generated only once, and then the same cached schema will be used for the next requests.
from fastapi import from fastapi.openapi.utils import get_openapiapp = FastAPI()
@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapiOverride the method¶
Now you can replace the .openapi() method with your new function.
from fastapi import from fastapi.openapi.utils import get_openapiapp = FastAPI()
@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapiCheck it¶
Once you go to http://127.0.0.1:8000/redoc you will see that you are using your custom logo (in this example, FastAPI's logo):
Conditional OpenAPI
Separate OpenAPI Schemas for Input and Output or Not
Separate OpenAPI Schemas for Input and Output or Not 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
General - How To - Recipes
GraphQL
Custom Request and APIRoute class
Conditional OpenAPI
Extending OpenAPI
Separate OpenAPI Schemas for Input and Output or Not
Custom Docs UI Static Assets (Self-Hosting)
Configure Swagger UI
Testing a Database
Table of contents
Pydantic Models for Input and Output
Model for Input
Input Model in Docs
Model for Output
Model for Output Response Data
Model for Output in Docs
Model for Input and Output in Docs
Do not Separate Schemas
Same Schema for Input and Output Models in Docs
How To - Recipes
Separate OpenAPI Schemas for Input and Output or Not¶
When using Pydantic v2, the generated OpenAPI is a bit more exact and correct than before. 😎In fact, in some cases, it will even have two JSON Schemas in OpenAPI for the same Pydantic model, for input and output, depending on if they have default values.Let's see how that works and how to change it if you need to do that.Pydantic Models for Input and Output¶
Let's say you have a Pydantic model with default values, like this one:
from fastapi import from pydantic import BaseModel
class Item(BaseModel):
    name: str
    description: str | None = None# Code below omitted 👇👀 Full file preview
🤓 Other versions and variants
Model for Input¶
If you use this model as an input like here:
from fastapi import from pydantic import BaseModel
class Item(BaseModel):
    name: str
    description: str | None = None
app = FastAPI()
@app.post("/items/")
def create_item(item: Item):
    return item# Code below omitted 👇👀 Full file preview
🤓 Other versions and variants
...then the description field will not be required. Because it has a default value of None.Input Model in Docs¶
You can confirm that in the docs, the description field doesn't have a red asterisk, it's not marked as required:
Model for Output¶
But if you use the same model as an output, like here:
from fastapi import from pydantic import BaseModel
class Item(BaseModel):
    name: str
    description: str | None = None
app = FastAPI()
@app.post("/items/")
def create_item(item: Item):
    return item
@app.get("/items/")
def read_items() -> list[Item]:
    return [
        Item(
            name="Portal Gun",
            description="Device to travel through the multi-rick-verse",
        ),
        Item(name="Plumbus"),
    ]🤓 Other versions and variants
...then because description has a default value, if you don't return anything for that field, it will still have that default value.Model for Output Response Data¶
If you interact with the docs and check the response, even though the code didn't add anything in one of the description fields, the JSON response contains the default value (null):
This means that it will always have a value, it's just that sometimes the value could be None (or null in JSON).That means that, clients using your API don't have to check if the value exists or not, they can assume the field will always be there, but just that in some cases it will have the default value of None.The way to describe this in OpenAPI, is to mark that field as required, because it will always be there.Because of that, the JSON Schema for a model can be different depending on if it's used for input or output:for input the description will not be required
for output it will be required (and possibly None, or in JSON terms, null)
Model for Output in Docs¶
You can check the output model in the docs too, both name and description are marked as required with a red asterisk:
Model for Input and Output in Docs¶
And if you check all the available Schemas (JSON Schemas) in OpenAPI, you will see that there are two, one Item-Input and one Item-Output.For Item-Input, description is not required, it doesn't have a red asterisk.But for Item-Output, description is required, it has a red asterisk.
With this feature from Pydantic v2, your API documentation is more precise, and if you have autogenerated clients and SDKs, they will be more precise too, with a better developer experience and consistency. 🎉Do not Separate Schemas¶
Now, there are some cases where you might want to have the same schema for input and output.Probably the main use case for this is if you already have some autogenerated client code/SDKs and you don't want to update all the autogenerated client code/SDKs yet, you probably will want to do it at some point, but maybe not right now.In that case, you can disable this feature in FastAPI, with the parameter separate_input_output_schemas=False.InfoSupport for separate_input_output_schemas was added in FastAPI 0.102.0. 🤓
from fastapi import from pydantic import BaseModel
class Item(BaseModel):
    name: str
    description: str | None = None
app = FastAPI(separate_input_output_schemas=False)
@app.post("/items/")
def create_item(item: Item):
    return item
@app.get("/items/")
def read_items() -> list[Item]:
    return [
        Item(
            name="Portal Gun",
            description="Device to travel through the multi-rick-verse",
        ),
        Item(name="Plumbus"),
    ]🤓 Other versions and variants
Same Schema for Input and Output Models in Docs¶
And now there will be one single schema for input and output for the model, only Item, and it will have description as not required:
This is the same behavior as in Pydantic v1. 🤓
Extending OpenAPI
Custom Docs UI Static Assets (Self-Hosting)
Custom Docs UI Static Assets (Self-Hosting) 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
General - How To - Recipes
GraphQL
Custom Request and APIRoute class
Conditional OpenAPI
Extending OpenAPI
Separate OpenAPI Schemas for Input and Output or Not
Custom Docs UI Static Assets (Self-Hosting)
Configure Swagger UI
Testing a Database
Table of contents
Custom CDN for JavaScript and CSS
Disable the automatic docs
Include the custom docs
Create a path operation to test it
Test it
Self-hosting JavaScript and CSS for docs
Project file structure
Download the files
Serve the static files
Test the static files
Disable the automatic docs for static files
Include the custom docs for static files
Create a path operation to test static files
Test Static Files UI
How To - Recipes
Custom Docs UI Static Assets (Self-Hosting)¶
The API docs use Swagger UI and ReDoc, and each of those need some JavaScript and CSS files.By default, those files are served from a CDN.But it's possible to customize it, you can set a specific CDN, or serve the files yourself.Custom CDN for JavaScript and CSS¶
Let's say that you want to use a different CDN, for example you want to use https://unpkg.com/.This could be useful if for example you live in a country that restricts some URLs.Disable the automatic docs¶
The first step is to disable the automatic docs, as by default, those use the default CDN.To disable them, set their URLs to None when creating your FastAPI app:
from fastapi import from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)app = FastAPI(docs_url=None, redoc_url=None)
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )
@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
    )
@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}Include the custom docs¶
Now you can create the path operations for the custom docs.You can reuse FastAPI's internal functions to create the HTML pages for the docs, and pass them the needed arguments:openapi_url: the URL where the HTML page for the docs can get the OpenAPI schema for your API. You can use here the attribute app.openapi_url.
title: the title of your API.
oauth2_redirect_url: you can use app.swagger_ui_oauth2_redirect_url here to use the default.
swagger_js_url: the URL where the HTML for your Swagger UI docs can get the JavaScript file. This is the custom CDN URL.
swagger_css_url: the URL where the HTML for your Swagger UI docs can get the CSS file. This is the custom CDN URL.
And similarly for ReDoc...
from fastapi import from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)app = FastAPI(docs_url=None, redoc_url=None)
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )
@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
    )
@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}TipThe path operation for swagger_ui_redirect is a helper for when you use OAuth2.If you integrate your API with an OAuth2 provider, you will be able to authenticate and come back to the API docs with the acquired credentials. And interact with it using the real OAuth2 authentication.Swagger UI will handle it behind the scenes for you, but it needs this "redirect" helper.Create a path operation to test it¶
Now, to be able to test that everything works, create a path operation:
from fastapi import from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)app = FastAPI(docs_url=None, redoc_url=None)
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )
@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
    )
@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}Test it¶
Now, you should be able to go to your docs at http://127.0.0.1:8000/docs, and reload the page, it will load those assets from the new CDN.Self-hosting JavaScript and CSS for docs¶
Self-hosting the JavaScript and CSS could be useful if, for example, you need your app to keep working even while offline, without open Internet access, or in a local network.Here you'll see how to serve those files yourself, in the same FastAPI app, and configure the docs to use them.Project file structure¶
Let's say your project file structure looks like this:
.
├── app
│   ├── __init__.py
│   ├── main.py
Now create a directory to store those static files.Your new file structure could look like this:
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static/
Download the files¶
Download the static files needed for the docs and put them on that static/ directory.You can probably right-click each link and select an option similar to Save link as....Swagger UI uses the files:swagger-ui-bundle.js
swagger-ui.css
And ReDoc uses the file:redoc.standalone.js
After that, your file structure could look like:
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static
    ├── redoc.standalone.js
    ├── swagger-ui-bundle.js
    └── swagger-ui.css
Serve the static files¶
Import StaticFiles.
"Mount" a StaticFiles() instance in a specific path.from fastapi import from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFilesapp = FastAPI(docs_url=None, redoc_url=None)app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )
@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )
@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}Test the static files¶
Start your application and go to http://127.0.0.1:8000/static/redoc.standalone.js.You should see a very long JavaScript file for ReDoc.It could start with something like:
/*!
 * ReDoc - OpenAPI/Swagger-generated API Reference Documentation
 * -------------------------------------------------------------
 *   Version: "2.0.0-rc.18"
 *   Repo: https://github.com/Redocly/redoc
 */
!function(e,t){"object"==typeof exports&&"object"==typeof m...
That confirms that you are being able to serve static files from your app, and that you placed the static files for the docs in the correct place.Now we can configure the app to use those static files for the docs.Disable the automatic docs for static files¶
The same as when using a custom CDN, the first step is to disable the automatic docs, as those use the CDN by default.To disable them, set their URLs to None when creating your FastAPI app:
from fastapi import from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFilesapp = FastAPI(docs_url=None, redoc_url=None)app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )
@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )
@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}Include the custom docs for static files¶
And the same way as with a custom CDN, now you can create the path operations for the custom docs.Again, you can reuse FastAPI's internal functions to create the HTML pages for the docs, and pass them the needed arguments:openapi_url: the URL where the HTML page for the docs can get the OpenAPI schema for your API. You can use here the attribute app.openapi_url.
title: the title of your API.
oauth2_redirect_url: you can use app.swagger_ui_oauth2_redirect_url here to use the default.
swagger_js_url: the URL where the HTML for your Swagger UI docs can get the JavaScript file. This is the one that your own app is now serving.
swagger_css_url: the URL where the HTML for your Swagger UI docs can get the CSS file. This is the one that your own app is now serving.
And similarly for ReDoc...
from fastapi import from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFilesapp = FastAPI(docs_url=None, redoc_url=None)app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )
@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )
@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}TipThe path operation for swagger_ui_redirect is a helper for when you use OAuth2.If you integrate your API with an OAuth2 provider, you will be able to authenticate and come back to the API docs with the acquired credentials. And interact with it using the real OAuth2 authentication.Swagger UI will handle it behind the scenes for you, but it needs this "redirect" helper.Create a path operation to test static files¶
Now, to be able to test that everything works, create a path operation:
from fastapi import from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFilesapp = FastAPI(docs_url=None, redoc_url=None)app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )
@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )
@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}Test Static Files UI¶
Now, you should be able to disconnect your WiFi, go to your docs at http://127.0.0.1:8000/docs, and reload the page.And even without Internet, you would be able to see the docs for your API and interact with it.
Separate OpenAPI Schemas for Input and Output or Not
Configure Swagger UI
Configure Swagger UI 
Python Types Intro
Concurrency and async / await
Environment Variables
Virtual Environments
Advanced User Guide
FastAPI CLI
Deployment
How To - Recipes
General - How To - Recipes
GraphQL
Custom Request and APIRoute class
Conditional OpenAPI
Extending OpenAPI
Separate OpenAPI Schemas for Input and Output or Not
Custom Docs UI Static Assets (Self-Hosting)
Configure Swagger UI
Testing a Database
Table of contents
Disable Syntax Highlighting
Change the Theme
Change Default Swagger UI Parameters
Other Swagger UI Parameters
JavaScript-only settings
How To - Recipes
Configure Swagger UI¶
You can configure some extra Swagger UI parameters.To configure them, pass the swagger_ui_parameters argument when creating the FastAPI() app object or to the get_swagger_ui_html() function.swagger_ui_parameters receives a dictionary with the configurations passed to Swagger UI directly.FastAPI converts the configurations to JSON to make them compatible with JavaScript, as that's what Swagger UI needs.Disable Syntax Highlighting¶
For example, you could disable syntax highlighting in Swagger UI.Without changing the settings, syntax highlighting is enabled by default:But you can disable it by setting syntaxHighlight to False:
from fastapi import 
app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})
@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}...and then Swagger UI won't show the syntax highlighting anymore:Change the Theme¶
The same way you could set the syntax highlighting theme with the key "syntaxHighlight.theme" (notice that it has a dot in the middle):
from fastapi import 
app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})
@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}That configuration would change the syntax highlighting color theme:Change Default Swagger UI Parameters¶
FastAPI includes some default configuration parameters appropriate for most of the use cases.It includes these default configurations:
# Code above omitted 👆swagger_ui_default_parameters: Annotated[
    Dict[str, Any],
    Doc(
        """
        Default configurations for Swagger UI.        You can use it as a template to add any other configurations needed.
        """
    ),
] = {
    "dom_id": "#swagger-ui",
    "layout": "BaseLayout",
    "deepLinking": True,
    "showExtensions": True,
    "showCommonExtensions": True,
}# Code below omitted 👇👀 Full file preview
You can override any of them by setting a different value in the argument swagger_ui_parameters.For example, to disable deepLinking you could pass these settings to swagger_ui_parameters:
from fastapi import 
app = FastAPI(swagger_ui_parameters={"deepLinking": False})
@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}Other Swagger UI Parameters¶
To see all the other possible configurations you can use, read the official docs for Swagger UI parameters.JavaScript-only settings¶
Swagger UI also allows other configurations to be JavaScript-only objects (for example, JavaScript functions).FastAPI also includes these JavaScript-only presets settings:
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
These are JavaScript objects, not strings, so you can't pass them from Python code directly.If you need to use JavaScript-only configurations like those, you can use one of the methods above. Override all the Swagger UI path operation and manually write any JavaScript you need.
Custom Docs UI Static Assets (Self-Hosting)
Testing a Database
