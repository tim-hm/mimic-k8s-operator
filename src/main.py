import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Response, status


def load_env_var(name: str, default=None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise EnvironmentError(f"Missing env var: {name}")
    else:
        return value


def main() -> None:
    load_dotenv()

    try:
        port = int(load_env_var("APP_PORT", 8080))
    except ValueError:
        raise EnvironmentError("APP_PORT must be an integer")

    log_level: str = load_env_var("APP_LOG_LEVEL", "info")

    # Require name to be set because I'm learnign how all this works
    # and this helps me trace from the charm pebble layer to the container
    name: str = load_env_var("APP_NAME")

    # mimic fastapi's log format
    logging.basicConfig(level=log_level.upper(), format="%(levelname)s:     %(message)s")

    logging.info(f"Configuring {name} 🚀")
    app = FastAPI()

    @app.get("/")
    def get_root():
        return "Ok, lets begin ..."

    @app.get("/healthz")
    def get_healthz(response: Response):
        response.status_code = status.HTTP_200_OK
        return "OK"

    @app.get("/version")
    def get_version():
        return {"app": name, "port": port, "log_level": log_level}

    uvicorn.run(app, host="0.0.0.0", port=port, log_level=log_level)


if __name__ == "__main__":
    main()
