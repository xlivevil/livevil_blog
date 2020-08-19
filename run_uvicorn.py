import uvicorn
import os


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "livevil_blog.settings.production")
    uvicorn.run(
        "livevil_blog.wsgi:application",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )


if __name__ == "__main__":
    main()
