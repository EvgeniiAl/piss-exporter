import signal
import sys
import time

from lightstreamer.client import *
from prometheus_client import start_http_server, Gauge


class SubListener:
  def onItemUpdate(self, update):
    ts=update.getValue("TimeStamp")
    value=update.getValue("Value")
    print("{ts:<18}: {value:>6}".format(ts=ts, value=value))
    iss_urine_tank_gauge.set(value)
    pass
  def onClearSnapshot(self, itemName, itemPos):
    pass
  def onCommandSecondLevelItemLostUpdates(self, lostUpdates, key):
    pass
  def onCommandSecondLevelSubscriptionError(self, code, message, key):
    pass
  def onEndOfSnapshot(self, itemName, itemPos):
    pass
  def onItemLostUpdates(self, itemName, itemPos, lostUpdates):
    pass
  def onListenEnd(self):
    pass
  def onListenStart(self):
    pass
  def onSubscription(self):
    pass
  def onSubscriptionError(self, code, message):
    pass
  def onUnsubscription(self):
    pass
  def onRealMaxFrequency(self, frequency):
    pass

loggerProvider = ConsoleLoggerProvider(ConsoleLogLevel.WARN)
LightstreamerClient.setLoggerProvider(loggerProvider)

# Establishing a new connection to Lightstreamer Server
lightstreamer_client = LightstreamerClient("http://push.lightstreamer.com", "ISSLIVE")
lightstreamer_client.connect()

# Making a new Subscription in MERGE mode
subscription = Subscription(
    mode="MERGE",
    items=["NODE3000005"],
    fields=["Value", "TimeStamp"])

# Adding the subscription listener to get notifications about new updates
subscription.addListener(SubListener())

# Registering the Subscription
lightstreamer_client.subscribe(subscription)

iss_urine_tank_gauge = Gauge(
    "iss_urine_tank_gauge",
    "URINE TANK QTY",
    [],
)

def handle_sigint(signal, frame):
    """Handles SIGINT (Ctrl+C) gracefully."""
    print("\nShutting down piss-exporter...")
    lightstreamer_client.unsubscribe(subscription)
    lightstreamer_client.disconnect()
    sys.exit(0)


if __name__ == "__main__":
    # Register SIGINT handler
    signal.signal(signal.SIGINT, handle_sigint)

    # Start the Prometheus HTTP server on port 8000
    start_http_server(8000)
    print("piss-exporter running on http://localhost:8000/metrics")

    while True:
      time.sleep(10**8)
