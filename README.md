# Look Ma, No HTTP!

This repository contains the code I wrote during my EuroPython 2019 talk "Look
Ma, No HTTP!".

Here is the talk abstract:

> In this talk I'm going to live code a web application that is built
> exclusively on top of WebSocket, without using HTTP at all!
> 
> What's the benefit of using WebSocket over HTTP, you may ask? With WebSocket
> each client establishes a permanent connection to the server, so there is no
> request/response cycle and no need for the client to poll the server for
> data. Each side can freely send data to the other side at any time, so this
> is an ideal stack for building highly dynamic, event-driven applications.
> 
> For this live coding exercise I'm going to use the Socket.IO server for
> Python, and the Socket.IO client for JavaScript. No Flask, no Django, no
> HTTP!
