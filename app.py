from website import create_app

app = create_app()

def main():
    app.run(host='192.168.0.102') #run directly

if __name__ == '__main__':
    main()