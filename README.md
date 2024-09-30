**TODO List Django app**

This project provides the ability to track your TODOs. With the help of this app you can:
* create, update, delete your tasks (TODOs).
* submit task completion
* group tasks into categories
* set tasks priority
* manage your profile data and change password

There is a default admin account. If you log in as admin, you can manage users profiles.
**Only staff user** has access to complete deletion of any tasks.

**To run this app** you just need to:
1. Clone this repo
2. Go to the folder with this project on your computer.
3. Run 'docker-compose up -d --build'. It can take some time, but when you see [+] Running 3/3 on terminal, you can proceed to the next step.
   P.s. You need Docker installed on your computer, so if you don't have it, proceed to this link and install Docker on your machine: https://docs.docker.com/desktop/
4. Now you can view implemented API on **localhost:8000/docs/** in your browser, **BUT** to perform any requests on it, you need to get authentication token first.
5. In order to access these endpoints, you need to use Postman or something like that. So install Postman, if you don't have it yet: https://www.postman.com/downloads/<br>
**Note that** you need to send described requests from docs to http://localhost:8000/api (it is the base URL), not to http://localhost:8000/docs.
6. After that you need open Postman and create one simple POST request to http://127.0.0.1:8000/api/api-token-auth/ with JSON body having value (this is the default superuser credentials): <br>
{
    "username": "admin",
    "password": "admin99password"
}
7. Now you need to copy returned Token value and put it as Authorization header in Headers section of Postman. You need to do so for all further requests to this API.<br>
Required header format:
   * Key: Authorization
   * Value: Token <token you have from step 6>