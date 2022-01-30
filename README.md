## General info
RESTful API made with Django Rest Framework

**API Docs:** https://todo-test-task.herokuapp.com/docs/swagger

**Site administration**
* url: https://todo-test-task.herokuapp.com/admin/
* email: admin@test.com
* password: admin


### Local Setup
Configure your environment.
Activate virtualenv: (venv - your virtual environment name).
```shell
source venv/bin/activate
```

Then copy env.example to .env file and set up environment variables.
Export CONFIG_NAME variable. For local setup it should be set to base:
```shell
export CONFIG_NAME=base
```

To make and apply migrations run the following command:
```shell
python3 manage.py makemigrations
python3 manage.py migrate
```

To start server go to the project root and run:
```shell
python3 manage.py runserver
```


# Deployment
Production: https://todo-test-task.herokuapp.com/

If you are sure that your changes won't break anything on the server: 
1. Push your changes to the **develop** branch
2. Checkout **master** branch
3. Merge **develop** branch and push to **master**

If not, please, follow the instructions below

**Deploy To Production Instructions**
1. Commit and push changes to your working branch
2. Create a Pull Request (PR) from your working branch to master
3. If there are any errors and PR can't be merged, resolve the issues locally and then push again to your branch
4. Merge PR
