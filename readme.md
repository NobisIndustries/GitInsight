# GitInsight

**tl;dr**: This is a standalone web application that shows various analyses of a given repository. You can assign teams
to the contributors and use this information to gain new insights into your project.

**Try it out**: `docker run -v ~/gitinsight_data:/app/data -p 80:80 fabianproductions/gitinsight:latest`

## What is this about?

You want to get a feeling for your repository: *Which development team maintains which part? What part is most active?
Who can I ask for help with this class I've never seen before? And are there architectural problems that I haven't
noticed yet?*

GitInsight lets you assign teams to the contributors of a git repository. Different analyses combine this metadata with
the edit history of every tracked file to provide you with better overview.

Since this application is meant to be hosted, you can create accounts and manage user permissions. So the compliance 
people don't yell at you. Again. Also you should probably use a reverse proxy for encryption, integration in existing 
networks and so on.