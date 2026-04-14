# General Instructions

# General Instructions

- You are a coding agent that develops Anchorpoint Actions. 
- An action is composed of a Python and YAML file. 
- Use the Documentation below "# Documentation". It contains all API methods, classes, functions properties and other descriptions. 
- Do not add anything that is not listed in the Documentation.

## Files

The YAML describes how the Action behaves in the UI of Anchorpoint. See the examples below for YAML files. In the Python file, you describe the logic of the Action.

**Important:** Each action requires its own dedicated YAML file. You cannot define multiple actions in a single YAML file. If the user wants multiple actions, create one YAML file (and one Python file) per action. 

### YAML

Here are the required keys of a YAML file. They are all sub keys of the "action" key: 

- version: In most cases "1.0"
- name: The name of the Action, which will be displayed in the UI of Anchorpoint
- id: a generic unique string
- type: always write "python"
- script: the name of the Python script
- register: Where the action should be triggered in the UI. 

The content is clear about YAML indentation, but could be more explicit. Here's a rewrite for the placeholder:

```yaml
register:
  sidebar:
    enable: true
```

**Note:** `register`, `sidebar`, and `enable` must align vertically using consistent indentation (spaces, not tabs). `sidebar` is indented under `register`, and `enable` is indented under `sidebar`. The `register` key must align with `id`, `name`, and `type` at the same indentation level.
```

This clarifies that "register" is sibling to other action properties (id, type, etc.), while its nested keys use additional indentation. An AI will better understand explicit alignment guidance than vague references to "tab alignment."

### Python

- The Python file will always import the "anchorpoint" module and if needed the "apsync" module. 
- If you create or access a function, property, class or method, make sure that it is listed in the documentation below. 
- Never add anything that is not listed in the documentation to avoid hallucination. 
- Add prints for debugging purposes where needed. Prints do not replace a dialog or a toast. They are an addition just for debugging.

## Agent behavior

### Referencing examples

Take a look at the examples.md file if the user has linked it to your context. There you will find action examples.

### Responding to the user in the chat

- When you finished implementing the code, in your chat response provide a link to the documentation online. The base URL is docs.anchorpoint.app/. The pages are defined in the documentation as source. The construction of the URL is the base URL + the markdown file path. From the markdown file path, you have to remove the "docs/" at the beginning and the ".md" extension at the end.
- If your source is "docs/api/yaml.md", then the url will be "docs.anchorpoint.app/api/yaml/". If your source is "docs/api/python/context.md" then the url is "docs.anchorpoint.app/api/python/context/". Do not use the class or function name to build the url. Always use the source with the .md file.

### Creating New Actions

- An Action is placed in the following subfolder [PROJECTFOLDER]/.ap/actions/
- There, you have to create the Python and YAML file if the user does not give you any information about the Action location. - You have to look in the root folder of your project for the .ap folder. If this folder does not exist, ask the user where the Action should be placed.
- Always ask for the name of the Action if the user does not provide it. Based on the name, create the ID and the file names for YAML and Python.

#### Basic Example for Creating a New Action That Adds a Button to the Sidebar and Shows a Toast to the User When Clicking on It

These two files will be placed inside the project folder in the hidden .ap/actions folder. You have to create an empty "actions" folder if it does not exist yet. The structure will look like this:

project folder
|--.ap/
| |--actions/
| | |--toast_example.yaml
| | |--toast_example.py

```yaml
version: "1.0"
action:
  name: "Show Toast"  
  id: "toast"
  type: python
  script: "toast_example.py"

  register:
    sidebar:
      enable: true

```
The toast_example.yaml file will add a button to the left sidebar. It will trigger the Python file that contains the logic.

```python
import anchorpoint
ui = anchorpoint.UI()
ui.show_info("This is a toast example")
```
The toast_example.py file will show a toast (a message) to the user.

### Developing Existing Actions

When the user has already set up the Action, don't create a new one. You will edit existing Python code.

### Implementing Hooks

A hook is a special type of Action that runs automatically in response to an internal Anchorpoint event (e.g. after a git clone), rather than being triggered by the user clicking a button in the UI.

**Key differences from a regular Action:**
- The YAML has **no `register` key** — hooks are not shown in the UI.
- The Python file must define an `on_event_received(id, payload, ctx)` function — this is the entry point Anchorpoint calls when the event fires.
- The `id` parameter identifies the event type (e.g. `"gitclone"`), and `payload` contains event-specific data.

**YAML example:**
```yaml
version: 1.0
action:
  name: My Hook
  id: my_namespace::my_hook
  type: python
  script: my_hook.py
```

**Python example:**
```python
import anchorpoint as ap
import apsync as aps

def on_event_received(id, payload, ctx: ap.Context):
    if isinstance(payload, dict):
        payload = payload.get("type")

    if id != "gitclone" or payload != "success":
        return

    # Hook logic here
    print(f"Hook triggered for event: {id}")
```

**Restart requirement:** Like any YAML change, adding a hook for the first time requires restarting Anchorpoint. Follow the same restart process described in the "Launching Anchorpoint After Implementing an Action" section.

### Launching Anchorpoint After Implementing an Action

**When to ask:**
- After implementing a new Action for the first time, always ask the user whether they want to launch Anchorpoint to test it.
- After making changes **only to a Python file**, a restart is **not needed** — Anchorpoint hot-reloads Python scripts. Do not ask.
- After making changes **to a YAML file** (new action or updated YAML), a restart **is required**. Ask the user if they want to restart Anchorpoint.

**How to restart:**
1. Check if Anchorpoint is currently running using the task manager, and if so, kill it before launching:
   - **Windows (PowerShell):** `Stop-Process -Name "Anchorpoint" -ErrorAction SilentlyContinue`
   - **macOS (Terminal):** `pkill -x Anchorpoint`
2. Then launch the application as described below.

If yes, launch the application using the appropriate path for the user's OS:

**macOS:**
```
/Applications/Anchorpoint.app/Contents/MacOS/Anchorpoint
```

**Windows:**

The executable is located under the user's AppData folder and includes the installed version number in the path:
```
C:\Users\\AppData\Local\Anchorpoint\app-\Anchorpoint.exe
```

To find the correct path on Windows:
1. List the contents of `C:\Users\\AppData\Local\Anchorpoint\` to find all `app-*` directories.
2. Pick the one with the highest version number (e.g. `app-1.34.0` over `app-1.33.4`).
3. Launch `Anchorpoint.exe` inside that folder.

Use `Start-Process` in PowerShell to launch it, for example:
```powershell
Start-Process -FilePath "C:\Users\\AppData\Local\Anchorpoint\app-1.34.0\Anchorpoint.exe"
```

# Documentation

## Source: documentation/docs/api/yaml.md


## YAML reference

The YAML file describes how an action behaves in Anchorpoint, registers it and can control Python scripts or command line applications. Each action needs a YAML file. The YAML file is declaratively described with key - value pairs.

```yaml
# The action version
version: 1.0
# The action definition
action: 
  # name of the action
  name: Batch Rename 
  # unique id
  id: ap::rename
  # Type can be either a cmd command or a python script
  type: python
  # Will be shown in the tooltip of the Action
  description: Renames a set of selected files
  # What is the icon that will be shown in the context menu. Use the Anchorpoint icon picker to get the path of the Anchorpoint icons.
  icon:
    path: :/icons/design-tools-photo-editing/pencil.svg
  # The Python script that will be triggered
  script: batch_rename.py

  # In which area of the Anchorpoint desktop app will this action be placed
  register:
    # Place it in the file context menu
    file: 
      enable: true
```
This example triggers a Python script that passes a selection of files to a batch renaming process.

### Triggers in Anchorpoint

You can trigger actions from various places in the UI. To add triggers in the YAML file, scroll down to the "register" section.

|  | Register actions for `sidebar`, `new_task`, `new_folder` and `new_file`. On the sidebar, the name of the action will appear as a button, for the "new" registrations, the buttons will appear each in a context menu. |
| ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|   | Opening the context menu for `new_task`, `new_folder` and `new_file`. All the actions registered under these types, will be listed here.                                                                              |
|                  | Examples for a `folder` action, which will show up in the context menu of a folder.                                                                                                                                   |
|                  | Examples for registering the `file` action, which will show up in the context menu of a file.                                                                                                                         |
|                  | Here you can register `workspace_overview` actions and `new_drive` actions. The `drive` register is an entry in the context menu when you do a right-click on a drive.                                                |

### Basic Keys
See the following list to learn about the basic keys that can be used to define your action.

#### version
A required property that sets the current action version. 
```yaml
# Required
version: 1.0
```

The following keys are subkeys of the **action** key.

#### name
Provides the name that shows up in Anchorpoint e.g. in the context menu
```yaml
action:
  #This will appear in the UI
  name: "Convert Video to mp4"
```

#### id
A unique identifier. It is generally a good idea to provide a "namespace" for your action so that there is a lower chance to clash with Actions provided by other users.
```yaml
action:
  id: "ap::ffmpegConvertVideo"
```

#### type
What type of action, either "command", "python", or "package".

```yaml
# Example for triggering a python script
action:
  # The Python script that will be triggered
  type: python
  script: batch_rename.py
```

```yaml
# Example for triggering an executable directly
action:
  # In case an executable will be triggered
  type: command
  command: "ffmpeg.exe" 
  arguments: "-i ${path} ${root}/03_Export/Videos/yamlExample.mp4"
```

#### command
The path to the executable of a command line application like FFmpeg (e.g. ffmpeg.exe) if the action is of type "command". The path can be absolute or relative to the yaml file.

#### arguments
The variables to be passed to the command line application. In this example, instead of an absolute path, we take the `$\{path\}` variable, which returns us the file we selected in Anchorpoint. 
We also use the `$\{root\}` variable, which gives us the path of the project.But this also means that this action can only be called in a project that contains a "03_Export/Videos" folder. 
```yaml
action:
  type: command
  command: ffmpeg.exe
  arguments: "-i ${path} ${root}/03_Export/Videos/yamlExample.mp4"
```

#### script
The path to the Python script if the action is of type "python". It expects a Python 3.9 script. The path can be absolute or relative to the yaml file.
```yaml
action:
  type: python
  script: save_as_template.py
```

#### author
Who created this action.
```yaml
action:
  author: "Anchorpoint Software GmbH"
```

#### description
What does your action do?.
```yaml
action:
  author: "Create a video from all files that are sharing the same suffix"
```
#### details
A detailed description of your action. Currently this is only used for packages. The content supports basic HTML.
```yaml
action:
  author: "Create a video from all files that are sharing the same suffix"
```

#### register
Specify where your action should be registered within Anchorpoint. Actions can be registered for the:
- file and folder context menu
- for the new file, folder, and drive buttons
- the left sidebar in the browser
- the timeline right-click context menu (commits, stashes, changed files).
Use the filter wildcard key to only register the action if the filter matches. Separate multiple filters with a semicolon.
```yaml
register:   
  file:       
    filter: "*.png;*.exr" #Wildcard matching    
  folder:      
    filter: "*/assets/*"       
  new_file:
    enable: true
  new_folder:
    filter: "*/shots/*" 
  new_task:
    enable: true
  drive:
    enable: true
  new_drive:
    enable: true
  sidebar:
    enable: true
  workspace_overview:
    enable: true
  timeline_commit:
    enable: true
  timeline_stash:
    enable: true
  timeline_changed_files:
    enable: true
```

The `timeline_commit`, `timeline_stash`, and `timeline_changed_files` registrations add your action to the right-click context menu of timeline entries. See Event Hooks for the corresponding Python hook functions.

### Advanced Keys
This section handles more advanced YAML keys that can be used to specify how your action functions exactly.

#### inputs
A list of inputs for your action that can be defined in YAML and read in Python. Here it is worthwhile to store parameters, such as paths or certain settings, so that you don't have to modify your python script. 
```yaml
inputs:     
  URL: "anchorpoint.app"    
  target: ${root}/03_Export/Videos
```

You can also show basic prompts to ask the user for input. See more examples here.
```yaml
inputs:     
  URL: 
    message: "What website do you like the most?"
    default: "anchorpoint.app"  
```

#### platforms
By default, actions are supported on all platforms. With the **platforms** key you can explicitly list the supported platforms:
```yaml
platforms:    
  - win
  - mac
```

#### python_packages
Anchorpoint ships with it's own Python interpreter to not depend on local installations. Hence, Anchorpoint is not using the locally installed python packages.
Installing your own python packages for your actions is simple. Just specify your required packages in the action or packge YAML and Anchorpoint will install them, if needed.
```yaml
python_packages:    
  - pillow
  - opencv-python
```

#### toast
With the toast key you can control whether or not Anchorpoint shows a toast message on success or error. By default, Anchorpoint will show no message at all. In python you can fire up toasts directly.
```yaml
toast:    
  success:      
    enable: false    
  error:      
    message: "Could not export file, please check your file system"
```

### Variables
Within the YAML file you can access predefined and environment variables as well as defined inputs easily with the `$\{var\}` syntax.
```yaml
inputs:     
  blender_path: "${BLENDER_DIR}/blender.exe" #environment variable BLENDER_DIR
command: ${blender_path}
arguments: --scene ${path} #access the predefined path variable
```

#### path
The absolute path to the file or folder.
```yaml
inputs:     
  URL: "anchorpoint.app"    
  target: ${path}/ExportedFiles
```

#### relative_path
Path to the file or folder relative to the active project.

#### project_path
The project root folder.
```yaml
inputs:     
  URL: "anchorpoint.app"    
  target: ${project_path}/03_Export/Videos
```

#### yaml_dir
The directory containing this YAML file.
```yaml
action:     
  script: "${yaml_dir}/sbsToTextures.py"
```

#### folder
The active folder where you executed that action.

#### filename
The active filename without the path and without the suffix.

#### suffix
The suffix of the file, e.g. PNG.

### Action Packages
An Action Package is a group of Actions bundled as a "feature". Action Packages are listed under "Workspace Settings / Actions" in the Anchorpoint desktop app. All default Anchorpoint actions are grouped via a package. You can package a set of actions in an **action package**. Action packages have 2 main advantages:

- They can be distributed using the Action Distribution System
- They can be enabled and disabled for the entire workspace

To define an action package set the type to **package** and provide a list of **actions**.

```yaml
action:
  #The package name
  name: Batch Rename
  id: ap::package::rename
  # Mark it as a package type
  type: package
  # Should it be on/off per default
  enable: false
  # The description will be shown in the Action package list under Workspace Settings / Actions
  description: A simple batch rename tool, that can be customized to your needs
  # Package icon
  icon:
    path: batch_rename.svg
  # List all the actions that are affected and will be enabled when the package is enabled
  actions:
    - ap::rename
  # Restrict the action package for specific platforms
  platforms:
    - mac
    - win
```

The YAML for a package features 2 main differences to a normal action YAML:
- The type is set to "package"
- A list of action ids is provided through the "actions" key

For workspace owners or administrators the packages show up in the Action settings for your workspace:

## Source: documentation/docs/api/python/api.md


## API

The API class is a container that holds metadata for attributes and tasks. It can also get the current project and workspace information and allows you to set metadata in projects that are not included in the context. E.g. projects, that are currently not open in Anchorpoint.

### Usage
The API is obtained using the `get_api()` function from the `anchorpoint` module:

```python
import anchorpoint

api = anchorpoint.get_api()
```

### API Class

#### Properties

- **`attributes`** *(class: AttributeAPI):* Access to the Attributes API for managing file and folder metadata. Provides methods for creating, reading, and writing attributes. See Attributes documentation for detailed usage.
- **`tasks`** *(class: TaskAPI):* Access to the Tasks API for managing task lists and individual tasks. Provides methods for creating, reading, and updating tasks. Supports task organization within task lists.

#### Methods

##### Project and Workspace Information

- **`get_project()`** Gets the current project information.

    Returns: (*class: Project or None*) The current project or None if not in a project context

- **`get_workspace()`** Gets the current workspace identifier.

    Returns: (*str*) The workspace ID

### Examples

#### Working with Project Information

```python
import anchorpoint

api = anchorpoint.get_api()

# Get current project
project = api.get_project()
if project:
    print(f"Project name: {project.name}")
    print(f"Project ID: {project.id}")
    print(f"Project path: {project.path}")
else:
    print("Not currently in a project")

# Get workspace information
workspace_id = api.get_workspace()
print(f"Workspace ID: {workspace_id}")
```

#### Cross-Project Attribute Management

```python
import anchorpoint
import apsync

api = anchorpoint.get_api()

# Set attributes on files in different projects
# This works even if the project is not currently open in Anchorpoint
file_in_other_project = "/path/to/other/project/asset.jpg"

# Set metadata for files outside current context
api.attributes.set_attribute_value(file_in_other_project, "Status", "Approved")
api.attributes.set_attribute_value(file_in_other_project, "Review Notes", "Ready for production")

# Create attributes that can be used across projects
quality_attribute = api.attributes.get_attribute("Quality Rating")
if not quality_attribute:
    quality_attribute = api.attributes.create_attribute("Quality Rating", apsync.AttributeType.rating)

# Apply to multiple files across different projects
files_to_rate = [
    "/project1/characters/hero.fbx",
    "/project2/environments/level1.ma", 
    "/project3/props/sword.blend"
]

for file_path in files_to_rate:
    api.attributes.set_attribute_value(file_path, quality_attribute, 4)
    print(f"Set quality rating for: {file_path}")
```

#### Combining API with Context

```python
import anchorpoint
import apsync

# Get both context and API for comprehensive workflow
ctx = anchorpoint.get_context()
api = anchorpoint.get_api()

# Use context for current selection
current_files = ctx.selected_files

# Use API for broader project management
project = api.get_project()

if project and current_files:
    print(f"Processing {len(current_files)} files in project: {project.name}")
    
    # Set project-level attributes on selected files
    for file_path in current_files:
        api.attributes.set_attribute_value(file_path, "Project", project.name)
        api.attributes.set_attribute_value(file_path, "Workspace", api.get_workspace())
        
        # Use context information in the metadata
        api.attributes.set_attribute_value(file_path, "Processed By", ctx.username)
    
    print("Added project metadata to all selected files")
```

#### Batch Operations Across Multiple Projects

```python
import anchorpoint
import apsync
import os

api = anchorpoint.get_api()

