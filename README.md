# UdonProfiler

<p align="center">
  <img src="https://github.com/bSenpai/UdonProfiler/blob/main/resources/logo.png">
</p>

<p align="center">
  <img src="https://github.com/bSenpai/UdonProfiler/blob/main/resources/demo.gif">
</p>

## Table of Content
* [About](#about)
* [Installation](#installation)
* [Usage](#usage)
* [Notes](#notes)
* [GUI Interface](#gui-interface)
  * [Control Panel](#control-panel)
  * [Frame Chart](#frame-chart)
  * [Details Panel](#details-panel)
    * [Hierarchy View](#hierarchy-view)
    * [Timeline View](#timeline-view)
    * [Statistics View](#statistics-view)
* [How It Works](#how-it-works)
* [Contributing](#contributing)
* [License](#license)

## About

UdonProfiler is a deep profiling utility designed for benchmarking UdonSharp scripts. UdonProfiler allows world 
developers to measure script performance in a similar fashion to Unity's built-in profiling utility. UdonSharp
by default does not support Unity's deep-profiling module, so UdonProfiler aims to fill that gap.

UdonProfiler does a great job at helping pinpoint slow code paths, such as those found in procedural generation scripts,
which was the original reason behind the making of this application.

## Installation

1. Download the latest release [here](https://github.com/bSenpai/UdonProfiler/releases/latest). The UdonProfiler zip file contains a setup executable for the GUI application, and a unitypackage 
for interfacing with the profiler and GUI. 

2. Run UdonProfiler-v1.0.exe to start the setup process. At the end of the setup process, you should have an application installed on your computer called Udon Profiler.
If you opted to create a desktop shortcut, you should see the following:

<p align="center">
  <img src="https://github.com/bSenpai/UdonProfiler/blob/main/resources/desktop-shortcut.png">
</p>

3. Drag and drop UdonProfiler-v1.0.unitypackage into an active Unity project for a VRChat world you're working on.

4. Copy the ```Profiler``` prefab found under ```bSenpai/UdonProfiler/UdonProfilerExampleScene/Prefabs``` into the scene.

## Usage

1. The profiler uses samples to collect script performance information for a given code segment. To add a new sample, call the ```BeginSample``` method from the ```Profiler``` class, passing in a unique name for that sample. Then, add an ```EndSample``` method to signal where to stop collecting information.

  * Example:
    ```C#
    profiler.BeginSample("Sample A");
    // Do stuff here
    profiler.EndSample();
    ```

  * See the [demo game manager script](./UdonProfilerDemo/Assets/bSenpai/UdonProfiler/UdonProfilerExampleScene/GameManager.cs) for more examples.

2. Launch the UdonProfiler application (see [GUI Interface](#gui-interface) for more information).

3. Click the record button to start listening for Unity messages.

4. Enter Play Mode in your Unity Project. Make sure the ```Profiler``` prefab is included in your scene, is active and has its ```Script Enabled``` field checked. You should see a continuous stream of messages under your Unity Console (see [How It Works](#how-it-works) if you want to know what the messages represent).

5. After confirming that the messages are being output to your console, check the UdonProfiler application. You should see new information being populated in the application. The GUI application is designed to mimic Unity's Profiler GUI, so it should look familiar if you're already experienced with it. 

6. To stop recording, click the record button again. 

## Notes

* Each ```BeginSample``` must be paired with an ```EndSample``` - not doing so will result in the profiler failing to work.

* If a function has multiple return paths, make sure you have an ```EndSample``` for each respective path, or alternatively wrap the ```BeginSample``` and ```EndSample``` around each function call instead of having them inside the function.

* Do not use the ```BeginFrame``` and ```EndFrame``` methods - these are strictly for use by the profiler (see [How It Works](#how-it-works) for more information).

* If you're making use of default execution order for your own custom scripts, make sure the values don't exceed the lower and upper limits imposed by the profiler (currently at -2 million and +2 million) (see [How It Works](#how-it-works) for more information).

* The profiling script comes with some overhead, so make sure you only have it running during testing and development, and ideally only when you're actively measuring your project's performance.

* To deactivate the profiler, uncheck the ```Script Enabled``` field under the ```Profiler``` script in your scene. This field can be alternatively toggled via a script if you choose to do so.

* When not in use, you'll notice the application takes up a little CPU overhead (see [How It Works](#how-it-works) for more information). Hence, when not in use for extended periods of time, it's recommended to just close the application.

## GUI Interface

### Control Panel

<p align="center">
  <img src="https://github.com/bSenpai/UdonProfiler/blob/main/resources/control-panel.png">
</p>

At the top of the GUI, you have the control panel. Here, you can start and pause recording, iterate through recorded frames, and clear the application of all current frames. You can also see the current frame number and total frames recorded so far.

### Frame Chart

<p align="center">
  <img src="https://github.com/bSenpai/UdonProfiler/blob/main/resources/frame-chart.png">
</p>

Below the control panel sits the frame chart. Here, you get a live-view of your Unity application's frame timings. Clicking anywhere on the graph will pause the live-view (but won't pause recording) and populate the views below with information about the current frame that you selected from the graph.

### Details Panel 

<p align="center">
  <img src="https://github.com/bSenpai/UdonProfiler/blob/main/resources/details-panel.png">
</p>

Below the frame chart sits the details panel. Here, you get three different views: hierarchy view, timeline view, and statistics view.

#### Hierarchy View

<p align="center">
  <img src="https://github.com/bSenpai/UdonProfiler/blob/main/resources/hierarchy-view.png">
</p>

The hierarchy view displays the current frame information in a hierarchical order - sorted by call order initially. This is meant to mimic Unity Profiler's hierarchy view.

Each sample contains information about the total time it took (in both percentage and milliseconds), the time it spent on itself only (excluding time spent on child calls), and the total number of calls.

If you haven't set any sample points, you should see the default sample called ```UdonBehaviour```. Clicking the expand arrow will show the children of the current sample. By default, ```UdonBehaviour``` has children for each core stage in the Unity scripting pipeline, that is: ```FixedUpdate```, ```Update```, ```LateUpdate```, and ```PostLateUpdate``` (see https://docs.unity3d.com/Manual/ExecutionOrder.html for more information). Your samples will always belong to, and as a result be children of, one of these samples.

#### Timeline View

<p align="center">
  <img src="https://github.com/bSenpai/UdonProfiler/blob/main/resources/timeline-view.png">
</p>

The timeline view displays allows you to see when each call to a given sample was made. This was meant to mimic Unity Profiler's timeline view.

At the bottom left corner of this view, you have the option to reset the graph, pan through it, and zoom into a specific region.

Hovering over a bar gives you additional information about the sample, namely its name (if it was not visible already), the time that call took in milliseconds, and the total time (and number of calls) for all calls to that sample (if more than one exist).

#### Statistics View

<p align="center">
  <img src="https://github.com/bSenpai/UdonProfiler/blob/main/resources/statistics-view.png">
</p>

The statistics view shows general statistics for samples collected. This view is unique to UdonProfiler, and is meant to give a quick overview of how each sample is performing on an overall basis.

Here you get information on the total number of samples collected, average sample times, and minimum and maximum times.

Note here this view is not hierarchical, so if you have a sample that is called from two or more different paths, you'll see the combined information only.

## How It Works

The core profiler consists of a ```Kickoff``` script, a ```Handler``` script, and a ```Profiler``` script.

The ```Kickoff``` script aims to run before any other scripts run by using a low default execution order, while the ```Handler``` script aims to run after all other scripts have run, courtesy of MerlinVR (see [Credits](#credits)).

The ```Profiler``` script provides the interface for collecting sample information for each frame.

The ```Kickoff``` script starts a new frame inside the ```FixedUpdate``` loop, as it is the first loop to run (see [Unity](https://docs.unity3d.com/Manual/ExecutionOrder.html)), while the ```Handler``` script ends the current frame in the ```PostLateUpdate``` loop, as its the last loop to run.

For each ```BeginSample``` and ```EndSample``` pair, the ```Profiler``` script stores the sample information (timing, number of calls, etc.) inside a ```DataDictionary``` object. Since a given sample can contain child samples (think nested function calls), this object is recursive in nature, using a data structure similar to that of an n-ary tree. The ```BeginFrame``` creates the tree and its root for the current frame.

Once the ```EndFrame``` method is called by the ```Handler``` script, the ```Profiler``` script iterates through the tree and creates a string containing information about the samples collected, then outputs this information to the console. The reason for doing so instead of writing to a file is that the latter option is not currently supported by UdonSharp.

Each message is wrapped with ```##BEGIN_FRAME##``` and ```##END_FRAME##``` tags (this desgin also allows for creating new GUIs using other frameworks if you choose to do so). The GUI application scans Unity's log file (where the console output is written to), filtering for these tags.

When the message is read, the GUI application prepares all necessary information and data structures, and passes them on to the various views to be displayed to the user. The GUI application is constantly scanning the Unity log files, even when not recording, hence the slight CPU overhead when the application is idle. 

## Contributing

UdonProfiler is a solo open-source project. I highly appreciate any contributions. Please refer to the [contribution guidelines](./CONTRIBUTING.md) for more information on how you can help.

* Bug Report: If you see an error message or run into an issue while using UdonProfiler, please create a [bug report](https://github.com/bSenpai/UdonProfiler/issues/new?assignees=&labels=&projects=&template=bug_report.md&title=%5BBUG%5D).

* Feature Request: If you have an idea or you're missing a capability that would make development easier and more robust, please submit a [feature request](https://github.com/bSenpai/UdonProfiler/issues/new?assignees=&labels=&projects=&template=feature_request.md&title=%5BFEATURE%5D).

## Credits

* [UdonSharp script profiler](https://gist.github.com/MerlinVR/2da80b29361588ddb556fd8d3f3f47b5)

## License

Distributed under the MIT Open Source license. See [LICENSE](./LICENSE) for more information.
