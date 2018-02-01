from api_server import app


if __name__ == "__main__":
    app.logger.info('info log')
    app.run(port=9000)