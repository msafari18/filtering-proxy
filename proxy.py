import socket, sys
import webbrowser
from threading import Thread


class proxy :
    def __init__(self,allowed_list,port):
        self.allowed_sites = allowed_list
        for i in self.allowed_sites:
            print(i)
        self.listening_port = int(port)
        self.max_connection = 10
        self.buffer_size = 4096
        # make tcp connection
        try:
            self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(self.listening_port)
            self.my_socket.bind(("", self.listening_port))
            self.my_socket.listen(self.max_connection)
            print("server started... ")
        except:
            print("unable to make connectin ... ")

    def set_connection(self):


        #accept connection from client
        while True:
            try:
                connection, address = self.my_socket.accept()
                data = connection.recv(self.buffer_size)
                thread = Thread(target= self.client_req, args = (connection ,data, address))
                thread.start()
                print("thread")
                thread.join()
            except:
                pass
                # print("no request...")



    def client_req(self, connection, data, address):
        # try:
        # print("client data : ", data)
        data2 = data.decode("utf-8")
        line = data2.split("\n")[0]
        # print("line: ", line)
        splited = line.split(" ")
        if type(splited) is list and len(splited)>1:
            url = splited[1]
        elif type(splited) is list and len(splited)==1 :
            url = splited[0]
        else:
            url = splited
        # print("first url : ", url)

        new_url = ""
        final_url = ""
        port = -1
        http = -1
        try:
            http = url.find("://")
        except:
            print("error")
        if http == -1:
            new_url = url
        else:
            url_pos = http + 3
            new_url = url[url_pos:]

        port_pos = new_url.find(":")
        end_pos = new_url.find("/")

        if end_pos == -1:
            end_pos = len(new_url)

        if(port_pos == -1 or end_pos < port_pos):
            port = 80 #defult
            final_url = new_url[:end_pos]
        else:
            temp = new_url[(port_pos+1):]
            port = int(temp[:end_pos-port_pos-1])
            final_url = new_url[:port_pos]

        # print("port: ", port)
        print("url: ", final_url)
        with_www = ""
        if "www" not in final_url:
            with_www = "www."+ final_url
        if final_url in self.allowed_sites or with_www in self.allowed_sites:
            self.server(final_url, port, data, connection, address)
        else:
            print("not allowed")
            try:
                connection.send(('HTTP/1.0 200 OK\n').encode('utf-8'))
                connection.send('Content-Type: text/html\n'.encode('utf-8'))
                connection.send('\n'.encode('utf-8'))
                connection.send("""
                <html>
                <body>
                <h1>filtering proxy</h1> you can't see this site :D!
                </body>
                </html>
                """.encode('utf-8'))
                # self.not_allowed(connection, port)
                connection.close()
            except:
                connection.close()
                print("error...")


    def server(self, final_url, port, data, connection, address):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("----------------> ",final_url, port)
            s.settimeout(10)
            s.connect((final_url, port))
            s.sendall(data)
            while 1:
                print("yoho",final_url)
                server_reply = s.recv(self.buffer_size)
                if (len(server_reply) > 0):
                    connection.send(server_reply)
                else:
                    print("------>")
                    break

            s.close()
            connection.close()
        except:
            print("failed...")
            s.close()
            connection.close()



# proxy = proxy()
# proxy.set_connection()






