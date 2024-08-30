import pika
import sys
import threading

def main():

    print("Ingresa tu nombre: ")
    name = gettext()
    text = ""
    
    t1 = threading.Thread(target=consume)
    t1.start()    

    while(text != "adios" and text != "salir"):
        if text != "":
            print("Usted: "+text)

        text = gettext()
        publish(name + ': ' + text)

    t1.join()

    sys.exit()

def publish(message: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='room')

    channel.basic_publish(exchange='', routing_key='room', body=message)
    
    connection.close()

def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    consume_channel = connection.channel()

    consume_channel.queue_declare(queue='room')

    def callback(ch, method, properties, body):
        print(body)

    consume_channel.basic_consume(queue='room', on_message_callback=callback, auto_ack=True)

    print(' [*] Esperando mensajes... CTRL+C para salir.')
    consume_channel.start_consuming()    

def gettext():
    return input()

if __name__ == '__main__':
    main()
    