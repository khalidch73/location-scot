# FastAPI App with PostgresSQL and SQLModel

Create Project:

    poetry new location-server

Change directory to project:

    cd location-server 

Add dependecies in pyproject.toml file and run following command:

    poetry install

Add poetry virtualenv interpreter in VSCode make a file main.py in todo_app folder

Write main.py
write settings.py

Create a Neon Database Project and copy the connection string and paste it to .env file (check .env_back sample):

https://neon.tech/docs/guides/python#create-a-neon-project

Create a Neon Database Project Test Branch and copy the connection string and paste it to .env file (check .env_back sample):

https://neon.tech/docs/manage/branches#create-a-branch



Run test:

    poetry run pytest

Run project in Poetry Envirnoment:

    poetry run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

Open in Browser:

    http://127.0.0.1:8000/

    http://127.0.0.1:8000/docs

    http://127.0.0.1:8000/openapi.json

## Publish on the Web while running locally

Install Ngrok:

https://ngrok.com/docs/getting-started/

Run the following command to add your authtoken to the default ngrok.yml:

    ngrok config add-authtoken 2bZGNZ3Mj3HdRxPt19defOl_7oFHsvr5AmM9A9UZUyhFn

Deploy with your static domain:

    ngrok http --domain=my-static-domain.ngrok-free.app 8000

Open in Browser:

    https://my-static-domain.ngrok-free.app/

Open in Browser:

    https://my-static-domain.ngrok-free.app/

Open Docs in Browser:

    https://my-static-domain.ngrok-free.app/docs

Open OpenAPI specs in Browser:

    https://my-static-domain.ngrok-free.app/openapi.json

Now we will use this json to create GPT Action.

Now create a Custom GPT here:

    https://chat.openai.com/gpts






# 02 Define the route for creating a location
@app.post("/locations/", response_model=LocationFinder)
async def create_location(location_data: Annotated[LocationFinder, "Data to create a location"], session: Annotated[Session, "Database session"] = Depends(get_session)):
    try:
        # Create a new Location instance
        location = LocationFinder(**location_data.dict())
        
        # Add the location to the session and commit changes
        session.add(location)
        session.commit()
        
        # Refresh the location instance to get the updated values
        session.refresh(location)
        
        return location  # Return the created location
    except Exception as e:
        # Rollback the transaction in case of error
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create location: {str(e)}")