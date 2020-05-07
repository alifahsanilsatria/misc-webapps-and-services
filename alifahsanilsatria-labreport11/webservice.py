import logging
from flask import request
from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.handler import LogstashFormatter

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	# Create the logger and set it's logging level
	logger = initiate_log()

	n = int(request.args.get('n'))
	FibArray = [0,1]
	logger.debug('fib : 0 --> 0')
	logger.debug('fib : 1 --> 1')

	fib_result = fibonacci(n, FibArray, logger)

	return str(fib_result)

def fibonacci(n, FibArray, logger):
	if n<0:
		logger.debug("Incorrect input")
		return None
	elif n<=len(FibArray):
        	return FibArray[n-1]
	else:
		temp_fib = fibonacci(n-1, FibArray, logger) + fibonacci(n-2, FibArray, logger)
		print(logger)
		logger.debug('fib : ' + str(n) + ' --> ' + str(temp_fib))
		FibArray.append(temp_fib)
		return temp_fib

def initiate_log():
	# Create the logger and set it's logging level
	logger = logging.getLogger("logstash")
	logger.setLevel(logging.DEBUG)

	# Create the handler
	handler = AsynchronousLogstashHandler(
	    host='ab5413e7-7e28-45a6-bdaa-d6c3e00cab46-ls.logit.io',
	    port=27421,
	    ssl_enable=True,
	    ssl_verify=False,
	    database_path='')

	# Here you can specify additional formatting on your log record/message
	formatter = LogstashFormatter()
	handler.setFormatter(formatter)

	# Assign handler to the logger
	logger.addHandler(handler)

	return logger

if __name__ == "__main__":
	app.run(port=5500, debug=True)
