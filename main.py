from website import create_app
import socket
import webbrowser

IP = socket.gethostbyname(socket.gethostname())
app = create_app()

if __name__ == '__main__':
    webbrowser.open_new(f"http://{IP}:5000/admin-login")
    from waitress import serve
    serve(app, host=f"{IP}",port=5000)
    #app.run(host=f"{IP}",debug=True, port=5000)