def update_project_metadata(project_paths):
    """Update metadata for multiple projects"""
    
    for project_path in project_paths:
        print(f"Processing project: {project_path}")
        
        # Walk through all files in the project
        for root, dirs, files in os.walk(project_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Set common project attributes
                api.attributes.set_attribute_value(file_path, "Project Root", project_path)
                api.attributes.set_attribute_value(file_path, "Last Updated", apsync.datetime.now())
                
                # Set file type based on extension
                _, ext = os.path.splitext(file)
                if ext.lower() in ['.jpg', '.png', '.tiff']:
                    api.attributes.set_attribute_value(file_path, "Asset Type", "Texture")
                elif ext.lower() in ['.fbx', '.obj', '.ma', '.blend']:
                    api.attributes.set_attribute_value(file_path, "Asset Type", "3D Model")

# Process multiple projects
project_list = [
    "/path/to/project1",
    "/path/to/project2", 
    "/path/to/project3"
]

update_project_metadata(project_list)
```

#### Working with Attributes API

```python
import anchorpoint
import apsync

api = anchorpoint.get_api()

# Create a comprehensive attribute system
def setup_project_attributes():
    """Set up standard attributes for project management"""
    
    # Create status attribute with predefined options
    status_attr = api.attributes.get_attribute("Asset Status")
    if not status_attr:
        status_attr = api.attributes.create_attribute("Asset Status", apsync.AttributeType.single_choice_tag)
        
        # Define status options
        status_tags = [
            apsync.AttributeTag("Work in Progress", "orange"),
            apsync.AttributeTag("Review Required", "yellow"),
            apsync.AttributeTag("Approved", "green"),
            apsync.AttributeTag("Needs Revision", "red")
        ]
        api.attributes.set_attribute_tags(status_attr, status_tags)
    
    # Create priority attribute
    priority_attr = api.attributes.get_attribute("Priority")
    if not priority_attr:
        priority_attr = api.attributes.create_attribute("Priority", apsync.AttributeType.single_choice_tag)
        
        priority_tags = [
            apsync.AttributeTag("High", "red"),
            apsync.AttributeTag("Medium", "yellow"), 
            apsync.AttributeTag("Low", "blue")
        ]
        api.attributes.set_attribute_tags(priority_attr, priority_tags)
    
    return status_attr, priority_attr

# Set up the attribute system
status_attr, priority_attr = setup_project_attributes()

# Apply to files
file_path = "/project/characters/main_character.fbx"
api.attributes.set_attribute_value(file_path, status_attr, "Review Required")
api.attributes.set_attribute_value(file_path, priority_attr, "High")
api.attributes.set_attribute_value(file_path, "Notes", "Final review before production")

print("Project attribute system configured and applied")
```

## Source: documentation/docs/api/python/attributes.md


## Attributes

Attributes in Anchorpoint are custom metadata that can be attached to files, folders, and tasks to add context and organization to your assets. The Attributes API provides comprehensive functionality to read, write, and manage different types of attributes including tags, text fields, ratings, links, dates, and checkboxes.

### Usage

```python
import apsync
import anchorpoint
from datetime import datetime

ctx = anchorpoint.get_context()
api = anchorpoint.get_api()

# Set a text attribute by name
api.attributes.set_attribute_value(ctx.path, "Description", "Hero character artwork")

# Get a text attribute
description = api.attributes.get_attribute_value(ctx.path, "Description")
print(description)  # Output: "Hero character artwork"

# Set a date attribute
api.attributes.set_attribute_value(ctx.path, "Created At", datetime.now())

# Work with attribute objects for more control
attribute = api.attributes.get_attribute("Status")
if not attribute:
    attribute = api.attributes.create_attribute("Status", apsync.AttributeType.single_choice_tag)

# Set attribute value using attribute object
api.attributes.set_attribute_value(ctx.path, attribute, "In Progress")
```

### Attribute Types

Anchorpoint supports several attribute types defined in the `AttributeType` class:

```python
import apsync

# Available attribute types
apsync.AttributeType.single_choice_tag      # Select one tag from predefined options
apsync.AttributeType.multiple_choice_tag    # Select multiple tags from predefined options
apsync.AttributeType.text                   # Free text input
apsync.AttributeType.rating                 # Numeric rating
apsync.AttributeType.hyperlink              # URL or file path links
apsync.AttributeType.date                   # Date/timestamp values
apsync.AttributeType.checkbox               # Boolean true/false values
apsync.AttributeType.user                   # User attribute
```

### AttributeType Class

The `AttributeType` class identifies the type of an attribute.

#### Members

- **`single_choice_tag`** Select one tag from predefined options.
- **`multiple_choice_tag`** Select multiple tags from predefined options.
- **`text`** Free text input.
- **`rating`** Numeric rating.
- **`hyperlink`** URL or file path link.
- **`date`** Date value.
- **`checkbox`** Boolean true/false value.
- **`user`** User attribute.

### Attributes API

The Attributes API is accessed through `api.attributes` and provides methods for creating, managing, and working with attributes.

```python
import anchorpoint

api = anchorpoint.get_api()
attributes = api.attributes
```

#### Getting and Setting Attribute Values

- **`api.attributes.get_attribute_value(target, attribute)`** Retrieves the value of an attribute for a file, folder, or task.

    Arguments
    - `target` *(str or class: Task):* Path to the file or folder, or a Task object
    - `attribute` *(class: Attribute or str):* The attribute object or attribute name

    Returns: *The attribute value, or None*

- **`api.attributes.set_attribute_value(target, attribute, value, update_timeline=False)`** Sets the value of an attribute for a file, folder, or task. Creates the attribute if it cannot be found.

    Arguments
    - `target` *(str or class: Task):* Path to the file or folder, or a Task object
    - `attribute` *(class: Attribute or str):* The attribute object or attribute name
    - `value` *(int, str, list, class: AttributeTag, class: AttributeTagList, bool):* Value to set
    - `update_timeline` *(bool, optional):* True if the timeline should be notified about the update. Default is False

#### Managing Attributes

- **`api.attributes.get_attribute(name, type=None)`** Returns an attribute by name, or None if not found.

    Arguments
    - `name` *(str):* Name of the attribute (e.g., "Status")
    - `type` *(class: AttributeType, optional):* Attribute type to filter by, or None

    Returns: *class: Attribute or None*

- **`api.attributes.get_attribute_by_id(id)`** Returns an attribute with a given id.

    Arguments
    - `id` *(str):* The id of the attribute

    Returns: *class: Attribute*

- **`api.attributes.get_attributes(type=None)`** Returns all attributes in the workspace or project, optionally filtered by type.

    Arguments
    - `type` *(class: AttributeType, optional):* Attribute type to filter for, or None

    Returns: *listclass: [Attribute]*

- **`api.attributes.create_attribute(name, type, tags=None, rating_max=None)`** Creates a new attribute in the workspace or project.

    Arguments
    - `name` *(str):* Name of the attribute (e.g., "Status")
    - `type` *(class: AttributeType):* The attribute type
    - `tags` *(class: AttributeTagList or list, optional):* List of tags to create, or None
    - `rating_max` *(int, optional):* The maximum rating value. Only valid for rating attributes

    Returns: *class: Attribute*

- **`api.attributes.rename_attribute(attribute, name)`** Renames an attribute.

    Arguments
    - `attribute` *(class: Attribute):* The attribute to rename
    - `name` *(str):* The new name

#### Managing Tags

- **`api.attributes.set_attribute_tags(attribute, tags)`** Sets the available tags for a single or multiple choice tag attribute.

    Arguments
    - `attribute` *(class: Attribute):* The attribute to update
    - `tags` *(class: AttributeTagList):* The list of tags

- **`api.attributes.set_attribute_rating_max(attribute, max)`** Sets the maximum rating for a rating attribute.

    Arguments
    - `attribute` *(class: Attribute):* The attribute to update
    - `max` *(int):* The new maximum rating value

### AttributeTag Class

The `AttributeTag` class represents a single or multiple choice tag.

```python
import apsync

tag = apsync.AttributeTag("In Progress", apsync.TagColor.yellow)
```

#### Constructor

- **`apsync.AttributeTag(name)`** Creates a new attribute tag with a default color.

    Arguments
    - `name` *(str):* Name of the tag

- **`apsync.AttributeTag(name, color)`** Creates a new attribute tag with a specified color.

    Arguments
    - `name` *(str):* Name of the tag
    - `color` *(class: TagColor or str):* The color of the tag

#### Properties

- **`id`** *(str):* Unique identifier of the tag.
- **`name`** *(str):* Name of the tag.
- **`color`** *(class: TagColor):* The color of the tag.

### Attribute Class

The `Attribute` class represents an attribute definition. Attributes are not created directly — use `api.attributes.get_attribute()` or `api.attributes.create_attribute()` to obtain one.

```python
import apsync
import anchorpoint

api = anchorpoint.get_api()
attribute = api.attributes.get_attribute("Status")
if not attribute:
    attribute = api.attributes.create_attribute("Status", apsync.AttributeType.single_choice_tag)
```

#### Properties

- **`id`** *(str):* Unique identifier for the attribute. Read-only.
- **`name`** *(str):* Name of the attribute.
- **`type`** *(class: AttributeType):* Type of the attribute. Read-only.
- **`tags`** *(class: AttributeTagList):* Available tags for tag-type attributes.
- **`rating_max`** *(int or None):* Maximum rating value. Only valid for rating attributes.

### TagColor Class

The `TagColor` class represents the color of a single or multiple choice tag. Use the provided class members instead of raw strings.

```python
import apsync

color = apsync.TagColor.green
```

#### Members

- **`red`** Red color.
- **`orange`** Orange color.
- **`yellow`** Yellow color.
- **`green`** Green color.
- **`turk`** Turquoise color.
- **`blue`** Blue color.
- **`purple`** Purple color.
- **`grey`** Grey color.

#### Constructor

- **`apsync.TagColor()`** Creates a default TagColor.
- **`apsync.TagColor(color)`** Creates a TagColor from a string value.

    Arguments
    - `color` *(str):* Color string (e.g., `"blue"`, `"red"`)

### AttributeTagList Class

The `AttributeTagList` class is a list of AttributeTag objects. It behaves like a standard Python list.

```python
import apsync

tags = apsync.AttributeTagList()
tags.append(apsync.AttributeTag("In Progress", apsync.TagColor.yellow))
tags.append(apsync.AttributeTag("Done", apsync.TagColor.green))
```

#### Methods

- **`append(x)`** Adds an item to the end of the list.

    Arguments
    - `x` *(class: AttributeTag):* The tag to append

- **`insert(i, x)`** Inserts an item at a given position.

    Arguments
    - `i` *(int):* The index to insert at
    - `x` *(class: AttributeTag):* The tag to insert

- **`pop()`** Removes and returns the last item.

    Returns: *class: AttributeTag*

- **`clear()`** Clears the contents.

- **`extend(L)`** Extends the list by appending all items from another list.

    Arguments
    - `L` *(class: AttributeTagList or iterable):* The items to append

### Standalone Attribute Functions

These are module-level functions that read and write individual attribute values directly by attribute title, without requiring an `Attributes` class instance.

#### Getting Attribute Values

- **`apsync.get_attribute_text(absolute_path, attribute_title, workspace_id=None)`** Retrieves the text content of an attribute for a given file or folder.

    Arguments
    - `absolute_path` *(str):* Path to the file or folder
    - `attribute_title` *(str):* Title of the attribute
    - `workspace_id` *(str, optional):* The workspace id, or None

    Returns: *str or None*

- **`apsync.get_attribute_tag(absolute_path, attribute_title, workspace_id=None)`** Retrieves the tag content of an attribute for a given file or folder.

    Arguments
    - `absolute_path` *(str):* Path to the file or folder
    - `attribute_title` *(str):* Title of the attribute
    - `workspace_id` *(str, optional):* The workspace id, or None

    Returns: *class: AttributeTag or None*

- **`apsync.get_attribute_tags(absolute_path, attribute_title, workspace_id=None)`** Retrieves the list of assigned tags of a multiple or single choice tag attribute.

    Arguments
    - `absolute_path` *(str):* Path to the file or folder
    - `attribute_title` *(str):* Title of the attribute
    - `workspace_id` *(str, optional):* The workspace id, or None

    Returns: *listclass: [AttributeTag]*

- **`apsync.get_attribute_rating(absolute_path, attribute_title, workspace_id=None)`** Retrieves the rating content of an attribute for a given file or folder.

    Arguments
    - `absolute_path` *(str):* Path to the file or folder
    - `attribute_title` *(str):* Title of the attribute
    - `workspace_id` *(str, optional):* The workspace id, or None

    Returns: *int*

- **`apsync.get_attribute_checked(absolute_path, attribute_title, workspace_id=None)`** Retrieves the checkbox content of an attribute for a given file or folder.

    Arguments
    - `absolute_path` *(str):* Path to the file or folder
    - `attribute_title` *(str):* Title of the attribute
    - `workspace_id` *(str, optional):* The workspace id, or None

    Returns: *bool*

- **`apsync.get_attribute_date(absolute_path, attribute_title, workspace_id=None)`** Retrieves the date content of an attribute for a given file or folder. The date is in seconds since the epoch.

    Arguments
    - `absolute_path` *(str):* Path to the file or folder
    - `attribute_title` *(str):* Title of the attribute
    - `workspace_id` *(str, optional):* The workspace id, or None

    Returns: *int*

- **`apsync.get_attribute_link(absolute_path, attribute_title, workspace_id=None)`** Retrieves the link content of an attribute for a given file or folder.

    Arguments
    - `absolute_path` *(str):* Path to the file or folder
    - `attribute_title` *(str):* Title of the attribute
    - `workspace_id` *(str, optional):* The workspace id, or None

    Returns: *str or None*

#### Setting Attribute Values

- **`apsync.set_attribute_text(absolute_path, attribute_title, text, workspace_id=None, auto_create=True, update_timeline=False)`**

    Sets the text content of an attribute for a given file or folder. Creates the attribute if it cannot be found and `auto_create` is True.

    Arguments
    - `absolute_path` *(str):* Path to the file or folder
    - `attribute_title` *(str):* Title of the attribute
    - `text` *(str):* The text to set
    - `workspace_id` *(str, optional):* The workspace id, or None
    - `auto_create` *(bool, optional):* Automatically create the attribute if it does not exist. Default is True
    - `update_timeline` *(bool, optional):* True if the timeline should be notified. Default is False

- **`apsync.set_attribute_tag(absolute_path, attribute_title, tag_name, type=AttributeType.single_choice_tag, workspace_id=None, auto_create=True, tag_color=None, update_timeline=False)`**

    Sets the tag of an attribute for a given file or folder. Creates the attribute if it cannot be found and `auto_create` is True.

    Arguments
    - `absolute_path` *(str):* Path to the file or folder
    - `attribute_title` *(str):* Title of the attribute
    - `tag_name` *(str):* The name of the tag to set — creates a new tag if unknown
    - `type` *(class: AttributeType, optional):* The type of attribute. Default is `single_choice_tag`
    - `workspace_id` *(str, optional):* The workspace id, or None
    - `auto_create` *(bool, optional):* Automatically create the attribute if it does not exist. Default is True
    - `tag_color` *(class: TagColor, optional):* The color of the created tag, or None for a random color
    - `update_timeline` *(bool, optional):* True if the timeline should be notified. Default is False

- **`apsync.set_attribute_tags(absolute_path, attribute_title, tag_names, type=AttributeType.multiple_choice_tag, workspace_id=None, auto_create=True, update_timeline=False)`**

    Sets the tags of an attribute for a given file or folder, overwriting any existing tags. Creates the attribute if it cannot be found and `auto_create` is True.

    Arguments
    - `absolute_path` *(str):* Path to the file or folder
    - `attribute_title` *(str):* Title of the attribute
    - `tag_names` *(list[str]):* The tags to set, identified by name
    - `type` *(class: AttributeType, optional):* Must be `multiple_choice_tag` or `single_choice_tag`. Default is `multiple_choice_tag`
    - `workspace_id` *(str, optional):* The workspace id, or None
    - `auto_create` *(bool, optional):* Automatically create the attribute if it does not exist. Default is True
    - `update_timeline` *(bool, optional):* True if the timeline should be notified. Default is False

- **`apsync.set_attribute_rating(absolute_path, attribute_title, rating, workspace_id=None, auto_create=True, update_timeline=False)`**

    Sets the rating content of an attribute for a given file or folder. Creates the attribute if it cannot be found and `auto_create` is True.

    Arguments
    - `absolute_path` *(str):* Path to the file or folder
    - `attribute_title` *(str):* Title of the attribute
    - `rating` *(int):* The rating to set
    - `workspace_id` *(str, optional):* The workspace id, or None
    - `auto_create` *(bool, optional):* Automatically create the attribute if it does not exist. Default is True
    - `update_timeline` *(bool, optional):* True if the timeline should be notified. Default is False

- **`apsync.set_attribute_checked(absolute_path, attribute_title, checked, workspace_id=None, auto_create=True, update_timeline=False)`**

    Sets the checkbox content of an attribute for a given file or folder. Creates the attribute if it cannot be found and `auto_create` is True.

    Arguments
    - `absolute_path` *(str):* Path to the file or folder
    - `attribute_title` *(str):* Title of the attribute
    - `checked` *(bool):* Check or uncheck the attribute
    - `workspace_id` *(str, optional):* The workspace id, or None
    - `auto_create` *(bool, optional):* Automatically create the attribute if it does not exist. Default is True
    - `update_timeline` *(bool, optional):* True if the timeline should be notified. Default is False

- **`apsync.set_attribute_date(absolute_path, attribute_title, secs_since_epoch, workspace_id=None, auto_create=True, update_timeline=False)`**

    Sets the date content of an attribute for a given file or folder. The date is in seconds since the epoch. Creates the attribute if it cannot be found and `auto_create` is True.

    Arguments
    - `absolute_path` *(str):* Path to the file or folder
    - `attribute_title` *(str):* Title of the attribute
    - `secs_since_epoch` *(int):* The date to set in seconds since the epoch
    - `workspace_id` *(str, optional):* The workspace id, or None
    - `auto_create` *(bool, optional):* Automatically create the attribute if it does not exist. Default is True
    - `update_timeline` *(bool, optional):* True if the timeline should be notified. Default is False

- **`apsync.set_attribute_link(absolute_path, attribute_title, link, workspace_id=None, auto_create=True, update_timeline=False)`**

    Sets the link content of an attribute for a given file or folder. A link can point to a website or a file or folder. Creates the attribute if it cannot be found and `auto_create` is True.

    Arguments
    - `absolute_path` *(str):* Path to the file or folder
    - `attribute_title` *(str):* Title of the attribute
    - `link` *(str):* The link to set
    - `workspace_id` *(str, optional):* The workspace id, or None
    - `auto_create` *(bool, optional):* Automatically create the attribute if it does not exist. Default is True
    - `update_timeline` *(bool, optional):* True if the timeline should be notified. Default is False

#### Tag Helpers

- **`apsync.add_attribute_tag(absolute_path, attribute_title, tag_name, type=AttributeType.multiple_choice_tag, workspace_id=None, auto_create=True, tag_color=None, update_timeline=False)`**

    Adds a tag identified by name to an attribute. If no tags are assigned yet, this is equivalent to `set_attribute_tag`. Creates the attribute if it cannot be found and `auto_create` is True.

    Arguments
    - `absolute_path` *(str):* Path to the file or folder
    - `attribute_title` *(str):* Title of the attribute
    - `tag_name` *(str):* The tag to add, identified by name
    - `type` *(class: AttributeType, optional):* Must be `multiple_choice_tag` or `single_choice_tag`. Default is `multiple_choice_tag`
    - `workspace_id` *(str, optional):* The workspace id, or None
    - `auto_create` *(bool, optional):* Automatically create the attribute if it does not exist. Default is True
    - `tag_color` *(class: TagColor, optional):* The color of the created tag, or None
    - `update_timeline` *(bool, optional):* True if the timeline should be notified. Default is False
 
- **`apsync.add_attribute_tags(absolute_path, attribute_title, tag_names, type=AttributeType.multiple_choice_tag, workspace_id=None, auto_create=True, update_timeline=False)`**

    Adds a list of tags identified by name to an attribute. If no tags are assigned yet, this is equivalent to `set_attribute_tags`. Creates the attribute if it cannot be found and `auto_create` is True.

    Arguments
    - `absolute_path` *(str):* Path to the file or folder
    - `attribute_title` *(str):* Title of the attribute
    - `tag_names` *(list[str]):* The tags to add, identified by name
    - `type` *(class: AttributeType, optional):* Must be `multiple_choice_tag` or `single_choice_tag`. Default is `multiple_choice_tag`
    - `workspace_id` *(str, optional):* The workspace id, or None
    - `auto_create` *(bool, optional):* Automatically create the attribute if it does not exist. Default is True
    - `update_timeline` *(bool, optional):* True if the timeline should be notified. Default is False

- **`apsync.remove_attribute_tag(absolute_path, attribute_title, tag_name, type=AttributeType.multiple_choice_tag, workspace_id=None)`**

    Removes a tag identified by name from an attribute.

    Arguments
    - `absolute_path` *(str):* Path to the file or folder
    - `attribute_title` *(str):* Title of the attribute
    - `tag_name` *(str):* The tag to remove, identified by name
    - `type` *(class: AttributeType, optional):* Must be `multiple_choice_tag` or `single_choice_tag`. Default is `multiple_choice_tag`
    - `workspace_id` *(str, optional):* The workspace id, or None

### Examples

#### Basic Text Attributes

```python
import apsync
import anchorpoint

ctx = anchorpoint.get_context()
api = anchorpoint.get_api()

# Set a text attribute by name (will auto-create if doesn't exist)
api.attributes.set_attribute_value(ctx.path, "Description", "Hero character concept art for level 1")

# Get the description
description = api.attributes.get_attribute_value(ctx.path, "Description")
print(f"Description: {description}")
```
Sets a text attribute by name on the current file and reads it back. If the attribute does not exist yet, it is created automatically.

#### Working with Tags

```python
import apsync
import anchorpoint

ctx = anchorpoint.get_context()
api = anchorpoint.get_api()

# Create or get a single choice tag attribute
status_attribute = api.attributes.get_attribute("Status")
if not status_attribute:
    status_attribute = api.attributes.create_attribute("Status", apsync.AttributeType.single_choice_tag)
    
    # Set up the available tags for this attribute
    tags = [
        apsync.AttributeTag("In Progress", "blue"),
        apsync.AttributeTag("Complete", "green"),
        apsync.AttributeTag("On Hold", "orange")
    ]
    api.attributes.set_attribute_tags(status_attribute, tags)

# Set the status value
api.attributes.set_attribute_value(ctx.path, status_attribute, "In Progress")

# Or set using attribute name (simpler for existing attributes)
api.attributes.set_attribute_value(ctx.path, "Status", "Complete")

# Get the current status
current_status = api.attributes.get_attribute_value(ctx.path, "Status")
print(f"Current status: {current_status}")
```
Creates a single-choice tag attribute called "Status" with three predefined options, sets a value on the current file, and reads it back.

#### Rating and Review Workflow

```python
import apsync
import anchorpoint
from datetime import datetime

ctx = anchorpoint.get_context()
api = anchorpoint.get_api()

# Set quality rating (1-5 stars)
api.attributes.set_attribute_value(ctx.path, "Quality", 4)

# Mark as reviewed
api.attributes.set_attribute_value(ctx.path, "Reviewed", True)

# Set review date to current time
api.attributes.set_attribute_value(ctx.path, "Review Date", datetime.now())

# Add reviewer link
api.attributes.set_attribute_value(ctx.path, "Reviewer Profile", "

# Get review information
rating = api.attributes.get_attribute_value(ctx.path, "Quality")
is_reviewed = api.attributes.get_attribute_value(ctx.path, "Reviewed")
review_date = api.attributes.get_attribute_value(ctx.path, "Review Date")

print(f"Rating: {rating}/5 stars")
print(f"Reviewed: {is_reviewed}")
print(f"Review date: {review_date}")
```
Demonstrates setting multiple attribute types on a single file — a numeric rating, a checkbox, a date, and a hyperlink — then reads them all back.

#### Batch Processing with Attributes

```python
import apsync
import anchorpoint
import os
from datetime import datetime

ctx = anchorpoint.get_context()
api = anchorpoint.get_api()

# Process all selected files
for file_path in ctx.selected_files:
    filename = os.path.basename(file_path)
    
    # Set common attributes based on file type
    if filename.lower().endswith(('.jpg', '.png', '.tiff')):
        api.attributes.set_attribute_value(file_path, "Type", "Image")
        api.attributes.set_attribute_value(file_path, "Format", "Raster")
    elif filename.lower().endswith(('.fbx', '.obj', '.blend')):
        api.attributes.set_attribute_value(file_path, "Type", "3D Model")
        api.attributes.set_attribute_value(file_path, "Format", "3D Mesh")
    
    # Set processing timestamp
    api.attributes.set_attribute_value(file_path, "Processed", datetime.now())
    
    print(f"Processed: {filename}")
```
Iterates over all selected files and sets "Type" and "Format" attributes based on the file extension, tagging images and 3D models differently.

#### Creating Complex Attribute Workflows

```python
import apsync
import anchorpoint

ctx = anchorpoint.get_context()
api = anchorpoint.get_api()

def create_attribute_example():
    # This example shows how to access attributes and update the set of tags
    attribute = api.attributes.get_attribute("Python Example")
    if not attribute:
        attribute = api.attributes.create_attribute(
            "Python Example", apsync.AttributeType.single_choice_tag
        )

    new_tag_name = f"Example Tag {len(attribute.tags) + 1}"
    tags = attribute.tags
    tags.append(apsync.AttributeTag(new_tag_name, "blue"))
    api.attributes.set_attribute_tags(attribute, tags)

    return attribute

def set_attributes(file_path, example_attribute):
    # We can either use the attribute that we have created before ...
    latest_tag = example_attribute.tags[-1]
    api.attributes.set_attribute_value(file_path, example_attribute, latest_tag)
    print(api.attributes.get_attribute_value(file_path, example_attribute))

    # ... or create / use attributes described by their title
    api.attributes.set_attribute_value(file_path, "Message", "Hello from Python")
    print(api.attributes.get_attribute_value(file_path, "Message"))

    # To set a date, use datetime.datetime or a unix timestamp
    from datetime import datetime
    api.attributes.set_attribute_value(file_path, "Created At", datetime.now())

# Create the example attribute
attribute = create_attribute_example()

# Apply to all selected files
for file_path in ctx.selected_files:
    set_attributes(file_path, attribute)
```
Shows a reusable pattern for managing a tag attribute: creates the attribute if it doesn't exist, appends a new tag to its list, then applies both a tag value and a text value to every selected file.

## Source: documentation/docs/api/python/context.md


## Context

The Context API provides essential information about the current execution environment when an action is triggered in Anchorpoint. It gives you access to the selected files, folders, user information, project details, and input parameters defined in your action's YAML configuration.

### Usage

The context is obtained using the `get_context()` function from the `anchorpoint` module:

```python
import anchorpoint

ctx = anchorpoint.get_context()
```

### Context Class

#### Properties

##### File and Folder Information

- **`path`** *(str):* The absolute path to the file or folder where the action was triggered. For file actions: path to the selected file. For folder actions: path to the selected folder.
- **`folder`** *(str):* The absolute path to the parent folder. Always represents the directory containing the selected item.
- **`filename`** *(str):* The name of the selected file (without path). Empty string for folder actions.
- **`suffix`** *(str):* The file extension including the dot (e.g., `.py`, `.txt`). Empty string for folders or files without extensions.
- **`selected_files`** *(List[str]):* List of absolute paths to all selected files. Useful for batch operations on multiple files.
- **`type`** *(class: Type):* The type of object that triggered the action (file, folder, task, etc.).

##### User and Project Information

- **`username`** *(str):* The username of the current Anchorpoint user.
- **`user_id`** *(str):* Unique identifier of the current user.
- **`workspace_id`** *(str):* Unique identifier of the current workspace.
- **`project_id`** *(str):* Unique identifier of the current project. Empty string if not in a project context.
- **`project_path`** *(str):* The absolute file path to the root folder of the project.

##### Task Context

- **`task_id`** *(str):* Unique identifier of the task if action was triggered from a task. Empty string if not triggered from a task.
- **`task_list_id`** *(str):* Unique identifier of the task list containing the task. Empty string if not triggered from a task.

##### Action Configuration

- **`inputs`** *(Dict[str, Any]):* Dictionary containing input values defined in the action's YAML file inputs section. Access custom parameters passed to your action.
- **`icon`** *(str):* The icon path specified in the action's YAML configuration.
- **`module_path`** *(str):* Path to the directory containing the action's files.

##### Browser State

- **`browser_path`** *(str):* Current path shown in the Anchorpoint browser. May differ from `path` when action is triggered on specific items.
- **`browser_workspace_id`** *(str):* Workspace ID of the current browser view.
- **`browser_project_id`** *(str):* Project ID of the current browser view.

#### Methods

##### Asynchronous triggering of functions

- **`run_async(func, *args, **kwargs)`** Executes a function asynchronously with progress indication. Automatically shows progress dialog and handles UI updates. Use for long-running operations to keep UI responsive.

    Arguments
    - `func`: The function to execute asynchronously
    - `*args`: Positional arguments to pass to the function
    - `**kwargs`: Keyword arguments to pass to the function

    Returns: The return value of the executed function

##### Python Module Installation

- **`install(package, upgrade=False)`** Installs a Python module using pip to the global Python module directory. Only call this function when the module import fails to avoid slowing down your scripts.

    Arguments
    - `package` *(str):* The name of the package to install (e.g., "Pillow", "pywin32")
    - `upgrade` *(bool):* Set to True to upgrade the package to the latest version. Default is False

    Returns: None

### Examples

#### Basic File Information

```python
import anchorpoint

ctx = anchorpoint.get_context()

print(f"Selected file: {ctx.filename}")
print(f"File path: {ctx.path}")
print(f"Parent folder: {ctx.folder}")
print(f"File extension: {ctx.suffix}")
```
Prints several properties of the current context, when the action was triggered from a file context menu.

#### Working with Multiple Files

```python
import anchorpoint
import os

ctx = anchorpoint.get_context()

# Process all selected files
for file_path in ctx.selected_files:
    filename = os.path.basename(file_path)
    print(f"Processing: {filename}")
    
    # Your file processing logic here
```
Iterating over files, that have been selected in the Anchorpoint browser and the action has been triggered from the file context menu.

#### Using Input Parameters

In your YAML file:
```yaml
inputs:
  quality:
    name: "Quality"
    type: "dropdown"
    options: ["Low", "Medium", "High"]
    default: "Medium"
  compress:
    name: "Compress Output"
    type: "checkbox"
    default: true
```

In your Python script:
```python
import anchorpoint

ctx = anchorpoint.get_context()

# Access the input values
quality = ctx.inputs.get("quality", "Medium")
compress = ctx.inputs.get("compress", True)

print(f"Quality setting: {quality}")
print(f"Compression enabled: {compress}")
```
Reads values that have been added to the YAML file using the inputs key.

#### Async Operations

```python
import anchorpoint
import time

def long_running_task(file_path, output_path):

    # Create a simple infinite spinning progress indicator
    progress = anchorpoint.Progress("My Action", "Writing file...")

    # Simulate a time-consuming operation
    time.sleep(5)
    
    # Your actual processing logic here
    with open(output_path, 'w') as f:
        f.write(f"Processed: {file_path}")        

    # Explicitly finish the progress
    progress.finish()
    
    return f"Successfully processed {file_path}"

ctx = anchorpoint.get_context()

# Run the task asynchronously with automatic progress dialog
result = ctx.run_async(long_running_task, ctx.path, ctx.path + ".processed")
```
Triggers a background process that does not block the UI. Usually used with a progress indicator.

#### Project Context

```python
import anchorpoint
import apsync

ctx = anchorpoint.get_context()
api = anchorpoint.get_api()

# Check if we're in a project
if ctx.project_id:
    project = api.get_project()
    if project:
        print(f"Working in project: {project.name}")
        print(f"Project path: {project.path}")
else:
    print("Not in a project context")

# Access workspace information
print(f"Workspace ID: {ctx.workspace_id}")
print(f"Current user: {ctx.username}")
```
Reads information about the current project, workspace and user.

#### Installing Python Modules

```python
import anchorpoint
import time

def process_file(file_path):
    ctx = anchorpoint.get_context()
    
    # Try to import the module, install if not available
    try:
        import win32com.client
    except ImportError:
        ctx.install("pywin32")
        import win32com.client
    
    # Use the module
    # Your processing logic here
    time.sleep(2)
    
    return f"Processed {file_path} with win32com"

ctx = anchorpoint.get_context()

# Run the installation and processing asynchronously
result = ctx.run_async(process_file, ctx.path)
print(result)
```
Installs a Python module on-demand when it's not available and processes the file in an async function to keep the UI responsive.

## Source: documentation/docs/api/python/hooks.md


## Event Hooks

Event hooks in Anchorpoint allow you to respond to specific events that happen within the application. Every time a certain event occurs, a Python callback function is triggered automatically. This enables you to create reactive workflows and automate tasks based on user interactions and system changes.

### Usage

To implement event hooks, simply define callback functions with specific names within your action's Python script. You don't need to register these functions explicitly - Anchorpoint will automatically detect and call them when the corresponding events occur.

```python
import anchorpoint

def on_timeout(ctx: anchorpoint.Context):
    # This code will be automatically executed once every minute
    print("timeout callback")

def on_folder_opened(ctx: anchorpoint.Context):
    # This code will be executed when user navigates to a folder
    print(f"folder opened: {ctx.path}")

if __name__ == "__main__":
    # This code will be executed when the user triggers the action manually
    print("Action invoked!")
```

**Important:** When mixing event hooks with regular action code, make sure to guard your normal action code using `if __name__ == "__main__":` to prevent it from executing when the script is loaded for hooks.

### Application Events

- **`on_timeout(ctx)`** Called once every minute automatically. Useful for periodic checks, background tasks, or monitoring file system state.

    Arguments
    - `ctx` *(class: Context)*: Current context with browser state

- **`on_folder_opened(ctx)`** Called whenever the user navigates to a folder in Anchorpoint. Useful for folder-specific initialization or validation.

    Arguments
    - `ctx` *(class: Context)*: Current context with the opened folder path

- **`on_project_directory_changed(ctx)`** Called when any change is detected within the active project directory. Triggered by file modifications, additions, deletions, etc. Only works for the currently active project in Anchorpoint.

    Arguments
    - `ctx` *(class: Context)*: Current context of the active project

- **`on_application_started(ctx)`** Called once for each workspace when Anchorpoint starts up. Useful for initialization routines or startup checks.

    Arguments
    - `ctx` *(class: Context)*: Context for the starting workspace

- **`on_application_closing(ctx)`** Called just before Anchorpoint closes. Useful for cleanup tasks or saving state.

    Arguments
    - `ctx` *(class: Context)*: Current context before shutdown

### Task Events

- **`on_task_created(task_id, source, ctx)`** Called when a new task is created.

    Arguments
    - `task_id` *(str)*: ID of the newly created task
    - `source` *(class: ChangeSource)*: Source of the change (You, Action, Other)
    - `ctx` *(class: Context)*: Current context

- **`on_task_changed(task_id, source, ctx)`** Called when an existing task is modified.

    Arguments
    - `task_id` *(str)*: ID of the modified task
    - `source` *(class: ChangeSource)*: Source of the change (You, Action, Other)
    - `ctx` *(class: Context)*: Current context

- **`on_task_removed(task_id, source, ctx)`** Called when a task is deleted.

    Arguments
    - `task_id` *(str)*: ID of the deleted task
    - `source` *(class: ChangeSource)*: Source of the change (You, Action, Other)
    - `ctx` *(class: Context)*: Current context

### Attribute Events

- **`on_attributes_changed(parent_path, attributes, ctx)`** Called when attributes are modified on files, folders, or tasks. Provides detailed information about what changed.

    Arguments
    - `parent_path` *(str)*: Path of the parent object containing the changed attributes
    - `attributes` *(List[AttributeChange])*: List of attribute changes
    - `ctx` *(class: Context)*: Current context

### AttributeChange Class

- **`AttributeChange`** Represents a value change of an attribute. Provides information about what changed, including the old and new values, and the source of the change.

#### Properties

- **`path`** *(str):* Path of the object where the attribute changed (None for tasks).
- **`task_id`** *(str):* ID of the task where the attribute changed (None for files/folders).
- **`object_type`** *(class: ObjectType):* Type of object (file, folder, or task).
- **`name`** *(str):* Name of the changed attribute.
- **`type`** *(class: AttributeType):* Type of the attribute (text, rating, tag, etc.).
- **`value`** *(Any):* New value of the attribute.
- **`old_value`** *(Any):* Previous value of the attribute.
- **`source`** *(class: ChangeSource):* Source of the change.
- **`source_value`** *(str):* Client name for "Other" source changes.

#### ChangeSource Enumeration

- **`ChangeSource`** Enumeration that indicates who made a change to an attribute or task. Used to identify the source of modifications for proper handling and filtering.

##### Values
- `ChangeSource.You` *(enum)*: The change was made by yourself
- `ChangeSource.Action` *(enum)*: The change was made by an action on your machine
- `ChangeSource.Other` *(enum)*: The change was made by someone else

### Notification Events

- **`on_channel_notification(channel_id, channel_entry_ids, messages, module, branch, project_id, project_path, ctx)`** Called when a channel notification is triggered. This hook is invoked when `schedule_channel_notification` is executed, allowing you to respond to timeline channel notifications.

    Arguments
    - `channel_id` *(str):* Timeline channel identifier where the notification occurred
    - `channel_entry_ids` *(list[str]):* List of channel entry IDs associated with the notification
    - `messages` *(list[str]):* List of notification messages (may contain @username mentions)
    - `module` *(str or None):* Module name for the channel (if specified)
    - `branch` *(str or None):* Branch name for the channel (if specified)
    - `project_id` *(str or None):* Project identifier where the notification occurred
    - `project_path` *(str or None):* Absolute path to the project
    - `ctx` *(class: Context)*: Current context

- **`on_custom_notification(message, meta_data, project_id, project_path, ctx)`** Called when a custom notification is triggered. This hook is invoked when `schedule_custom_notification` is executed, allowing you to respond to custom notifications with metadata.

    Arguments
    - `message` *(str):* The notification message sent to the user
    - `meta_data` *(dict or None):* Dictionary of metadata included with the notification (if provided)
    - `project_id` *(str or None):* Project identifier where the notification occurred (if specified)
    - `project_path` *(str or None):* Absolute path to the project (if specified)
    - `ctx` *(class: Context)*: Current context

### Action Events

- **`on_is_action_enabled(path, type, ctx)`** Special hook called to determine if an action should be shown to the user. Must be enabled in YAML configuration: `register: folder: enable: script_with_hook.py`

    Arguments
    - `path` *(str)*: Path to check (may differ from ctx.path)
    - `type` *(class: Type)*: Type of the action being checked
    - `ctx` *(class: Context)*: Current browser context

    Returns: (*bool*) True if action should be enabled, False otherwise

- **`on_event_received(id, payload, ctx)`** Listens to other actions and triggers once the other action has been triggered. This hook follows the fire and forget principle. Useful for e.g. a post-merge hook.

    Arguments
    - `id` *(str)*: The id of the event that has been triggered
    - `payload` *(dict)*: A dictionary with event details, typically `{"type": "success"}`, `{"type": "error"}`, `{"type": "conflict"}`, or `{"type": "cancel"}`
    - `ctx` *(class: Context)*: Current context

##### Built-in Git Events

The following events are sent automatically by Anchorpoint's built-in Git operations. You can listen to them using `on_event_received`.

| Event ID | Description | Payload Types |
|----------|-------------|---------------|
| `gitpull` | Fired after a git pull or sync operation | `success`, `error`, `cancel`, `conflict` |
| `gitclone` | Fired after cloning or joining a git repository | `success`, `error` |
| `gitswitchbranch` | Fired after switching to a different branch | `success`, `error`, `conflict` |
| `gitmergebranch` | Fired after merging a branch | `success`, `error`, `conflict` |

##### Sending Custom Events

You can also send your own events from actions using `ap.send_event` and listen to them in other actions with `on_event_received`.

```python
import anchorpoint as ap

ctx = ap.get_context()
ap.send_event(ctx, "my_custom_event", {"type": "success"})
```

### Version Control Hooks

- **`on_before_commit(channel_id, message, changes, all_files_selected, progress, ctx)`** Called right before a git commit or sync is executed. This hook lets you modify the commit message, validate the commit, or cancel it entirely.

    Arguments
    - `channel_id` *(str)*: The timeline channel ID (e.g. "Git")
    - `message` *(str)*: The commit message entered by the user
    - `changes` *(list[VCPendingChange])*: List of pending changes that will be committed
    - `all_files_selected` *(bool)*: True if the user selected all files for the commit
    - `progress` *(class: Progress)*: Progress indicator for long-running validations
    - `ctx` *(class: Context)*: Current context

    Returns: *(str or None)* Return the commit message (original or modified) to proceed with the commit. Return `None` to cancel the commit.

#### VCPendingChange Class

Inherits from VCChange. Represents a file that is about to be committed.

##### Properties

- **`is_dirty_module`** *(bool):* True if the change is in a dirty submodule
- **`is_unsynced_module`** *(bool):* True if the change is in an unsynced submodule

#### VCChange Class

Represents a version-controlled file change.

##### Properties

- **`path`** *(str):* Absolute path to the changed file
- **`status`** *(class: VCFileStatus)*: The type of change (new, modified, deleted, etc.)
- **`is_module`** *(bool):* True if the change is a submodule

#### VCFileStatus Enumeration

Indicates what kind of change was made to a file.

##### Values
- `VCFileStatus.Unknown`
- `VCFileStatus.New`
- `VCFileStatus.Deleted`
- `VCFileStatus.Modified`
- `VCFileStatus.Renamed`
- `VCFileStatus.Conflicted`

### Examples

#### Periodic Monitoring

```python
import anchorpoint
import os
from datetime import datetime

def on_timeout(ctx: anchorpoint.Context):
    """Monitor project for large files every minute"""
    if not ctx.project_id:
        return
    
    api = anchorpoint.get_api()
    large_files = []
    
    # Check for files larger than 100MB in current project
    for root, dirs, files in os.walk(ctx.path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getsize(file_path) > 100 * 1024 * 1024:  # 100MB
                large_files.append(file_path)
    
    # Tag large files
    for file_path in large_files:
        api.attributes.set_attribute_value(file_path, "Size Warning", "Large File")
        api.attributes.set_attribute_value(file_path, "Last Checked", datetime.now())

if __name__ == "__main__":
    print("Large file monitor action invoked manually")
```
Checks for large files every minute and sets a text Attribute on the large file

#### Folder Navigation Tracking

```python
import anchorpoint
import apsync
from datetime import datetime

def on_folder_opened(ctx: anchorpoint.Context):
    """Track folder access and set last visited timestamp"""
    api = anchorpoint.get_api()
    
    # Set last visited attribute on folder
    api.attributes.set_attribute_value(ctx.path, "Last Visited", datetime.now())
    api.attributes.set_attribute_value(ctx.path, "Visited By", ctx.username)
    
    # Check if this is a project folder
    project = api.get_project()
    if project and ctx.path == project.path:
        print(f"Project {project.name} accessed by {ctx.username}")

if __name__ == "__main__":
    print("Folder tracking action invoked")
```
Triggers once the user navigates to a folder in the Anchorpoint browser and sets an Attribute on the current folder that is being opened.

#### Attribute Change Monitoring

```python
import anchorpoint

def on_attributes_changed(parent_path: str, attributes: list[anchorpoint.AttributeChange], ctx: anchorpoint.Context):
    """Monitor and react to attribute changes"""
    api = anchorpoint.get_api()
    
    for attribute in attributes:
        print(f"Attribute '{attribute.name}' changed from '{attribute.old_value}' to '{attribute.value}'")        
        
		print(f"File/folder '{attribute.path}' attribute changed")
		
		# Auto-create backup when marked as "Final"
		if attribute.name == "Version" and attribute.value == "Final":
			backup_path = attribute.path + ".backup"
			# Implementation would copy file to backup location
			api.attributes.set_attribute_value(backup_path, "Backup Of", attribute.path)

if __name__ == "__main__":
    print("Attribute monitoring loaded")
```
Triggers if an Attribute changes and iterates through the changed Attributes.

#### Conditional Action Enabling

```python
import anchorpoint
import os

def on_is_action_enabled(path: str, type: anchorpoint.Type, ctx: anchorpoint.Context) -> bool:
    """Enable action only for specific conditions"""
    
    # Enable only in "shots" folders
    if "shots" in path.lower():
        return True
    
    # Enable for video files
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv']
    if any(path.lower().endswith(ext) for ext in video_extensions):
        return True
    
    # Enable if file has specific attribute
    api = anchorpoint.get_api()
    try:
        status = api.attributes.get_attribute_value(path, "Render Status")
        return status == "Ready"
    except:
        return False

if __name__ == "__main__":
    print("Conditional action executed")
```
This hook triggers when Anchorpoint starts up or loads a project and can be used to e.g. enable a button. The Python script has to be referenced in a YAML file like in this example.

#### Post merge actions

```python
import anchorpoint
import os

def on_event_received(id, payload, ctx: anchorpoint.Context):

    # payload looks like this: {'type': 'success'} 
    if isinstance(payload, dict):
        payload = payload.get('type')  

    # trigger on pull
    if id == "gitpull" and payload == "success":
        print("Git pull finished")

    # trigger on merge
    if id == "gitmergebranch" and payload == "success":
        print("Git branch merge finished")

    # trigger on switch branch
    if id == "gitswitchbranch" and payload == "success":
        print("Git branch switch finished")
```
This hook listens to the Git events "git pull", "git merge branch" and "git switch branch" and triggers a print if the payload is "success".

#### Before Commit Validation

```python
import anchorpoint

def on_before_commit(channel_id, message, changes, all_files_selected, progress, ctx: anchorpoint.Context):
    """Validate commit message and files before committing"""

    # Require a commit message with a minimum length
    if len(message.strip()) < 10:
        anchorpoint.UI().show_info("Commit Rejected", "Commit message must be at least 10 characters.")
        return None

    # Check for forbidden file types
    for change in changes:
        if change.path.endswith(".tmp"):
            anchorpoint.UI().show_info("Commit Rejected", f"Cannot commit temporary file: {change.path}")
            return None

    # Optionally modify the commit message
    return f"[{ctx.username}] {message}"
```
This hook validates that the commit message has a minimum length, prevents committing `.tmp` files, and prepends the username to the commit message. Return `None` to cancel the commit, or the (modified) message string to proceed.

#### Before Commit - Cancel

```python
def on_before_commit(channel_id, message, changes, all_files_selected, progress, ctx):
    return None
```
Return `None` to cancel the commit entirely.

#### Before Commit - Modify Message

```python
def on_before_commit(channel_id, message, changes, all_files_selected, progress, ctx):
    return "[HOOK] " + message
```
Return a modified string to change the commit message before it is applied.

#### Channel Notification Handler

```python
import anchorpoint
import json

def on_channel_notification(channel_id: str, channel_entry_ids: list[str], messages: list[str], 
                           module: str, branch: str, project_id: str, project_path: str, 
                           ctx: anchorpoint.Context):
    """Handle channel notifications and perform custom actions"""
    
    print(f"Notification received for channel: {channel_id}")
    print(f"Project: {project_id} at {project_path}")
    print(f"Module: {module}, Branch: {branch}")
    
    # Process each notification message
    for entry_id, message in zip(channel_entry_ids, messages):
        print(f"Entry {entry_id}: {message}")
        
        # Check if the current user was mentioned
        if f"@{ctx.username}" in message:
            print(f"You were mentioned in: {message}")
            
            # Create a task for the mention
            api = anchorpoint.get_api()
            project = api.get_project()
            
            if project:
                # You could create a task, send another notification, or trigger other workflows
                print(f"Creating follow-up task for mention in {channel_id}")
    
    # Example: Log notification to a file for audit purposes
    log_file = f"{ctx.path}/notifications.log"
    with open(log_file, "a") as f:
        f.write(f"[{channel_id}] {len(messages)} notifications received\n")

if __name__ == "__main__":
    print("Channel notification handler loaded")
```
This hook is triggered when `schedule_channel_notification` is called and receives all notification details, allowing you to create custom workflows based on timeline notifications.

#### Custom Notification Handler

```python
import anchorpoint
import apsync

def on_custom_notification(message: str, meta_data: dict, project_id: str, 
                          project_path: str, ctx: anchorpoint.Context):
    """Handle custom notifications with metadata"""
    
    print(f"Custom notification received: {message}")
    print(f"Project: {project_id} at {project_path}")
    
    # Check if metadata was provided
    if meta_data:
        print(f"Metadata: {meta_data}")
        
        # Example: Handle workflow-based notifications
        workflow = meta_data.get("workflow")
        
        if workflow == "asset_approval":
            status = meta_data.get("status")
            asset_path = meta_data.get("asset_path")
            priority = meta_data.get("priority")
            
            print(f"Asset approval workflow triggered")
            print(f"Status: {status}, Priority: {priority}")
            print(f"Asset: {asset_path}")
            
            # Auto-respond to high-priority notifications
            if priority == "high":
                api = anchorpoint.get_api()
                project = api.get_project()
                
                if project and asset_path:
                    # Set attribute or create task
                    api.attributes.set_attribute_value(
                        asset_path, 
                        "Review Status", 
                        "In Review"
                    )
                    print(f"Set review status for {asset_path}")
        
        # Example: Handle file update notifications
        elif workflow == "file_updated":
            file_path = meta_data.get("file_path")
            version = meta_data.get("version")
            
            print(f"File updated: {file_path} (version {version})")
            
            # You could trigger a reload, open the file, or sync
            if file_path:
                print(f"Consider reloading: {file_path}")
    
    # Log the notification
    if project_path:
        log_file = f"{project_path}/.anchorpoint/custom_notifications.log"
        with open(log_file, "a") as f:
            f.write(f"[{message}] Metadata: {meta_data}\n")

if __name__ == "__main__":
    print("Custom notification handler loaded")
```
This hook is triggered when `schedule_custom_notification` is called and receives the message and metadata, allowing you to create automated workflows and respond to custom events.

### Timeline Context Menu Hooks

Timeline context menu hooks allow you to add custom actions to the right-click menu of timeline entries. Register your action using the YAML register keys `timeline_commit`, `timeline_stash`, or `timeline_changed_files`.

#### Commit and Stash Actions

- **`on_timeline_entry_context_action(channel_id, action_id, entry_id, ctx)`** Called when a user clicks your custom action in the right-click menu of a commit or stash entry.

    Arguments
    - `channel_id` *(str)*: The timeline channel identifier (e.g. `"Git"`)
    - `action_id` *(str)*: Your action's unique identifier from the YAML file
    - `entry_id` *(str)*: The commit hash or stash id
    - `ctx` *(class: Context)*: Current context

Both `timeline_commit` and `timeline_stash` YAML registrations use the same hook function. If you need to distinguish between commits and stashes, you can check the `entry_id` format — commit hashes are long hex strings, stash ids are short numbers.

```yaml
version: 1.0
action:
  name: "Show Commit in GitLab"
  id: "my::show_in_gitlab"
  type: python
  icon:
    path: :/icons/link.svg
  script: "show_in_gitlab.py"
  register:
    timeline_commit:
      enable: true
```

```python
import anchorpoint as ap
import webbrowser

def on_timeline_entry_context_action(channel_id, action_id, entry_id, ctx):
    gitlab_url = f"
    webbrowser.open(gitlab_url)
```

#### Changed Files Actions

- **`on_timeline_changed_files_context_action(channel_id, action_id, changes, ctx)`** Called when a user clicks your custom action in the right-click menu of the "Changed Files" entry.

    Arguments
    - `channel_id` *(str)*: The timeline channel identifier (e.g. `"Git"`)
    - `action_id` *(str)*: Your action's unique identifier from the YAML file
    - `changes` *(list[VCPendingChange])*: The list of currently pending changes
    - `ctx` *(class: Context)*: Current context

```yaml
version: 1.0
action:
  name: "List Changed Files"
  id: "my::list_changes"
  type: python
  icon:
    path: :/icons/list.svg
  script: "list_changes.py"
  register:
    timeline_changed_files:
      enable: true
```

```python
import anchorpoint as ap

def on_timeline_changed_files_context_action(channel_id, action_id, changes, ctx):
    for change in changes:
        print(f"Changed: {change.path}")
    ap.UI().show_success(f"{len(changes)} files changed")
```

## Source: documentation/docs/api/python/locks.md


## Locks

The Locks API in Anchorpoint provides file locking functionality to prevent concurrent modifications and ensure workflow integrity. File locks are essential for collaborative workflows, especially with binary files that cannot be merged automatically.

### Usage

Lock-related functions are accessed directly from the `anchorpoint` module and work in conjunction with Context to manage file access in projects.

```python
import anchorpoint

ctx = anchorpoint.get_context()

# Basic lock operation
anchorpoint.lock(
    ctx.workspace_id,
    ctx.project_id,
    [ctx.path],
    description="Working on texture adjustments"
)

# Perform your work...

# Unlock when finished
anchorpoint.unlock(ctx.workspace_id, ctx.project_id, [ctx.path])
```

### Functions

- **`lock(workspace_id, project_id, targets, description=None, metadata=None)`** Locks one or more files or folders to prevent other users from modifying them. Locked files appear with a lock indicator in Anchorpoint and prevent conflicts during collaborative work.

    Arguments
    - `workspace_id` *(str)*: Unique identifier of the workspace
    - `project_id` *(str)*: Unique identifier of the project
    - `targets` *(List[str])*: List of absolute file or folder paths to lock
    - `description` *(str, optional)*: Human-readable description of why files are locked
    - `metadata` *(Dict[str, str], optional)*: Additional metadata associated with the lock

- **`unlock(workspace_id, project_id, targets, force=False)`** Unlocks previously locked files or folders, allowing other users to modify them again.

    Arguments
    - `workspace_id` *(str)*: Unique identifier of the workspace
    - `project_id` *(str)*: Unique identifier of the project
    - `targets` *(List[str])*: List of absolute file or folder paths to unlock
    - `force` *(bool, optional)*: Force unlock even if you are not the lock owner (requires appropriate permissions)

- **`get_locks(workspace_id, project_id)`** Retrieves all current locks within a project, including lock details and ownership information.

    Arguments
    - `workspace_id` *(str)*: Unique identifier of the workspace
    - `project_id` *(str)*: Unique identifier of the project

    Returns: (*List[Lock]*) List of Lock objects representing all active locks

- **`evaluate_locks(workspace_id, project_id)`** Triggers lock evaluation and synchronization within the project. Useful for refreshing lock states and ensuring consistency.

    Arguments
    - `workspace_id` *(str)*: Unique identifier of the workspace
    - `project_id` *(str)*: Unique identifier of the project

- **`update_locks(workspace_id, project_id, locks)`** Updates lock information for existing locks. Used internally for synchronization but can be called manually when needed.

    Arguments
    - `workspace_id` *(str)*: Unique identifier of the workspace
    - `project_id` *(str)*: Unique identifier of the project
    - `locks` *(List[Lock])*: List of Lock objects to update

### LockDisabler Class

- **`class LockDisabler()`** Context manager that temporarily disables lock evaluation during batch operations. Useful when performing multiple file operations that might trigger unnecessary lock checks.

#### Usage
```python
with anchorpoint.LockDisabler():
    # Perform multiple file operations without lock overhead
    pass
```

### Lock Class

The Lock class represents a file or folder lock with the following properties:

#### Properties

- **`path`** *(str):* Absolute path to the locked file or folder.
- **`owner`** *(str):* Username of the lock owner.
- **`description`** *(str):* Description of why the file is locked.
- **`metadata`** *(Dict[str, str]):* Additional lock metadata.
- **`timestamp`** *(datetime):* When the lock was created.

### Examples

#### Basic File Locking

```python
import anchorpoint

ctx = anchorpoint.get_context()

# Lock the currently selected file
if ctx.path:
    anchorpoint.lock(
        ctx.workspace_id, 
        ctx.project_id, 
        [ctx.path], 
        description=f"Editing {ctx.filename}"
    )
    print(f"Locked: {ctx.filename}")

# Later, unlock the file
anchorpoint.unlock(ctx.workspace_id, ctx.project_id, [ctx.path])
print(f"Unlocked: {ctx.filename}")
```

#### Batch File Operations

```python
import anchorpoint
import os

ctx = anchorpoint.get_context()

# Lock multiple files before batch processing
files_to_process = [
    "/project/models/character.fbx",
    "/project/models/environment.fbx",
    "/project/textures/character_diffuse.png"
]

# Lock all files with descriptive message
anchorpoint.lock(
    ctx.workspace_id,
    ctx.project_id,
    files_to_process,
    description="Batch processing: Optimizing models and textures",
    metadata={"batch_id": "optimization_001", "tool": "model_optimizer"}
)

try:
    # Perform batch processing
    for file_path in files_to_process:
        print(f"Processing: {os.path.basename(file_path)}")
        # Your processing logic here
        
finally:
    # Always unlock files when done
    anchorpoint.unlock(ctx.workspace_id, ctx.project_id, files_to_process)
    print("Batch processing complete - all files unlocked")
```

#### Lock Management and Monitoring

```python
import anchorpoint

ctx = anchorpoint.get_context()

def show_project_locks():
    """Display all locks in the current project"""
    if not ctx.project_id:
        print("Not in a project context")
        return
    
    locks = anchorpoint.get_locks(ctx.workspace_id, ctx.project_id)
    
    if not locks:
        print("No locks found in project")
        return
    
    print(f"Found {len(locks)} locks:")
    for lock in locks:
        print(f"  📁 {lock.path}")
        print(f"     Owner: {lock.owner}")
        print(f"     Reason: {lock.description}")
        if lock.metadata:
            print(f"     Metadata: {lock.metadata}")
        print()

def unlock_my_files():
    """Unlock all files locked by current user"""
    locks = anchorpoint.get_locks(ctx.workspace_id, ctx.project_id)
    my_locks = [lock.path for lock in locks if lock.owner == ctx.username]
    
    if my_locks:
        anchorpoint.unlock(ctx.workspace_id, ctx.project_id, my_locks)
        print(f"Unlocked {len(my_locks)} files owned by you")
    else:
        print("No files locked by you")

# Show current locks
show_project_locks()

# Unlock your files
unlock_my_files()
```

## Source: documentation/docs/api/python/progress.md


## Progress

The Progress API in Anchorpoint provides functionality to display progress indicators and status updates during long-running operations. Progress dialogs help users understand that operations are running and provide feedback on completion status. The progress logic is usually placed in an asynchronous function.

### Usage

The Progress class is used to show progress dialogs and status updates to users during operations. You create a Progress instance and use its methods to update the display. This code should be placed in an asynchronous function, that is managed by the context.

```python
import anchorpoint

# Create a progress dialog
progress = anchorpoint.Progress(
    title="Processing Files",
    text="Please wait while files are being processed...",
    infinite=False,
    cancelable=True
)

# Report progress percentage
progress.report_progress(0.5)  # 50% complete
progress.set_text("Processing files...")

# Check if user canceled
if progress.canceled:
    print("Operation was canceled")
```

### Progress Class

#### Constructor

- **`anchorpoint.Progress(title, text=None, infinite=True, cancelable=False, show_loading_screen=False, delay=None)`**

    Creates a Progress object that starts spinning in the Anchorpoint UI. When creating a Progress object a spinning indicator is shown to the user indicating that something is being processed.

    Arguments
    - `title` *(str)*: Title text displayed in the progress dialog
    - `text` *(str, optional)*: Additional descriptive text shown below the title
    - `infinite` *(bool, optional)*: If True, shows an infinite progress bar; if False, shows determinate progress (default: True)
    - `cancelable` *(bool, optional)*: Whether users can cancel the operation (default: False)
    - `show_loading_screen` *(bool, optional)*: Whether to show a loading screen overlay (default: False)
    - `delay` *(float, optional)*: Delay in seconds before showing the progress indicator (default: None)

#### Methods

- **`finish()`** Explicitly finishes the progress indicator.

- **`report_progress(percentage)`** Reports progress to the users by showing a loading bar. Only works if `infinite=False`.

    Arguments
    - `percentage` *(float)*: Percentage from 0.0 to 1.0

- **`set_cancelable(cancelable)`** Changes if the progress indicator is cancelable.

    Arguments
    - `cancelable` *(bool)*: Whether to allow cancellation

- **`set_text(text)`** Updates the text in the progress indicator.

    Arguments
    - `text` *(str)*: The text to set

- **`stop_progress()`** Falls back to a spinning progress indicator.

### Properties

**`canceled`** *(bool)*
- True if the user has canceled the action
- Can be polled when doing a long running async job to check for user cancellation
- Returns False if the operation is still running normally

### Examples

#### Simple Spinning Progress

```python
import anchorpoint

# Create a simple infinite spinning progress indicator
progress = anchorpoint.Progress("My Action", "Rendering the scene")

# Do some work...
import time
time.sleep(2)

# Explicitly finish the progress
progress.finish()
```
Shows an infinite progress.

#### Determinate Progress with Percentage

```python
import anchorpoint

# Create progress with percentage reporting
progress = anchorpoint.Progress("My Action", "Rendering the scene", infinite=False)

# Report 50% progress
progress.report_progress(0.5)

# Update the text
progress.set_text("Almost done...")

# Report completion
progress.report_progress(1.0)
```
Shows a percentage-based progress.

#### Cancelable Progress

```python
import anchorpoint
import time

# Create cancelable progress
progress = anchorpoint.Progress("Long Operation", "Processing data...", cancelable=True)

# Simulate long operation with cancellation check
for i in range(100):
    if progress.canceled:
        print("Operation was canceled by user")
        break
    
    # Do some work
    time.sleep(0.1)
    
    # Update progress if using determinate mode
    if not progress.infinite:
        progress.report_progress(i / 100.0)

progress.finish()
```
In this example the option to cancel the progress is enabled. Once the user clicks on cancel, a print statement is shown and the progress is finished.

#### Progress Reporting in an asynchronous function

```python
import anchorpoint
import time

def process_files(files, progress):
    """Process a list of files with progress updates"""
    total_files = len(files)
    
    for i, file_path in enumerate(files):
        # Update progress percentage
        percentage = i / total_files
        progress.report_progress(percentage)
        progress.set_text(f"Processing: {file_path}")
        
        # Check for cancellation
        if progress.canceled:
            print(f"Processing canceled at file {i}")
            return False
        
        # Simulate file processing
        print(f"Processing {file_path}")
        time.sleep(0.5)
    
    # Final update
    progress.report_progress(1.0)
    progress.set_text("Processing complete")
    return True

ctx = anchorpoint.get_context()

# Create progress object
progress = anchorpoint.Progress("Processing Files", "Processing selected files...", infinite=False, cancelable=True)

# Process selected files
if ctx.selected_files:
    result = ctx.run_async(process_files, ctx.selected_files, progress)
    if result:
        print("All files processed successfully")
    else:
        print("Processing was interrupted")
```
This is a real life scenario how progress should be implemented in a asynchronous function using the context class.

## Source: documentation/docs/api/python/project.md


## Project

The Project class represents an Anchorpoint project, providing access to project metadata, settings, and operations. Projects in Anchorpoint serve as containers for organizing files, tasks, and team collaboration within specific workspaces.

### Usage

Projects are typically accessed through the API or context, but can also be managed using utility functions:

```python
import anchorpoint
import apsync

# Get current project through API
api = anchorpoint.get_api()
project = api.get_project()

# Get project from a specific path
project = apsync.get_project("/path/to/project")

# Get project by ID
project = apsync.get_project_by_id("project_id", "workspace_id")

# Create a new project
new_project = apsync.create_project("/path/to/new/project", "My New Project", "workspace_id")

# Check if a path is within a project
is_in_project = apsync.is_project("/some/path", recursive=True)
```

### Project Class

#### Properties

- **`id`** *(str):* Unique identifier for the project within the workspace. Used for API calls and project references.
- **`name`** *(str):* Human-readable name of the project. Can be modified by project administrators.
- **`path`** *(str):* Absolute file system path to the project root directory. Where project files and folders are stored.
- **`workspace_id`** *(str):* Identifier of the workspace containing this project. Links the project to its parent workspace.
- **`description`** *(str):* Optional project description. Provides additional context about the project's purpose.
- **`color`** *(str):* Project color for visual identification in the UI. Hex color code (e.g., "#FF5733").
- **`icon`** *(str):* Path or identifier for the project icon. Used in the Anchorpoint interface for visual recognition.
- **`created_at`** *(int):* Creation timestamp in seconds since epoch. When the project was first created.
- **`updated_at`** *(int):* Last update timestamp in seconds since epoch. When project metadata was last modified.

#### Methods

- **`get_members()`** Gets all members who have access to this project.

    Returns: (*class: GroupMemberList*) List of project members with their access levels

- **`add_member(email, access_level)`** Adds a new member to the project with specified access level.

    Arguments
    - `email` *(str)*: Email address of the user to add
    - `access_level` *(class: AccessLevel)*: Permission level for the user

- **`remove_member(email)`** Removes a member from the project.

    Arguments
    - `email` *(str)*: Email address of the user to remove

- **`update_settings(settings)`** Updates project configuration settings.

    Arguments
    - `settings` *(dict)*: Dictionary of setting key-value pairs

- **`get_timeline_channels()`** Gets all timeline channels associated with this project.

    Returns: (*list of TimelineChannel*) Project timeline channels

### Project Utility Functions

#### Project Management

- **`create_project(path, name, workspace_id=None)`** Creates a new Anchorpoint project.

    Arguments
    - `path` *(str):* Project root path
    - `name` *(str):* Project name
    - `workspace_id` *(str):* Optional workspace ID

    Returns: (*class: Project*) Created project object

- **`get_project(path)`** Gets project information for a given path.

    Arguments
    - `path` *(str):* Path within a project

    Returns: (*class: Project or None*) Project object or None if not found

- **`get_project_by_id(id, workspace_id)`** Gets a project by its ID.

    Arguments
    - `id` *(str):* Project identifier
    - `workspace_id` *(str):* Workspace identifier

    Returns: (*class: Project*) Project object

- **`get_projects(workspace_id)`** Gets all projects in a workspace.

    Arguments  
    - `workspace_id` *(str):* Workspace identifier

    Returns: (*listclass: [Project]*) List of Project objects

- **`is_project(path, recursive=False)`** Checks if a path is within an Anchorpoint project.

    Arguments
    - `path` *(str):* Path to check
    - `recursive` *(bool):* Whether to check parent directories

    Returns: (*bool*) True if path is within a project

- **`remove_project(project)`** Removes a project.

    Arguments
    - `project` *(class: Project):* Project to remove

#### Project File Operations

- **`create_project_file(path, project_id, workspace_id)`** Creates a project file at the specified path.

    Arguments
    - `path` *(str):* Path where project file should be created
    - `project_id` *(str):* Project identifier
    - `workspace_id` *(str):* Workspace identifier

#### Project Import/Export

- **`export_project(project, userIds=None)`** Exports project data.

    Arguments
    - `project` *(class: Project):* Project to export
    - `userIds` *(list[str]):* Optional list of user IDs to include in export

    Returns: (*str*) Path to exported project data

- **`import_project(workspace_id, project_data_path, target_path)`** Imports project data.

    Arguments
    - `workspace_id` *(str):* Target workspace ID
    - `project_data_path` *(str):* Path to project data to import
    - `target_path` *(str):* Target path for imported project

#### Project User Management

- **`add_user_to_project(workspace_id, project_id, invited_from, email, access_level)`** Adds a user to a project.

    Arguments
    - `workspace_id` *(str):* Workspace identifier
    - `project_id` *(str):* Project identifier
    - `invited_from` *(str):* Email of user sending invitation
    - `email` *(str):* Email of user to add
    - `access_level` *(class: AccessLevel):* Access level for the user

- **`remove_user_from_project(workspace_id, project_id, email)`** Removes a user from a project.

    Arguments
    - `workspace_id` *(str):* Workspace identifier
    - `project_id` *(str):* Project identifier  
    - `email` *(str):* Email of user to remove

- **`get_project_members(workspace_id, project_id)`** Gets all members of a project.

    Arguments
    - `workspace_id` *(str):* Workspace identifier
    - `project_id` *(str):* Project identifier

    Returns: (*class: GroupMemberList*) List of project members

#### Project Dialog Management

- **`show_create_project_dialog(path=None, project_id=None, remote_url=None, tags=[])`** Shows the create project dialog.

    Arguments
    - `path` *(str):* Optional initial path
    - `project_id` *(str):* Optional project ID for editing existing project
    - `remote_url` *(str):* Optional remote repository URL
    - `tags` *(list[str]):* Optional list of project tags

- **`close_create_project_dialog()`** Closes the create project dialog.

- **`reload_create_project_dialog()`** Reloads the create project dialog.

### Examples

#### Basic Project Information

```python
import anchorpoint
import apsync

# Get current project
api = anchorpoint.get_api()
project = api.get_project()

if project:
    print(f"Project Name: {project.name}")
    print(f"Project ID: {project.id}")
    print(f"Project Path: {project.path}")
    print(f"Workspace ID: {project.workspace_id}")
    print(f"Description: {project.description}")
    print(f"Created: {project.created_at}")
    print(f"Updated: {project.updated_at}")
else:
    print("No project found in current context")
```

#### Working with Project Members

```python
import anchorpoint
import apsync

# Get project and manage members
project = apsync.get_project("/path/to/project")

if project:
    # Get current members
    members = project.get_members()
    print(f"Project has {len(members)} members:")
    
    for member in members:
        print(f"- {member.email}: {member.access_level}")
    
    # Add new member with Admin access
    try:
        project.add_member("newuser@company.com", apsync.AccessLevel.Admin)
        print("Successfully added new admin member")
    except Exception as e:
        print(f"Failed to add member: {e}")
    
    # Add member with Member access
    try:
        project.add_member("viewer@company.com", apsync.AccessLevel.Member)
        print("Successfully added new member")
    except Exception as e:
        print(f"Failed to add member: {e}")
```

#### Project-Based File Operations

```python
import anchorpoint
import apsync
import os

# Get current project context
api = anchorpoint.get_api()
project = api.get_project()

if project:
    # Set project-specific attributes on files
    project_files = []
    for root, dirs, files in os.walk(project.path):
        for file in files:
            if file.lower().endswith(('.jpg', '.png', '.fbx', '.ma')):
                file_path = os.path.join(root, file)
                project_files.append(file_path)
    
    # Apply project metadata to all assets
    for file_path in project_files:
        # Set project identification
        api.attributes.set_attribute_value(file_path, "Project Name", project.name)
        api.attributes.set_attribute_value(file_path, "Project ID", project.id)
        
        # Set relative path within project
        rel_path = os.path.relpath(file_path, project.path)
        api.attributes.set_attribute_value(file_path, "Project Path", rel_path)
    
    print(f"Applied project metadata to {len(project_files)} files")
```

#### Project Creation and Management

```python
import anchorpoint
import apsync
import os

def create_and_setup_project():
    """Create a new project and set it up with initial structure"""
    
    ctx = anchorpoint.get_context()
    
    # Create new project
    project_path = os.path.join(ctx.path, "NewGameProject")
    project_name = "Epic Adventure Game"
    
    try:
        # Create project directory structure
        os.makedirs(project_path, exist_ok=True)
        
        # Create the Anchorpoint project
        project = apsync.create_project(project_path, project_name, ctx.workspace_id)
        print(f"Created project: {project.name}")
        print(f"Project ID: {project.id}")
        print(f"Project path: {project.path}")
        
        # Create project file for integration
        apsync.create_project_file(project_path, project.id, ctx.workspace_id)
        
        # Verify project creation
        retrieved_project = apsync.get_project(project_path)
        if retrieved_project:
            print(f"Project verified: {retrieved_project.name}")
        
        return project
        
    except Exception as e:
        anchorpoint.log_error(f"Project creation failed: {str(e)}")
        print(f"Error: {e}")
        return None

create_and_setup_project()
```

#### Project Discovery and Validation

```python
import apsync
import anchorpoint
import os

def discover_projects_in_workspace():
    """Discover and validate projects in current workspace"""
    
    ctx = anchorpoint.get_context()
    
    # Get all projects in workspace
    projects = apsync.get_projects(ctx.workspace_id)
    print(f"Found {len(projects)} projects in workspace:")
    
    for project in projects:
        print(f"\nProject: {project.name}")
        print(f"  ID: {project.id}")
        print(f"  Path: {project.path}")
        
        # Check if project path exists and is valid
        if os.path.exists(project.path):
            is_project = apsync.is_project(project.path)
            print(f"  Valid project: {is_project}")
            
            # Get project by ID to verify
            retrieved = apsync.get_project_by_id(project.id, ctx.workspace_id)
            print(f"  Retrieved successfully: {retrieved.name == project.name}")
        else:
            print(f"  Warning: Project path does not exist!")

discover_projects_in_workspace()
```

#### Project Member Management

```python
import apsync
import anchorpoint

def manage_project_members():
    """Manage project members using utility functions"""
    
    ctx = anchorpoint.get_context()
    project = apsync.get_project(ctx.path)
    
    if not project:
        print("Not in a project context")
        return
    
    # Get current project members
    members = apsync.get_project_members(ctx.workspace_id, project.id)
    print(f"Current members ({len(members)}):")
    
    for member in members:
        print(f"  - {member.email}: {member.access_level}")
    
    # Add new members with different access levels
    new_members = [
        ("developer@company.com", apsync.AccessLevel.Member),
        ("lead@company.com", apsync.AccessLevel.Admin),
        ("viewer@company.com", apsync.AccessLevel.Guest)
    ]
    
    for email, access_level in new_members:
        try:
            apsync.add_user_to_project(
                ctx.workspace_id,
                project.id,
                ctx.username,  # invited_from
                email,
                access_level
            )
            print(f"✓ Added {email} with {access_level} access")
        except Exception as e:
            print(f"✗ Failed to add {email}: {e}")
    
    # Update member list
    updated_members = apsync.get_project_members(ctx.workspace_id, project.id)
    print(f"\nUpdated member count: {len(updated_members)}")

manage_project_members()
```

#### Project Import and Export

```python
import apsync
import anchorpoint
import os
import tempfile

def project_backup_and_restore():
    """Demonstrate project export and import functionality"""
    
    ctx = anchorpoint.get_context()
    project = apsync.get_project(ctx.path)
    
    if not project:
        print("Not in a project context")
        return
    
    try:
        # Export current project
        print(f"Exporting project: {project.name}")
        export_path = apsync.export_project(project)
        print(f"Project exported to: {export_path}")
        
        # Create a backup directory
        backup_dir = tempfile.mkdtemp(prefix="project_backup_")
        backup_project_path = os.path.join(backup_dir, f"{project.name}_restored")
        
        # Import project to backup location
        print(f"Importing project to: {backup_project_path}")
        apsync.import_project(ctx.workspace_id, export_path, backup_project_path)
        
        # Verify restored project
        restored_project = apsync.get_project(backup_project_path)
        if restored_project:
            print(f"✓ Successfully restored project: {restored_project.name}")
            print(f"  Original ID: {project.id}")
            print(f"  Restored ID: {restored_project.id}")
        else:
            print("✗ Failed to verify restored project")
        
    except Exception as e:
        anchorpoint.log_error(f"Project backup/restore failed: {str(e)}")
        print(f"Error: {e}")

project_backup_and_restore()
```

## Source: documentation/docs/api/python/settings.md


## Settings

The Settings API provides a powerful mechanism to store and retrieve configuration data, user preferences, and persistent information for your Anchorpoint actions. There are two types of settings available: local user settings and shared workspace/project settings.

### Usage

Settings are accessed through the `apsync` module:

```python
import apsync

# Create a local user settings instance
settings = apsync.Settings()

# Create a named settings instance
named_settings = apsync.Settings("Blender Action Settings")

# Create workspace-wide shared settings
project = apsync.get_project(path)
if project:
    shared_settings = apsync.SharedSettings(project.workspace_id, "Team Settings")
```

### Settings Class

The `Settings` class stores data locally on the user's machine. These settings are private and not synchronized across users or devices.

#### Constructor

- **`apsync.Settings(name=None, identifier=None, location=None, user=True)`** Creates a new Settings instance with optional scoping and naming parameters.

    Arguments
    - `name` *(str, optional)*: A name to identify the settings, allowing retrieval of the same settings across different actions
    - `identifier` *(str, optional)*: An identifier to scope the settings (e.g., project ID to make settings unique per project)
    - `location` *(str, optional)*: Custom location where settings are stored on disk
    - `user` *(bool)*: Set to True to make settings available for all users (default: True)

#### Methods

- **`set(key, value)`** Stores a value identified by a key name.

    Arguments
    - `key` *(str)*: The name of the settings value
    - `value` *(object)*: The value to be stored (can be string, number, boolean, etc.)

- **`get(key, default='')`** Retrieves a stored value by key name, returning a default value if the key doesn't exist.

    Arguments
    - `key` *(str)*: The name of the settings value
    - `default` *(object)*: The default value to return if key is not found (default: empty string)

    Returns: (*object*) The stored value or the provided default

- **`contains(key)`** Checks if a key exists in the settings.

    Arguments
    - `key` *(str)*: The name of the settings value

    Returns: (*bool*) True if the key exists, False otherwise

- **`remove(key)`** Removes a value from the settings by key name.

    Arguments
    - `key` *(str)*: The name of the settings value to remove

- **`clear()`** Removes all stored values from the settings - essentially a factory reset.

- **`store()`** Persists all changes made to the settings. **This method must be called after any modifications** to ensure changes are saved to disk.

### SharedSettings Class

The `SharedSettings` class stores data in the cloud that is shared across all users in a workspace or project. These settings are synchronized and accessible to all team members with appropriate access.

**Note:** Currently, SharedSettings are not encrypted.

#### Constructor

- **`SharedSettings(workspace_id, identifier)`** Creates workspace-wide shared settings accessible to all workspace members.

    Arguments
    - `workspace_id` *(str)*: The ID of the workspace where the settings will be stored
    - `identifier` *(str)*: A unique identifier for this set of shared settings within the workspace

- **`SharedSettings(project_id, workspace_id, identifier)`** Creates project-scoped shared settings accessible only to users with access to the specific project.

    Arguments
    - `project_id` *(str)*: The ID of the project where the settings will be stored
    - `workspace_id` *(str)*: The ID of the workspace containing the project
    - `identifier` *(str)*: A unique identifier for this set of shared settings within the project

#### Methods

The `SharedSettings` class provides the same methods as the `Settings` class:

- **`set(key, value)`** Stores a shared value identified by a key name.

    Arguments
    - `key` *(str)*: The name of the settings value
    - `value` *(object)*: The value to be stored (can be string, number, boolean, etc.)

- **`get(key, default='')`** Retrieves a stored shared value by key name, returning a default value if the key doesn't exist.

    Arguments
    - `key` *(str)*: The name of the settings value
    - `default` *(object)*: The default value to return if key is not found (default: empty string)

    Returns: (*object*) The stored value or the provided default

- **`contains(key)`** Checks if a key exists in the shared settings.

    Arguments
    - `key` *(str)*: The name of the settings value

    Returns: (*bool*) True if the key exists, False otherwise

- **`remove(key)`** Removes a value from the shared settings by key name.

    Arguments
    - `key` *(str)*: The name of the settings value to remove

- **`clear()`** Removes all stored values from the shared settings - essentially a factory reset.

- **`store()`** Persists all changes made to the shared settings. **This method must be called after any modifications** to ensure changes are saved to the cloud.

### Examples

#### Basic Settings Operations
```python
import apsync

# Create a settings instance
settings = apsync.Settings()

# Store various types of data
settings.set("lottery numbers", 4815162342)
settings.set("user_name", "John Doe")
settings.set("auto_save", True)
settings.store()  # Don't forget to persist changes

# Retrieve stored values
jackpot = settings.get("lottery numbers", 4815162342)
username = settings.get("user_name", "Anonymous")
auto_save = settings.get("auto_save", False)

# Check if settings exist
if settings.contains("lottery numbers"):
    print("Lucky numbers are saved!")

# Remove individual settings
settings.remove("lottery numbers")
settings.store()  # Persist the removal

# Clear all settings (factory reset)
settings.clear()
settings.store()  # Make the clearing permanent
```

#### SharedSettings - Workspace Level
```python
import apsync

# Create workspace-wide shared settings
project = apsync.get_project(path)
if project:
    shared_settings = apsync.SharedSettings(project.workspace_id, "Blender Action Settings")
    
    # Store team preferences
    shared_settings.set("render_quality", "high")
    shared_settings.set("auto_backup", True)
    shared_settings.store()
    
    # Later, any team member can access these settings
    quality = shared_settings.get("render_quality", "medium")
    backup_enabled = shared_settings.get("auto_backup", False)
```

#### SharedSettings - Project Level
```python
import apsync

# Create project-scoped shared settings
project = apsync.get_project(path)
if project:
    project_shared_settings = apsync.SharedSettings(
        project.project_id, 
        project.workspace_id, 
        "Team Render Settings"
    )
    
    # Store project-specific team settings
    project_shared_settings.set("output_path", "/shared/renders")
    project_shared_settings.set("file_format", "exr")
    project_shared_settings.store()
```

#### User Preferences Storage
```python
import apsync

# Store user preferences that persist across action executions
preferences = apsync.Settings("UserPreferences")

# Set user preferences
preferences.set("theme", "dark")
preferences.set("auto_save_interval", 300)  # 5 minutes
preferences.set("show_notifications", True)
preferences.store()

# Retrieve preferences in another action
def load_user_preferences():
    prefs = apsync.Settings("UserPreferences")
    theme = prefs.get("theme", "light")
    auto_save = prefs.get("auto_save_interval", 600)
    notifications = prefs.get("show_notifications", True)
    return theme, auto_save, notifications
```

#### Project-Specific Configuration
```python
import apsync

# Store project-specific settings
project = apsync.get_project("/path/to/project")
if project:
    config = apsync.Settings("ProjectConfig", project.project_id)
    config.set("render_engine", "cycles")
    config.set("output_format", "png")
    config.set("resolution", [1920, 1080])
    config.store()
```

## Source: documentation/docs/api/python/tasks.md


## Tasks

The Tasks API provides functionality for creating and managing tasks within Anchorpoint projects. Tasks help organize work items and metadata for project assets and workflows.

### Usage

```python
import apsync
import anchorpoint

ctx = anchorpoint.get_context()
api = anchorpoint.get_api()

# Access tasks through the API
tasks_api = api.tasks

# Create a task list for organizing tasks
task_list = tasks_api.create_task_list(ctx.folder, "Asset Tasks")

# Create a new task in the task list
task = tasks_api.create_task(task_list, "Review character model")

# Or create a task by finding/creating a task list by name
task2 = tasks_api.create_task(ctx.folder, "Asset Tasks", "Check topology")

print(f"Created task: {task.name}")
print(f"Task ID: {task.id}")
print(f"List ID: {task.list_id}")
```

### Task Class

##### `apsync.Task`

The Task class represents an individual work item within a task list.

#### Properties

- **`icon`** *(class: Icon or None):* Optional icon for the task. Can be set using the Tasks API methods.
- **`id`** *(str):* Unique identifier for the task. Automatically generated when task is created.
- **`list_id`** *(str):* ID of the task list this task belongs to. Links task to its containing list.
- **`name`** *(str):* Title or name of the task. Brief description of what needs to be done.
- **`project_id`** *(str or None):* ID of the project this task belongs to. Can be None for workspace-level tasks.
- **`workspace_id`** *(str):* The ID of the workspace this task belongs to. Always present for all tasks.

### TaskList Class

##### `apsync.TaskList`

The TaskList class provides a container for organizing related tasks.

#### Properties

- **`id`** *(str):* Unique identifier for the task list. Automatically generated when task list is created.
- **`name`** *(str):* Name of the task list. Brief title describing the task collection.
- **`project_id`** *(str or None):* ID of the project this task list belongs to. Can be None for workspace-level task lists.
- **`workspace_id`** *(str):* ID of the workspace this task list belongs to. Always present for all task lists.

### Tasks API

The Tasks API is accessed through `api.tasks` and provides task management functionality.

#### Methods

- **`copy_task(task)`** Creates a copy of an existing task.

    Arguments
    - `task` *(class: Task)*: Task to copy

    Returns: (*class: Task*) New task object that is a copy of the original

- **`create_task(task_list, name)`** Creates a new task in a given task list.

    Arguments
    - `task_list` *(class: TaskList)*: The task list to add the task to
    - `name` *(str)*: Name of the task

    Returns: (*class: Task*) Created task object

- **`create_task(target, task_list_name, name)`** Creates a new task by finding or creating a task list by name.

    Arguments
    - `target` *(str)*: The folder used to search for task lists
    - `task_list_name` *(str)*: The name of the task list
    - `name` *(str)*: Name of the task

    Returns: (*class: Task*) Created task object

- **`create_task_list(target, name)`** Creates a new task list at the specified location.

    Arguments
    - `target` *(str)*: Path where the task list should be created
    - `name` *(str)*: Name of the task list

    Returns: (*class: TaskList*) Created task list object

- **`get_task(task_list, name)`** Retrieves a task by name from a task list.

    Arguments
    - `task_list` *(class: TaskList)*: Task list to search
    - `name` *(str)*: Name of the task to find

    Returns: (*class: Task or None*) Task object or None if not found

- **`get_task_by_id(id)`** Retrieves a task by its unique identifier.

    Arguments
    - `id` *(str)*: Unique identifier of the task

    Returns: (*class: Task*) Task object

- **`get_task_list(target, name)`** Retrieves a task list by name from the specified location.

    Arguments
    - `target` *(str)*: Path where to look for the task list
    - `name` *(str)*: Name of the task list

    Returns: (*class: TaskList or None*) Task list object or None if not found

- **`get_task_list_by_id(id)`** Retrieves a task list by its unique identifier.

    Arguments
    - `id` *(str)*: Unique identifier of the task list

    Returns: (*class: TaskList*) Task list object

- **`get_task_lists(target)`** Gets all task lists at the specified location.

    Arguments
    - `target` *(str)*: Path where to look for task lists

    Returns: (*list of TaskList*) List of task lists found

- **`get_tasks(task_list)`** Gets all tasks within a task list.

    Arguments
    - `task_list` *(class: TaskList)*: Task list to get tasks from

    Returns: (*list of Task*) List of tasks in the task list

- **`remove_task(task)`** 
Removes a task permanently.

    Arguments
    - `task` *(class: Task)*: Task to remove

- **`remove_task_list(task_list)`** 
Removes a task list and all its tasks permanently.

    Arguments
    - `task_list` *(class: TaskList)*: Task list to remove

- **`rename_task(task, name)`** 
Renames a task.

    Arguments
    - `task` *(class: Task)*: Task to rename
    - `name` *(str)*: New name for the task

- **`rename_task_list(task_list, name)`** Renames a task list.

    Arguments
    - `task_list` *(class: TaskList)*: Task list to rename
    - `name` *(str)*: New name for the task list

- **`set_task_icon(task, icon)`** Sets the icon for a task.

    Arguments
    - `task` *(class: Task)*: Task to set icon for
    - `icon` *(class: Icon or None)*: Icon to set, or None to remove icon

- **`set_task_icons(tasks, icon)`** Sets the same icon for multiple tasks.

    Arguments
    - `tasks` *(list of Task)*: List of tasks to set icon for
    - `icon` *(class: Icon or None)*: Icon to set, or None to remove icons

### Examples

#### Basic Task Creation

```python
import apsync
import anchorpoint

ctx = anchorpoint.get_context()
api = anchorpoint.get_api()

# Create a task list first
task_list = api.tasks.create_task_list(ctx.folder, "Review Tasks")

# Create a new task in the task list
task = api.tasks.create_task(task_list, "Review concept art")

print(f"Created task: {task.name}")
print(f"Task ID: {task.id}")
print(f"Task list ID: {task.list_id}")
print(f"Workspace ID: {task.workspace_id}")
```

#### Managing Task Lists

```python
import apsync
import anchorpoint

ctx = anchorpoint.get_context()
api = anchorpoint.get_api()

# Create a task list for character development
task_list = api.tasks.create_task_list(ctx.folder, "Character Development")

# Create multiple related tasks
task_names = ["Concept Design", "3D Modeling", "Texturing", "Rigging"]

created_tasks = []
for name in task_names:
    # Use the overload that finds/creates task list by name
    task = api.tasks.create_task(ctx.folder, "Character Development", name)
    created_tasks.append(task)

print(f"Created {len(created_tasks)} tasks")

# Get all tasks in the task list
all_tasks = api.tasks.get_tasks(task_list)
print(f"Task list contains {len(all_tasks)} tasks")
```

#### Task Management Operations

```python
import apsync
import anchorpoint

ctx = anchorpoint.get_context()
api = anchorpoint.get_api()

# Get an existing task list
task_list = api.tasks.get_task_list(ctx.folder, "Asset Tasks")

if task_list:
    # Get all tasks in the list
    tasks = api.tasks.get_tasks(task_list)
    
    for task in tasks:
        print(f"Task: {task.name}")
        print(f"  ID: {task.id}")
        print(f"  List ID: {task.list_id}")
        print(f"  Project ID: {task.project_id}")
        print(f"  Workspace ID: {task.workspace_id}")
        
        # Check if task has an icon
        if task.icon:
            print(f"  Icon: {task.icon.path}")
        
        print()
    
    # Find a specific task by name
    review_task = api.tasks.get_task(task_list, "Review character model")
    if review_task:
        print(f"Found task: {review_task.name}")
```

#### Task Icon Management

```python
import apsync
import anchorpoint

ctx = anchorpoint.get_context()
api = anchorpoint.get_api()

# Create an icon for high priority tasks
high_priority_icon = apsync.Icon("qrc:/icons/interface/warning.svg", "red")

# Get a task and set its icon
task_list = api.tasks.get_task_list(ctx.folder, "Project Tasks")
if task_list:
    tasks = api.tasks.get_tasks(task_list)
    
    # Set icon for individual task
    if tasks:
        api.tasks.set_task_icon(tasks[0], high_priority_icon)
        print(f"Set icon for task: {tasks[0].name}")
    
    # Set same icon for multiple tasks
    urgent_tasks = [t for t in tasks if "urgent" in t.name.lower()]
    if urgent_tasks:
        api.tasks.set_task_icons(urgent_tasks, high_priority_icon)
        print(f"Set icons for {len(urgent_tasks)} urgent tasks")
```

## Source: documentation/docs/api/python/thumbnails.md


## Thumbnails

The Thumbnails API provides functionality for generating, managing, and retrieving thumbnail images for files in Anchorpoint projects. Thumbnails improve browsing experience and provide visual previews of assets without opening the full files.

### Usage

Thumbnail functions are accessed directly from the `apsync` module:

```python
import apsync
import anchorpoint

ctx = anchorpoint.get_context()

# Generate thumbnail for a file
success = apsync.generate_thumbnail(
    ctx.path,
    "/output/directory",
    with_preview=True,
    with_detail=False
)

# Attach custom thumbnail
apsync.attach_thumbnail(ctx.path, "/path/to/custom_thumb.jpg", is_detail=False)

# Get existing thumbnail
thumb_path = apsync.get_thumbnail(ctx.path, is_detail=False)
```

### Functions

- **`generate_thumbnail(file_path, output_directory, with_preview=True, with_detail=False, workspace_id=None)`**

    Generates thumbnail images for a file automatically using Anchorpoint's built-in thumbnail generators.

    Arguments
    - `file_path` *(str)*: Absolute path to the source file
    - `output_directory` *(str)*: Directory where thumbnails should be saved
    - `with_preview` *(bool, optional)*: Generate preview-sized thumbnail (default: True)
    - `with_detail` *(bool, optional)*: Generate detail-sized thumbnail (default: False)
    - `workspace_id` *(str, optional)*: Workspace ID for context (uses current if not provided)

    Returns: (*bool*) True if thumbnail generation succeeded, False otherwise

- **`generate_thumbnails(file_paths, output_directory, with_preview=True, with_detail=False, workspace_id=None)`**

    Generates thumbnails for multiple files in batch mode for better performance.

    Arguments
    - `file_paths` *(List[str])*: List of absolute paths to source files
    - `output_directory` *(str)*: Directory where thumbnails should be saved
    - `with_preview` *(bool, optional)*: Generate preview-sized thumbnails (default: True)
    - `with_detail` *(bool, optional)*: Generate detail-sized thumbnails (default: False)
    - `workspace_id` *(str, optional)*: Workspace ID for context

    Returns: (*List[str]*) List of successfully generated thumbnail paths

- **`attach_thumbnail(file_path, local_file, is_detail=True)`** Attaches a custom thumbnail image to a file, replacing any existing thumbnail.

    Arguments
    - `file_path` *(str)*: Absolute path to the target file
    - `local_file` *(str)*: Path to the thumbnail image file
    - `is_detail` *(bool, optional)*: Whether this is a detail thumbnail vs. preview (default: True)

- **`attach_thumbnails(file_path, local_preview_file, local_detail_file)`** Attaches both preview and detail thumbnails to a file in one operation.

    Arguments
    - `file_path` *(str)*: Absolute path to the target file
    - `local_preview_file` *(str)*: Path to the preview thumbnail image
    - `local_detail_file` *(str)*: Path to the detail thumbnail image

- **`get_thumbnail(file_path, is_detail)`** Retrieves the path to an existing thumbnail for a file.

    Arguments
    - `file_path` *(str)*: Absolute path to the file
    - `is_detail` *(bool)*: Whether to get the detail thumbnail (True) or preview thumbnail (False)

    Returns: (*str or None*) Path to the thumbnail file, or None if no thumbnail exists

### Examples

#### Basic Thumbnail Generation

```python
import apsync
import anchorpoint
import os

ctx = anchorpoint.get_context()

def generate_file_thumbnails():
    """Generate thumbnails for selected files"""
    
    if not ctx.selected_files:
        ui = anchorpoint.UI()
        ui.show_info("No Selection", "Please select files to generate thumbnails for")
        return
    
    ui = anchorpoint.UI()
    
    # Create output directory for thumbnails
    thumb_dir = os.path.join(ctx.folder, ".thumbnails")
    os.makedirs(thumb_dir, exist_ok=True)
    
    success_count = 0
    failed_files = []
    
    for file_path in ctx.selected_files:
        filename = os.path.basename(file_path)
        
        try:
            # Generate both preview and detail thumbnails
            success = apsync.generate_thumbnail(
                file_path,
                thumb_dir,
                with_preview=True,
                with_detail=True,
                workspace_id=ctx.workspace_id
            )
            
            if success:
                success_count += 1
                print(f"Generated thumbnail for: {filename}")
            else:
                failed_files.append(filename)
                
        except Exception as e:
            failed_files.append(filename)
            print(f"Failed to generate thumbnail for {filename}: {e}")
    
    # Show results
    if success_count > 0:
        ui.show_success("Thumbnails Generated", 
                       f"Successfully generated thumbnails for {success_count} files")
    
    if failed_files:
        failed_list = "\n".join(failed_files)
        ui.show_warning("Some Failed", 
                       f"Failed to generate thumbnails for:\n{failed_list}")

generate_file_thumbnails()
```

#### Batch Thumbnail Processing

```python
import apsync
import anchorpoint
import os

ctx = anchorpoint.get_context()

def batch_thumbnail_generation():
    """Generate thumbnails for all supported files in a directory"""
    
    if not os.path.isdir(ctx.path):
        ui = anchorpoint.UI()
        ui.show_error("Not a Directory", "Please select a directory for batch processing")
        return
    
    # Supported file types for thumbnails
    supported_extensions = {
        '.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif',  # Images
        '.psd', '.ai', '.eps',  # Adobe files
        '.fbx', '.obj', '.ma', '.mb', '.max', '.blend',  # 3D models
        '.mp4', '.avi', '.mov', '.mkv',  # Videos
        '.pdf', '.docx', '.xlsx'  # Documents
    }
    
    # Find all supported files
    supported_files = []
    for root, dirs, files in os.walk(ctx.path):
        for file in files:
            _, ext = os.path.splitext(file.lower())
            if ext in supported_extensions:
                supported_files.append(os.path.join(root, file))
    
    if not supported_files:
        ui = anchorpoint.UI()
        ui.show_info("No Supported Files", "No supported files found for thumbnail generation")
        return
    
    # Create thumbnail output directory
    thumb_dir = os.path.join(ctx.path, ".anchorpoint_thumbnails")
    os.makedirs(thumb_dir, exist_ok=True)
    
    # Use batch generation for better performance
    try:
        # Generate thumbnails in batch
        generated_thumbs = apsync.generate_thumbnails(
            supported_files,
            thumb_dir,
            with_preview=True,
            with_detail=False,
            workspace_id=ctx.workspace_id
        )
        
        ui = anchorpoint.UI()
        ui.show_success("Batch Complete", 
                       f"Generated {len(generated_thumbs)} thumbnails out of {len(supported_files)} files")
    
    except Exception as e:
        ui = anchorpoint.UI()
        ui.show_error("Batch Failed", f"Batch thumbnail generation failed: {e}")

batch_thumbnail_generation()
```

#### Custom Thumbnail Attachment

```python
import apsync
import anchorpoint
import os
from PIL import Image, ImageDraw, ImageFont

ctx = anchorpoint.get_context()

def create_custom_thumbnails():
    """Create and attach custom thumbnails for files"""
    
    if not ctx.selected_files:
        ui = anchorpoint.UI()
        ui.show_info("No Selection", "Please select files to create custom thumbnails for")
        return
    
    # Create temporary directory for custom thumbnails
    temp_dir = anchorpoint.temp_dir()
    custom_thumb_dir = os.path.join(temp_dir, "custom_thumbnails")
    os.makedirs(custom_thumb_dir, exist_ok=True)
    
    for file_path in ctx.selected_files:
        filename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(filename)[0]
        
        try:
            # Create custom thumbnail image
            thumb_path = create_text_thumbnail(file_path, custom_thumb_dir)
            
            if thumb_path:
                # Attach the custom thumbnail
                apsync.attach_thumbnail(file_path, thumb_path, is_detail=False)
                print(f"Attached custom thumbnail to: {filename}")
        
        except Exception as e:
            print(f"Failed to create custom thumbnail for {filename}: {e}")
    
    ui = anchorpoint.UI()
    ui.show_success("Custom Thumbnails", "Custom thumbnails created and attached")

def create_text_thumbnail(file_path, output_dir):
    """Create a text-based thumbnail image"""
    
    filename = os.path.basename(file_path)
    name_without_ext = os.path.splitext(filename)[0]
    
    # Create thumbnail image
    thumb_size = (256, 256)
    image = Image.new('RGB', thumb_size, color='lightblue')
    draw = ImageDraw.Draw(image)
    
    # Try to load a font (fallback to default if not available)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
    
    # Draw file information
    draw.text((10, 10), "CUSTOM", fill='darkblue', font=font)
    draw.text((10, 30), name_without_ext[:20], fill='black', font=font)
    
    # Add file extension
    ext = os.path.splitext(filename)[1].upper()
    draw.text((10, 220), ext, fill='darkred', font=font)
    
    # Save thumbnail
    thumb_path = os.path.join(output_dir, f"{name_without_ext}_thumb.jpg")
    image.save(thumb_path, 'JPEG', quality=85)
    
    return thumb_path

create_custom_thumbnails()
```

## Source: documentation/docs/api/python/timeline.md


## Timeline

The Timeline API provides functionality for managing timeline channels, entries, and operations within Anchorpoint projects. The timeline serves as a central activity feed that tracks version control operations.

### Usage

Timeline functions are accessed from both the `anchorpoint` and `apsync` modules:

```python
from dataclasses import dataclass
from datetime import datetime
import anchorpoint as ap
import apsync as aps
import json

# Create a timeline channel entry
def create_timeline_entry(history_item):
    entry = ap.TimelineChannelEntry()
    entry.id = history_item["id"]
    entry.time = int(datetime.fromisoformat(history_item["time"]).timestamp())
    entry.message = history_item["message"]
    entry.user_email = history_item["user_email"]
    entry.has_details = True
    
    # Set icon based on application type
    if history_item["type"] == "cinema4d":
        entry.icon = aps.Icon(":/icons/organizations-and-products/c4d.svg", "#F3D582")
        entry.tooltip = "Published from Cinema 4D"
    elif history_item["type"] == "maya":
        entry.icon = aps.Icon(":/icons/organizations-and-products/maya.svg", "#F3D582")
        entry.tooltip = "Published from Maya"
    else:
        entry.icon = aps.Icon(":/icons/user-interface/information.svg", "#70717A")
        entry.tooltip = "Created a new file"
    
    return entry

# Load timeline channel callback
def on_load_timeline_channel(channel_id: str, page_size: int, ctx):
    if channel_id != "custom-channel":
        return None
    
    info = ap.TimelineChannelInfo(ctx.project_id)
    history = get_history_entries(ctx)  # Your custom history function
    has_more = False
    changes = None
    
    return info, changes, history, has_more

# Update timeline entries
ap.update_timeline_entries("custom-channel", project_id, entries, has_more=False)
```

### Anchorpoint Timeline Functions

#### Timeline Interface Management

- **`open_timeline()`** Opens the timeline view in Anchorpoint.

- **`close_timeline_sidebar()`** Closes the timeline sidebar.

- **`reload_timeline_entries()`** Reloads all timeline entries.

- **`update_timeline_last_seen()`** Updates the last seen timestamp for timeline.

#### Timeline Channel Operations

- **`refresh_timeline_channel(channel_id)`** Refreshes a specific timeline channel.

    Arguments
    - `channel_id` *(str):* Timeline channel identifier

- **`get_timeline_update_count()`** Gets the current timeline update count.

    Returns: (*int*) Current update count

- **`set_timeline_update_count(project_id, channel_id, count, since=0)`** Sets the timeline update count for a channel.

    Arguments
    - `project_id` *(str):* Project identifier
    - `channel_id` *(str):* Channel identifier
    - `count` *(int):* New update count
    - `since` *(int):* Timestamp since when to count updates

- **`delete_timeline_channel_entries(channel_id, entry_ids)`** Deletes specific timeline entries.

    Arguments
    - `channel_id` *(str):* Channel identifier
    - `entry_ids` *(list[str]):* List of entry IDs to delete

#### Timeline Channel Actions

- **`enable_timeline_channel_action(channel_id, action_id, enable=True)`** Enables or disables a timeline channel action.

    Arguments
    - `channel_id` *(str):* Channel identifier
    - `action_id` *(str):* Action identifier
    - `enable` *(bool):* Whether to enable the action

- **`stop_timeline_channel_action_processing(channel_id, action_id)`** Stops processing of a timeline channel action.

    Arguments
    - `channel_id` *(str):* Channel identifier
    - `action_id` *(str):* Action identifier

- **`timeline_channel_action_processing(channel_id, action_id, message=None)`** Indicates that a timeline channel action is processing.

    Arguments
    - `channel_id` *(str):* Channel identifier
    - `action_id` *(str):* Action identifier
    - `message` *(str):* Optional status message

#### Timeline Channel Notifications

- **`schedule_channel_notification(project_id, workspace_id, channel_id, channel_entry_ids, messages, file_paths, module=None, branch=None)`** Schedules a channel notification with mentions.

    This function schedules a notification for a timeline channel. Users mentioned in the messages using @username or that are subscribed to files in file_paths will receive notifications.
    
    The messages and channel_entry_ids lists must have the same length.

    Arguments
    - `project_id` *(str):* Project identifier
    - `workspace_id` *(str):* Workspace identifier
    - `channel_id` *(str):* Timeline channel identifier
    - `channel_entry_ids` *(list[str]):* List of channel entry IDs
    - `messages` *(list[str]):* List of messages (supports @username mentions)
    - `file_paths` *(list[str]):* List of file paths that trigger notifications for subscribers
    - `module` *(str, optional):* Module name for the channel
    - `branch` *(str, optional):* Branch name for the channel

    Example:
    ```python
    anchorpoint.schedule_channel_notification(
        ctx.project_id,
        ctx.workspace_id,
        "timeline-123",
        ["entry-456", "entry-457"],
        ["@john Check out these changes!", "Updated the main scene"],
        ["/path/to/file1.blend", "/path/to/file2.txt"],
        module="modeling",
        branch="main"
    )
    ```

#### Version Control Operations

- **`vc_load_pending_changes(channel_id, reload=False)`** Loads pending version control changes.

    Arguments
    - `channel_id` *(str):* Channel identifier
    - `reload` *(bool):* Whether to force reload the changes

- **`vc_resolve_conflicts(channel_id)`** Resolves version control conflicts.

    Arguments
    - `channel_id` *(str):* Channel identifier

### Apsync Timeline Functions

#### Timeline Entries

- **`add_timeline_entry(path, text)`** Adds an entry to the timeline.

    Arguments
    - `path` *(str):* File or folder path the entry relates to
    - `text` *(str):* Timeline entry text

#### Timeline Channel Management

- **`add_timeline_channel(project, channel)`** Adds a timeline channel to a project.

    Arguments
    - `project` *(class: Project):* Project to add channel to
    - `channel` *(class: TimelineChannel):* Channel to add

- **`remove_timeline_channel(project, channelId)`** Removes a timeline channel from a project.

    Arguments
    - `project` *(class: Project):* Project to remove channel from
    - `channelId` *(str):* Channel identifier to remove

- **`update_timeline_channel(project, channel)`** Updates a timeline channel.

    Arguments
    - `project` *(class: Project):* Project containing the channel
    - `channel` *(class: TimelineChannel):* Updated channel object

- **`get_timeline_channel(project, channelId)`** Gets a specific timeline channel.

    Arguments
    - `project` *(class: Project):* Project containing the channel
    - `channelId` *(str):* Channel identifier

    Returns: (*class: TimelineChannel or None*) Channel object or None if not found

- **`get_timeline_channels(project)`** Gets all timeline channels in a project.

    Arguments  
    - `project` *(class: Project):* Project to get channels from

    Returns: (*list[class: TimelineChannel]*) List of timeline channels

### Timeline Classes

#### TimelineChannel Class

The TimelineChannel class represents a timeline channel within a project.

##### Properties

- **`id`** *(str):* Unique identifier for the channel
- **`name`** *(str):* Display name of the channel
- **`description`** *(str):* Description of the channel's purpose

### Examples

#### Basic Timeline Operations

```python
import anchorpoint
import apsync

ctx = anchorpoint.get_context()

def basic_timeline_operations():
    """Demonstrate basic timeline operations"""
    
    # Open timeline view
    anchorpoint.open_timeline()
    
    # Add entry for current action
    apsync.add_timeline_entry(ctx.path, f"Processed {ctx.filename} with custom action")
    
    # Get current project for channel operations
    api = anchorpoint.get_api()
    project = api.get_project()
    
    if project:
        # Get all timeline channels
        channels = apsync.get_timeline_channels(project)
        print(f"Project has {len(channels)} timeline channels:")
        
        for channel in channels:
            print(f"  - {channel.name} (ID: {channel.id})")
    
    # Update timeline display
    anchorpoint.reload_timeline_entries()
    anchorpoint.update_timeline_last_seen()

basic_timeline_operations()
```

#### Timeline Channel Management

```python
import anchorpoint
import apsync

def manage_timeline_channels():
    """Demonstrate timeline channel management"""
    
    api = anchorpoint.get_api()
    project = api.get_project()
    
    if not project:
        print("Not in a project context")
        return
    
    # Get all existing channels
    channels = apsync.get_timeline_channels(project)
    print(f"Found {len(channels)} timeline channels:")
    
    for channel in channels:
        print(f"  Channel: {channel.name}")
        print(f"    ID: {channel.id}")
        print(f"    Description: {channel.description}")
        
        # Refresh each channel
        anchorpoint.refresh_timeline_channel(channel.id)
    
    # Create a new channel for version control operations
    vc_channel = apsync.TimelineChannel()
    vc_channel.name = "Version Control"
    vc_channel.description = "Git operations and version control activities"
    
    try:
        apsync.add_timeline_channel(project, vc_channel)
        print(f"\nCreated new channel: {vc_channel.name}")
        
        # Add initial entry to the new channel
        apsync.add_timeline_entry(project.path, "Version control channel initialized")
        
        # Update the channel information
        vc_channel.description = "Git operations, commits, and version control activities"
        apsync.update_timeline_channel(project, vc_channel)
        print("Updated channel description")
        
    except Exception as e:
        print(f"Error creating channel: {e}")

manage_timeline_channels()
```

#### Timeline Action Processing

```python
import anchorpoint
import apsync
import time

ctx = anchorpoint.get_context()

def timeline_action_workflow():
    """Demonstrate timeline action processing workflow"""
    
    # Simulate a long-running operation with timeline feedback
    channel_id = "main_channel"  # This would be a real channel ID
    action_id = "batch_processor"
    
    try:
        # Indicate that processing is starting
        anchorpoint.timeline_channel_action_processing(
            channel_id, 
            action_id, 
            "Starting batch file processing..."
        )
        
        # Add timeline entry for the start of processing
        apsync.add_timeline_entry(ctx.path, "Batch processing started")
        
        # Simulate work with progress updates
        for i in range(5):
            time.sleep(1)  # Simulate work
            anchorpoint.timeline_channel_action_processing(
                channel_id,
                action_id,
                f"Processing step {i+1}/5..."
            )
        
        # Complete the processing
        apsync.add_timeline_entry(ctx.path, "Batch processing completed successfully")
        
        # Stop the processing indicator
        anchorpoint.stop_timeline_channel_action_processing(channel_id, action_id)
        
        print("Timeline action workflow completed")
        
    except Exception as e:
        # Handle errors and update timeline
        anchorpoint.log_error(f"Timeline action failed: {str(e)}")
        apsync.add_timeline_entry(ctx.path, f"Batch processing failed: {str(e)}")
        
        # Make sure to stop processing indicator even on error
        try:
            anchorpoint.stop_timeline_channel_action_processing(channel_id, action_id)
        except:
            pass

timeline_action_workflow()
```

#### Timeline Channel Notifications

```python
import anchorpoint
import apsync

ctx = anchorpoint.get_context()

def send_channel_notifications():
    """Demonstrate timeline channel notification with mentions"""
    
    # Send a channel notification with mentions
    # This notifies users mentioned in the messages and file subscribers
    
    channel_id = "project-updates"
    
    # Create timeline entries with messages
    entry_ids = ["entry-001", "entry-002"]
    messages = [
        "@alice Please review the updated models",
        "@bob The textures have been finalized"
    ]
    file_paths = [
        "/project/models/character.blend",
        "/project/textures/character_diffuse.png"
    ]
    
    # Schedule the channel notification
    # Users @alice and @bob will be notified, plus anyone subscribed to the files
    anchorpoint.schedule_channel_notification(
        ctx.project_id,
        ctx.workspace_id,
        channel_id,
        entry_ids,
        messages,
        file_paths,
        module="assets",
        branch="main"
    )
    
    print("Channel notification scheduled successfully")

send_channel_notifications()
```

## Source: documentation/docs/api/python/userinterface.md


## User Interface

The User Interface API provides comprehensive functionality for creating interactive dialogs, displaying notifications, and managing user interactions within Anchorpoint actions. This includes dialog creation with various input types, progress indicators, file browsers, and user feedback mechanisms.

### Usage

#### Use the toast system
Using the toast system allows you to display messages to the users such as alerts, successes or errors.

```python
import anchorpoint

# Get UI instance
ui = anchorpoint.UI()

# Show toast
ui.show_info("Process completed successfully")
ui.show_error("An error occurred", "Please check your input and try again")
```
#### Create a simple dialog
Build custom popup windows by adding new rows using methods in the dialog class. You can also add "columns" to your dialog by chaining UI elements such as `dialog.add_text("First Row: ").add_input()`.

```python
import anchorpoint
# Create and show a simple dialog
dialog = anchorpoint.Dialog()
dialog.title = "My Custom Dialog"
dialog.add_text("First Row: ").add_input()
dialog.add_button("Second Row")
dialog.show()
```

### UI Class

#### Constructor

- **`anchorpoint.UI()`** The UI class provides methods for user notifications, navigation, and browser interactions.

#### Methods

- **`show_info(title, description="", duration=4000)`** Shows an info toast message within Anchorpoint.

    Arguments
    - `title` *(str)*: The title of the toast
    - `description` *(str, optional)*: The description of the toast
    - `duration` *(int, optional)*: The duration (in ms) the toast is shown to the user
    

- **`show_success(title, description="", duration=4000)`** Shows a success toast message within Anchorpoint.

    Arguments
    - `title` *(str)*: The title of the toast
    - `description` *(str, optional)*: The description of the toast
    - `duration` *(int, optional)*: The duration (in ms) the toast is shown to the user

    
    Shows a toast using a teal color scheme

- **`show_error(title, description="", duration=4000)`** Shows an error toast message within Anchorpoint.

    Arguments
    - `title` *(str)*: The title of the toast
    - `description` *(str, optional)*: The description of the toast
    - `duration` *(int, optional)*: The duration (in ms) the toast is shown to the user

- **`show_system_notification(title, message, callback=None, path_to_image=None)`** Shows a notification on the operating system.

    Arguments
    - `title` *(str)*: The title of the system notification
    - `message` *(str)*: The message of the system notification
    - `callback` *(function, optional)*: A callback triggered when the notification is clicked
    - `path_to_image` *(str, optional)*: Optional file path to an image displayed in the notification
    

- **`navigate_to_file(file_path)`** Navigates the Anchorpoint browser to the provided file path.

    Arguments
    - `file_path` *(str)*: The file to navigate to
    

- **`navigate_to_folder(folder_path)`** Navigates the Anchorpoint browser to the provided folder path.

    Arguments
    - `folder_path` *(str)*: The folder to navigate into
    

- **`show_console()`** Shows the command console to the user.

- **`clear_console()`** Clears the console.

- **`reload()`** Reloads the current view of the Anchorpoint browser.

### Dialog Class

#### Constructor

- **`anchorpoint.Dialog()`** The Dialog class provides a flexible framework for creating custom user interfaces with various input controls and layouts. All `add_*` methods return the Dialog instance for method chaining.

#### Properties

- **`title`** *(str):* Title displayed in the dialog window. Sets the main heading for the dialog.
- **`icon`** *(str):* Path or identifier for the dialog icon. Displayed alongside the title.

#### Methods

##### Layout and Structure

- **`add_text(text)`** Adds a text label to the dialog.

    Arguments
    - `text` *(str)*: Text content to display

    Returns: (*class: Dialog*) Returns self for method chaining

    
    Adds a text field. Basic HTML formatting such as "``" or "``" is supported. This example uses it as a label for a tag input using `my_dialog.add_text("Auto Lock Text Files").add_tag_input()`

- **`add_empty()`** Adds vertical spacing between elements.

    Returns: (*class: Dialog*) Returns self for method chaining
    
    
    Adds an empty space

- **`add_info(text)`** Adds an informational text block with distinctive styling.

    Arguments
    - `text` *(str)*: Information text to display (supports HTML formatting)

    Returns: (*class: Dialog*) Returns self for method chaining

    
    Adds a greyed out text field. Basic HTML formatting such as "``" or "``" is supported. 

##### Input Controls

- **`add_input(default="", placeholder="", callback=None, var=None, enabled=True, browse=None, browse_path=None, password=False, width=200, validate_callback=None)`**

    Adds a text input field to the dialog.

    Arguments
    - `default` *(str, optional)*: Default value for the input
    - `placeholder` *(str, optional)*: Placeholder text shown when empty
    - `callback` *(function, optional)*: Function called when input changes
    - `var` *(str, optional)*: Variable name for retrieving the value
    - `enabled` *(bool, optional)*: Whether the input is enabled (default: True)
    - `browse` *(class: BrowseType, optional)*: Add browse button for file/folder selection
    - `browse_path` *(str, optional)*: Initial browse path
    - `password` *(bool, optional)*: Whether to hide input text (default: False)
    - `width` *(int, optional)*: Width of the input field (default: 200)
    - `validate_callback` *(function, optional)*: Function for input validation

    Returns: (*class: Dialog*) Returns self for method chaining

    
    Adds a text input field. In case of selecting a folder or a file you can also add a browse button, which will open up the system's file browser.

- **`add_dropdown(default, values, callback=None, var=None, enabled=True, filterable=False, validate_callback=None)`**

    Adds a dropdown selection control.

    Arguments
    - `default` *(str)*: Default selected value
    - `values` *(list of str or DropdownEntry)*: Available options
    - `callback` *(function, optional)*: Function called when selection changes
    - `var` *(str, optional)*: Variable name for retrieving the selected value
    - `enabled` *(bool, optional)*: Whether the dropdown is enabled (default: True)
    - `filterable` *(bool, optional)*: Whether users can filter options by typing (default: False)
    - `validate_callback` *(function, optional)*: Function for validating selection

    Returns: (*class: Dialog*) Returns self for method chaining

    
    Adds a dropdown button where the user can select a pre defined entry

- **`add_checkbox(default=False, callback=None, var=None, enabled=True, text="")`** Adds a checkbox control.

    Arguments
    - `default` *(bool, optional)*: Initial checked state (default: False)
    - `callback` *(function, optional)*: Function called when state changes
    - `var` *(str, optional)*: Variable name for retrieving the value
    - `enabled` *(bool, optional)*: Whether the checkbox is enabled (default: True)
    - `text` *(str, optional)*: Label text displayed next to checkbox

    Returns: (*class: Dialog*) Returns self for method chaining

    
    Adds a basic checkbox with a description

- **`add_switch(default=False, callback=None, var=None, enabled=True, text="")`** Adds a switch control (similar to checkbox but different styling).

    Arguments
    - `default` *(bool, optional)*: Initial switch state (default: False)
    - `callback` *(function, optional)*: Function called when state changes
    - `var` *(str, optional)*: Variable name for retrieving the value
    - `enabled` *(bool, optional)*: Whether the switch is enabled (default: True)
    - `text` *(str, optional)*: Label text displayed next to switch

    Returns: (*class: Dialog*) Returns self for method chaining

    
    Adds a switch with a description

##### Action Controls

- **`add_button(text, callback=None, var=None, enabled=True, primary=True)`** Adds an action button to the dialog.

    Arguments
    - `text` *(str)*: Button label text
    - `callback` *(function, optional)*: Function called when button is clicked
    - `var` *(str, optional)*: Variable name for the button
    - `enabled` *(bool, optional)*: Whether the button is enabled (default: True)
    - `primary` *(bool, optional)*: Whether this is a primary button (default: True)

    Returns: (*class: Dialog*) Returns self for method chaining

    
    Adds a button. This one has set `primary=False`. 

##### Additional Controls

- **`add_separator()`** Adds a visual separator line to the dialog.

    Returns: (*class: Dialog*) Returns self for method chaining

    
    Adds a basic line for visual separation

- **`add_image(path, var=None, width=300)`** Adds an image to the dialog.

    Arguments
    - `path` *(str)*: Path to the image file
    - `var` *(str, optional)*: Variable name for the image
    - `width` *(int, optional)*: Width of the image (default: 300)

    Returns: (*class: Dialog*) Returns self for method chaining

    
    Adds an image. The height will be proportional to the width.

- **`add_tag_input(values, placeholder=None, callback=None, var=None, enabled=True, width=300)`**

    Adds a tag input control for multiple selections.

    Arguments
    - `values` *(list of str)*: Available tag values
    - `placeholder` *(str, optional)*: Placeholder text
    - `callback` *(function, optional)*: Function called when tags change
    - `var` *(str, optional)*: Variable name for retrieving values
    - `enabled` *(bool, optional)*: Whether the input is enabled (default: True)
    - `width` *(int, optional)*: Width of the input (default: 300)

    Returns: (*class: Dialog*) Returns self for method chaining

    
    A tag input can be used for filtering file types or adding keywords

##### Organization

- **`start_section(text, foldable=True, folded=True, enabled=True)`** Begins a collapsible section for grouping related controls.

    Arguments
    - `text` *(str)*: Section header text
    - `foldable` *(bool, optional)*: Whether section can be collapsed (default: True)
    - `folded` *(bool, optional)*: Whether section is folded by default (default: True)
    - `enabled` *(bool, optional)*: Whether the section is enabled (default: True)

    Returns: (*class: Dialog*) Returns self for method chaining

    
    Adds a section that can show or hide interface elements. You always need to use `end_section()` at the end of the interface group.

- **`end_section()`** Ends the current section.

    Returns: (*class: Dialog*) Returns self for method chaining

##### Dialog Management

- **`show()`** Displays the dialog to the user.

- **`close()`** Closes the dialog.

- **`get_value(var)`** Retrieves the current value of a named control.

    Arguments
    - `var` *(str)*: Variable name of the control

    Returns: *The current value of the control (type depends on control type)*

- **`set_enabled(var, enabled)`** Enables or disables a control.

    Arguments
    - `var` *(str)*: Variable name of the control
    - `enabled` *(bool)*: Whether the control should be enabled

### Examples

#### Basic Dialog Creation

```python
import anchorpoint

def create_simple_dialog():
    dialog = anchorpoint.Dialog()
    dialog.title = "File Processor"
    dialog.icon = ":/icons/action.svg"
    
    # Add form elements
    dialog.add_text("Select processing options:")
    dialog.add_dropdown("Medium", ["Low", "Medium", "High"], var="quality")
    dialog.add_checkbox(True, var="backup", text="Create backup")
    dialog.add_input("output_", placeholder="Enter prefix", var="prefix")
    
    # Add action buttons
    dialog.add_button("Process", callback=process_files, var="process")
    dialog.add_button("Cancel", callback=lambda d: d.close(), primary=False)
    
    dialog.show()

def process_files(dialog):
    quality = dialog.get_value("quality")
    backup = dialog.get_value("backup")
    prefix = dialog.get_value("prefix")
    
    print(f"Processing with quality: {quality}, backup: {backup}, prefix: {prefix}")
    dialog.close()

create_simple_dialog()
```
A dialog that shows a text label, a dropdown, a checkbox and an input each in a new row. The `process_files` is a callback that is triggered once the user clicks on the "Process" button. It reads the values from the input fields which the user has edited.

#### File Selection and Processing

```python
import anchorpoint
import os

def file_conversion_dialog():
    # Show file selection dialog using browse input
    dialog = anchorpoint.Dialog()
    dialog.title = "Image Conversion Setup"
    
    # File selection with browse button
    dialog.add_text("Select input file:")
    dialog.add_input("", placeholder="Select image file", var="input_file", 
                    browse=anchorpoint.BrowseType.File)
    
    dialog.add_text("Select output folder:")
    dialog.add_input("", placeholder="Select output folder", var="output_folder",
                    browse=anchorpoint.BrowseType.Folder)
    
    # Conversion settings
    dialog.add_separator()
    dialog.add_text("Conversion Settings:")
    dialog.add_dropdown("JPEG", ["JPEG", "PNG", "TIFF"], var="format")
    dialog.add_dropdown("100%", ["25%", "50%", "75%", "100%"], var="scale")
    dialog.add_checkbox(False, var="watermark", text="Apply watermark")
    
    dialog.add_button("Convert", callback=convert_image)
    dialog.add_button("Cancel", callback=lambda d: d.close(), primary=False)
    
    dialog.show()

def convert_image(dialog):
    input_file = dialog.get_value("input_file")
    output_folder = dialog.get_value("output_folder")
    format_type = dialog.get_value("format")
    scale = dialog.get_value("scale")
    watermark = dialog.get_value("watermark")
    
    ui = anchorpoint.UI()
    
    # Validate inputs
    if not input_file or not output_folder:
        ui.show_error("Missing Input", "Please select both input file and output folder")
        return
    
    try:
        # Simulate image processing
        print(f"Converting {input_file} to {format_type} at {scale} scale")
        if watermark:
            print("Applying watermark")
        
        ui.show_success("Conversion Complete", f"Image saved to {output_folder}")
        dialog.close()
        
    except Exception as e:
        ui.show_error("Conversion Failed", str(e))

file_conversion_dialog()
```
A dialog that also adds interface elements each in a new row. In the input field, the user can browse to a folder which is then validated in the callback. By the end, a toast is shown.

#### Advanced Dialog with Sections

```python
import anchorpoint

def advanced_settings_dialog():
    dialog = anchorpoint.Dialog()
    dialog.title = "Advanced Processing Settings"
    dialog.icon = ":/icons/settings.svg"
    
    # Input Settings Section
    dialog.start_section("Input Settings", folded=False)
    dialog.add_input("", placeholder="Select source folder", var="source",
                    browse=anchorpoint.BrowseType.Folder)
    dialog.add_input("*.jpg;*.png", placeholder="File filter", var="filter")
    dialog.add_checkbox(True, var="recursive", text="Include subfolders")
    dialog.end_section()
    
    # Processing Options Section  
    dialog.start_section("Processing Options")
    dialog.add_dropdown("Balanced", ["Fast", "Balanced", "Quality"], var="mode")
    dialog.add_checkbox(False, var="metadata", text="Preserve metadata")
    dialog.add_dropdown("4", ["1", "2", "4", "8"], var="threads")
    dialog.end_section()
    
    # Output Settings Section
    dialog.start_section("Output Settings")
    dialog.add_input("", placeholder="Select output folder", var="output",
                    browse=anchorpoint.BrowseType.Folder)
    dialog.add_input("processed_", placeholder="Filename prefix", var="prefix")
    dialog.add_checkbox(True, var="overwrite", text="Overwrite existing")
    dialog.end_section()
    
    # Action buttons
    dialog.add_empty()
    dialog.add_button("Start Processing", callback=start_processing, primary=True)
    dialog.add_button("Cancel", callback=lambda d: d.close(), primary=False)
    
    dialog.show()

def start_processing(dialog):
    # Collect all settings
    settings = {
        'source': dialog.get_value("source"),
        'filter': dialog.get_value("filter"),
        'recursive': dialog.get_value("recursive"),
        'mode': dialog.get_value("mode"),
        'metadata': dialog.get_value("metadata"),
        'threads': dialog.get_value("threads"),
        'output': dialog.get_value("output"),
        'prefix': dialog.get_value("prefix"),
        'overwrite': dialog.get_value("overwrite")
    }
    
    # Validate settings
    if not settings['source'] or not settings['output']:
        ui = anchorpoint.UI()
        ui.show_error("Invalid Settings", "Please select both source and output folders")
        return
    
    dialog.close()
    
    # Start processing with progress
    process_with_progress(settings)

def process_with_progress(settings):
    import time
    
    # Create progress indicator
    progress = anchorpoint.Progress("Processing Files", "Starting processing...", 
                                   infinite=False, cancelable=True)
    
    try:
        steps = ["Scanning files", "Processing images", "Applying filters", "Saving results"]
        
        for i, step in enumerate(steps):
            if progress.canceled:
                print("Processing cancelled by user")
                break
                
            progress.set_text(step)
            progress.report_progress((i + 1) / len(steps))
            
            print(f"Step {i+1}: {step}")
            time.sleep(2)  # Simulate work
        
        if not progress.canceled:
            ui = anchorpoint.UI()
            ui.show_success("Processing Complete", 
                           f"All files processed and saved to {settings['output']}")
    
    finally:
        progress.finish()

advanced_settings_dialog()
```
This example organizes interface elements into sections (into foldable groups) and uses a process indicator at the end that can be used for a heavy operation. Note that in practice you would run this process asynchronously. 

#### Dynamic Dialog Updates

```python
import anchorpoint

def dynamic_dialog_example():
    dialog = anchorpoint.Dialog()
    dialog.title = "Dynamic Settings"
    
    # Initial form
    dialog.add_text("Select media type:")
    dialog.add_dropdown("Image", ["Image", "Video", "Audio"], var="type", callback=update_options)
    
    dialog.add_text("Select format:")
    dialog.add_dropdown("JPEG", ["JPEG", "PNG", "TIFF", "BMP"], var="format")
    
    dialog.add_text("Output path:")
    dialog.add_input("", placeholder="Enter output path", var="output")
    
    dialog.add_button("Process", callback=process_media, var="process", enabled=False)
    dialog.add_button("Cancel", callback=lambda d: d.close(), primary=False)
    
    dialog.show()

def update_options(dialog, value):
    # This is a simplified example showing the concept
    # In practice, dynamic updates require more complex handling
    
    format_options = {
        "Image": ["JPEG", "PNG", "TIFF", "BMP"],
        "Video": ["MP4", "AVI", "MOV", "MKV"], 
        "Audio": ["MP3", "WAV", "FLAC", "AAC"]
    }
    
    # Get current type
    media_type = value
    formats = format_options.get(media_type, [])
    print(f"Available formats for {media_type}: {formats}")
    
    # Enable process button once type is selected
    dialog.set_enabled("process", True)

def process_media(dialog):
    media_type = dialog.get_value("type")
    format_type = dialog.get_value("format")
    output = dialog.get_value("output")
    
    ui = anchorpoint.UI()
    
    if not format_type or not output:
        ui.show_error("Incomplete Settings", "Please select format and output path")
        return
    
    ui.show_info("Processing Started", f"Converting to {format_type} format")
    dialog.close()

dynamic_dialog_example()
```
This dialog enables/disables the "Process" button when a value is selected using the callback function `update_options`.

## Source: documentation/docs/api/python/utility.md


## Utility Classes and Functions

The Anchorpoint Python API provides various utility functions and classes for common operations such as file management, project operations, application detection, logging, and more. These utilities are distributed across the `anchorpoint` and `apsync` modules to support different aspects of Anchorpoint workflows.

### Usage

Utility functions are accessed directly from their respective modules:

```python
import anchorpoint
import apsync

# Get application directory
app_dir = anchorpoint.get_application_dir()

# Check if an application exists
has_blender = anchorpoint.check_application("/path/to/blender.exe", "Blender 3D")

# Copy files within Anchorpoint workspace
apsync.copy_file("/source/file.jpg", "/target/file.jpg", workspace_id="ws_123")

# Log error messages
anchorpoint.log_error("Something went wrong during processing")
```

### Anchorpoint Utilities

#### Application Management

- **`check_application(application_path, info='', name=None)`** Checks if an application exists and is accessible at the specified path.

    Arguments
    - `application_path` *(str):* Absolute path to the application executable
    - `info` *(str):* Additional information about the application (optional)
    - `name` *(str):* Display name for the application (optional)

    Returns: (*bool*) True if the application exists and is accessible

- **`get_application_dir()`** Gets the Anchorpoint application directory path.

    Returns: (*str*) Absolute path to the Anchorpoint installation directory

#### Configuration and Context

- **`get_config()`** Gets the Anchorpoint configuration object containing default settings and OAuth credentials for various services.

    Returns: (*class: APConfig*) Configuration object with the following properties:
    - `gcs_client_id` *(str):* Google Cloud Storage OAuth client ID
    - `gcs_key` *(str):* Google Cloud Storage OAuth client key  
    - `github_client_id` *(str):* GitHub OAuth client ID
    - `github_client_key` *(str):* GitHub OAuth client key
    - `gitlab_client_id` *(str):* GitLab OAuth client ID
    - `gitlab_client_key` *(str):* GitLab OAuth client key

    Example
    ```python
    import anchorpoint as ap
    
    config = ap.get_config()
    github_id = config.github_client_id
    gcs_credentials = (config.gcs_client_id, config.gcs_key)
    ```

- **`get_context()`** Gets the current execution context containing file, user, and project information.

    Returns: (*class: Context*) Current context object

- **`get_api()`** Gets the main API object for accessing Anchorpoint functionality.

    Returns: (*class: Api*) Main API object

#### File and System Operations

- **`copy_files_to_clipboard(file_paths)`** Copies file paths to the system clipboard.

    Arguments
    - `file_paths` *(list[str]):* List of absolute file paths to copy

- **`temp_dir()`** Gets the temporary directory path used by Anchorpoint.

    Returns: (*str*) Absolute path to the temporary directory

- **`join_project_path(path, project_id, workspace_id)`** Joins a path with project information for cross-project operations.

    Arguments
    - `path` *(str):* File or folder path
    - `project_id` *(str):* Target project identifier
    - `workspace_id` *(str):* Workspace identifier

#### Logging and Error Handling

- **`log_error(message)`** Logs an error message to the Anchorpoint error log.

    Arguments
    - `message` *(str):* Error message to log

#### Action and Integration Management

- **`create_action(yaml_path, action)`** Creates a new action from an Action object.

    Arguments
    - `yaml_path` *(str):* Path where the action YAML file should be created
    - `action` *(class: Action):* Action object containing action configuration

- **`create_app_link(target)`** Creates an application link for files or tasks.

    Arguments
    - `target` *(str or class: Task):* File path or Task object to create link for

    Returns: (*str*) Generated application link

- **`open_integration_preferences(integration_name)`** Opens the preferences dialog for a specific integration.

    Arguments
    - `integration_name` *(str):* Name of the integration to configure

#### Notifications

- **`schedule_custom_notification(project_id, workspace_id, message, user_ids, meta_data=None)`** Schedules a custom notification to specific users.

    This function sends a custom notification to specified users. You can include metadata as a dictionary that will be converted to JSON and then will be accessible in the receiving custom trigger hook via the `on_custom_notification` event hook.

    Arguments
    - `project_id` *(str):* Project identifier
    - `workspace_id` *(str):* Workspace identifier
    - `message` *(str):* Notification message to send
    - `user_ids` *(list[str]):* List of user IDs to notify
    - `meta_data` *(dict, optional):* Dictionary of metadata to include with the notification (supports str, int, float, and bool values)

    Example:
    ```python
    import anchorpoint
    
    ctx = anchorpoint.get_context()
    
    # Send notification with metadata to specific users
    user_ids = ["user-123", "user-456"]
    metadata = {
        "action": "file_updated",
        "file_path": "/project/asset.blend",
        "version": 5,
        "priority": "high"
    }
    
    anchorpoint.schedule_custom_notification(
        ctx.project_id,
        ctx.workspace_id,
        "Your asset has been updated!",
        user_ids,
        metadata
    )
    ```

For timeline-related utilities and operations, see the Timeline documentation.

For version control-related utilities and operations, see the Timeline documentation.

For project-related utilities and operations, see the Project documentation.

### Apsync Utilities

#### File Operations

- **`copy_file(source, target, overwrite=False, workspace_id=None)`** Copies a file within the Anchorpoint workspace.

    Arguments
    - `source` *(str):* Source file path
    - `target` *(str):* Target file path
    - `overwrite` *(bool):* Whether to overwrite existing files
    - `workspace_id` *(str):* Optional workspace ID for cross-workspace operations

- **`copy_folder(source, target, overwrite=False, workspace_id=None)`** Copies a folder within the Anchorpoint workspace.

    Arguments  
    - `source` *(str):* Source folder path
    - `target` *(str):* Target folder path
    - `overwrite` *(bool):* Whether to overwrite existing folders
    - `workspace_id` *(str):* Optional workspace ID for cross-workspace operations

- **`rename_file(source, target)`** Renames or moves a file.

    Arguments
    - `source` *(str):* Current file path
    - `target` *(str):* New file path

- **`rename_folder(source, target)`** Renames or moves a folder.

    Arguments
    - `source` *(str):* Current folder path
    - `target` *(str):* New folder path

#### Template Operations

- **`copy_file_from_template(source, target, variables={}, workspace_id=None)`** Copies a file from a template with variable substitution.

    Arguments
    - `source` *(str):* Template file path
    - `target` *(str):* Target file path
    - `variables` *(dict[str, str]):* Variables to substitute in the template
    - `workspace_id` *(str):* Optional workspace ID

    Returns: (*str*) Path to the created file

- **`copy_from_template(source, target, variables={}, skip_root=True, workspace_id=None)`** Copies files and folders from a template with variable substitution.

    Arguments
    - `source` *(str):* Template source path
    - `target` *(str):* Target path
    - `variables` *(dict[str, str]):* Variables to substitute
    - `skip_root` *(bool):* Whether to skip the root template folder
    - `workspace_id` *(str):* Optional workspace ID

    Returns: (*str*) Path to the created content

- **`create_template(path, name, workspace_id, type)`** Creates a template from existing content.

    Arguments
    - `path` *(str):* Path to create template from
    - `name` *(str):* Template name
    - `workspace_id` *(str):* Workspace identifier
    - `type` *(class: TemplateType):* Type of template to create

- **`resolve_variables(text, variables)`** Resolves template variables in text.

    Arguments
    - `text` *(str):* Text containing variable placeholders
    - `variables` *(dict[str, str]):* Variables to substitute

    Returns: (*str*) Text with resolved variables

For project-related utilities and operations, see the Project documentation.

#### User and Access Management

- **`add_user_to_project(workspace_id, project_id, invited_from, email, access_level)`** Adds a user to a project.

    Arguments
    - `workspace_id` *(str):* Workspace identifier
    - `project_id` *(str):* Project identifier
    - `invited_from` *(str):* Email of user sending invitation
    - `email` *(str):* Email of user to add
    - `access_level` *(class: AccessLevel):* Access level for the user

- **`remove_user_from_project(workspace_id, project_id, email)`** Removes a user from a project.

    Arguments
    - `workspace_id` *(str):* Workspace identifier
    - `project_id` *(str):* Project identifier  
    - `email` *(str):* Email of user to remove

- **`remove_user_from_workspace(workspace_id, email)`** Removes a user from a workspace.

    Arguments
    - `workspace_id` *(str):* Workspace identifier
    - `email` *(str):* Email of user to remove

- **`get_workspace_access(workspace_id)`** Gets the current user's access level in a workspace.

    Arguments
    - `workspace_id` *(str):* Workspace identifier

    Returns: (*class: AccessLevel*) User's access level

- **`get_workspace_members(workspace_id)`** Gets all members of a workspace.

    Arguments
    - `workspace_id` *(str):* Workspace identifier

    Returns: (*class: WorkspaceMemberList*) List of workspace members

- **`get_project_members(workspace_id, project_id)`** Gets all members of a project.

    Arguments
    - `workspace_id` *(str):* Workspace identifier
    - `project_id` *(str):* Project identifier

    Returns: (*class: GroupMemberList*) List of project members

For timeline-related utilities and operations, see the Timeline documentation.

For thumbnail-related utilities and operations, see the Thumbnails documentation.

#### File Metadata Operations

- **`comment_file(file_path, comment)`** Adds or updates a comment on a file.

    Arguments
    - `file_path` *(str):* Path to file to comment on
    - `comment` *(str or None):* Comment text, or None to remove comment

- **`set_folder_icon(folder_path, icon)`** Sets a custom icon for a folder.

    Arguments
    - `folder_path` *(str):* Path to folder
    - `icon` *(class: Icon or None):* Icon object or None to remove custom icon

#### System Configuration

- **`get_api()`** Gets the main API object for apsync operations.

    Returns: (*class: Api*) Main API object

- **`get_api_version()`** Gets the current API version information.

    Returns: (*class: ApiVersion*) API version object

- **`configure_daemon(address, port)`** Configures the Anchorpoint daemon connection.

    Arguments
    - `address` *(str):* Daemon address
    - `port` *(str):* Daemon port

- **`get_daemon_address()`** Gets the current daemon address.

    Returns: (*str*) Daemon address

- **`set_daemon_address(address)`** Sets the daemon address.

    Arguments
    - `address` *(str):* New daemon address

- **`get_server_url()`** Gets the current server URL.

    Returns: (*str*) Server URL

- **`set_server_url(url)`** Sets the server URL.

    Arguments
    - `url` *(str):* New server URL

- **`get_server_version()`** Gets the server version.

    Returns: (*str*) Server version string

- **`get_client_name()`** Gets the client name.

    Returns: (*str*) Client name

- **`set_client_name(name)`** Sets the client name.

    Arguments
    - `name` *(str):* New client name

- **`set_account_email(email)`** Sets the account email.

    Arguments
    - `email` *(str):* Account email address

#### IPC (Inter-Process Communication)

- **`ipc_publish(message)`** Publishes an IPC message.

    Arguments
    - `message` *(class: IpcMessage):* Message to publish

- **`ipc_get_message(topic)`** Gets an IPC message from a topic.

    Arguments
    - `topic` *(str):* Topic to get message from

    Returns: (*class: IpcMessage or None*) Message object or None if no message

- **`ipc_has_messages(topic)`** Checks if there are messages in a topic.

    Arguments
    - `topic` *(str):* Topic to check

    Returns: (*bool*) True if there are messages

- **`ipc_unsubscribe(topic)`** Unsubscribes from an IPC topic.

    Arguments
    - `topic` *(str):* Topic to unsubscribe from

#### File ID Management

- **`get_file_id(path)`** Gets the unique ID for a file.

    Arguments
    - `path` *(str):* File path

    Returns: (*str*) Unique file ID

- **`get_folder_id(path)`** Gets the unique ID for a folder.

    Arguments
    - `path` *(str):* Folder path

    Returns: (*str*) Unique folder ID

- **`get_file_by_id(id, project=None)`** Gets file path from its unique ID.

    Arguments
    - `id` *(str):* File ID
    - `project` *(class: Project):* Optional project context

    Returns: (*str or None*) File path or None if not found

- **`get_folder_by_id(id, project=None)`** Gets folder path from its unique ID.

    Arguments
    - `id` *(str):* Folder ID
    - `project` *(class: Project):* Optional project context

    Returns: (*str or None*) Folder path or None if not found

#### Dynamic Module Loading

- **`import_local(relative_path, reload)`** Imports a local Python module dynamically.

    Arguments
    - `relative_path` *(str):* Relative path to the Python module
    - `reload` *(bool):* Whether to reload the module if already loaded

    Returns: (*object*) Imported module object

### Utility Classes

#### APConfig Class

The APConfig class provides default configuration values for various integrations and services used by Anchorpoint.

##### Properties

- **`gcs_client_id`** *(str):* Google Cloud Storage client ID for integration
- **`gcs_key`** *(str):* Google Cloud Storage API key  
- **`github_client_id`** *(str):* GitHub OAuth client ID for integration
- **`github_client_key`** *(str):* GitHub OAuth client secret
- **`gitlab_client_id`** *(str):* GitLab OAuth client ID for integration
- **`gitlab_client_key`** *(str):* GitLab OAuth client secret

#### Action Class

The Action class represents an Anchorpoint action configuration that can be used to create new actions programmatically.

##### Constructor

- **`Action()`** Creates a new Action instance.

##### Properties

- **`author`** *(str):* Author of the action
- **`category`** *(str):* Category for organizing the action
- **`description`** *(str):* Description of what the action does
- **`file_registration`** *(str):* File filter pattern for when action should appear
- **`folder_registration`** *(str):* Folder filter pattern for when action should appear
- **`icon`** *(str):* Icon path or identifier for the action
- **`id`** *(str):* Unique identifier for the action
- **`is_python`** *(bool):* Whether the action uses Python scripting
- **`name`** *(str):* Display name of the action
- **`script`** *(str):* Script file path or content for the action

### Examples

#### Application Detection and Setup

```python
import anchorpoint
import os

def check_required_applications():
    """Check if required applications are installed"""
    
    # Define application paths to check
    apps_to_check = [
        ("C:/Program Files/Blender Foundation/Blender 3.6/blender.exe", "Blender 3D", "Blender"),
        ("C:/Program Files/Autodesk/Maya2024/bin/maya.exe", "Autodesk Maya", "Maya"),
        ("C:/Program Files/Adobe/Adobe Photoshop 2024/Photoshop.exe", "Adobe Photoshop", "Photoshop")
    ]
    
    available_apps = []
    
    for app_path, info, name in apps_to_check:
        if anchorpoint.check_application(app_path, info, name):
            available_apps.append(name)
            print(f"✓ {name} is available")
        else:
            print(f"✗ {name} not found at {app_path}")
    
    return available_apps

# Check applications
available = check_required_applications()
print(f"\nFound {len(available)} applications: {', '.join(available)}")
```

#### File Operations and Backup

```python
import apsync
import anchorpoint
import os

ctx = anchorpoint.get_context()

def manage_file_operations():
    """Demonstrate file operations and organization"""
    
    if not ctx.path or not os.path.isfile(ctx.path):
        ui = anchorpoint.UI()
        ui.show_error("Invalid Selection", "Please select a file to process")
        return
    
    try:
        # Copy current file to a backup location
        backup_dir = os.path.join(ctx.folder, "backups")
        os.makedirs(backup_dir, exist_ok=True)
        
        backup_path = os.path.join(backup_dir, f"backup_{ctx.filename}")
        apsync.copy_file(ctx.path, backup_path, overwrite=True, workspace_id=ctx.workspace_id)
        print(f"Created backup: {backup_path}")
        
        # Add comment to the original file
        apsync.comment_file(ctx.path, f"Backup created on {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Add timeline entry for the backup action
        apsync.add_timeline_entry(ctx.path, f"Created backup of {ctx.filename}")
        
        print(f"File operations completed for: {ctx.filename}")
        
    except Exception as e:
        anchorpoint.log_error(f"File operations failed: {str(e)}")
        print(f"Error: {e}")

manage_file_operations()
```

#### Template System Usage

```python
import apsync
import anchorpoint
import os
from datetime import datetime

ctx = anchorpoint.get_context()

def batch_organize_assets():
    """Organize and process multiple asset files"""
    
    if not ctx.selected_files:
        ui = anchorpoint.UI()
        ui.show_info("No Selection", "Please select files to organize")
        return
    
    # Create organized folder structure
    base_path = ctx.folder
    folders = {
        'textures': ['jpg', 'png', 'tiff', 'exr', 'hdr'],
        'models': ['fbx', 'obj', 'ma', 'mb', 'blend', 'max'],
        'audio': ['wav', 'mp3', 'ogg', 'aiff'],
        'videos': ['mp4', 'avi', 'mov', 'mkv']
    }
    
    # Create folders
    for folder_name in folders.keys():
        folder_path = os.path.join(base_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
    
    moved_files = []
    
    for file_path in ctx.selected_files:
        filename = os.path.basename(file_path)
        file_ext = os.path.splitext(filename)[1][1:].lower()
        
        # Find appropriate folder
        target_folder = None
        for folder_name, extensions in folders.items():
            if file_ext in extensions:
                target_folder = folder_name
                break
        
        if target_folder:
            # Move file to appropriate folder
            target_path = os.path.join(base_path, target_folder, filename)
            
            try:
                apsync.rename_file(file_path, target_path)
                moved_files.append((filename, target_folder))
                
                # Add comment about the organization
                apsync.comment_file(target_path, f"Organized on {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                
                print(f"Moved {filename} to {target_folder}/")
                
            except Exception as e:
                anchorpoint.log_error(f"Failed to move {filename}: {str(e)}")
                print(f"Error moving {filename}: {e}")
    
    # Create summary timeline entry
    if moved_files:
        summary = f"Organized {len(moved_files)} files into folders"
        apsync.add_timeline_entry(base_path, summary)
        print(f"\nSummary: {summary}")

batch_organize_assets()
```

#### Template System Usage

```python
import apsync
import anchorpoint
import os

ctx = anchorpoint.get_context()

def create_project_from_template():
    """Create a new project structure from a template"""
    
    # Define template variables
    variables = {
        "PROJECT_NAME": "MyAwesomeGame", 
        "CLIENT_NAME": "Epic Games",
        "PROJECT_CODE": "EG001",
        "CREATION_DATE": "2025-11-15"
    }
    
    # Template source (could be a shared template directory)
    template_source = "/templates/game_project_template"
    target_path = os.path.join(ctx.path, variables["PROJECT_NAME"])
    
    try:
        # Copy template with variable substitution
        created_path = apsync.copy_from_template(
            template_source,
            target_path,
            variables=variables,
            skip_root=True,
            workspace_id=ctx.workspace_id
        )
        
        print(f"Created project structure at: {created_path}")
        
        # Resolve variables in template text
        readme_template = "Project: {{PROJECT_NAME}} for {{CLIENT_NAME}}"
        readme_content = apsync.resolve_variables(readme_template, variables)
        print(f"README content: {readme_content}")
        
        # Add timeline entry for the template creation
        apsync.add_timeline_entry(created_path, f"Project structure created from template")
        
        return created_path
        
    except Exception as e:
        anchorpoint.log_error(f"Template project creation failed: {str(e)}")
        print(f"Error creating project from template: {e}")
        return None

# Create project structure
project_path = create_project_from_template()
```
