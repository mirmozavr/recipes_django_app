## Recipes Web Application
Django-powered web application to share your favorite recipes with the world!  
Admin panel is provided for adding new recipe entry including title, main text instruction, ingredients
and weight, and total cooking time. Slug will be automatically provided for every entry based
on the title. Manual ingredient addition is also available at the admin panel.  
For every recipe, the average dish calories are calculated based on the weight and calories of its ingredients.

>This is how a single recipe page looks like 
![SingleRecipe](https://user-images.githubusercontent.com/68658828/157976811-fbb88fec-5c0d-402e-860e-b12f338061b9.png)
>

>Main page with all recipes represented as square blocks
![MainPage](https://user-images.githubusercontent.com/68658828/157977028-a60e5a24-a313-45b2-a52f-f174001471c2.png)
> 

>All entities may be added and edited via the admin panel.
![AdminPanel](https://user-images.githubusercontent.com/68658828/157977794-9e4aedae-c9bb-4ee9-b8ec-75fc719fdca8.png)
>
 
##<u>Launch</u>
Application consists of 2 parts: web part powered by Django framework and DB
part powered by PostgreSQL and have its Docker volume. Both are separated in different Docker containers and
are launched via docker-compose. Following instructions require Docker installed.  
> `.env` file is uploaded for demonstration purposes 
> 
1. Change `DEBUG` variable to 0 at `.env.dev` for the production.
2. Create a docker image  
`docker-compose build`
3. Run docker image  
`docker-compose up -d`  
'-d' is used to skip printing anything to STDOUT  
At this point step 1 might be skipped, this command will build an image if it is absent

>Commands in the next steps must start with 'docker-compose exec web' to be applied to the app in a container.  
Also, the following steps are for 1st launch of the application and may be skipped for the next launches. 
>
4. At the first start DB is fully empty and doesn't have any tables so migrations have to be applied. All initial migration files are already provided.  
`docker-compose exec web python manage.py migrate --noinput`  
5. Create superuser to access admin panel  
`python manage.py createsuperuser`  
And simply follow instructions. Or you may run the following command to create 'admin' user with 'admin' password using
a fixture JSON file.  
`docker-compose exec web python manage.py loaddata admin.json`
6. Prepopulate ingredients table with 'food.json' file or skip this step and
provide your fixture or fill ingredients in the admin panel.  
`docker-compose exec web python manage.py loaddata food.json`  
7. If you executed the command from the previous step and you want to populate tables
further with 20 random recipes, use 2 more fixtures.  
`docker-compose exec web python manage.py loaddata recepies.json`  
`docker-compose exec web python manage.py loaddata weight.json`  