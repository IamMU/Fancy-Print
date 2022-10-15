# Contributing Guidelines

First off, thanks for taking the time to contribute! ❤️ </br>
When contributing to this repository, please first discuss the change you wish to make via issues before making a change. New issues are always welcome.
</br>
Please note that :
</br>
- NO PR will be accepted unless assigned in issues
- NO One should change file structure like deleting src and creating some other directory
</br>
> We have a [Code of Conduct](CODE_OF_CONDUCT.md), please follow it in all your interactions with the project.

<br>

* * * * *

<br>

# Basics of Git and GitHub

Before we proceed, it's better to know the difference between Git and Github. Git is a version control system (VCS) that allows us to keep track of the history of our source code , whereas GitHub is a service that hosts Git projects. 

We assume you have created an account on Github and installed Git on your System.

Now enter your name and E-mail (used on Github) address in Git, by using following command.

```
git config --global user.name "YOUR NAME"
git config --global user.email "YOUR EMAIL ADDRESS"
```
This is an important step to mark your commits to your name and email.

<br>

* * * * *

<br>

## Now We'll see the basic workflow of Contributing to Open Source
<br />

## Step 0 : Opening an issue

Thank you for taking the time to open an issue!
Before opening an issue, please be sure that your issue hasn't already been asked.

Here are a few things that will help us help resolve your issues:

- A descriptive title that gives an idea of what your issue refers to
- A thorough description of the issue, (one word descriptions are very hard to understand)
- Screenshots (if appropriate)
- Links (if appropriate)

## Step 1 : Fork a project

You can make a copy of the project to your account. This process is called forking a project to your Github account. On Upper right side of project page on Github, you can see -

<p align="center">  <img  src="https://i.imgur.com/P0n6f97.png">  </p>
Click on fork to create a copy of project to your account. This creates a separate copy for you to work on.

<br />

<br />

## Step 2 : Clone the forked project

You have forked the project you want to contribute to your github account. To get this project on your development machine we use clone command of git.

```
git clone https://github.com/IamMU/Fancy-Print.git
``` 
<br/>
Now you have the project on your local machine.

<br />

## Step 3 : Add a remote (upstream) to original project repository

Remote means the remote location of project on Github. By cloning, we have a remote called origin which points to your forked repository. Now we will add a remote to the original repository from where we had forked.

```
cd <your-forked-project-folder>
git remote add upstream https://github.com/IamMU/Fancy-Print.git
``` 
<br/>
You will see the benefits of adding remote later.

<br />

## Step 4 : Synchronizing your fork

Open Source projects have a number of contributors who can push code anytime. So it is necessary to make your forked copy equal with the original repository. The remote added above called Upstream helps in this.

```
git checkout main
git fetch upstream
git merge upstream/main
git push origin main 
``` 
<br/>

The last command pushes the latest code to your forked repository on Github. The origin is the remote pointing to your forked repository on github.

<br />

## Step 5 : Create a new branch for a feature or bugfix

Usually, all repositories have a main branch that is regarded to be stable, and any new features should be developed on a separate branch before being merged into the main branch. As a result, we should establish a new branch for our feature or bugfix and go to work on the issue. 

```
git checkout -b <feature-branch>
```

This will create a new branch out of master branch. Now start working on the problem and commit your changes.

```
git add --all
git commit -m "<commit message>"
```
The first command adds all the files or you can add specific files by removing -a and adding the file names. The second command gives a message to your changes so you can know in future what changes this commit makes. If you are solving an issue on original repository, you should add the issue number like #35 to your commit message. This will show the reference to commits in the issue.

<br />

## Step 6 : Push code and create a pull request

You now have a new branch containing the modifications you want in the project you forked. Now, push your new branch to your remote github fork. 

```
git push origin <feature-branch>
```
Now you are ready to help the project by opening a pull request means you now tell the project managers to add the feature or bug fix to original repository. You can open a pull request by clicking on green icon -

<p align="center">  <img  src="https://i.imgur.com/aGaqAD5.png">  </p>

Remember your upstream base branch should be main and source should be your feature branch. Click on create pull request and add a name to your pull request. You can also describe your feature.

Fantastic! You've already made your first contribution.🥳

#### Happy Coding 👩‍💻👩‍💻

<br>

* * * * *

<br>

# How can I contribute

There are various ways to contribute to the project : 
- Bug fixes : If you feel that the current website is not working properly or have some bugs that needs fixing, you can raise an issue regarding the same. 
- New features : If you think that new features can be added to the project that are relevant, you can again raise an issue regarding it, and explain what and why you want to add that feature. 
- Updating documentation : If you feel that the current documentations have scope to improve, you can discuss it in by raising an issue.

Any other contribution you feel can be done to the project, you can first discuss with the maintainers and then proceed to contribute.

<br>

* * * * *

<br>

# Important Rules to follow :

- While contributing to this project, please make sure to follow the [*PEP-8 Coding Style*](https://www.geeksforgeeks.org/pep-8-coding-style-guide-python/)
- New code regions are to be commented as : 
```
   ########
   # Name #
   ########
```
- All functions that are not of use for end-use are to be marked private (adding the **__** before the function)

**Regarding comments:**
- Uncommented code will not be merged.
- Overly commented code may be merged but is not recommended.
Be sure to write good comments that are informative and not too long.

> PR's will not be accepted unless they have been thoroughly tested and explained, and screenshots should also be provided in the PR.

<br>

* * * * *

<br>
