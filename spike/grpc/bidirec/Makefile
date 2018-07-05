all:
	echo "all"

compile:
	echo "compiling proto file"
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculator.proto

clean:
	rm *pb2*
