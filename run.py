import uvicorn
from dotenv import load_dotenv

from it_co_test.app import app


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    load_dotenv()
    main()
