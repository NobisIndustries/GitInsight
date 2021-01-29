# GitInsight

**tl;dr**: This is a standalone web application that shows various analyses of a given repository. You can assign teams
to the contributors and use this information to gain new insights into your project.

**Try it out**: `docker run -v ~/gitinsight_data:/app/data -p 80:80 nobisindustries/gitinsight:latest` and visit `http://localhost`

## What is this about?

You want to get a feeling for your repository: *Which development team maintains which part? What part is most active?
Who can I ask for help with this class I've never seen before? And are there architectural problems that I haven't
noticed yet?*

GitInsight lets you assign teams to the contributors of a git repository. Different analyses combine this metadata with
the edit history of every tracked file to provide you with better overview.

Since this application is meant to be hosted, you can create accounts and manage user permissions. So the compliance 
people don't yell at you. Again.

## I want to deploy it

To use this application in a productive environment, you may want better control of the routing as well as encrypted 
connections. The common approach for these issues is to use a reverse proxy. This can be an extra application like 
nginx or Traefik which wraps GitInsight and takes care of all the communication with the rest of the network.

To get started, you can find a basic reverse proxy setup using nginx in the directory `example_deployment`. This has 
encryption enabled, but you have to replace the dummy files in `certificates` with your own certificate and key.
Also you should change the server name in `nginx_config/main.conf` to point to the url the service will be deployed
to later.

After you have made the changes, go to the parent dir of `docker-compose.yml` and run it with 
`docker-compose up`. 