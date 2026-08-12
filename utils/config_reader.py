import yaml


def load_config():

    with open("config/config.yaml", "r") as file:
        config = yaml.safe_load(file)

    env = config["env"]

    base_url = config["environments"][env]["base_url"]
    print(f"Running tests on environment: {env}")
    print(f"Base URL: {base_url}")

    return {
        "env": env,
        "base_url": base_url,
        "browser": config["browser"],
        "headless": config["headless"],
        "timeouts": config["timeouts"],
    }
