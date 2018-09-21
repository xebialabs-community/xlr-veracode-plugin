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

## References

<https://help.veracode.com/home>
