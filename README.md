# TMNA XL Release Veracode plugin v1.0.0

## Preface

This document describes the functionality provided by the XL Release Veracode plugin.

See the [XL Release reference manual](https://docs.xebialabs.com/xl-release) for background information on XL Release and release automation concepts.  

## Overview

This plugin allows XL Release to pull code analysis data for a build from Veracode's API.

## Requirements

* XL Release 8.x

## Installation

* Run ./gradlew build from the repository root.
* Copy the jar file in build/libs to the xl-release-server/plugins/__local__ directory.
* Restart the XL Deploy|Release server.

## Features/Usage/Types/Tasks

### GetDetailedReportPdf task
Retrieves a PDF file from Veracode and attaches it to the task.

### VeracodeResultsTile
Displays data in a dashboard tile.

### Configuration:

* In Shared Configuration at the folder or global level, create a Tmna:Veracode Server with url, username, and password:
 
![](images/server-config.png)
 
* In any template or release, go to the Release Dashboard and add a Veracode Results tile:
 
![](images/tile-config-1.png)
 
* Configure the tile with a title and a server from the configuration in step 2.
 
![](images/tile-config-2.png)
 
* Go back to view mode and confirm the tile is on the dashboard with a Refresh button visible:

![](images/tile-1.png) 
 
* Press Refresh and wait a few seconds for the display to appear.  This is just a sampling of the data available in the output that Henry showed me.
 
![](images/tile-2.png)

 
* Add a Tmna:GetVeracodeDetailedReportPdf task to the template's Release Flow page:
 
![](images/task-1.png)
 
* Configure the task with the Veracode server from the configuration in step 2.
 
![](images/task-2.png)
 
* On the template or release properties panel, add user and password entries for "Run automated tasks as user".
 
![](images/run-as-user.png)

* Run the release.  The pdf file will be pulled down from Veracode and affixed to the task as a downloadable attachment:

![](images/task-3.png)
 
## References

<https://help.veracode.com/home>

