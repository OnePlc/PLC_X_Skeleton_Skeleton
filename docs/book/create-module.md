# Create Module based on skeleton

In this tutorial we'll show you how you can create your 
own onePlace Module based on Skeleton.

In this example we gonna make a module called "Book",
which allows us to manage our book library.

As onePlace is opensource, and we want to encourage you to 
also work under an open licence, we will use composer in this
tutorial for packaging and distributing the module. 

if you plan to make an closed source project / module, you will
need other ways to install & autoload your module in oneplace than
the open composer infrastructure. we will provide tutorials for this
also at a later point.

## The bootstrap script

As you can see in `data\createmodulefromskeleton.ps1` and `data\createmodulefromskeleton.sh` we are
currently working on a bootstrap script, that will do most of the work
described here for you. 

So this tutorial is for those who want a technical understanding of the process
and also for those who want to start before the scripts are finished which can
take a couple of weeks.

## Getting started (manual process)

So lets start to create our new module "Book".

* Go to [https://github.com/OnePlc/PLC_X_Skeleton/releases](https://github.com/OnePlc/PLC_X_Skeleton/releases) and download the latest release of oneplace-skeleton
* Unpack the files to your destination folder
* Open the project with your desired editor (we recommend [PHPStorm](https://www.jetbrains.com/phpstorm/))
* Search and Replace within the whole project directory for the following terms (without """)

> (Example) "SearchFor" - "ReplaceWith" (MUST be case-sensitive)

> "Skeleton" - "Book"

> "skeleton" - "book"

* Rename all necessary files and folders
```
.
+-- src
|   +-- Controller
|   |   +-- SkeletonController.php
|   +-- Model
|   |   +-- Skeleton.php
|   |   +-- SkeletonTable.php
+-- test
|   +-- Controller
|   |   +-- SkeletonControllerTest.php
+-- view
|   +-- layout
|   |   +-- skeleton-default.phtml
|   +-- one-place
|   |   +-- skeleton
|   |   |   +-- skeleton
|   |   |   |   +-- add.phtml (edit/view/index)
```
* so you will end up with something like
```
.
+-- src
|   +-- Controller
|   |   +-- BookController.php
|   +-- Model
|   |   +-- Book.php
|   |   +-- BookTable.php
+-- test
|   +-- Controller
|   |   +-- BookControllerTest.php
+-- view
|   +-- layout
|   |   +-- book-default.phtml (optional - you can also delete it)
|   +-- one-place
|   |   +-- book
|   |   |   +-- book
|   |   |   |   +-- add.phtml (edit/view/index)

```

Done - you finally have a working "Book" Module for onePlace !

Now, lets see how we can add this module to onePlace

## Packaging and distribution

For opensource projects, you can use [packagist.org](https://packagist.org) and [composer](https://getcomposer.org)
to package and distribute your package. Also composer handles autoloading and integration
of your new "Book" module into onePlace.

Before you start, check `composer.json` within your "Book" module directory and 
make all changes you want to the file for publishing (like change name, customize description and so on)

* Publish your module on [github.com](https://github.com) with an open licence
* Go to [packagist.org](https://packagist.org) and submit your new module
* Add your new package to oneplace with composer as shown on packagist.org

Your new module is now available in onePlace ! As with Skeleton, go to /update and perform
the updates to run your `install.sql` so your module "Book" is fully installed in onePlace!

Congrats and have Fun with your new module