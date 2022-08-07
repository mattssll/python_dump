# RabbitMQ Official Tutorial

From <a href='https://www.rabbitmq.com/getstarted.html'> here </a>

## 1. Hello World

One producer sending messages to a single queue, single subscriber picking it up.

## 2. Work queues

Distributing tasks among workers: <a href='https://www.enterpriseintegrationpatterns.com/patterns/messaging/CompetingConsumers.html'>the competing consumers pattern) </a> <br><br>
We can raise multiple workers to process the arriving tasks. <br>
By default rabbitmq uses the "round-robin approach", which means tasks will be equally distributed across workers.<br>
We also added <i>message acknowledgement</i> in our workers, so task is only deleted from queue after worker garantees it was completed. <br>
A default <i>timeout</i> of 30 mins is set in our worker (<i>Delivery Acknowledgement Timeout</i>), to get rid of buggy tasks. This number can be increased if necessary.
<br> The following helps debugging unacknowledged tasks:

```
sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged
```

### Handling RabbitMQ Server Faillures

<ul>
<li>Adding "durable = True" to the queue makes it able to survive from</li>
<li>We add "delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE" to our "send_task" to make our messages durable too (weak guarantee though) </li>
<li>We use "channel.basic_qos" to make sure rabbitmq will give only 1 message per queue at a time </li>
</ul>

## 3. Pub/Sub - Sending messages to many consumers at once

We will be using the fanout exchange type for the "many consumers" at once concept.

### Exchange types:

<ul>
<li>direct</li>
<li>topic</li>
<li>headers</li>
<li>fanout</li>
</ul>
