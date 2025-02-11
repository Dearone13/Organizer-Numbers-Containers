# ORGANIZE NUMBERS PROJECT DOCKER CONTAINERS

## Project Description

This project organizes numbers using Docker containers. It is entirely developed in Python and provides an API to perform various mathematical operations and using RPC connections.

## Project Structure

The project structure is as follows:

## Clients
- **client1**
- **client2**
- **client3**
- **client4**
- **client5**
- **client6**

## Server
- **serverIndex**


## Cloning the Repository

To clone this repository, follow these steps:

1. Open your terminal.
2. Navigate to the directory where you want to clone the repository.
3. Execute the following command:

```sh
git clone https://github.com/Dearone13/numbersRPC2.gi
```

## Functionality of program
1. **Index Server (server.py):**  
   - Registers clients by their IP address (simulated).  
   - When a client registers, the server increments the counter of registered clients.
   - Returns a sequence of random numbers. The sequence length is calculated as (number of clients × 11), where each number is an integer between 0 and 10.
   - Generate random numbers for clients.

2. **Client Container (clients_container.js):**  
   - Connects to the index server and registers itself.
   - Prints the sequence of random numbers assigned by the server upon registration.
   - Received messages using RPC client connections to enable server functionality by url.
   - Search repeated and unique numbers and start changes of number between others clients servers.

   ## License

   MIT